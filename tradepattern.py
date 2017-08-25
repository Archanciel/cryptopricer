import re

inputStr = "[btc 22/08 23:54 0.00043306 ccex] [usd]"
upperInputStr = inputStr.upper()

#r"(\d+/\d+) ([0-9]+\.[0-9]+)"

CURRENCY_SYMBOL_GRP_PATTERN = r"([A-Z]+)"
DD_MM_DATE_GRP_PATTERN = r"(\d+/\d+)"
HH_MM_TIME_GRP_PATTERN = r"(\d+:\d+)"
DOUBLE_PRICE_PATTERN = r"([0-9]+\.[0-9]+)"
DOUBLE_PRICE_PATTERN = r"(\d+\.\d+)"
EXCHANGE_SYMBOL_GRP_PATTERN = r"([A-Z]+)"

pattern = r"(\[" + \
	           CURRENCY_SYMBOL_GRP_PATTERN + \
	           	r" " + \
	           	DD_MM_DATE_GRP_PATTERN + \
	           	r" " + \
	           	HH_MM_TIME_GRP_PATTERN + \
	           	r" " + \
	           	DOUBLE_PRICE_PATTERN + \
	           	r" " + \
	           	EXCHANGE_SYMBOL_GRP_PATTERN + \
	           	r"\] \[" + \
	           	CURRENCY_SYMBOL_GRP_PATTERN + \
	           	r"\])"

pattern2 = r"(\[" + \
	           CURRENCY_SYMBOL_GRP_PATTERN + \
	           	r" " + \
	           	DD_MM_DATE_GRP_PATTERN + \
	           	r" " + \
	           	HH_MM_TIME_GRP_PATTERN + \
	           	r" )"
	           	
#print(pattern)
#print(upperInputStr)
match = re.match(pattern, upperInputStr)

if match:
    for g in match.groups():
        print(g)

