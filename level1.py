"""http://www.pythonchallenge.com/pc/def/map.html
"""

# The hint shows three letters mapped into a letter coming two
# positions later in the English alphabet. There is encrypted
# text. We see Python docs has string methods for translating
# characters, so let's try to use those.

encrypted_text = """g fmnc wms bgblr rpylqjyrc gr zw fylb.
rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq 
glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle 
qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj. 
"""

source = "abcdefghijklmnopqrstuvwxyz ()."
target = "cdefghijklmnopqrstuvwxyzab ()."
tr_table = str.maketrans(source, target)
translated_text = encrypted_text.translate(tr_table)
print(translated_text)

# This prints out recommendation to use maketrans
# and tells to apply the same translation to URL.
#   m -> o
#   a -> c
#   p -> r