from peft import PeftConfig, PeftModel
from transformers import AutoTokenizer, AutoModelForTokenClassification, RobertaTokenizerFast
import nltk
from commafixer.src.comma_fixer_interface import CommaFixerInterface
import re
import numpy as np
from typing import Tuple
# TODO fix formatting with ctrl + alt + l

#TODO optimize imports with ctrl + alt + O
class CommaFixer(CommaFixerInterface):
    def __init__(self):
        self.id2label = {0: 'O', 1: 'B-COMMA'}
        self.label2id = {'O': 0, 'B-COMMA': 1}
        self.model, self.tokenizer = self._load_peft_model()

# TODO ctrl + shift + t go to tests, find test_baseline_fix_commas_fixes_incorrect_commas
    def fix_commas(self , s : str ) -> str   :
        """TODO this function could use some documentation and testing"""

        s_no_commas = re.sub(r'\s*,', '', s)
        tokenized = self.tokenizer(s_no_commas ,return_tensors = 'pt' ,return_offsets_mapping =  True, return_length = True, is_split_into_words=False, trim_offsets=True)

        if tokenized['length'] [0] > self.tokenizer.model_max_length:
            return ' '.join(self.fix_commas(sentence) for sentence in nltk.sent_tokenize(s, ))

        logits = self.model(input_ids=tokenized['input_ids'], attention_mask=tokenized['attention_mask']).logits
        labels = [self.id2label[tag_id.item()] for tag_id in logits.argmax(dim=2).flatten()]
        return _fix_commas_based_on_labels_and_offsets(labels, s_no_commas, tokenized['offset_mapping'][0])

    def _load_peft_model(self, model_name="klasocki/roberta-large-lora-ner-comma-fixer") -> Tuple[
        PeftModel, RobertaTokenizerFast]:
        config = PeftConfig.from_pretrained(model_name)
        # TODO completion ctrl + double space

        inference_model = AutoModelForTokenClassification.from_pretrained(
            config.base_model_name_or_path, num_labels=len(self.id2label), id2label=self.id2label,
            label2id=self.label2id
        )
        tokenizer = AutoTokenizer.from_pretrained(config.base_model_name_or_path)
        model = PeftModel.from_pretrained(inference_model, model_name)
        model = model.merge_and_unload()
        return model.eval(), tokenizer


def _fix_commas_based_on_labels_and_offsets(
        labels: list[str],
        original_s: str,
        offset_map: list[tuple[int, int]]
) -> str:
    result = original_s
    commas_inserted = 0

    for i, label in enumerate(labels):
        current_offset = offset_map[i][1] + commas_inserted
        # TODO extract method or variable - ctrl + alt + v/m, or ctrl + shift + alt + t for all the options - get rid of comments
        # Should we insert commas
        if label == 'B-COMMA' and result[current_offset].isspace():
            # insert a comma between tokens
            result = result[:current_offset] + ',' + result[current_offset:]
            commas_inserted += 1
    return result


# TODO if __name__ == main with postfix refactoring - .main, .if, .not, .return, .par, .while
# to pre-download the model and tokenizer
CommaFixer()

# TODO alt + h -> My productivity
#  Feedback please!!


def fix_commas_with_todos(self, s: str) -> str:
    s_no_commas = re.sub(r'\s*,', '', s)
    tokenized = self.tokenizer(
        s_no_commas, return_tensors='pt', return_offsets_mapping=True, return_length=True, is_split_into_words=False,
        trim_offsets=True
    )

    if tokenized['length'][0] > self.tokenizer.model_max_length:
        # TODO how was the parameter called? ctrl + p or ctrl + q
        return ' '.join(self.fix_commas(sentence) for sentence in nltk.sent_tokenize(s, ))

    logits = self.model(input_ids=tokenized['input_ids'], attention_mask=tokenized['attention_mask']).logits
    # TODO ctrl + shift + p -> show expression type
    labels = [self.id2label[tag_id.item()] for tag_id in logits.argmax(dim=2).flatten()]
    return _fix_commas_based_on_labels_and_offsets(labels, s_no_commas, tokenized['offset_mapping'][0])


# TODO If time left:
#  move block or line with ctrl + shift + arrow or ctrl + alt + arrow
#  surround with - ctrl + alt + t. ALso shit + enter for newline, and ctrl + shift + enter for finishing statement.
#  recent locations with ctrl + shift + e
#  alt + enter in signature -> flip ,
#  shift + click for logging conditional breakpoints
