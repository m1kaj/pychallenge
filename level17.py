"""http://www.pythonchallenge.com/pc/return/romance.html
"""

# login credentials when returning are still: huge/file
#
# Page has a picture of chocolate chip cookies. Lower left corner has a smaller
# picture that looks like some mechanical gadget or toy that represents two
# men sawing a log. Page title is "eat?" and image file name is cookies.jpg.

# download image
import urllib.request
password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
top_level_url = "http://www.pythonchallenge.com/"
password_mgr.add_password(None, top_level_url, "huge", "file")
handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
opener = urllib.request.build_opener(handler)
urllib.request.install_opener(opener)
urllib.request.urlretrieve("http://www.pythonchallenge.com/pc/return/cookies.jpg",
    filename="cookies.jpg")

# Quick binary dump of image didn't reveal anything clearly interesting...
# Let's reload the page and look at response headers. Do we get cookies?

resp = urllib.request.urlopen("http://www.pythonchallenge.com/pc/return/romance.html")
for k, v in resp.getheaders():
    print(f"  {k}: {v}")

#  Vary: Accept-Encoding
#  Content-Type: text/html
#  Accept-Ranges: bytes
#  ETag: "1726728061"
#  Last-Modified: Sat, 12 Mar 2016 19:38:46 GMT
#  Content-Length: 207
#  Connection: close
#  Date: Fri, 12 Jun 2020 20:26:20 GMT
#  Server: lighttpd/1.4.35
#
# Don't really see anything interesting in response headers. Next I tried
# to send cookie to server in request headers, with content eat; cookie; eat=cookies.
# Did not change the response at all.
#
# I had to look up a hint from internet. And the hint was that the smaller image
# is from level 4. I did not have any memory of it, because I am doing these 
# challenges over an extended time due to work and other tasks.
#
# Let's then repeat level 4, and expect to get a cookie in the headers:

resp = urllib.request.urlopen("http://www.pythonchallenge.com/pc/def/linkedlist.php")
cookie = resp.getheader("Set-Cookie")
print(f"Set-Cookie: {cookie}")

# We got
# Set-Cookie: info=you+should+have+followed+busynothing...; expires=Fri,
#   19-Jun-2020 20:54:57 GMT; Max-Age=604800; path=/; domain=.pythonchallenge.com
#
# In level 4 we kept repeating the URL with query parameter ?nothing=<number>.
# Now when trying manually with query parameter ?busynothing, it returns similar
# sequence. And every page has a cookie in header. Cookie has "info=" followed by
# character. Maybe they form some sequence? We copy level 4 loop here and try:

import re
parameter = "12345"
infos = list()

while parameter:
    with urllib.request.urlopen(f"http://www.pythonchallenge.com/pc/def/linkedlist.php?busynothing={parameter}") as html:
        cookie = html.getheader("Set-Cookie", "FAIL")
        match = re.search("info=(.+?);", cookie)
        info = match.group(1)
        print(f"info: {info}")
        infos.append(info)
        text = html.read().decode("utf-8")
        print(text)

    # Get next parameter, divide by two, or quit
    match = re.search("next busynothing is ([0-9]+)", text)
    if match:
        parameter = match.group(1)
    elif text.find("Divide by two") > -1:
        parameter = str(int(parameter) / 2)
    else:
        parameter = None

print(f"\n INFO={infos}")

# INFO=['B', 'Z', 'h', '9', '1', 'A', 'Y', '%26', 'S', 'Y', '%94', '%3A', '%E2', 'I', '%00', '%00',
# '%21', '%19', '%80', 'P', '%81', '%11', '%00', '%AF', 'g', '%9E', '%A0', '+', '%00', 'h', 'E',
# '%3D', 'M', '%B5', '%23', '%D0', '%D4', '%D1', '%E2', '%8D', '%06', '%A9', '%FA', '%26', 'S',
# '%D4', '%D3', '%21', '%A1', '%EA', 'i', '7', 'h', '%9B', '%9A', '%2B', '%BF', '%60', '%22', '%C5',
# 'W', 'X', '%E1', '%AD', 'L', '%80', '%E8', 'V', '%3C', '%C6', '%A8', '%DB', 'H', '%26', '3', '2',
# '%18', '%A8', 'x', '%01', '%08', '%21', '%8D', 'S', '%0B', '%C8', '%AF', '%96', 'K', 'O', '%CA',
# '2', '%B0', '%F1', '%BD', '%1D', 'u', '%A0', '%86', '%05', '%92', 's', '%B0', '%92', '%C4', 'B',
# 'c', '%F1', 'w', '%24', 'S', '%85', '%09', '%09', 'C', '%AE', '%24', '%90']
#
# What is that? Google search for BZ and BZh gave various results. One of them was Bzip2:
# https://en.wikipedia.org/wiki/Bzip2
#
# .magic:16                       = 'BZ' signature/magic number
# .version:8                      = 'h' for Bzip2 ('H'uffman coding), '0' for Bzip1 (deprecated)
# .hundred_k_blocksize:8          = '1'..'9' block-size 100 kB-900 kB (uncompressed)
#
# Pretty sure we have a Huffman coded Bzip2 file. At this point I looked at solved levels and
# we already did Bzip2 in level 8.  *facepalm*

