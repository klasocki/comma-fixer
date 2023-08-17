from flask import Flask, request, jsonify, make_response
from baseline import fix_commas, create_baseline_pipeline
import logging

app = Flask(__name__)
logger = logging.Logger(__name__)
logging.basicConfig(level=logging.INFO)


@app.route('/', methods=['GET'])
def root():
    return ("Welcome to the comma fixer. Go to /fix-commas?s='some text' or /baseline/fix-commas?s='some text' to try "
            "out the functionality.")


@app.route('/baseline/fix-commas/', methods=['POST'])
def fix_commas_with_baseline():
    data = request.get_json()
    if 's' in data:
        return make_response(jsonify({"s": fix_commas(app.baseline_pipeline, data['s'])}), 200)
    else:
        return make_response("Parameter 's' missing", 400)


if __name__ == '__main__':
    logger.info("Loading the baseline model.")
    app.baseline_pipeline = create_baseline_pipeline()
    app.run(debug=True)
