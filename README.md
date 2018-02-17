# CryptoPricer
RT and historical crypto currencies price requester.

![](screenshots/CryptoPricerWebp.net-gifmaker.gif)

## What does it do ?
CryptoPricer runs on your smartphone (Android, and, later, IPhone). It accepts user requests
and returns either real time or historical crypto currency rates. The prices are obtained not
directly from the exchanges, but from the [cryptocompare.com](http://cryptocompare.com) site which collects in 
real time price and volume information from more than 90 exchanges.

## Usage examples
### Requesting RT BTC/USD on Bitfinex
btc usd 0 bitfinex
![](screenshots/Screenshot_2018-02-16-21-33-53.jpg)

Comment: 
* 0 means real time
* the request is displayed in the status bar
* R after the price means real time

### Requesting historical price ETH/USD on Binance
eth usd 12/2/18 12:43 bitfinex
![](screenshots/Screenshot_2018-02-16-21-36-07.jpg)

Comment: 
* M after the price means historical minute price. On cryptocompare, historical prices are available at a minute resolution for the last 7 days. Older prices are day prices

