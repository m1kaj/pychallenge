"""http://www.pythonchallenge.com/pc/return/uzi.html
"""

# login credentials: huge/file
#
# Page title is "Whom?". There is a picture of a calendar month.
# The picture has parts obscured, but we get the following clues:
#
# - year starts with "1" and ends with "6"
# - January 26th is circled
# - January 26th is Monday
# - year is leap year (February has 29 days)
#
# Additionally, page source has comments:
#     "he ain't the youngest, he is the second"
#     "todo: buy flowers for tomorrow"

# We could start by finding out which year it could be. Let's start
# by assuming year is between 1000 - 2000.

import calendar

candidate_years = list()
for year in range(1000, 2000):
    if not str(year).endswith("6"): continue
    if not calendar.isleap(year): continue
    weekday = calendar.weekday(year, 1, 26)
    if calendar.day_name[weekday] != "Monday": continue
    candidate_years.append(year)
print (candidate_years)

# this gave us years: [1176, 1356, 1576, 1756, 1976]
# If this was about birthdays, the youngest would be born 26-Jan-1976.
# The second youngest would be born 26-Jan-1756. Who is born that day?
# Google doesn't find anyone interesting, but the clue says to buy flowers for tomorrow.
# And Wolfgang Amadeus Mozart was born 27-Jan-1756.
#
# Solution is http://www.pythonchallenge.com/pc/return/mozart.html