import re


def testPatt(str, pattern):
    search = re.search(pattern, str)
    if search:
        print(search.group())
        
str = '0'
pattern = r"\d+/\d+|^0$"
#pattern = r"[\d]+:[\d]+|^0$"

testPatt(str, pattern)

str = '1'
testPatt(str, pattern)

str = '10'
testPatt(str, pattern)

str = '01'
testPatt(str, pattern)

str = '01/1'
testPatt(str, pattern)

str = '01/10'
testPatt(str, pattern)

str = '1/10'
testPatt(str, pattern)

pattern = r"\d+:\d\d|^0$"

print('hour/min')
str = '0'
testPatt(str, pattern)

str = '1'
testPatt(str, pattern)

str = '10'
testPatt(str, pattern)

str = '01'
testPatt(str, pattern)

str = '01:1'
testPatt(str, pattern)

str = '01:01'
testPatt(str, pattern)

str = '01:10'
testPatt(str, pattern)