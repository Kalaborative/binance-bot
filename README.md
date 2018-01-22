# binance-bot
Very simple binance trading Bot using Binance REST API

# Welcome to Binance Bot!
***Disclaimer:*** This bot will not guarantee you profits. By using this bot, you agree that you assume full responsibility and full liability for all transactions. It has been designed so that you will not have to deal with any API limits. Please don't go crazy.

**Trading Concept:** Input the Symbol you want to trade on (for example, "TRXBTC"). The bot will then take half of your available cryptocurrency and make a limit order according to the last minute's close. Once confirmed, it will try to sell the same amount on a 1.1% profit (this can be changed within the program). It will keep running until this is successful, or you can manually stop it.  After the transactions are complete, it will calculate your percentage gain using the formula:

[![enter image description here][1]][1]


  [1]: https://i.imgur.com/JjgXkZY.png

## To Download:
Make sure you have the `binance`package installed via pip. Then clone this repo and run `binance_bot.py`.
Any contributions are welcome, as this is purely experimental. Cheers!
