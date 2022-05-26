#!/usr/bin/env python
# coding: utf-8

import codecs
from gc import callbacks
import os
from random import randint
from time import time, sleep
import sys

import telebot
from telebot import types

import bot_parser
import bot_database

def get_token():
	try:
		return open('.token', 'r').read()
	except FileNotFoundError:
		return os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(get_token())

def bot_send_msg(message, _msg):
	msg_id = f'{message.chat.id} - {message.chat.title if message.chat.title != None else "PM"} - {message.from_user.username}'
	bot.send_message(message.chat.id, text=_msg)
	print(f'[{msg_id}] bot-self: "{_msg}."')

def bot_got_msg(message):
	msg_id = f'{message.chat.id} - {message.chat.title if message.chat.title != None else "PM"} - {message.from_user.username}'
	print(f'[{msg_id}] {message.from_user.username}: "{message.text}."')

@bot.message_handler(commands=['start'])
def start_command(message: types.Message):
	bot_send_msg(message, 'Приветствую!\nДождитесь регистраци в системе...')
	bot_database.userDB_reg(message)
	bot_send_msg(message, 'Готово! Вы можете пользоваться ботом!\nДля этого напишите\n"/search {что искать}".')

@bot.message_handler(commands=['search'])
def search_command(message: types.Message):
# msg_id = f'{message.chat.id} - {message.chat.title if message.chat.title != None else "PM"} - {message.from_user.username}'
	bot_got_msg(message)
	bot_database.userDB_update(message)

	msg_data = message.text.split()[1:]
	print(msg_data)

	retail_data = bot_parser.parse_LMD(message, msg_data)
	
	if not retail_data:
		bot_send_msg(message, 'По Вышему запросу ничего не найдено...')
	else:
		# results = analysis(retail_data)

		bot_send_msg(message, 'Найдено на LAMODA:')
		for key in retail_data:
			data = retail_data[key]
			print(data)
			button_price = types.InlineKeyboardButton(
				text=data['price'],
				url=data['link'])
			print(data['link'].split('/')[4])
			callback = f"{data['link'].split('/')[-3]},{data['title']},{''.join(data['price'].split('|')[-1][:-2].strip().split())}"
			button_subscribe = types.InlineKeyboardButton(
				text='Отслеживание',
				callback_data=callback)
			keyboard = types.InlineKeyboardMarkup(row_width=1)
			keyboard.add(button_price)
			keyboard.add(button_subscribe)

			bot_send_msg(message, data['caption'])
			bot.send_photo(message.chat.id, data['img_src'], caption=data['title'], reply_markup=keyboard, parse_mode= 'Markdown')
		# add_item_to_db()

		# follow_item()

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call: types.CallbackQuery):
	alert_data = bot_database.itemDB_add(call.message, call.data)
	if len(alert_data) == 3:
		ex_data, new_data = alert_data
		for id in ex_data['lookout']:
			button_price = types.InlineKeyboardButton(
				text=new_data['price'],
				url=new_data['link'])
			callback = f"{new_data['link'].split('/')[-3]},{new_data['title']},{''.join(new_data['price'].split('|')[-1][:-2].strip().split())}"
			button_subscribe = types.InlineKeyboardButton(
				text='Отслеживание',
				callback_data=callback)
			keyboard = types.InlineKeyboardMarkup(row_width=1)
			keyboard.add(button_price)
			keyboard.add(button_subscribe)
			bot.send_photo(
				id,
				new_data['img_src'],
				caption=f"ОБНОВЛЕНИЕ!\n{new_data['title']}\n{new_data['price']}",
				reply_markup=keyboard, parse_mode= 'Markdown')
	if alert_data[0] == 1:
		bot_send_msg(call.message, 'Товар отслеживается!')
	elif alert_data[0] == -1:
		bot_send_msg(call.message, 'Товар больше не отслеживается!')

print('------------------------\n/// BOT IS POLLING ///\n\nChat log:\n')
bot.polling()
