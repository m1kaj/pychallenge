"""http://www.pythonchallenge.com/pc/def/linkedlist.php
"""

# The hint is an image. Clicking the image loads URL
# http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=12345
# which contains just text "and the next nothing is 44827"
# Setting 44827 into the URL parameter returns 
# "and the next nothing is 45439". Using this returns
# "Your hands are getting tired and the next nothing is 94485"

# Our first guess: we'll need to follow the links until we get
# something that does NOT include "next nothing is <number>"

# This worked for a number of times, then we got response
# "Yes. Divide by two and keep going." Clearly this was
# not the final answer.

# So, we keep reading new numbers, or as special case,
# divide previous number by two. Until the response is 
# something different than these two.

import urllib.request
import re

parameter = "12345"

while parameter:

    # Read page content
    print(f"trying parameter: {parameter}")
    with urllib.request.urlopen(f"http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing={parameter}") as html:
        text = html.read().decode("utf-8")

    # Get next parameter, divide by two, or quit
    match = re.search("next nothing is ([0-9]+)", text)
    if match:
        parameter = match.group(1)
    elif text.find("Divide by two") > -1:
        parameter = str(int(parameter) / 2)
    else:
        parameter = None

print(text)
