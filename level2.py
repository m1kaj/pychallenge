"""http://www.pythonchallenge.com/pc/def/ocr.html
"""

# The hint says to recognize the characters, and that they
# are in the page source. Viewing the HTML source in browser
# shows at the end there is an empty line followed by a
# large blob of text. The blob has special characters and
# starts with:
# <!--%%$@_$^__#)^)&!_+]!*@&^}@[@%]()%+$&  ...

# Let's just read the source, split using empty lines,
# grab the last part and strip every character except
# a-z, space, period or comma.

import urllib.request
import re

with urllib.request.urlopen("http://www.pythonchallenge.com/pc/def/ocr.html") as html:
    text = html.read().decode("utf-8")
blob = text.split("<!--")[-1]

# We could use regular expression to substitute all
# non-wanted characters from the blob.

answer = re.sub("[^a-zA-Z]{1}", "", blob)
print(answer)
