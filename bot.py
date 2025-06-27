import sqlite3 as sq
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from aiogram.types import Message
import asyncio
from datetime import datetime
from aiogram import types, loggers
from aiogram.filters import CommandStart
from aiogram import Router
import requests
from lxml import etree
from urllib.request import urlopen


router = Router()


@router.message(CommandStart())
async def main(message: Message, bot):

    await message.answer('Здравствуйте, {0.first_name}!'.format(message.from_user))

    btn_chat = types.InlineKeyboardButton(text='Напишите нашему эксперту в чат', url='https://t.me/EES_chat')
    markup = types.InlineKeyboardMarkup(inline_keyboard=[[btn_chat]])
    offer = '🌟 Понравилась квартира? Готовы к покупке?' \
            '\nНапишите нашему эксперту в чат, и мы оперативно организуем показ объекта. ' \
            '\nВаш новый дом ждет вас! 🏡💼'

    base = sq.connect('base.db')
    cur = base.cursor()
    base.execute('CREATE TABLE IF NOT EXISTS base(name TEXT)')

    page = 0

    while True:

        ua = UserAgent()
        headers = {'User-agent': ua.random}
        count = 0
        page += 1

        session = requests.Session()
        session.headers.update(headers)

        res_rooms = session.get(f"https://www.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&minprice=25000000&"
                               f"object_type%5B0%5D=2&offer_type=flat&p={page}&region=-1&room1=1&room2=1&room3=1&room4=1&"
                               f"room5=1&room6=1&room7=1&room9=1", headers=headers)

        await asyncio.sleep(3)

        soup_rooms = BeautifulSoup(res_rooms.text, 'lxml')
        card = soup_rooms.find_all('article', class_='_93444fe79c--container--Povoi _93444fe79c--cont--OzgVc')

        await asyncio.sleep(3)

        for j in card:

            cur_datetime = datetime.now()
            hour = cur_datetime.hour

            if 2 <= hour <= 5:
                await asyncio.sleep(14400)

            if page == 54:
                page = 0
                base.execute("DELETE FROM base")
                base.commit()
                break

            count += 1

            try:

                price = j.find('span', class_="_93444fe79c--color_text-primary-default--vSRPB _93444fe79c--lineHeight_28px--KFXmc _93444fe79c--fontWeight_bold--BbhnX _93444fe79c--fontSize_22px--sFuaL _93444fe79c--display_block--KYb25 _93444fe79c--text--b2YS3 _93444fe79c--text_letterSpacing__normal--yhcXb").text
                name = j.find('div', class_='_93444fe79c--row--kEHOK').find('a', class_='_93444fe79c--link--VtWj6').\
                    find('span', class_='').text
                url_card = j.find('div', class_='_93444fe79c--row--kEHOK').find('a', class_='_93444fe79c--link--VtWj6').\
                    get("href")

                info = cur.execute('SELECT * FROM base WHERE name=?', (url_card,)).fetchone()

                if info is None:

                    cur.execute('INSERT INTO base (name) VALUES (?)', (url_card,))
                    base.commit()

                count_base = cur.execute('SELECT COUNT (*) FROM base').fetchone()[0]

                address_all = j.find_all('a', class_='_93444fe79c--link--NQlVc')
                street = address_all[4].text
                card_room = requests.get(url_card, headers=headers)
                soup_room = BeautifulSoup(card_room.text, 'lxml')

                soup_room_xpath = urlopen(url_card)
                html_code = soup_room_xpath.read().decode('utf-8')
                tree = etree.HTML(html_code)

                await asyncio.sleep(3)

                rc = soup_room.find('div', class_='a10a3f92e9--container--mTzLi').\
                    find('a', class_='a10a3f92e9--link--A5SdC').text.replace('ЖК', '')
                rc_go = ''.join(filter(str.isalnum, rc))

                try:

                    img = soup_room.find_all('li', class_='a10a3f92e9--container--Havpv')
                    img_1 = img[0].find('img', class_='a10a3f92e9--container--KIwW4 a10a3f92e9--container--contain--cYP76').get("src")

                except AttributeError:

                    img_1 = img[1].find('img', class_='a10a3f92e9--container--KIwW4 a10a3f92e9--container--contain--cYP76').get("src")

                square_meter = tree.xpath('//*[@id="frontend-offer-card"]/div/div/div[2]/div[3]/div/div[1]/div[3]/div/div/div[1]/span[2]')[0].text
                deal = tree.xpath('//*[@id="frontend-offer-card"]/div/div/div[2]/div[3]/div/div[1]/div[3]/div/div/div[2]/span[2]')[0].text
                subway = soup_room.find('a', class_='a10a3f92e9--underground_link--VnUVj').text.replace(' ', '')
                description = soup_room.find('div', class_='a10a3f92e9--layout--BaqYw').text
                characteristics = soup_room.find_all('div', class_='a10a3f92e9--item--Jp5Qv')

                dict_addition = {
                    'Общая площадь': None,
                    'Жилая площадь': None,
                    'Площадь кухни': None,
                    'Этаж': None,
                    'Год сдачи': None,
                    'Дом': None,
                    'Отделка': None,
                }

                for addition in range(len(characteristics)):

                    variable = characteristics[addition].find('span', class_='a10a3f92e9--color_gray60_100--r_axa a10a3f92e9--lineHeight_4u--E1SPG a10a3f92e9--fontWeight_normal--JEG_c a10a3f92e9--fontSize_12px--pY5Xn a10a3f92e9--display_block--KYb25 a10a3f92e9--text--b2YS3 a10a3f92e9--text_letterSpacing__0--CNLlz').text

                    if variable in dict_addition:
                        dict_addition[variable] = characteristics[addition].find('span', class_='a10a3f92e9--color_text-primary-default--vSRPB a10a3f92e9--lineHeight_6u--cedXD a10a3f92e9--fontWeight_bold--BbhnX a10a3f92e9--fontSize_16px--QNYmt a10a3f92e9--display_block--KYb25 a10a3f92e9--text--b2YS3').text

                    if variable not in dict_addition:
                        continue

                for k, v in dict_addition.items():

                    if v is None:
                        dict_addition[k] = '-'
                    else:
                        continue

                await bot.send_message(-1002006923323, f"[🌇]({img_1}){name} {street}"
                                                       f"\n#ЖК{rc_go}"
                                                       f"\nⓂ️ #{subway}"
                                                       f"\n💰{price} Цена за кв.м² {square_meter}"
                                                       f"\nГод сдачи: {dict_addition['Год сдачи']}"
                                                       f"\nОбщая площадь: {dict_addition['Общая площадь']}"
                                                       f"\nЖилая площадь: {dict_addition['Жилая площадь']}"
                                                       f"\nПлощадь кухни: {dict_addition['Площадь кухни']}"
                                                       f"\nЭтаж: {dict_addition['Этаж']}"
                                                       f"\nДом: {dict_addition['Дом']}"
                                                       f"\nОтделка: {dict_addition['Отделка']}"
                                                       f"\nУсловия сделки: {deal}"
                                                       f"\n{description}"
                                                       f"\n{offer}", parse_mode="Markdown", reply_markup=markup)
                await asyncio.sleep(900)

                if count_base > 0:
                    continue

                if count == len(card):
                    break

            except Exception as e:
                failed = True
                loggers.dispatcher.error("Failed to fetch updates - %s: %s", type(e).__name__, e)
                await asyncio.sleep(5)