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


def _convert_pipeline_json_to_string(pipeline_json: list[dict]) -> str:
    # TODO is it ok to remove redundant spaces, or should we keep input data as is and only touch commas?
    # TODO don't accept tokens with commas inside words
    return ''.join(
        token['word'].replace('▁', ' ') + token['entity'].replace('0', '')
        for token in pipeline_json
    ).strip()


def fix_commas(ner_pipeline: NerPipeline, s: str) -> str:
    return _convert_pipeline_json_to_string(
        ner_pipeline(_remove_punctuation(s))
    )
