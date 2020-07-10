"""http://www.pythonchallenge.com/pc/return/balloons.html
"""

# login credentials when returning are still: huge/file
#
# Page has an image which contains two side by side images of swans (birds).
# Both sides are the same picture but have two distinct brightness 
# levels. Page title is "can you tell the difference?". Page source
# code contains string "it is more obvious that what you might think".

# I guessed we just need to subtract one half of the image from the other.
# So copied script from previous levels to open the image, crop new images
# from left and right side, and use PIL.ImageChops.difference to  ake a new
# image. This only resulted in the same image, no hidden message with subtle
# differences in brightness.

# Have to resort to guessing. Trying the following URL endings:
# difference.html, swan.html, swans.html, brightness.html, and so on...
# They all returned 404 except one: http://www.pythonchallenge.com/pc/return/brightness.html
# That one returned the same page as original page. Onmly this time view source
# showed comment: "<!-- maybe consider deltas.gz -->"
#
# Manually downloading and decrypting http://www.pythonchallenge.com/pc/return/deltas.gz
# shows it a text file. It has two tables of hex bytes, side by side. 
# Both have header/magic bytes telling they are PNG image files. One table 
# has more rows than the other. Also some rows near bottom are not equal
# length, or are missing bytes. Closer look at the PNG bytes, in the first chunk
# called IHDR we see image dimensions are 650 * 200 pixels.

# Started by writing this data out into two PNG images. Result was
# the PNG images do not show any content in Ubuntu. Trying to build
# difference of the images using PIL library gave error:
# "OSError: unrecognized data stream contents when reading image file"
# Also pypng library complained IDAT chunk checksums were bad.
# Have to assume then, that the data is not two complete PNG files.
# Need to try to find differences in the rows and build a valid image.

# Let's write data to two text files
import urllib.request
import gzip
password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
top_level_url = "http://www.pythonchallenge.com/"
password_mgr.add_password(None, top_level_url, "huge", "file")
handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
opener = urllib.request.build_opener(handler)
urllib.request.install_opener(opener)
urllib.request.urlretrieve("http://www.pythonchallenge.com/pc/return/deltas.gz",
    filename="deltas.gz")

out1 = open("left.txt", "w")
out2 = open("right.txt", "w")
with gzip.open("deltas.gz") as fp:
    try:
        text = fp.read().decode("utf-8")
        for line in text.splitlines():
            left = line[:55].strip()
            right = line[55:].strip()
            out1.write(left + "\n")
            out2.write(right + "\n")
    except Exception as err:
        print(repr(err))
    finally:
        out1.close()
        out2.close()
        fp.close()

# Stopped at this point. If we need to subtract one image chunk values from another,
# using text files, I think there would be checksums to handle as well. 