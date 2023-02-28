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
