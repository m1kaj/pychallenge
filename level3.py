"""http://www.pythonchallenge.com/pc/def/euality.html
"""

# Just like the previous level, here we have a blob
# of text in the end of the page HTML source.
# The blob has lots of special characters and
# starts with:
# <!--%%$@_$^__#)^)&!_+]!*@&^}@[@%]()%+$&  ...

# This time the hint is "One small letter surrounded
# by EXACTLY three big bodyguards on each of its sides"

import urllib.request
import re

with urllib.request.urlopen("http://www.pythonchallenge.com/pc/def/equality.html") as html:
    text = html.read().decode("utf-8")
blob = text.split("<!--")[-1]

# We use regexp to look for a pattern:
#   anything but upper case letter,
#   followed by three upper case letters,
#   followed by one lower case letter,
#   followed by three upper case letters,
#   followed by anything but an upper case letter

answer = re.findall("[^A-Z]{1}[A-Z]{3}([a-z]{1})[A-Z]{3}[^A-Z]{1}", blob)
print(answer)   # will be single letters in a list
