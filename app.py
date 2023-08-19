import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.baseline import BaselineCommaFixer
import logging

logger = logging.Logger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI()  # TODO router?
logger.info('Loading the baseline model...')
app.baseline_model = BaselineCommaFixer()


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


app.mount("/", StaticFiles(directory="static", html=True), name="static")


@app.get('/')
async def index() -> FileResponse:
    return FileResponse(path="static/index.html", media_type="text/html")


if __name__ == '__main__':
    uvicorn.run("app:app", port=8000)
