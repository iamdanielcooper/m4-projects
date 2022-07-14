import blue_square
import red_circle

import board
import digitalio
from adafruit_matrixportal.matrix import Matrix

def main():

    display = get_matrix_display()
    display_image = None

    mode = None

    count = 0
    while True:

        # Request an API & get the current state
        # If the mode has been updated, update the mode state of the app. This will determine which route below is called.

        if count % 2 == 0:
            display_image = blue_square.say_hello()
        else:
            display_image = red_circle.red_circle()

        count += 1

        display.show(display_image)


def get_matrix_display():
    matrix = Matrix(width=32, height=32, bit_depth=6)
    return matrix.display

if __name__ == '__main__':
    main()
