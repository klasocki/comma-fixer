from os.path import realpath
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from commafixer.routers import baseline, fixer

app = FastAPI()
app.include_router(fixer.router, prefix='/fix-commas')
app.include_router(baseline.router, prefix='/baseline')

# Without the realpath hack tests fail
app.mount("/", StaticFiles(directory=realpath(f'{realpath(__file__)}/../static'), html=True), name="static")


@app.get('/')
async def index() -> FileResponse:
    return FileResponse(path="static/index.html", media_type="text/html")


if __name__ == '__main__':
    uvicorn.run("app:app", port=8000)
