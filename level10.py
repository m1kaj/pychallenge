"""http://www.pythonchallenge.com/pc/return/bull.html
"""

# Page title is "what are you looking at?". Page has an image
# of a cow looking at the camera. And a hint: "len(a[30]) = ?"
# The picture is also a link to /sequence.txt. That file contains
# only "a = [1, 11, 21, 1211, 111221, "

# We have a sequence of integers. But why to ask length of
# an integer then? Aah, they are to be treated as strings.
# It seems:
#    a[3] = a[3-3] + first half of a[3-1] + a[3-2]
#    a[4] = a[4-3] + first half of a[4-1] + a[4-2]
# this way answer became 566727 but it was not correct

# Next: a[n] = a[n-1] with halves swapped + a[n-2]
# This would work for the two last given numbers.
# Answer: 1664080
# But this is not correct either

# So I had to look up a hint. And it was about language again.
# The hint said: "SAY the numbers, then look at them"
# 1  => one one => 11
# 11 => two one's => 21
# 21 => one two, one one => 1211
# 1211 => one one, one two, two one's => 111221
# 111221 => three one's, two two's, one one => 312211
# 312211 => one three, one one, two two's, two one's => 13112221

# Hint said to checkout itertools.groupby()
# Well, I briefly did and it looked like I needed time to
# study those itertools. So we go with function using
# just len() and string indexing. Given a string s
# function calculates next value in string form

def look_and_say(s):
    # handle trivial case of single digit
    if len(s) == 1:
        return "1" + s
    # loop and handle 2 or more digit numbers
    i = 1
    current_number = s[0]
    how_many = 1
    result = ""
    while True:
        if current_number == s[i]:
            how_many += 1
        else:
            result += str(how_many) + current_number
            current_number = s[i]
            how_many = 1
        i += 1
        # if we reached the end, append remaining digit and
        # exit loop
        if i == len(s):
            result += str(how_many) + current_number
            break
    return result

# start with "1"
a = ["1"]

# calculate enough numbers in sequence
for i in range (1, 31):
    a.append(look_and_say(a[-1]))

# check length of number at index 30
print(f"Answer: {len(a[30])}")

# Answer: 5808