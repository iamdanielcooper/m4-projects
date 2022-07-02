import time
import board
import displayio
from adafruit_matrixportal.matrix import Matrix
import adafruit_imageload
from digitalio import DigitalInOut
import busio
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_requests as requests
import time



def main():
    current_album_title = ""
    current_album_title_url = "https://pi-screen.herokuapp.com/currentAlbum"
    get_current_album_artwork_url = "https://pi-screen.herokuapp.com/"

    # Connect to the network.

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

        response = requests.get("https://pi-screen.herokuapp.com/currentAlbum").text


        if response == current_album_title:
            # wait and continue with next loop, nothing new needs to be rendered.
            print("nothing to change")
            time.sleep(5)
            continue
        elif user_is_listening_to_song():
            # render the board with the artwork as an argument.
            print("Fetching album artwork")
            r = requests.get("https://pi-screen.herokuapp.com/")

            with open("art.bmp", 'wb') as handler:
                handler.write(r.content)

            current_album_title = get_new_album_title()
            render_board_with_artwork("/art.bmp")

        else:
            # render the board with the placeholder as an argument
            print("rendering placeholder")
            render_board_with_artwork("/placeholder.bmp")

    return

def user_is_listening_to_song():
    response = requests.get("https://pi-screen.herokuapp.com/currentAlbum")

    return False if response.text == "no song is playing" else True

def get_new_album_title():
    response = requests.get("https://pi-screen.herokuapp.com/currentAlbum")

    return response.text

def render_board_with_artwork(file_location):

    matrix_width = 32
    matrix_height = 32

    #  create matrix display
    #  I also added a bit_depth to make more colors pop out
    matrix = Matrix(width=matrix_width, height=matrix_height, bit_depth=6)
    display = matrix.display

    image_bit, image_pal = adafruit_imageload.load(file_location,
                                                     bitmap=displayio.Bitmap,
                                                     palette=displayio.Palette)
    # bitmap & pallet above are used to create the grid of individual
    # tiles, 32 x 32, cut from the long bitmap image named in the
    # quotes, above
    image_grid = displayio.TileGrid(image_bit, pixel_shader=image_pal,
                                     width=1, height=1,
                                     tile_height=matrix_height, tile_width=matrix_width,
                                     default_tile=0,
                                     x=0, y=0)

    group = displayio.Group()
    group.append(image_grid)

    display.show(group)
    time.sleep(5)

main()
