"""http://www.pythonchallenge.com/pc/def/channel.html
"""

# Page title is "now there are pairs" and the hint is an
# image of pants or skirt with an open zipper. Page source
# has string: <!-- <-- zip -->
# Following link /zip.html loads a page that just has text:
# "yes. find the zip"

# Trying link /channel.zip returns binary data that starts
# with "PK". We know .ZIP file format was created by Phil
# Katz and his company Pkware. The binary data also has 
# what looks like file names. So we'll download the file
# and use Python's zipfile library, which seems to have
# methods for accessing file contents straight from the
# opened zip archive. Nice!
# But first we examine the files manually. There is a file
# readme.txt that says "start from 90052". File 90052.txt
# contains: "next nothing is 94191".

# This then starts to look like Level 4 again with the 
# linked list to follow to the end!

# After running the linked list, we end up with file
# 46145.txt that says "Collect the comments."
# Going to Wikipedia, the entry for zip file format does 
# tell that each file has a central directory header. And
# that header includes a comment field. Conveniently 
# zipfile library has a method for getting the comment.

import urllib.request
import re
import zipfile

urllib.request.urlretrieve("http://www.pythonchallenge.com/pc/def/channel.zip",
    filename="channel.zip")

parameter = "90052"
comments = ""

with zipfile.ZipFile("channel.zip", "r") as myzip:
    while parameter:
        # read file contents from archive using file name
        print(f"trying file: {parameter}.txt")
        text = myzip.read(f"{parameter}.txt").decode("utf-8")
        # get comment for archived file and append to string
        zipobj = myzip.getinfo(f"{parameter}.txt")
        comments += zipobj.comment.decode("utf-8")
        # check whether file has link to next file, divide
        # by two request, or something else (final answer)
        match = re.search("Next nothing is ([0-9]+)", text)
        parameter = match.group(1) if match else None

print(comments)

# output is
#
# ****************************************************************
# ****************************************************************
# **                                                            **
# **   OO    OO    XX      YYYY    GG    GG  EEEEEE NN      NN  **
# **   OO    OO  XXXXXX   YYYYYY   GG   GG   EEEEEE  NN    NN   **
# **   OO    OO XXX  XXX YYY   YY  GG GG     EE       NN  NN    **
# **   OOOOOOOO XX    XX YY        GGG       EEEEE     NNNN     **
# **   OOOOOOOO XX    XX YY        GGG       EEEEE      NN      **
# **   OO    OO XXX  XXX YYY   YY  GG GG     EE         NN      **
# **   OO    OO  XXXXXX   YYYYYY   GG   GG   EEEEEE     NN      **
# **   OO    OO    XX      YYYY    GG    GG  EEEEEE     NN      **
# **                                                            **
# ****************************************************************
#  **************************************************************

# But link /hockey.html returns just "it's in the air. look at
# the letters"
#
# Answer: oxygen
