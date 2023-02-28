import io
import math
import cairo

from models import ImageParams, ImageResponse


class Image:
    def __init__(self, params: ImageParams):
        self.params = params

    def generate(self):
        size = self.params.size
        orient = self.params.orientation
        sub = self.params.subdivision
        pcolor = [
            int(self.params.primary_color[x * 2 : (x + 1) * 2], 16) / 256
            for x in range(3)
        ]
        scolor = [
            int(self.params.secondary_color[x * 2 : (x + 1) * 2], 16) / 256
            for x in range(3)
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
        return ImageResponse(image=image, params=self.params)
