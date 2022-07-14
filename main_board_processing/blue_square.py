from adafruit_display_shapes.rect import Rect
import displayio
import time


def say_hello():

    group = displayio.Group()
    # Create a bitmap object
    bitmap = displayio.Bitmap(32, 32, 3)  # width, height, bit depth
    # Create a color palette
    color = displayio.Palette(1)

    color[0] = 0x550000

    tile_grid = displayio.TileGrid(bitmap, pixel_shader=color)
    group.append(tile_grid)

    time.sleep(2)
    return group

