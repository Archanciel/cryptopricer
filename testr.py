import unittest
import os,sys,inspect
from io import StringIO

import re
PATTERN_FULL_PRICE_REQUEST_DATA = r"(\w+)(?: (\w+)|) ([\d/]+) ([0-9:]+)(?: (\w+)|)"

'''
Grabs one group of kind -cbtc or -t12:54 or -d15/09 followed
by several OPTIONAL groups sticking to the same format
-<command letter> followed by 1 or more \w or \d or / or :
characters.

Unlike with pattern 'full', the groups can occur in
any order, reason for which all groups have the same
structure
'''
PATTERN_PARTIAL_PRICE_REQUEST_DATA = r"(?:(-\w)([\w\d/:]+))(?: (-\w)([\w\d/:]+))?(?: (-\w)([\w\d/:]+))?(?: (-\w)([\w\d/:]+))?(?: (-\w)([\w\d/:]+))?"

class Requester:
    def _parseGroups(self, pattern, inputStr):
        match = re.match(pattern, inputStr)

        if match != None:
            return match.groups()
        else:
            return ()


class TestR(unittest.TestCase):
    def setUp(self):
        self.requester = Requester()

    def test_parseGroupsFullDayMonthHHMM(self):
        inputStr = "btc usd 10/9 12:45 Kraken"
        groupList = self.requester._parseGroups(PATTERN_FULL_PRICE_REQUEST_DATA, inputStr)
    
        self.assertEqual(('btc','usd','10/9','12:45','Kraken'), groupList)


    def test_parseGroupsFullDayMonthYearHMM(self):
        inputStr = "btc usd 10/9/17 1:45 Kraken"
        groupList = self.requester._parseGroups(PATTERN_FULL_PRICE_REQUEST_DATA, inputStr)
    
        self.assertEqual(('btc','usd','10/9/17','1:45','Kraken'), groupList)


    def test_parseGroupsFullDH(self):
        inputStr = "btc usd 1 2 Kraken"
        groupList = self.requester._parseGroups(PATTERN_FULL_PRICE_REQUEST_DATA, inputStr)
    
        self.assertEqual(('btc','usd','1','2','Kraken'), groupList)


    def test_parseGroupsFullDayHH(self):
        inputStr = "btc usd 10 12 Kraken"
        groupList = self.requester._parseGroups(PATTERN_FULL_PRICE_REQUEST_DATA, inputStr)
    
        self.assertEqual(('btc','usd','10','12','Kraken'), groupList)


    def test_parseGroupsPartialDayMonthHHMM(self):
        inputStr = "-ceth -fgbp -d11/8 -t22:46 -eKraken"
        groupList = self.requester._parseGroups(PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c','eth','-f','gbp','-d','11/8','-t','22:46','-e','Kraken'), groupList)


    def test_parseGroupsPartialDayMonthYearHMM(self):
        inputStr = "-ceth -fgbp -d11/8/17 -t2:46 -eKraken"
        groupList = self.requester._parseGroups(PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c','eth','-f','gbp','-d','11/8/17','-t','2:46','-e','Kraken'), groupList)


    def test_parseGroupsPartialDayMonthYearHMM(self):
        inputStr = "-ceth -fgbp -d11/8/17 -t2:46 -eKraken"
        groupList = self.requester._parseGroups(PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c','eth','-f','gbp','-d','11/8/17','-t','2:46','-e','Kraken'), groupList)


    def test_parseGroupsPartialDH(self):
        inputStr = "-ceth -fgbp -d1 -t2 -eKraken"
        groupList = self.requester._parseGroups(PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c','eth','-f','gbp','-d','1','-t','2','-e','Kraken'), groupList)


    def test_parseGroupsPartialDayHH(self):
        inputStr = "-ceth -fgbp -d11 -t22 -eKraken"
        groupList = self.requester._parseGroups(PATTERN_PARTIAL_PRICE_REQUEST_DATA, inputStr)

        self.assertEqual(('-c','eth','-f','gbp','-d','11','-t','22','-e','Kraken'), groupList)


if __name__ == '__main__':
    unittest.main()