data = ['B', 'Z', 'h', '9', '1', 'A', 'Y', '%26', 'S', 'Y', '%94', '%3A', '%E2', 'I', '%00', '%00',
  '%21', '%19', '%80', 'P', '%81', '%11', '%00', '%AF', 'g', '%9E', '%A0', '+', '%00', 'h', 'E',
  '%3D', 'M', '%B5', '%23', '%D0', '%D4', '%D1', '%E2', '%8D', '%06', '%A9', '%FA', '%26', 'S',
  '%D4', '%D3', '%21', '%A1', '%EA', 'i', '7', 'h', '%9B', '%9A', '%2B', '%BF', '%60', '%22', '%C5',
  'W', 'X', '%E1', '%AD', 'L', '%80', '%E8', 'V', '%3C', '%C6', '%A8', '%DB', 'H', '%26', '3', '2',
  '%18', '%A8', 'x', '%01', '%08', '%21', '%8D', 'S', '%0B', '%C8', '%AF', '%96', 'K', 'O', '%CA',
  '2', '%B0', '%F1', '%BD', '%1D', 'u', '%A0', '%86', '%05', '%92', 's', '%B0', '%92', '%C4', 'B',
  'c', '%F1', 'w', '%24', 'S', '%85', '%09', '%09', 'C', '%AE', '%24', '%90']

# There is surely some library to url decode these values to bytes. 
# We try to mangle them to binary file with a hideous for loop and then decode.

import binascii
import bz2

fp = open("my.bz2", "wb")
for c in data:
    if c.startswith("%"):
        char = c.replace("%", "", 1)
        fp.write(binascii.unhexlify(char.encode()))
    else:
        c = ' ' if c == '+' else c   # + in URL encoding for space
        fp.write(c.encode())
fp.close()

with bz2.open("my.bz2", "rb") as f:
    hint = f.read()

print(hint)

# This gave:
# b'is it the 26th already? call his father and inform him that "the flowers are on their way". he\'ll understand.'

# 26th? Mozart's father? Call him? Wat?
# Level 13 had code for calling using the RPC method. Let's copy the code and call Mozart.

from xmlrpc.client import ServerProxy, Error

with ServerProxy("http://www.pythonchallenge.com/pc/phonebook.php") as proxy:
    try:
        r = proxy.phone("Mozart")
    except Error as ev:
        print(f"Error happened: {ev}")
    
    print(f"Answer: {r}")   # Answer: He is not the evil

    # We googled Mozart's father. His name was Leopold.
    try:
        r = proxy.phone("Leopold")
    except Error as ev:
        print(f"Error happened: {ev}")
    
    print(f"Answer: {r}")   # Answer: 555-VIOLIN

# Try: http://www.pythonchallenge.com/pc/return/violin.html
# => page says "no! i mean yes! but ../stuff/violin.php."
#
# Try: http://www.pythonchallenge.com/pc/stuff/violin.php
# Page title is "it's me. what do you want?" and there is photo of some man who we assume
# is Mozart's father.
#
# This is getting repetitive. We query for methods again, copying code
# from level 13. But that failed to an error, so code is remoaved from here.
# Looks like there is no proxy there. 
# 
# Try cookie to pass the message about flowers:

headers = {"Cookie": "info=the+flowers+are+on+their+way"}
req = urllib.request.Request("http://www.pythonchallenge.com/pc/stuff/violin.php", headers=headers)
with urllib.request.urlopen(req) as resp:
        cookie = resp.getheader("Set-Cookie", "FAIL")
        print(f"cookie: {cookie}")
        text = resp.read().decode("utf-8")
        print(text)

# We get:
# cookie: FAIL
# <html>
# <head>
#   <title>it's me. what do you want?</title>
#   <link rel="stylesheet" type="text/css" href="../style.css">
# </head>
# <body>
#         <br><br>
#         <center><font color="gold">
#         <img src="leopold.jpg" border="0"/>
# <br><br>
# oh well, don't you dare to forget the balloons.</font>
# </body>
# </html>

# YES! Solution is: http://www.pythonchallenge.com/pc/return/balloons.html
