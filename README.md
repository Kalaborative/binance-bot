# binance-bot
Very simple binance trading Bot using Binance REST API

# Welcome to Binance Bot!
***Disclaimer:*** This bot will not guarantee you profits. By using this bot, you agree that you assume full responsibility and full liability for all transactions. It has been designed so that you will not have to deal with any API limits. Please don't go crazy.

**Trading Concept:** Input the Symbol you want to trade on (for example, "TRXBTC"). The bot will then take half of your available cryptocurrency and make a limit order according to the last minute's close. Once confirmed, it will try to sell the same amount on a 1.1% profit (this can be changed within the program). It will keep running until this is successful, or you can manually stop it.  After the transactions are complete, it will calculate your percentage gain using the formula:

[![enter image description here][1]][1]


  [1]: https://i.imgur.com/JjgXkZY.png


## To Download:
Download [sammchardy's binance package](https://github.com/sammchardy/python-binance).
Make sure you have the `binance` package installed via pip. Then clone this repo, insert your API key and API secret at the top, and run `binance_bot.py`.
Note: If you run into an error having to do with installing Twisted and Microsoft Visual C++ Build Tools, simply download the appropriate wheel file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted) (cp26 for Python 2.6, cp35 for Python 3.5, etc.) then install the wheel (i.e., `pip install Twisted‑17.9.0‑cp34‑cp34m‑win32.whl`)
Any contributions are welcome, as this is purely experimental. Cheers!
