api_secret = 'ENTER-YOUR-SECRET-KEY-HERE'
api_key = 'ENTER-YOUR-API-HERE'

# Program supports BNB, BTC, and ETH markets only. No USDT.
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
from time import sleep
from sys import exit

def decimal_formatter(number):
	return format(number, '.8f')

def find_quantity(total, price):
	quantity = float(total) / float(price)
	return quantity

def calculate_price_target(initial, percentage=1.1):
	target = (percentage * float(initial) / 100 ) + float(initial) + 0.00000001
	return decimal_formatter(target)

def calculate_profit_percentage(initial, final):
	percent = (float(final) - float(initial)) / float(initial) * 100
	return format(percent, '.2f')

def order_confirm(symbol):
	confirm = False
	seconds = 0
	while not confirm:
		orders = client.get_open_orders(symbol=symbol)
		sleep(1)
		seconds += 1
		if not orders:
			confirm = True
		if seconds == 120:
			print("It's been over 2 minutes since you have placed this order. Cancel? Y/N")
			cancel = input("> ")
			if cancel.lower() == "y":
				orderId = orders[0]['orderId']
				client.cancel_order(symbol=symbol, orderId=orderId)
				confirm = True
			else:
				print("Order not cancelling. Selling...")
		if seconds == 300:
			print("It's been over 5 minutes since you have placed the order. ")
			print("If you stop here, your order will be sold at market value.")
			cancel2 = input('Stop? Y/N > ')
			if cancel2.lower() == "y":
				orderId = orders[0]['orderId']
				client.cancel_order(symbol=symbol, orderId=orderId)
				quant = input("enter quantity: ")
				if "." in quant:
					quantity = float(quant)
				else:
					quantity = int(quant)
				client.order_market_sell(symbol=symbol, quantity=quantity)
				confirm = True
			else:
				print("Not cancelling. The program will run until the order is confirmed.")
	print("Order is confirmed!")


client = Client(api_key, api_secret)

print("Welcome! type 'STOP' to stop")

while True:
	print("Enter a symbol.")
	sym = input('> ')

	if sym.lower() == "stop":
		exit()

	coin = sym[:-3]
	asset = sym[-3:]

	klines = client.get_historical_klines(sym, Client.KLINE_INTERVAL_1MINUTE, "1 min ago")
	most_recent = klines.pop()
	last_closing = most_recent[4]
	print("Last close price for {} was {}".format(sym, last_closing))

	balance = client.get_asset_balance(asset=asset)
	bitcoins = float(balance['free'])
	half_bitcoins = format(bitcoins / 2.0, '.8f')

	profit = calculate_price_target(last_closing)
	print("Your profit target is", profit)

	number_of_coins = find_quantity(half_bitcoins, last_closing)
	print("Your order will be for {} with {} {}".format(last_closing, number_of_coins, coin))

	try:
		print('Buying...')
		try:
			print("Buy method 1, three decimal places")
			client.order_limit_buy(symbol=sym, quantity=float(format(number_of_coins, '.3f')), price=last_closing)
		except:
			try:
				print("Method 1 failed.")
				print("Buy method 2, rounded coins")
				client.order_limit_buy(symbol=sym, quantity=round(number_of_coins), price=last_closing)
			except BinanceAPIException:
				try:
					print("Method 2 failed.")
					print("Buy method 3, rounded coins but minus one")
					client.order_limit_buy(symbol=sym, quantity=round(number_of_coins - 1), price=last_closing)
				except:
					print("Method 3 failed.")
					print("Buy method 4, 2 decimal places")
					client.order_limit_buy(symbol=sym, quantity=float(format(number_of_coins, '.2f')), price=last_closing)
		sleep(1)
		print("Order placed. Confirming...")
		order_confirm(sym)
		print("Selling... Might take a while...")
		try:
			print("Sell method float quantity 1")
			client.order_limit_sell(symbol=sym, quantity=float(format(number_of_coins, '.3f')), price=str(profit))
		except BinanceAPIException as e:
			print("Method 1 failed.")
			print("Sell method round quantity 2")
			if "LOT_SIZE" in e.message:
				try:
					client.order_limit_sell(symbol=sym, quantity=round(number_of_coins), price=str(profit))
				except BinanceAPIException as e:
					print("Method 2 failed.")
					print(e.message)
					print("Sell method round minus one quantity 3")
					try:
						client.order_limit_sell(symbol=sym, quantity=round(number_of_coins - 1), price=str(profit))
					except BinanceAPIException as e:
						print(e.message)
						print("Method 3 failed.")
						print("Sell method float quantity 4")
						client.order_limit_sell(symbol=sym, quantity=float(format(number_of_coins, '.2f')), price=str(profit))
			elif "PRICE_FILTER" in e.message:
				try:
					print("Method 2 failed.")
					print("Sell method 7 decimal places profit 3")
					profit = format(float(profit), '.7f')
					client.order_limit_sell(symbol=sym, quantity=float(format(number_of_coins, '.3f')), price=str(profit))
				except:
					try:
						print("Method 3 failed.")
						print("Sell method 6 decimal places profit 4")
						profit = format(float(profit), '.6f')
						client.order_limit_sell(symbol=sym, quantity=float(format(number_of_coins, '.3f')), price=str(profit))
					except BinanceAPIException:
						print("Method 4 failed.")
						print("Sell method float quantity 6 decimal places 5")
						profit = format(float(profit), '.6f')
						client.order_limit_sell(symbol=sym, quantity=float(format(number_of_coins, '.2f')), price=str(profit))
		print("Order placed. Confirming...")
		sleep(1)
		order_confirm(sym)
		percentage = calculate_profit_percentage(last_closing, profit)
		print("Congrats! You made a profit of {}%.".format(percentage))
	except BinanceAPIException as e:
		print(e.status_code)
		print(e.message)
