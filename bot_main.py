#!/usr/bin/env python
# coding: utf-8

import codecs
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
	bot_send_msg(message, 'Приветствую, ждите регистраци...')
	bot_database.reg_user_in_db(message)
	bot_send_msg(message, 'Можно пользоваться!')

@bot.message_handler(commands=['search'])
def search_command(message: types.Message):
# msg_id = f'{message.chat.id} - {message.chat.title if message.chat.title != None else "PM"} - {message.from_user.username}'
	bot_got_msg(message)
	bot_database.userDB_update(message)

	msg_data = message.text.split()[1:]
	print(msg_data)

	retail_data = (	bot_parser.parse_WB(message, msg_data),
					bot_parser.parse_LMD(message, msg_data))
	print(retail_data)
	# results = analysis(retail_data)

	# show_results(results)
	# add_item_to_db()

	# follow_item()

print('------------------------\n/// BOT IS POLLING ///\n\nChat log:\n')
bot.polling()
