from adafruit_display_shapes.rect import Rect
import adafruit_requests as requests
import adafruit_imageload
import displayio
import time

current_album_title = ""

def get_album_artwork():
    global current_album_title
    get_current_album_title_url = "https://pi-screen.herokuapp.com/currentAlbum"
    get_current_album_artwork_url = "https://pi-screen.herokuapp.com/"

    if user_is_listening_to_song() == True:

        response = requests.get("https://pi-screen.herokuapp.com/currentAlbum").text

        if response == current_album_title:
            print("nothing to change")
            time.sleep(5)
            return None
        # render the board with the artwork as an argument.
        else:
            try:
                print("Fetching album artwork")
                r = requests.get("https://pi-screen.herokuapp.com/")

                with open("art.bmp", 'wb') as handler:
                    handler.write(r.content)

                current_album_title = get_new_album_title()

                return get_artwork_group("/art.bmp")
            except:
                # Return the placeholder
                return get_artwork_group("/art.bmp")

    else:
        # render the board with the placeholder as an argument
        if current_album_title == "placeholder":
            print("nothing to change")
            time.sleep(5)
            return None
        print("rendering placeholder")
        r = requests.get("https://pi-screen.herokuapp.com/instagram")

        current_album_title = "placeholder"
        with open("placeholder.bmp", 'wb') as handler:
            handler.write(r.content)


        try:
            group = get_artwork_group("/placeholder.bmp")
            return group
        except RuntimeError:
            group = get_artwork_group("/fallback.bmp")
            return group

    return

def user_is_listening_to_song():
    response = requests.get("https://pi-screen.herokuapp.com/currentAlbum")
    return False if response.status_code == 500 else True

def get_new_album_title():
    response = requests.get("https://pi-screen.herokuapp.com/currentAlbum")

    return response.text

def get_artwork_group(file_location):
    image_bit, image_pal = adafruit_imageload.load(file_location,
                                                     bitmap=displayio.Bitmap,
                                                     palette=displayio.Palette)
    # bitmap & pallet above are used to create the grid of individual
    # tiles, 32 x 32, cut from the long bitmap image named in the
    # quotes, above
    image_grid = displayio.TileGrid(image_bit, pixel_shader=image_pal,
                                     width=1, height=1,
                                     tile_height=32, tile_width=32,
                                     default_tile=0,
                                     x=0, y=0)

    group = displayio.Group()

    group.append(image_grid)


    print(group)
    return group
 
