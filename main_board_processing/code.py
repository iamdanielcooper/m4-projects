import blue_square
import spotigram

import board
import busio
import digitalio
from adafruit_matrixportal.matrix import Matrix
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_requests as requests
from digitalio import DigitalInOut

def main():

    display = get_matrix_display()
    display_image = None
    
    connect_to_wifi()

    # modes: {"CLOCK", "INSTAGRAM", "TFL", "FLIGHTS"}
    mode = None

    count = 0
    while True:

        # Request an API & get the current state
        # If the mode has been updated, update the mode state of the app. This will determine which route below is called.

        if count == 10000:
            display_image = blue_square.say_hello()
        else:
            display_image = spotigram.get_album_artwork()

        count += 1

        display.show(display_image)


def get_matrix_display():
    matrix = Matrix(width=32, height=32, bit_depth=6)
    return matrix.display
    
def connect_to_wifi():
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

if __name__ == '__main__':
    main()
