# CryptoPricer
RT and historical cryptocurrencies price requester.

![](screenshots/CryptoPricerWebp.net-gifmaker.gif)

## What does it do ?
CryptoPricer runs on your smartphone (Android, and, later, IPhone). It accepts user requests
and returns either real time or historical cryptocurrency rates. The prices are obtained not
directly from the exchanges, but from the [cryptocompare.com](http://cryptocompare.com) site which collects in 
real time price and volume information from more than 90 exchanges.

## Usage examples
### Requesting RT BTC/USD on Bitfinex
#### Full request: btc usd 0 bitfinex
![](screenshots/Screenshot_2018-02-16-21-33-53.jpg)

Comment: 
* 0 means real time
* the request is displayed in the status bar
* R after the price means real time

### Requesting historical price ETH/USD on Binance
#### Full request: eth usd 12/2/18 12:43 bitfinex
![](screenshots/Screenshot_2018-02-16-21-36-07.jpg)

Comment: 
* M after the price means historical Minute price. On cryptocompare, historical prices are available at a minute resolution for the last 7 days. Older prices are day prices (followed by D).

### Changing only the date of the previous request
#### Partial request: -d13/2
![](screenshots/Screenshot_2018-02-16-21-37-13.jpg)

Comment: 
* -d is the partial request command for setting only the date
* -t --> time
* -c --> cryptocurrency
* -f --> fiat currency
* -e --> exchange
* the status bar shows the modified full request

### Changing the crypto, the fiat and the exchange of the previous request
#### Partial request: -cxmr -feth -eall
![](screenshots/Screenshot_2018-02-16-21-40-04.jpg)

Comment: 
* all means average of all exchanges (CCCAGG)

### Using the -v value command to obtain the counterparty value at the obtained price of the value command quantity of the crypto/fiat
#### Partial request: -vs100xmr to obtain the counterparty value of 100xmr at the returned RT or historical price
![](screenshots/Screenshot_2018-02-16-21-40-41.jpg)

Comment: 
* the s flag of -vS means the -vs command will be saved in the command history