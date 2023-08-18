from flask import Flask, request, jsonify, make_response
from baseline import fix_commas, create_baseline_pipeline
import logging

app = Flask(__name__)
logger = logging.Logger(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/', methods=['GET'])
def root():
    return ("Welcome to the comma fixer. Send a POST request to /fix-commas or /baseline/fix-commas with a string "
            "'s' in the JSON body to try "
            "out the functionality.")


@app.route('/baseline/fix-commas/', methods=['POST'])
def fix_commas_with_baseline():
    json_field_name = 's'
    data = request.get_json()
    if json_field_name in data:
        return make_response(jsonify({json_field_name: fix_commas(app.baseline_pipeline, data['s'])}), 200)
    else:
        return make_response(f"Parameter '{json_field_name}' missing", 400)


if __name__ == '__main__':
    logger.info("Loading the baseline model.")
    app.baseline_pipeline = create_baseline_pipeline()
    app.run(debug=True) # TODO get this from config or env variable
