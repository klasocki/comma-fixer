from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline, NerPipeline
import re

from comma_fixer_interface import CommaFixerInterface


class BaselineCommaFixer(CommaFixerInterface):
    """
    A wrapper class for the oliverguhr/fullstop-punctuation-multilang-large baseline punctuation restoration model.
    It adapts the model to perform comma fixing instead of full punctuation restoration, that is, removes the
    punctuation, runs the model, and then uses its outputs so that only commas are changed.
    """

    def __init__(self, device=-1):
        self._ner = _create_baseline_pipeline(device=device)

    def fix_commas(self, s: str) -> str:
        """
        The main method for fixing commas using the baseline model.
        In the future we should think about batching the calls to it, for now it processes requests string by string.
        :param s: A string with commas to fix, without length restrictions.
        Example: comma_fixer.fix_commas("One two thre, and four!")
        :return: A string with commas fixed, example: "One, two, thre and four!"
        """
        s_no_punctuation, punctuation_indices = _remove_punctuation(s)
        return _fix_commas_based_on_pipeline_output(
            self._ner(s_no_punctuation),
            s,
            punctuation_indices
        )


def _create_baseline_pipeline(model_name="oliverguhr/fullstop-punctuation-multilang-large", device=-1) -> NerPipeline:
    """
    Creates the huggingface pipeline object.
    Can also be used for pre-downloading the model and the tokenizer.
    :param model_name: Name of the baseline model on the huggingface hub.
    :param device: Device to use when running the pipeline, defaults to -1 for CPU, a higher number indicates the id
    of GPU to use.
    :return: A token classification pipeline.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    return pipeline('ner', model=model, tokenizer=tokenizer, device=device)


def _remove_punctuation(s: str) -> tuple[str, list[int]]:
    """
    Removes the punctuation (".,?-:") from the input text, since the baseline model has been trained on data without
    punctuation. It also keeps track of the indices where we remove it, so that we can restore the original later.
    Commas are the exception, since we remove them, but restore with the model.
    Hence we do not keep track of removed comma indices.
    :param s: For instance, "A short-string: with punctuation, removed.
    :return: A tuple of a string, for instance:
    "A shortstring with punctuation removed"; and a list of indices where punctuation has been removed, in ascending
    order
    """
    to_remove_regex = r"[\.\?\-:]"
    # We're not counting commas, since we will remove them later anyway. Only counting removals that will be restored
    # in the final resulting string.
    punctuation_indices = [m.start() for m in re.finditer(to_remove_regex, s)]
    s = re.sub(to_remove_regex, '', s)
    s = s.replace(',', '')
    return s, punctuation_indices


def _fix_commas_based_on_pipeline_output(pipeline_json: list[dict], original_s: str, punctuation_indices: list[int]) -> \
        str:
    """
    This function takes the comma fixing token classification pipeline output, and converts it to string based on the
    original
    string and punctuation indices, so that the string contains all the original characters, except commas, intact.
    :param pipeline_json: Token classification pipeline output.
    Contains five fields.
    'entity' is the punctuation that should follow this token.
    'word' is the token text together with preceding space if any.
    'end' is the end index in the original string (with punctuation removed in our case!!)
    Example: [{'entity': ':',
  'score': 0.90034866,
  'index': 1,
  'word': '▁Exam',
  'start': 0,
  'end': 4},
 {'entity': ':',
  'score': 0.9157294,
  'index': 2,
  'word': 'ple',
  'start': 4,
  'end': 7}]
    :param original_s: The original string, before removing punctuation.
    :param punctuation_indices: The indices of the removed punctuation except commas, so that we can correctly keep
    track of the current offset in the original string.
    :return: A string with commas fixed, and other the original punctuation from the input string restored.
    """
    result = original_s.replace(',', '')  # We will fix the commas, but keep everything else intact

    commas_inserted_or_punctuation_removed = 0
    removed_punctuation_index = 0

    for i in range(1, len(pipeline_json)):
        current_offset = pipeline_json[i - 1]['end'] + commas_inserted_or_punctuation_removed

        commas_inserted_or_punctuation_removed, current_offset, removed_punctuation_index = (
            _update_offset_by_the_removed_punctuation(
                commas_inserted_or_punctuation_removed, current_offset, punctuation_indices, removed_punctuation_index
            )
        )

        if _should_insert_comma(i, pipeline_json):
            result = result[:current_offset] + ',' + result[current_offset:]
            commas_inserted_or_punctuation_removed += 1
    return result


def _update_offset_by_the_removed_punctuation(
        commas_inserted_and_punctuation_removed, current_offset, punctuation_indices, removed_punctuation_index
):
    # increase the counters for every punctuation removed from the original string before the curent offset
    while (removed_punctuation_index < len(punctuation_indices) and
           punctuation_indices[removed_punctuation_index] < current_offset):

        commas_inserted_and_punctuation_removed += 1
        removed_punctuation_index += 1
        current_offset += 1
    return commas_inserted_and_punctuation_removed, current_offset, removed_punctuation_index


def _should_insert_comma(i, pipeline_json, new_word_indicator='▁') -> bool:
    # Only insert commas for the final token of a word, that is, if next word starts with a space.
    return pipeline_json[i - 1]['entity'] == ',' and pipeline_json[i]['word'].startswith(new_word_indicator)


if __name__ == "__main__":
    BaselineCommaFixer()  # to pre-download the model and tokenizer
