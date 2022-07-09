print("hello")

import time
import board
import displayio
import terminalio
from adafruit_display_text.label import Label
from digitalio import DigitalInOut
from adafruit_display_text.scrolling_label import ScrollingLabel
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_requests as requests
import busio
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.polygon import Polygon
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.line import Line
from adafruit_bitmap_font import bitmap_font
from adafruit_matrixportal.matrix import Matrix


# --- Display setup ---
matrix = Matrix(width=32, height=32, bit_depth=6)
display = matrix.display


esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

requests.set_socket(socket, esp)

try:
    from secrets import secrets
except ImportError:
    print("Secrets files were not found")
    raise


print("Connecting to AP...")
while not esp.is_connected:
    try:
        esp.connect_AP(secrets["ssid"], secrets["password"])
    except OSError as e:
        print("could not connect to AP, retrying: ", e)
        continue



while True:
    print("Fetching TFL information")

    r = requests.get("https://tfl-tracker.herokuapp.com/")
    print("-" * 40)
    print(r.json())
    print("-" * 40)
    r.close()

    stationInfo = r.json()

    # --- Drawing setup ---
    # Create a Group
    group = displayio.Group()
    # Create a bitmap object
    bitmap = displayio.Bitmap(32, 32, 3)  # width, height, bit depth
    # Create a color palette
    color = displayio.Palette(len(stationInfo))

    for i in range(len(stationInfo)):
        color[i] = stationInfo[i].get("color")
        

    # color[0] = 0x3b0c00 # bakerloo
    # color[1] = 0xff0000 # central
    # color[2] = 0xffee00 # circle
    # color[3] = 0x013d01 # district
    # color[4] = 0x9364CD # elizibeth
    # color[5] = 0xfc42ff # hamersmith and city
    # color[6] = 0xA0A5A9 # jubilee
    # color[7] = 0x000000 # nothern
    # color[8] = 0x003688 # picadilly
    # color[9] = 0x0098D4 # victoria
    # color[10] = 0x95CDBA # waterloo and city
    # color[11] = 0x00A4A7 # dlr
    # color[12] = 0xEE7C0E # overground
    # color[13] = 0x84B817 # trams

    for i in range(len(stationInfo)):
        # Create a TileGrid using the Bitmap and Palette
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=color)
        # Add the TileGrid to the Group

        group.append(tile_grid)

        background_color = stationInfo[i].get("color")
        temp = Rect(0, 0, 32, 32, fill=background_color)
        group.append(temp)

        display_text = Label(
            terminalio.FONT,
            color=0xffffff,
            text=stationInfo[i].get("formatted_display_text"),
        )

        display_text_background = Rect(0, 20, 32, 32, fill=0x000000)

        display_text.y = 32 - 7
        display_text.x = 2
        
        group.append(display_text_background)
        
        
        status_icon_bg_stroke = Circle(28, 16, 3, fill=0xffffff)
        group.append(status_icon_bg_stroke)

        if stationInfo[i].get("status") == "Good service":
            
            status_icon_bg = Circle(28, 16, 2, fill=0x00ff00)
            group.append(status_icon_bg)
        elif stationInfo[i].get("status").find("closure") != -1:
            status_icon_bg = Circle(28, 16, 2, fill=0xff0000)
            group.append(status_icon_bg)
        else:
            status_icon_bg = Circle(28, 16, 2, fill=0xffff00)
            group.append(status_icon_bg)

  
        group.append(display_text)

        display.show(group)

        for i in range(1):
            time.sleep(1)
            for j in range(display_text.width):
                if abs(display_text.x) > abs(display_text.width):
                    display_text.x = 2
                    break
                display_text.x -= j
                time.sleep(.3)
        