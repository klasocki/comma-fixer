from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline, NerPipeline


def create_baseline_pipeline() -> NerPipeline:
    tokenizer = AutoTokenizer.from_pretrained("oliverguhr/fullstop-punctuation-multilang-large")
    model = AutoModelForTokenClassification.from_pretrained("oliverguhr/fullstop-punctuation-multilang-large")
    return pipeline('ner', model=model, tokenizer=tokenizer)


def _remove_punctuation(s: str) -> str:
    to_remove = ".,?-:"
    for char in to_remove:
        s = s.replace(char, '')
    return s


def _convert_pipeline_json_to_string(pipeline_json: list[dict], original_s: str) -> str:
    # TODO is it ok to remove redundant spaces, or should we keep input data as is and only touch commas?
    # TODO don't accept tokens with commas inside words
    result = original_s.replace(',', '') # We will fix the commas, but keep everything else intact
    current_offset = 0
    for i in range(1, len(pipeline_json)):
        current_word = pipeline_json[i - 1]['word'].replace('▁', '')
        current_offset = result.find(current_word, current_offset) + len(current_word)
        # Only insert commas for the final token of a word
        if pipeline_json[i - 1]['entity'] == ',' and pipeline_json[i]['word'].startswith('▁'):
            result = result[:current_offset] + ',' + result[current_offset:]
            current_offset += 1
    return result


def fix_commas(ner_pipeline: NerPipeline, s: str) -> str:
    return _convert_pipeline_json_to_string(
        ner_pipeline(_remove_punctuation(s)),
        s
    )
