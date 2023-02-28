import io
import math
import cairo

from fastapi import FastAPI
from pydantic import (
    BaseModel,
    conint,
    constr,
)


class ImageParams(BaseModel):
    size: conint(gt=0)
    orientation: conint(gt=0, le=4)
    subdivision: conint(gt=1, le=256)
    primary_color: constr(regex="[0-9A-Fa-f]{6}", min_length=6, max_length=6)
    secondary_color: constr(regex="[0-9A-Fa-f]{6}", min_length=6, max_length=6)


class ImageResponse(BaseModel):
    image: str
    params: ImageParams


def generate_image(params: ImageParams):
    size = params.size
    orient = params.orientation
    sub = params.subdivision
    pcolor = [
        int(params.primary_color[x * 2 : (x + 1) * 2], 16) / 256 for x in range(3)
    ]
    scolor = [
        int(params.secondary_color[x * 2 : (x + 1) * 2], 16) / 256 for x in range(3)
    ]

    buffer = io.BytesIO()
    chunksize = size / sub

    with cairo.SVGSurface(buffer, size, size) as surface:
        context = cairo.Context(surface)
        mov = 0, -size * (1 - orient % 2)
        rot = math.pi / 2 * (1 - orient % 2)
        context.rotate(rot)
        context.translate(*mov)
        if orient in (1, 2):
            for x in range(sub):
                context.set_source_rgb(*([pcolor, scolor][x % 2]))
                context.rectangle(0, chunksize * x, size, chunksize)
                context.fill()
        elif orient in (3, 4):
            for x in range(sub * 2):
                context.set_source_rgb(*([pcolor, scolor][x % 2]))
                context.move_to(0, chunksize * x)
                context.line_to(0, chunksize * (x + 1))
                context.line_to(chunksize * (x + 1), 0)
                context.line_to(chunksize * x, 0)
                context.fill()
    image = buffer.getvalue().decode()
    return ImageResponse(image=image, params=params)


app = FastAPI()


@app.post("/generate_image")
def imagen(params: ImageParams):
    return generate_image(params)
