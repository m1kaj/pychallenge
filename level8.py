"""http://www.pythonchallenge.com/pc/def/integrity.html
"""

# Page has a fuzzy picture of an insect in a flower.
# Clicking the picture brings up an authorization box
# with a username and password input.
#
# Viewing the source shows the HTML body is
#<body>
#	<br><br>
#	<img src="integrity.jpg" width="640" height="480" border="0" usemap="#notinsect"/>
#	<map name="notinsect">
#	<area shape="poly" 
#		coords="179,284,214,311,255,320,281,226,319,224,363,309,339,222,371,225,411,229,404,242,415,252,428,233,428,214,394,207,383,205,390,195,423,192,439,193,442,209,440,215,450,221,457,226,469,202,475,187,494,188,494,169,498,147,491,121,477,136,481,96,471,94,458,98,444,91,420,87,405,92,391,88,376,82,350,79,330,82,314,85,305,90,299,96,290,103,276,110,262,114,225,123,212,125,185,133,138,144,118,160,97,168,87,176,110,180,145,176,153,176,150,182,137,190,126,194,121,198,126,203,151,205,160,195,168,217,169,234,170,260,174,282" 
#		href="../return/good.html" />
#	</map>
#	<br><br>
#	<font color="#303030" size="+2">Where is the missing link?</font>
#</body>

# There is also this comment
# <!--
# un: 'BZh91AY&SYA\xaf\x82\r\x00\x00\x01\x01\x80\x02\xc0\x02\x00 \x00!\x9ah3M\x07<]\xc9\x14\xe1BA\x06\xbe\x084'
# pw: 'BZh91AY&SY\x94$|\x0e\x00\x00\x00\x81\x00\x03$ \x00!\x9ah3M\x13<]\xc9\x14\xe1BBP\x91\xf08'
# -->

# We start by going to w3schools.com to see what these HTML tags mean. <map> tag 
# defines a client-side image map with clickable areas. There is only one area with
# the link leading to /good.html, which triggers the auth dialog. Maybe we should
# plot the coordinates in a 2D plot to see the shape of the clickable polygon.

# tried to draw a plot using shapely and matplotlib, but the env I'm using doesn't
# allow the lib to draw. Plotting the dots online looks like they only outline the 
# bee in the picture. So what is the use of that?
# link /insect.html returns "BE more specific"
# link /bee.html returns "and she is BUSY."
# link /busy.html returns "all bees sound busy too."

# Those bee and busy hints did nothing, I don't like these plays with foreign 
# language (English). But googling the starting bytes of encoded username and password 
# showed they are most likely BZIP2 encoded data. So we can decode them:

import bz2

un = b'BZh91AY&SYA\xaf\x82\r\x00\x00\x01\x01\x80\x02\xc0\x02\x00 \x00!\x9ah3M\x07<]\xc9\x14\xe1BA\x06\xbe\x084'
pw = b'BZh91AY&SY\x94$|\x0e\x00\x00\x00\x81\x00\x03$ \x00!\x9ah3M\x13<]\xc9\x14\xe1BBP\x91\xf08'
username = bz2.decompress(un)
password = bz2.decompress(pw)
print(username)   # => b'huge'
print(password)   # => b'file'

# answer : huge/file