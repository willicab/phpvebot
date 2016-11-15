# This example show how to write an inline mode telegramt bot use pyTelegramBotAPI.
import telebot
import time
import sys
import logging
from telebot import types
import requests
import re

API_TOKEN = '188169419:AAHFReEesPRkm40-coiKRlrG4uGmbKZdH9M'
PHP_URL = 'https://secure.php.net/manual-lookup.php?pattern='

bot = telebot.TeleBot(API_TOKEN)
#telebot.logger.setLevel(logging.DEBUG)



@bot.inline_handler(lambda query: True)
def query_text(inline_query):
    try:
        i = 0
        result = []
        print ('searching ' + inline_query.query)
        r = requests.get(PHP_URL + inline_query.query)
        salida = r.text.split("\n")
        if "PHP: Manual Quick Reference" in salida[7] :
            inicio = salida.index('<ul id="quickref_functions">') + 1
            fin = salida.index('<!-- result list end -->') - 1
            for x in range(inicio, fin):
                re_list = re.compile(r'<li><a href="(.*)">(.*)</a></li>')
                f_list = re_list.findall(salida[x])
                func = f_list[0][1].replace("<b>", "").replace("</b>", "")
                url = 'https://php.net' + f_list[0][0]
                result.append(types.InlineQueryResultArticle(str(i), func, types.InputTextMessageContent(func + " " + url)))
                i = i + 1
        else:
            for x in range(0, len(salida)):
                if '<base href' in salida[x]:
                    linea = x
            re_list = re.compile(r'<base href="(.*)">')
            f_list = re_list.findall(salida[linea])
            url = f_list[0]
            func = inline_query.query
            result.append(types.InlineQueryResultArticle('1', func, types.InputTextMessageContent(func + " " + url)))
        print (': Found ' + str(len(result)) + ' results')
        bot.answer_inline_query(inline_query.id, result)
    except Exception as e:
        print(e)

def main_loop():
    bot.polling(True)
    while 1:
        time.sleep(1)


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print >> sys.stderr, '\nExiting by user request.\n'
sys.exit(0)
