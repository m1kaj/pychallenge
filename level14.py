"""http://www.pythonchallenge.com/pc/return/italy.html
"""

# login credentials when returning are still: huge/file
#
# Page has an image of an edible bun or roll, which has been baked in spiral form.
# Page name is "walk around". Page has a second smaller PNG image. It seems
# to be size 100x100. It has vertical lines.
#
# Page source has comment: "remember: 100*100 = (100+99+99+98) + (..."
#
# When smaller PNG image is loaded in GIMP, it shows up as sRGB, 8-bit, 10000 x 1 pixel line.
# So it's not a square even thought browser draws it as square.
#
# fetch image to local disk, using password manager we put together
# in level9 challenge.

import urllib.request
password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
top_level_url = "http://www.pythonchallenge.com/"
password_mgr.add_password(None, top_level_url, "huge", "file")
handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
opener = urllib.request.build_opener(handler)
urllib.request.install_opener(opener)
urllib.request.urlretrieve("http://www.pythonchallenge.com/pc/return/wire.png",
    filename="wire.png")

# We guess we are to take pixels from wire image and walk a square spiral from outside
# towards the middle. We guess that we could start from upper left corner and first
# go right 100 pixels, then down 99, ...

def walk(src, tgt, source_x, position, distance, direction):
    x, y = position
    for _ in range(distance):
        if direction == "right":
            x += 1
        elif direction == "down":
            y += 1
        elif direction == "left":
            x -= 1
        elif direction == "up":
            y -= 1
        tgt[x, y] = src[source_x, 0]
        source_x += 1
    return source_x, (x, y)

from PIL import Image
wire = Image.open("wire.png")
pixels = wire.load()
result_img = Image.new(wire.mode, (100, 100))
result = result_img.load()
spot = (-1, 0)
p = 0
# spiral away!
for r in range(100, 0, -2):
    p, spot = walk(pixels, result, p, spot, r, "right")
    p, spot = walk(pixels, result, p, spot, r - 1, "down")
    p, spot = walk(pixels, result, p, spot, r - 1, "left")
    p, spot = walk(pixels, result, p, spot, r - 2, "up")
# save result
with open('result.png', 'wb') as fp:
    result_img.save(fp)
result_img.close()

# Resulting 100 x 100 image is a picture of a cat. Downloading URL
# http://www.pythonchallenge.com/pc/return/cat.html produces another cat image
# and text that says cat's name is "uzi".
#
# Solution is http://www.pythonchallenge.com/pc/return/uzi.html