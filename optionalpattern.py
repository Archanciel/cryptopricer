import unittest
import os,sys,inspect
from io import StringIO

import re

'''
Full price command parms pattern. Crypto symbol (mandatory), fiat symbol (optional), date (optional),
time (optional) and exchange (optional). Must be provided in this order.
    
Ex; btc usd 13/9 12:15 Kraken
'''
PATTERN_FULL_PRICE_REQUEST_DATA = r"(\w+)(?: ([\w\d/:]+)|)(?: ([\w\d/:]+)|)(?: ([\w\d/:]+)|)(?: (\w+)|)"

'''
Grabs one group of kind -cbtc or -t12:54 or -d15/09 followed
by several OPTIONAL groups sticking to the same format
-<command letter> followed by 1 or more \w or \d or / or :
characters.

Unlike with pattern 'full', the groups can occur in
any order, reason for which all groups have the same
structure
'''

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


    def test_parseGroupsFullDayNoTime(self):
        inputStr = "btc usd 12 Kraken"
        groupList = self.requester._parseGroups(PATTERN_FULL_PRICE_REQUEST_DATA, inputStr)
    
        self.assertEqual(('btc','usd','12','Kraken',None), groupList)


    def test_parseGroupsFullNoDayNoTime(self):
        inputStr = "btc usd Kraken"
        groupList = self.requester._parseGroups(PATTERN_FULL_PRICE_REQUEST_DATA, inputStr)
    
        self.assertEqual(('btc','usd','Kraken',None,None), groupList)


    def test_parseGroupsFullNoFiatNoDayNoTime(self):
        inputStr = "btc Kraken"
        groupList = self.requester._parseGroups(PATTERN_FULL_PRICE_REQUEST_DATA, inputStr)
    
        self.assertEqual(('btc','Kraken',None,None,None), groupList)


    def test_parseGroupsFullNoFiatNoDayNoTimeNoExchange(self):
        inputStr = "btc"
        groupList = self.requester._parseGroups(PATTERN_FULL_PRICE_REQUEST_DATA, inputStr)
    
        self.assertEqual(('btc',None,None,None,None), groupList)


    def test_parseGroupsFullNoFiatDMHHMMNoExchange(self):
        inputStr = "btc 1/9 12:05"
        groupList = self.requester._parseGroups(PATTERN_FULL_PRICE_REQUEST_DATA, inputStr)
        self.assertEqual(('btc', '1/9', '12:05', None, None), groupList)


if __name__ == '__main__':
    unittest.main()
