"""http://www.pythonchallenge.com/pc/return/evil.html
"""

# Page has an image of someone dealing cards on a table.
# They appear as playing cards with strange symbol on
# the back side. Page title is "dealing evil"
#
# Source shows image file is "evil1.jpg".
#
# As in previous challenge, the pixels in image appear
# interlaced somehow. Maybe we have to images mixed together
# again? Then how is this different than level 11?
#
# We try incrementing number in evil1.jpg:
#  evil2.jpg => picture that says "not jpg- _.gfx"
#  evil3.jpg => picture that says "no more evils..."
#  evil4.jpg => link seems to exist but size is 0 x 0
# 
# After playing with the URLs, there is a file evil2.gfx.
# Let's load it:

import urllib.request
password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
top_level_url = "http://www.pythonchallenge.com/"
password_mgr.add_password(None, top_level_url, "huge", "file")
handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
opener = urllib.request.build_opener(handler)
urllib.request.install_opener(opener)
urllib.request.urlretrieve("http://www.pythonchallenge.com/pc/return/evil2.gfx",
    filename="evil2.gfx")

# Doing hexdump evil2.gfx |head -10 in Ubuntu terminal 
# and entering the bytes into google search with words
# "image file header" shows pretty good amount of hits of
# bytes in page https://en.wikipedia.org/wiki/List_of_file_signatures

# Print 20 bytes from beginning of file
fp = open("evil2.gfx", "rb")
header = fp.read(20)
printable = ["{0:x}".format(b) for b in header]
print(printable)
fp.close()

# It looks like we have PNG, GIF and JPG headers interleaved, every 5th byte
#
# ['ff', '89', '47', '89', 'ff', 'd8', '50', '49', '50', 'd8', 'ff', '4e', '46', '4e', 'ff', 'e0', '47', '38', '47', 'e0']
#   C1    A1    B     A2    C2    C1    A1    B     A2    C2    C1    A1    B     A2    C2    C1    A1    B     A2    C2
#
# A) PNG header: 89 50 4E 47 0D 0A 1A 0A
# B) GIF87a header: 47 49 46 38 37 61
# C) JPG header: FF D8 FF E0 00 10 4A 46
#
# Try splitting to 5 files: JPG, PNG, GIF, PNG, JPG
# Input file is so small, we just read it to memory

fp = open("evil2.gfx", "rb")
mixed_bytes = fp.read()
fp.close()
suffixes = ["jpg", "png", "gif", "png", "jpg"]
writefiles = [open(f"img{i}.{suffixes[i - 1]}", "wb") for i in range(1, 6)]
n = 0
for b in mixed_bytes:
    writefiles[n % 5].write(b.to_bytes(1, byteorder="big", signed=False))
    n += 1
for fp in writefiles:
    fp.close()

# Output is four images and one apparently corrupted image (png).
# images say:  "dis", "pro", "port", <corrupt?>, "ity"
# Last part has strike-through font, so we guess solution is either 
# "disproportionality" or "disproportional". Trial and error show
# it is the latter: "disproportional".