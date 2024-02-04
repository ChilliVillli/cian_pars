import time
import cianparser
from aiogram.types import InputMediaPhoto, InputFile
from bs4 import BeautifulSoup
import requests
import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher, types
from fake_useragent import UserAgent


load_dotenv()
bot = Bot(token='5601906129:AAH1k-asnKub2yCS36TUmjHMUlr9UtcarW4')
dp = Dispatcher()
ua = UserAgent()
headers = {'User-agent': ua.random}


# moscow_parser = cianparser.CianParser(location="Москва и область")
# data = moscow_parser.get_newobjects()

data = ['https://zhk-poklonnaya-9-i.cian.ru/'] #, 'https://zhk-rezidencii-skolkovo-odintsovo-i.cian.ru/']

for i in data:
    # url_cian = i['url']
    url_cian = i
    session = requests.Session()
    session.headers.update(headers)
    r = session.get(url_cian)
    soup = BeautifulSoup(r.text, 'lxml')
    url_rooms = soup.find('div', class_='_7a3fb80146--container--bfJK8').find('a').get("href")
    res_rooms = session.get(url_rooms)
    soup_rooms = BeautifulSoup(res_rooms.text, 'lxml')
    # img = soup_rooms.find_all('ul', class_='_93444fe79c--container--Pf0cj')
    # img_1 = img[1].find('img', class_='_93444fe79c--container--KIwW4').get("src")
    card = soup_rooms.find_all('div', class_='_93444fe79c--container--kZeLu _93444fe79c--link--DqDOy')
    for j in card:
        # name = j.find('div', class_='_93444fe79c--row--kEHOK').find('a', class_='_93444fe79c--link--VtWj6').find('span', class_='').text
        url_card = j.find('div', class_='_93444fe79c--row--kEHOK').find('a', class_='_93444fe79c--link--VtWj6').get("href")
        # deadline_rc = j.find_all('div', class_='_93444fe79c--container--aWzpE')
        # square_meter = deadline_rc[3].find('p', class_='_93444fe79c--color_gray60_100--mYFjS _93444fe79c--lineHeight_20px--fX7_V _93444fe79c--fontWeight_normal--JEG_c _93444fe79c--fontSize_14px--reQMB _93444fe79c--display_block--KYb25 _93444fe79c--text--e4SBY _93444fe79c--text_letterSpacing__normal--tfToq').text
        # rc = deadline_rc[0].find('a', class_='_93444fe79c--jk--dIktL').text #цена за кв метр
        # time_to_metro = j.find('div', class_='_93444fe79c--remoteness--q8IXp').text
        # address_all = j.find_all('a', class_='_93444fe79c--link--NQlVc')
        # subway = address_all[3].text
        # street = address_all[4].text
        # num_haus = address_all[5].text
        # price = deadline_rc[2].find('span', class_='_93444fe79c--color_black_100--Ephi7 _93444fe79c--lineHeight_28px--KFXmc _93444fe79c--fontWeight_bold--BbhnX _93444fe79c--fontSize_22px--sFuaL _93444fe79c--display_block--KYb25 _93444fe79c--text--e4SBY _93444fe79c--text_letterSpacing__normal--tfToq').text
        card_room = session.get(url_card)
        soup_room = BeautifulSoup(card_room.text, 'lxml')
        time.sleep(3)
        # conditions = soup_room.find_all('div', class_='a10a3f92e9--item--n_zVq')
        # condit = conditions[-1].find_all('span', class_='a10a3f92e9--color_black_100--Ephi7 a10a3f92e9--lineHeight_5u--e6Sug a10a3f92e9--fontWeight_normal--JEG_c a10a3f92e9--fontSize_14px--reQMB a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY a10a3f92e9--text_letterSpacing__0--cQxU5 a10a3f92e9--text_whiteSpace__nowrap--hJYYl')
        # deal = f"Условия сделки: {condit[3].text}"
        characteristics = soup_room.find_all('div', class_='a10a3f92e9--item--Jp5Qv')
        # square = f"Общая площадь: {characteristics[0].find('span', class_='a10a3f92e9--color_black_100--Ephi7 a10a3f92e9--lineHeight_6u--cedXD a10a3f92e9--fontWeight_bold--BbhnX a10a3f92e9--fontSize_16px--QNYmt a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY').text}"
        # floor = f"Этаж: {characteristics[1].find('span', class_='a10a3f92e9--color_black_100--Ephi7 a10a3f92e9--lineHeight_6u--cedXD a10a3f92e9--fontWeight_bold--BbhnX a10a3f92e9--fontSize_16px--QNYmt a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY').text}"
        deadline = f"Год сдачи: {characteristics[2].find('span', class_='a10a3f92e9--color_black_100--Ephi7 a10a3f92e9--lineHeight_6u--cedXD a10a3f92e9--fontWeight_bold--BbhnX a10a3f92e9--fontSize_16px--QNYmt a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY').text}"
        print(deadline)
        time.sleep(5)









# @dp.message(CommandStart())
# async def cmd_start(message: types.Message):
#     await bot.send_message(message.from_user.id, 'Здравствуйте, {0.first_name}!'.format(message.from_user))
#     await asyncio.sleep(5)
#     for i in data:
#         # url_cian = i['url']
#         url_cian = i
#         session = requests.Session()
#         session.headers.update(headers)
#         r = session.get(url_cian)
#         soup = BeautifulSoup(r.text, 'lxml')
#         name = soup.find('div', class_='_7a3fb80146--container--bfJK8')
#         # await asyncio.sleep(5)
#         # await bot.send_media_group(message.from_user.id, media=media)
#         # await bot.send_message(message.from_user.id, f"[.]({img_2}){name},{address}🚇{subway}🚶‍♂{time_to_metro}"
#         #                                              f"\n💰{price}{deadline}{class_hause}"
#         #                                              f"\n{floor}{frame}{house_type}"
#         #                                              f"\n{ceiling}{finishing}{parking}{description}", parse_mode="Markdown")
#
#
# async def main():
#     await dp.start_polling(bot)
#
# asyncio.run(main())

