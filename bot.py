import re
import sqlite3 as sq
import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from aiogram.types import Message
import requests
import asyncio
from datetime import datetime
from aiogram import types
from loader import scheduler
from aiogram.filters import CommandStart
from aiogram import Router


router = Router()


@router.message(CommandStart())
async def main(message: Message, bot):

    await message.answer('Здравствуйте, {0.first_name}!'.format(message.from_user))

    btn_chat = types.InlineKeyboardButton(text='Напишите нашему эксперту в чат', url='https://t.me/EES_chat')
    markup = types.InlineKeyboardMarkup(inline_keyboard=[[btn_chat]])

    base = sq.connect('base.db')
    cur = base.cursor()
    base.execute('CREATE TABLE IF NOT EXISTS base(name TEXT)')

    page = 0

    while True:

        ua = UserAgent()
        headers = {'User-agent': ua.random}
        count = 0
        page += 1

        await asyncio.sleep(5)

        session = requests.Session()
        session.headers.update(headers)
        res_rooms = session.get(f"https://www.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&minprice=25000000&object_type%5B0%5D=2&offer_type=flat&p={page}&region=-1&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1")
        soup_rooms = BeautifulSoup(res_rooms.text, 'lxml')
        card = soup_rooms.find_all('article', class_='_93444fe79c--container--Povoi _93444fe79c--cont--OzgVc')
        price = soup_rooms.find('span', class_='_93444fe79c--color_black_100--Ephi7 _93444fe79c--lineHeight_28px--KFXmc _93444fe79c--fontWeight_bold--BbhnX _93444fe79c--fontSize_22px--sFuaL _93444fe79c--display_block--KYb25 _93444fe79c--text--e4SBY _93444fe79c--text_letterSpacing__normal--tfToq').text
        await asyncio.sleep(3)

        for j in card:

            cur_datetime = datetime.now()
            hour = cur_datetime.hour

            if 2 <= hour <= 5:
                await asyncio.sleep(14400)

            if page == 54:
                page = 0

            count += 1

            try:

                name = j.find('div', class_='_93444fe79c--row--kEHOK').find('a', class_='_93444fe79c--link--VtWj6').\
                    find('span', class_='').text
                url_card = j.find('div', class_='_93444fe79c--row--kEHOK').find('a', class_='_93444fe79c--link--VtWj6').\
                    get("href")

                info = cur.execute('SELECT * FROM base WHERE name=?', (url_card,)).fetchone()

                if info is None:

                    cur.execute('INSERT INTO base (name) VALUES (?)', (url_card,))
                    base.commit()

                deadline_rc = j.find_all('div', class_='_93444fe79c--container--aWzpE')
                rc = deadline_rc[0].find('a', class_='_93444fe79c--jk--dIktL').text.replace('ЖК', '')
                deadline = deadline_rc[1].find('span', class_='_93444fe79c--color_gray60_100--mYFjS _93444fe79c--lineHeight_20px--fX7_V _93444fe79c--fontWeight_normal--JEG_c _93444fe79c--fontSize_14px--reQMB _93444fe79c--display_inline--ySCqY _93444fe79c--text--e4SBY _93444fe79c--text_letterSpacing__normal--tfToq').text
                rc_go = ''.join(filter(str.isalnum, rc))
                address_all = j.find_all('a', class_='_93444fe79c--link--NQlVc')
                street = address_all[4].text
                card_room = session.get(url_card)
                soup_room = BeautifulSoup(card_room.text, 'lxml')

                # await asyncio.sleep(3)

                img = soup_room.find_all('li', class_='a10a3f92e9--container--Havpv')
                img_1 = img[0].find('img', class_='a10a3f92e9--container--KIwW4 a10a3f92e9--container--contain--cYP76').get("src")
                conditions = soup_room.find_all('div', class_='a10a3f92e9--item--n_zVq')
                condit = conditions[-1].find_all('span', class_='a10a3f92e9--color_black_100--Ephi7 a10a3f92e9--lineHeight_5u--e6Sug a10a3f92e9--fontWeight_normal--JEG_c a10a3f92e9--fontSize_14px--reQMB a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY a10a3f92e9--text_letterSpacing__0--cQxU5 a10a3f92e9--text_whiteSpace__nowrap--hJYYl')
                subway = soup_room.find('a', class_='a10a3f92e9--underground_link--VnUVj').text.replace(' ', '')
                square_meter = condit[1].text
                deal = f"Условия сделки: {condit[3].text}"
                description = soup_room.find('div', class_='a10a3f92e9--layout--BaqYw').text
                des = '🌟 Понравилась квартира? Готовы к покупке?' \
                      '\nНапишите нашему эксперту в чат, и мы оперативно организуем показ объекта. ' \
                      '\nВаш новый дом ждет вас! 🏡💼'
                characteristics = soup_room.find_all('div', class_='a10a3f92e9--item--Jp5Qv')
                square = re.sub(r'([А-Я ])', r' \1', characteristics[0].find('div', class_='a10a3f92e9--text--eplgM').text)
                floor = re.sub(r'([А-Я ])', r' \1', characteristics[1].find('div', class_='a10a3f92e9--text--eplgM').text)
                # deadline = re.sub(r'([А-Я ])', r' \1', characteristics[2].find('div', class_='a10a3f92e9--text--eplgM').text)
                finishing = re.sub(r'([А-Я ])', r' \1', characteristics[3].find('div', class_='a10a3f92e9--text--eplgM').text)

                # description = soup_room.find('div', class_='a10a3f92e9--layout--BaqYw').text
                # des = '🌟 Понравилась квартира? Готовы к покупке?' \
                #       '\nНапишите нашему эксперту в чат, и мы оперативно организуем показ объекта. ' \
                #       '\nВаш новый дом ждет вас! 🏡💼'

                # return img_1, name, street, rc_go, subway, price, deadline, square,\
                #        floor, square_meter, deal, finishing, description, des

                # await bot.send_message(-1001420035930, f"[🌇]({img_1}){name} {street}"
                #                                        f"\n#ЖК{rc_go}"
                #                                        f"\nⓂ️ #{subway.replace(' ', '')}"
                #                                        f"\n💰{price} {deadline} {square}"
                #                                        f"\n{floor}\nЦена за кв. м {square_meter}"
                #                                        f"\n{deal} {finishing}"
                #                                        f"\n{description}"
                #                                        f"\n{des}", parse_mode="Markdown", reply_markup=markup)#-1002006923323
                # await asyncio.sleep(900)

                if len(info) > 0:
                    continue

                if count == len(card):
                    break

            except Exception:
                await publication(bot, img_1, name, street, rc_go, subway, price, deadline, square, floor, square_meter,
                                  deal, finishing, description, des)
                continue


async def publication(bot, img_1=None, name=None, street=None, rc_go=None, subway=None, price=None, deadline=None,
                      square=None, floor=None, square_meter=None, deal=None, finishing=None, description=None, des=None):

    btn_chat = types.InlineKeyboardButton(text='Напишите нашему эксперту в чат', url='https://t.me/EES_chat')
    markup = types.InlineKeyboardMarkup(inline_keyboard=[[btn_chat]])

    await bot.send_message(-1001420035930, f"[🌇]({img_1}){name} {street}"
                                           f"\n#ЖК{rc_go}"
                                           f"\nⓂ️ #{subway}"
                                           f"\n💰{price} {deadline} {square}"
                                           f"\n{floor}\nЦена за кв. м {square_meter}"
                                           f"\n{deal} {finishing}"
                                           f"\n{description}"
                                           f"\n{des}", parse_mode="Markdown", reply_markup=markup)