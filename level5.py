"""http://www.pythonchallenge.com/pc/def/peak.html
"""

# The hint is an image of a grassy hill. Page title is
# "peak hell" and a hint is written: "pronounce it".
# At this point I have no idea what is going on, so
# I check page source and see a link "/banner.p".

# Loading the link shows strange data that is not random
# binary. Firefox displays it as few characters in a line.
# There are a lot of lines. It starts like this:
# (lp0
# (lp1
# (S' '
# p2
# I95
# tp3

# Web search reminds me that Python has module called pickle.
# It can serialize and de-serialize data, specifically Python 
# objects. So one can use it to save a list or dictionary
# to disk, for example. OK, I guess "peak hell" sounds like
# "pickle" when said aloud.

# So let's load the file using pickle and see what comes out:
#  - the object is a list of lists
#  - each sub list contains tuples
#  - each tuple has a single character of either ' ' or '#',
#    paired with a number

# Since the file name was banner.p, maybe this is some kind 
# of ASCII art where tuples pack the data =>
#    #####   becomes  ('#', 5)

# After printing it out we get a banner with text.

import urllib.request
import pickle

with urllib.request.urlopen("http://www.pythonchallenge.com/pc/def/banner.p") as html:
        content = html.read()
        
my_object = pickle.loads(content)
for item in my_object:
    line = ""
    for packed in item:
        line += packed[1] * packed[0]
    print(line)

                                                                                               
              #####                                                                      ##### 
               ####                                                                       #### 
               ####                                                                       #### 
               ####                                                                       #### 
               ####                                                                       #### 
               ####                                                                       #### 
               ####                                                                       #### 
               ####                                                                       #### 
      ###      ####   ###         ###       #####   ###    #####   ###          ###       #### 
   ###   ##    #### #######     ##  ###      #### #######   #### #######     ###  ###     #### 
  ###     ###  #####    ####   ###   ####    #####    ####  #####    ####   ###     ###   #### 
 ###           ####     ####   ###    ###    ####     ####  ####     ####  ###      ####  #### 
 ###           ####     ####          ###    ####     ####  ####     ####  ###       ###  #### 
####           ####     ####     ##   ###    ####     ####  ####     #### ####       ###  #### 
####           ####     ####   ##########    ####     ####  ####     #### ##############  #### 
####           ####     ####  ###    ####    ####     ####  ####     #### ####            #### 
####           ####     #### ####     ###    ####     ####  ####     #### ####            #### 
 ###           ####     #### ####     ###    ####     ####  ####     ####  ###            #### 
  ###      ##  ####     ####  ###    ####    ####     ####  ####     ####   ###      ##   #### 
   ###    ##   ####     ####   ###########   ####     ####  ####     ####    ###    ##    #### 
      ###     ######    #####    ##    #### ######    ###########    #####      ###      ######