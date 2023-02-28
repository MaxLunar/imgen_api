from fastapi import FastAPI

from logic import Image
from models import ImageParams

app = FastAPI()


@app.post("/generate_image")
def imagen(params: ImageParams):
    return Image(params).generate()
