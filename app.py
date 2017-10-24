# encoding: utf-8
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, ImageMessage, TextSendMessage, ImageSendMessage,
)
import requests
from bs4 import BeautifulSoup
import random
from get_news import get_news, get_news_help

app = Flask(__name__)

line_bot_api = LineBotApi('VBKhs6GIOaS7r+hCPWVGwEf2JlJBXhE6l0zsSZVvuUGeUq9lJAuAjr8nRZes4GTCyd8B385JqocMh1KZPQTCwAsTEhpJHmFERELVuOuKLK1beIr3+J1IqYGDjRoZk6T49V9fZdvfwiTFnqYC9WPK7QdB04t89/1O/w1cDnyilFU=') #Your Channel Access Token
handler = WebhookHandler('76b1b5851c558b2da21d45822fa2f6de') #Your Channel Secret

def get_beauty_url():
  which_page = str(int(random.random() * 1000) + 1298)

  res = requests.get('https://www.ptt.cc/bbs/Beauty/index' + which_page +'.html')
  soup = BeautifulSoup(res.text, "html.parser")
  url_beauty = []
  for link in soup.find_all('a'):
      if 'M' in link.get('href'):
        url_beauty.append('https://www.ptt.cc'+link.get('href'))

  target = url_beauty[int(random.random() * len(url_beauty))]
  res2 = requests.get(target)
  soup2 = BeautifulSoup(res2.text, "html.parser")
  img_beauty = []
  for link in soup2.find_all('a'):
    if '.jpg' in link.get('href') and 'https' not in link.get('href'):
      href = link.get('href')[:4] + 's' + link.get('href')[4:]
      img_beauty.append(href)
    elif 'http://imgur' in link.get('href'):
      href = link.get('href')[:4] + 's' + link.get('href')[4:] + '.jpg'
      img_beauty.append(href)
    elif '.jpg' in link.get('href') and 'https' in link.get('href'):
      href = link.get('href')
      img_beauty.append(href)
    elif 'https://imgur' in link.get('href'):
      href = link.get('href') + '.jpg'
      img_beauty.append(href)
  index = int(random.random() * len(img_beauty))
  repeat_count = 0
  while len(img_beauty) == 0:
      repeat_count += 1
      target = url_beauty[int(random.random() * len(url_beauty))]
      res2 = requests.get(target)
      soup2 = BeautifulSoup(res2.text, "html.parser")
      img_beauty = []
      for link in soup2.find_all('a'):
        if '.jpg' in link.get('href') and 'https' not in link.get('href'):
          href = link.get('href')[:4] + 's' + link.get('href')[4:]
          img_beauty.append(href)
        elif 'http://imgur' in link.get('href'):
          href = link.get('href')[:4] + 's' + link.get('href')[4:] + '.jpg'
          img_beauty.append(href)
        elif '.jpg' in link.get('href') and 'https' in link.get('href'):
          href = link.get('href')
          img_beauty.append(href)
        elif 'https://imgur' in link.get('href'):
          href = link.get('href') + '.jpg'
          img_beauty.append(href)
      index = int(random.random() * len(img_beauty))
      if len(img_beauty) != 0:
        target2 = img_beauty[index]
        return target2
      elif repeat_count == len(url_beauty):
        return 'https://i.ytimg.com/vi/WHkglDUZtTc/maxresdefault.jpg'
  else:
    target2 = img_beauty[index]
    return target2

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text #message from user
    if 'google:' in text or 'Google' in text:
      query = 'https://www.google.com.tw/search?q=' + text[7:] + '&tbm=isch&sa=X&rls=com.microsoft:zh-TW:%7Breferrer:source%3F%7D&rlz=1I7AMSA_zh-TWTW471&dcr=0&biw=1280&bih=586&gbv=1&sei=DebtWbjZLMux0AStnLP4Dw'
      res = requests.get(query)
      soup = BeautifulSoup(res.text, "html.parser")
      tag = '.images_table'
      for drink in soup.select('{}'.format(tag)):
          img_src = drink.img['src']
      if '雲林縣虎尾許大哥' in text:
        img_src = 'https://1.share.photo.xuite.net/bicyclecoffee/11d25ec/16795417/905242579_m.jpg'
      line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(original_content_url= img_src,
                          preview_image_url= img_src))
    elif '抽' in text:
      img_src = get_beauty_url()
      line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(original_content_url= img_src,
                          preview_image_url= img_src))
    elif text == '想看新聞' or text == '我想看新聞':
      news_url = get_news_help()
    elif text == '看旅遊新聞':
      news_url = get_news('travel')
    elif text == '看體育新聞':
      news_url = get_news('sports')
    elif text == '看星光新聞':
      news_url = get_news('star')
    elif text == '看時尚新聞':
      news_url = get_news('fashion')
    elif text == '看健康新聞':
      news_url = get_news('health')
    elif text == '看播吧新聞':
      news_url = get_news('boba')
    elif text == '看車雲新聞':
      news_url = get_news('speed')
    elif text == '看房產新聞':
      news_url = get_news('house')
    elif text == '看寵物新聞':
      news_url = get_news('pets')
    elif text == '看遊戲新聞':
      news_url = get_news('game')
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = news_url))

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(original_content_url='https://scontent-mxp1-1.cdninstagram.com/t51.2885-15/e35/14063449_1266706823340241_978293483_n.jpg',
                          preview_image_url='https://scontent-mxp1-1.cdninstagram.com/t51.2885-15/e35/14063449_1266706823340241_978293483_n.jpg')) #reply the same message from user


import os
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['PORT'])