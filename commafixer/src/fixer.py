from peft import PeftConfig, PeftModel
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline, NerPipeline, RobertaTokenizerFast
import nltk
import re

from commafixer.src.comma_fixer_interface import CommaFixerInterface


class CommaFixer(CommaFixerInterface):
    """
    A wrapper class for the fine-tuned comma fixer model.
    """

    def __init__(self, device=-1):
        self.id2label = {0: 'O', 1: 'B-COMMA'}
        self.label2id = {'O': 0, 'B-COMMA': 1}
        self.model, self.tokenizer = self._load_peft_model()

    def fix_commas(self, s: str) -> str:
        """
        The main method for fixing commas using the fine-tuned model.
        In the future we should think about batching the calls to it, for now it processes requests string by string.
        :param s: A string with commas to fix, without length restrictions.
        However, if the string is longer than the length limit (512 tokens), some whitespaces might be trimmed.
        Example: comma_fixer.fix_commas("One two thre, and four!")
        :return: A string with commas fixed, example: "One, two, thre and four!"
        """
        s_no_commas = re.sub(r'\s*,', '', s)
        tokenized = self.tokenizer(s_no_commas, return_tensors='pt', return_offsets_mapping=True, return_length=True)

        # If text too long, split into sentences and fix commas separately.
        # TODO this is slow, we should think about joining them until length, or maybe a length limit to avoid
        #  stalling the whole service
        if tokenized['length'][0] > self.tokenizer.model_max_length:
            return ' '.join(self.fix_commas(sentence) for sentence in nltk.sent_tokenize(s))

        logits = self.model(input_ids=tokenized['input_ids'], attention_mask=tokenized['attention_mask']).logits
        labels = [self.id2label[tag_id.item()] for tag_id in logits.argmax(dim=2).flatten()]
        return _fix_commas_based_on_labels_and_offsets(labels, s_no_commas, tokenized['offset_mapping'][0])

    def _load_peft_model(self, model_name="klasocki/roberta-large-lora-ner-comma-fixer") -> tuple[
        PeftModel, RobertaTokenizerFast]:
        """
        Creates the huggingface model and tokenizer.
        Can also be used for pre-downloading the model and the tokenizer.
        :param model_name: Name of the model on the huggingface hub.
        :return: A model with the peft adapter injected and weights merged, and the tokenizer.
        """
        config = PeftConfig.from_pretrained(model_name)
        inference_model = AutoModelForTokenClassification.from_pretrained(
            config.base_model_name_or_path, num_labels=len(self.id2label), id2label=self.id2label,
            label2id=self.label2id
        )
        tokenizer = AutoTokenizer.from_pretrained(config.base_model_name_or_path)
        model = PeftModel.from_pretrained(inference_model, model_name)
        model = model.merge_and_unload()  # Join LoRa matrices with the main model for faster inference
        # TODO batch, and move to CUDA if available
        return model.eval(), tokenizer


def _fix_commas_based_on_labels_and_offsets(
        labels: list[str],
        original_s: str,
        offset_map: list[tuple[int, int]]
) -> str:
    """
    This function returns the original string with only commas fixed, based on the predicted labels from the main
    model and the offsets from the tokenizer.
    :param labels: Predicted labels for the tokens.
    Should already be converted to string, since we will look for B-COMMA tags.
    :param original_s: The original string, used to preserve original spacing and punctuation.
    :param offset_map: List of offsets in the original string, we will only use the second integer of each pair
    indicating where the token ended originally in the string.
    :return: The string with commas fixed, and everything else intact.
    """
    result = original_s
    commas_inserted = 0

    for i, label in enumerate(labels):
        current_offset = offset_map[i][1] + commas_inserted
        if _should_insert_comma(label, result, current_offset):
            result = result[:current_offset] + ',' + result[current_offset:]
            commas_inserted += 1
    return result


def _should_insert_comma(label, result, current_offset) -> bool:
    # Only insert commas for the final token of a word, that is, if next word starts with a space.
    # TODO perhaps for low confidence tokens, we should use the original decision of the user in the input?
    return label == 'B-COMMA' and result[current_offset].isspace()


if __name__ == "__main__":
    CommaFixer()  # to pre-download the model and tokenizer
