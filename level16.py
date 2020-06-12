"""http://www.pythonchallenge.com/pc/return/mozart.html
"""

# login credentials when returning are still: huge/file
#
# Page has an image that looks noisy. But it has some white/pink pixels
# that could be markers of some sort. Page title is "let me get this straight".
# After zooming in, the image looks like it has a marker on every horizontal
# line, with the marker locations being horizontally in random positions.
# The first logical thing to try is thus to shift each line until the markers
# are in the same x-coordinates. By zooming the image in a viewer the markers
# can be seen as two white pixels with 5 pink pixels in between. Total of 7 pixels
# for each marker.

# download image
import urllib.request
password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
top_level_url = "http://www.pythonchallenge.com/"
password_mgr.add_password(None, top_level_url, "huge", "file")
handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
opener = urllib.request.build_opener(handler)
urllib.request.install_opener(opener)
urllib.request.urlretrieve("http://www.pythonchallenge.com/pc/return/mozart.gif",
    filename="mozart.gif")

# get image dimensions and mode. They are 640 * 480 
# mode: "P" == "8-bit pixels, mapped to any other mode using a color palette"
from PIL import Image
img = Image.open("mozart.gif")
print(f"image width: {img.width}, height: {img.height}")
print(f"image mode: {img.mode}")

# to get marker pixel values we can process the first 5 lines and look for 
# sections of 5 identical pixels. Print the first 7 pixel sequence found, together 
# with x position

def find_marker(img, line):
    for x in range(6, 640):
        p1 = img.getpixel((x - 5, line))
        p2 = img.getpixel((x - 4, line))
        p3 = img.getpixel((x - 3, line))
        p4 = img.getpixel((x - 2, line))
        p5 = img.getpixel((x - 1, line))
        if p1 == p2 and p2 == p3 and p3 == p4 and p4 == p5:
            return x - 6
    return -1   #error

# If we use above method for the first five lines and then print out pixels 
# x to x+7, we see the white end pixels are not identical brightness. There is 
# small variation in the white pixels. But the five pixels in between are 
# always value 195:
#   line 0: x=428, 249 195 195 195 195 195 252
#   line 1: x=499, 251 195 195 195 195 195 251
#   line 2: x=311, 252 195 195 195 195 195 252
#   line 3: x=106, 251 195 195 195 195 195 252
#   line 4: x=104, 249 195 195 195 195 195 252
#
# Note that image has a logo text "16" in upper corner. We see that the bold 
# font of this logo will mess with our marker detection, so we re-write detection 
# to take advantage of exact pixel value 195:

def find_marker_proper(img, line):
    for x in range(6, 640):
        p1 = img.getpixel((x - 5, line))
        p2 = img.getpixel((x - 4, line))
        p3 = img.getpixel((x - 3, line))
        p4 = img.getpixel((x - 2, line))
        p5 = img.getpixel((x - 1, line))
        if p1 == p2 and p2 == p3 and p3 == p4 and p4 == p5 and p5 == 195:
            return x - 6
    return -1   #error

# shift each line to build output image, and save image

def shift_line(img, line, x):
    l1 = img.crop((0, line, x, line + 1))
    l2 = img.crop((x, line, 640, line + 1))
    img.paste(l2, (0, line, 640 - x, line + 1))
    img.paste(l1, (640 - x, line, 640, line + 1))
    return img

for y in range(0, 480):
    xpos = find_marker_proper(img, y)
    img = shift_line(img, y, xpos)

with open("out.gif", "wb") as fp:
    img.save(fp)

# Result is an image that has text "romance" diagonally across the image.
# Solution is http://www.pythonchallenge.com/pc/return/romance.html