import re


def testPatt(str, pattern):
    search = re.search(pattern, str)
    if search:
        print("{}, accepted. ".format(search.group()))
    else:
        print("{}, rejected. ".format(str))

print('DATE')

str = '0'
pattern = r"\d+/\d+(?:/\d+)*|^0$"
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

str = '01/12/16'
testPatt(str, pattern)

str = '01/12/2015'
testPatt(str, pattern)

str = '1/10'
testPatt(str, pattern)

pattern = r"\d+:\d\d|^0$"

print('\nHOUR/MIN')
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

str = '00:00'
testPatt(str, pattern)

str = '0:0'
testPatt(str, pattern)