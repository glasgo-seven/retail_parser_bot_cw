from bs4 import BeautifulSoup
import requests as req
import sys
from time import time, strftime, localtime

from bot_alert import *

def parse_LMD_get_card_info(card):
	link	= f"https://www.lamoda.ru{card.find('a')['href']}"
	img_src	= card.find('img')['src'][2:]
	try:
		price	= card.find('span', {'class':'x-product-card-description__price-single'}).text
	except:
		priceA	= card.find('span', {'class':'x-product-card-description__price-old'}).text
		priceB	= card.find('span', {'class':'x-product-card-description__price-new'}).text
		price = f'~{priceA}~ | {priceB}'
	titleA	= card.find('div', {'class':'x-product-card-description__brand-name'}).text
	titleB	= card.find('div', {'class':'x-product-card-description__product-name'}).text
	return {
		'title'		:	f'{titleA}\n{titleB}',
		'img_src'	:	img_src,
		'price'		:	price,
		'link'		:	link
	}

def parse_LMD(message, msg_data):
	# try:
		resp = req.get(f"https://www.lamoda.ru/catalogsearch/result/?q={'%20'.join(msg_data)}")
		soup = BeautifulSoup(resp.text, 'lxml')

		item_card = soup.find_all('div', {'class':'x-product-card__card'})

		item_data = {}
		for i in range(5 if len(item_card) >= 5 else len(item_card)):
			item_data[i] = parse_LMD_get_card_info(item_card[i])
		return analyse(item_data)

	# except:
	# 	error(f"[ ERROR ] in PARSE_LMD of USER-{message.from_user.id} : {sys.exc_info()[0]}.")
	# 	return None

def analyse(item_data):
	min_price = -1
	min_item = ''
	pop_item = ''
	for key in item_data:
		price = float(''.join(item_data[key]['price'].split('|')[-1][:-2].strip().split()))
		if min_price == -1:
			pop_item = key
			min_price = price
			min_item = key
		elif price < min_price:
				min_price = price
				min_item = key

	item_data[min_item]['caption'] = 'Самый дешёвый товар из популярных:'
	item_data[pop_item]['caption'] = 'Самый популярный товар:'
	return {
		'cheap'		:	item_data[min_item],
		'popular'	:	item_data[pop_item]
	}
