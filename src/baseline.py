from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline, NerPipeline


def create_baseline_pipeline(model_name="oliverguhr/fullstop-punctuation-multilang-large") -> NerPipeline:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    return pipeline('ner', model=model, tokenizer=tokenizer)


def fix_commas(ner_pipeline: NerPipeline, s: str) -> str:
    return _fix_commas_based_on_pipeline_output(
        ner_pipeline(_remove_punctuation(s)),
        s
    )


def _remove_punctuation(s: str) -> str:
    to_remove = ".,?-:"
    for char in to_remove:
        s = s.replace(char, '')
    return s


def _fix_commas_based_on_pipeline_output(pipeline_json: list[dict], original_s: str) -> str:
    result = original_s.replace(',', '')  # We will fix the commas, but keep everything else intact
    current_offset = 0

    for i in range(1, len(pipeline_json)):
        current_offset = _find_current_token(current_offset, i, pipeline_json, result)
        if _should_insert_comma(i, pipeline_json):
            result = result[:current_offset] + ',' + result[current_offset:]
            current_offset += 1
    return result


def _should_insert_comma(i, pipeline_json, new_word_indicator='▁') -> bool:
    # Only insert commas for the final token of a word
    return pipeline_json[i - 1]['entity'] == ',' and pipeline_json[i]['word'].startswith(new_word_indicator)


def _find_current_token(current_offset, i, pipeline_json, result, new_word_indicator='▁') -> int:
    current_word = pipeline_json[i - 1]['word'].replace(new_word_indicator, '')
    # Find the current word in the result string, starting looking at current offset
    current_offset = result.find(current_word, current_offset) + len(current_word)
    return current_offset
