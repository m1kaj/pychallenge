"""http://www.pythonchallenge.com/pc/return/5808.html
"""

# Page presents a login prompt and displays message: "inflate"
# -> not sure if this should happen? But it can be bypassed using
# credentials gotten in level8 challenge: huge/file

# What is then displayed is a image that is unclear and seems
# to have a grid of pixels. Enlarging it in browser shows every
# other pixel is different. Not sure if the other pixels "o" are
# completely black. The second set definitely have colours "x".
# Starting from upper left corner, image looks like:
#
#    oxoxoxox...
#    xoxoxoxo...
#    oxoxoxox...
#    ...........
#
# Page title is "odd even"
#
# Source tells image is "cave.jpg" and displayed in size 640x480

# fetch image to local disk, using password manager we put together
# in level9 challenge.
import urllib.request
password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
top_level_url = "http://www.pythonchallenge.com/"
password_mgr.add_password(None, top_level_url, "huge", "file")
handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
opener = urllib.request.build_opener(handler)
urllib.request.install_opener(opener)
urllib.request.urlretrieve("http://www.pythonchallenge.com/pc/return/cave.jpg",
    filename="cave.jpg")

# Paying our respects to the free book Automate The Boring Stuff
# With Python, by Al Sweigart! He introduced mne to PIL library!
# (Here replaced by fork called Pillow for Python3)
from PIL import Image
with Image.open("cave.jpg") as cave:
    cave_width, cave_height = cave.size
    print(f"original width: {cave_width}, height: {cave_height}")  # 640, 480
    print(f"original mode: {cave.mode}")                           # RGB

    # Init two new images for the pixels "o" and "x", size 320, 480
    img_a = Image.new(cave.mode, (int(cave_width / 2), cave_height))
    img_b = Image.new(cave.mode, (int(cave_width / 2), cave_height))
    px_a = img_a.load()
    px_b = img_b.load()

    # Slowly process image pixel by pixel and build two images
    pixels = cave.load()
    for y in range(cave_height):
        for x in range(0, cave_width, 2):
            new_xy = (int(x / 2), y)
            if y % 2 == 0:
                px_a[new_xy] = pixels[x, y]
                px_b[new_xy] = pixels[(x + 1), y]
            else:
                px_b[new_xy] = pixels[x, y]
                px_a[new_xy] = pixels[(x + 1), y]
    with open('image_a.jpg', 'wb') as fp:
        img_a.save(fp)
    with open('image_b.jpg', 'wb') as fp:
        img_b.save(fp)
    img_a.close()
    img_b.close()

# Results in two images, one of which is very dark and has
# visible word "evil" in upper right corner.
# Answer: evil
