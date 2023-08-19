import uvicorn
from fastapi import FastAPI, HTTPException
from src.baseline import BaselineCommaFixer
import logging

logger = logging.Logger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI() #TODO router?
logger.info('Loading the baseline model...')
app.baseline_model = BaselineCommaFixer()


@app.get('/')
async def root():
    return ("Welcome to the comma fixer. Send a POST request to /fix-commas or /baseline/fix-commas with a string "
            "'s' in the JSON body to try "
            "out the functionality.")


@app.post('/baseline/fix-commas/')
async def fix_commas_with_baseline(data: dict):
    json_field_name = 's'
    if json_field_name in data:
        logger.debug('Fixing commas.')
        return {json_field_name: app.baseline_model.fix_commas(data['s'])}
    else:
        msg = f"Text '{json_field_name}' missing"
        logger.debug(msg)
        raise HTTPException(status_code=400, detail=msg)


if __name__ == '__main__':
    uvicorn.run("app:app", reload=True, port=8000)

