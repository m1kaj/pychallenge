"""http://www.pythonchallenge.com/pc/def/oxygen.html
"""

# Title of page is "smarty". Page contains PNG image.
# Image shows green grass and a river. Image has series
# of gray square blocks in the middle. So I guess now
# we will be parsing PNG format using Python?  :/
# It's a starting guess, so do "pip install pypng"
# and let's go.

import urllib.request
import png

with urllib.request.urlopen("http://www.pythonchallenge.com/pc/def/oxygen.png") as png_file:
    img = png.Reader(png_file)
    width, height, rows, info = img.read()
    print(info)
    # Ok, it's an 8-bit image and has 629 x 95 pixels and an alpha channel

    # If we were to print R,G,B,A values from first 16 pixels in each row,
    # we would see that rows 43-51 start with constant pixel colours. And
    # R=G=B for each pixel. These are the rows with the grey blocks.

    # If we then pick one of those identical rows, it seems to have first
    # 5 identical pixels, followed by groups of 7 identical pixels. So we
    # grab the R byte of first pixel, then R bytes of first pixel from each
    # group of seven pixels. Also, in the end there are actual image pixels.
    # we clear the MSB bit in bytes to avoid unicode decode errors.
    s = bytearray()
    row = list(rows)[45]
    s.append(row[0])           # grab 1st pixel R value

    # Each pixel is 4 bytes. Start from pixel 5 and step ahead 7 pixels
    for i in range(4 * 5, len(row), 4 * 7):
        s.append(row[i] & 0x7f)
    print(s.decode("utf-8"))

    # output: "smart guy, you made it. the next level is [105, 110, 116, 101, 103, 114, 105, 116, 121]]kU"
    # ignore the ]ku at the end, and we get again a list of character codes:

    chars = [105, 110, 116, 101, 103, 114, 105, 116, 121]
    s = [chr(c) for c in chars]
    print("".join(s))

    # answer: integrity