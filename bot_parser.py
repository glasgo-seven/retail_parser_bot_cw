from bs4 import BeautifulSoup
import requests as req
import sys
from time import time, strftime, localtime

from bot_alert import *

def parse_WB (message, msg_data):
	pass

def get_card_info(card):
	link	= card.find('a')['href']
	img_src	= card.find('img')['src'][2:]
	price	= card.find('span', {'class':'x-product-card-description__price-single'})
	titleA	= card.find('div', {'class':'x-product-card-description__brand-name'})
	titleB	= card.find('div', {'class':'x-product-card-description__product-name'})
	return {
		'title'		:	f'{titleA} {titleB}',
		'img_src'	:	img_src,
		'price'		:	price,
		'link'		:	link
	}

def parse_LMD(message, msg_data):
	try:
		resp = req.get(f"https://www.lamoda.ru/catalogsearch/result/?q={'%20'.join(msg_data)}")
		soup = BeautifulSoup(resp.text, 'lxml')

		item_card = soup.find_all('div', {'class':'x-product-card__card'})

		return {
			'LMD_0'	:	get_card_info(item_card[0]),
			'LMD_1'	:	get_card_info(item_card[1])
		}

	except:
		error(f"[ ERROR ] in PARSE_LMD of USER-{message.from_user.id} : {sys.exc_info()[0]}.")
		return None

def get_weather(message, location):
	try:
		resp = req.get(f"https://weather.com/ru-RU/weather/today/l/{location}")

		soup = BeautifulSoup(resp.text, 'lxml')

		loc = soup.find('div', id='WxuHeaderLargeScreen-header-9944ec87-e4d4-4f18-b23e-ce4a3fd8a3ba').find_all('span')
		lang = loc[0].text
		deg = loc[1].text[-1]

		grind = soup.find('div', id='WxuCurrentConditions-main-b3094163-ef75-4558-8d9a-e35e6b9b1034')
		gspans = grind.find_all('span')
		now_loca = grind.h1.text.split(': ')[1]
		now_temp = gspans[0].text
		now_weat = grind.title.text
		now_rain = gspans[-1].text

		
	except:
		error(f"[ ERROR ] in GET_WEATHER of USER-{message.from_user.id} : {sys.exc_info()[0]}.")
		return None