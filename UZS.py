import requests
from bs4 import BeautifulSoup
import json
import telebot
import time

def get_rate_paysend():
  response = requests.get('https://paysend.com/').text
  soup = BeautifulSoup(response, 'lxml')
  return float(soup.find("span", {"class": "foo"}).text.split(" ")[3])

def get_rate_binance(payment="Tinkoff", asset="USDT", fiat="RUB", tradeType="BUY", transferZize=1000):
  
  url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
  payload = json.dumps({
    "asset": asset,
    "fiat": fiat,
    "page": 1,
    "payTypes": [
      payment
    ],
    "publisherType": None,
    "rows": 20,
    "tradeType": tradeType
  })
  headers = {
    'authority': 'p2p.binance.com',
    'accept': '*/*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'bnc-uuid': 'a22ac882-02be-4fb3-aa5a-d24210b5d682',
    'c2ctype': 'c2c_merchant',
    'cache-control': 'no-cache',
    'clienttype': 'web',
    'content-type': 'application/json',
    'csrftoken': 'd41d8cd98f00b204e9800998ecf8427e',
    'dnt': '1',
    'fvideo-id': '3189895820caa9138d2949178ec2fd434114c4ff',
    'lang': 'ru',
    'origin': 'https://p2p.binance.com',
    'pragma': 'no-cache',
    'referer': 'https://p2p.binance.com/ru/trade/Tinkoff/USDT?fiat=RUB',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
    'x-trace-id': 'a0fec9f1-44a9-44a3-95f6-5ea864fdf7b0',
    'x-ui-request-trace': 'a0fec9f1-44a9-44a3-95f6-5ea864fdf7b0'
  }

  response = json.loads(requests.request("POST", url, headers=headers, data=payload).text)
  for x in response["data"]:
    if (transferZize >= float(x["adv"]["minSingleTransAmount"]) and transferZize <= float(x["adv"]["maxSingleTransAmount"])):
      return float(x["adv"]["price"])

def get_spread(transferZize=20000):
  rate_paysend = get_rate_paysend()
  SOM = (transferZize - 50)*get_rate_paysend()
  rate_paysend_binance_buy = get_rate_binance("Paysend", "USDT", "UZS", "BUY", SOM)
  rate_paysend_binance_sell = get_rate_binance("RosBank", "USDT", "RUB", "SELL", transferZize)
  if( rate_paysend_binance_sell != None and rate_paysend_binance_buy != None):
    USDT = SOM/rate_paysend_binance_buy
    RUB = USDT * rate_paysend_binance_sell
    SPRED = ((RUB/transferZize)-1.0)*100
    return f"{round(SPRED,3)} %"
  else:
    return "'Ошибка, нельзя купить/продать столько монет'"

def spread(message, value):
  print(f"{message.from_user.first_name} {message.from_user.username} {message.from_user.last_name} {value}")
  print(message.chat.id)
  try:
    num = value
    res = f"Спред для {num} рублей = {get_spread(num)}"
    bot.send_message(message.chat.id, res, parse_mode="html")
  except ValueError:
    res = "Ошибка ввода, смотрите /help"
    bot.send_message(message.chat.id, res, parse_mode="html")

bot = telebot.TeleBot("5398003951:AAGeIzIfaaGf6wv02Os90nBYcFfzXAQBEmI")
@bot.message_handler(commands=['start'])
def start(message):
  bot.send_message(message.chat.id, "Это бот для спреда\n /help - как работать с ботом", parse_mode="html")

@bot.message_handler(commands=['ping'])
def help(message):
  text = "Бот работает"
  bot.send_message(message.chat.id, text, parse_mode="html")

@bot.message_handler(commands=['help'])
def help(message):
  text = ""
  text += "/ping - проверить работает ли бот\n"
  text += "/info - узнать информацию\n"
  text += "/help - как работать с ботом\n"
  text += "/spred_10k - получить спред для 10 000 рублей\n"
  text += "/spred_20k - получить спред для 20 000 рублей\n"
  text += "/spred_30k - получить спред для 30 000 рублей\n"
  text += "/spred_40k - получить спред для 40 000 рублей\n"
  text += "/spred_50k - получить спред для 50 000 рублей\n"
  text += "/spred_60k - получить спред для 60 000 рублей\n"
  text += "/spred_70k - получить спред для 70 000 рублей\n"
  bot.send_message(message.chat.id, text, parse_mode="html")

@bot.message_handler(commands=['spred_10k'])
def spread_10k(message):
  spread(message, 10000)
@bot.message_handler(commands=['spred_20k'])
def spred_20k(message):
  spread(message, 20000)
@bot.message_handler(commands=['spred_30k'])
def spred_30k(message):
  spread(message, 30000)
@bot.message_handler(commands=['spred_40k'])
def spred_40k(message):
  spread(message, 40000)
@bot.message_handler(commands=['spred_50k'])
def spred_50k(message):
  spread(message, 50000)
@bot.message_handler(commands=['spred_60k'])
def spred_60k(message):
  spread(message, 60000)
@bot.message_handler(commands=['spred_70k'])
def spred_70k(message):
  spread(message, 70000)

@bot.message_handler(commands=['info'])
def info(message):
  text = ""
  text += "Версия 0.2\n"
  text += "Старайтесь проверять, работает ли бот, не всегда бывает возможность его запускать"
  bot.send_message(message.chat.id, text, parse_mode="html")

bot.polling(none_stop=True)
#-625724396
