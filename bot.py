import sqlite3 as sq
import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from aiogram.types import Message
import requests
import asyncio
from datetime import datetime
from aiogram import types
from aiogram.filters import CommandStart
from aiogram import Router


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

    async with aiohttp.ClientSession() as session:

        while True:

            ua = UserAgent()
            headers = {'User-agent': ua.random}
            count = 0
            page += 1

            async with session.get(f"https://www.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&minprice=25000000&"
                                   f"object_type%5B0%5D=2&offer_type=flat&p={page}&region=-1&room1=1&room2=1&room3=1&room4=1&"
                                   f"room5=1&room6=1", headers=headers) as res_rooms:

                soup_rooms = BeautifulSoup(await res_rooms.text(), 'lxml')
                card = soup_rooms.find_all('article', class_='_93444fe79c--container--Povoi _93444fe79c--cont--OzgVc')

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

                        price = j.find('span', class_='_93444fe79c--color_black_100--Ephi7 _93444fe79c--lineHeight_28px--KFXmc _93444fe79c--fontWeight_bold--BbhnX _93444fe79c--fontSize_22px--sFuaL _93444fe79c--display_block--KYb25 _93444fe79c--text--e4SBY _93444fe79c--text_letterSpacing__normal--tfToq').text
                        name = j.find('div', class_='_93444fe79c--row--kEHOK').find('a', class_='_93444fe79c--link--VtWj6').\
                            find('span', class_='').text
                        url_card = j.find('div', class_='_93444fe79c--row--kEHOK').find('a', class_='_93444fe79c--link--VtWj6').\
                            get("href")

                        info = cur.execute('SELECT * FROM base WHERE name=?', (url_card,)).fetchone()

                        if info is None:

                            cur.execute('INSERT INTO base (name) VALUES (?)', (url_card,))
                            base.commit()

                        count_base = cur.execute('SELECT COUNT (*) FROM base').fetchone()[0]

                        deadline_rc = j.find_all('div', class_='_93444fe79c--container--aWzpE')
                        rc = deadline_rc[0].find('a', class_='_93444fe79c--jk--dIktL').text.replace('ЖК', '')
                        deadline = deadline_rc[1].find('span', class_='_93444fe79c--color_gray60_100--mYFjS _93444fe79c--lineHeight_20px--fX7_V _93444fe79c--fontWeight_normal--JEG_c _93444fe79c--fontSize_14px--reQMB _93444fe79c--display_inline--ySCqY _93444fe79c--text--e4SBY _93444fe79c--text_letterSpacing__normal--tfToq').text.capitalize()
                        rc_go = ''.join(filter(str.isalnum, rc))
                        address_all = j.find_all('a', class_='_93444fe79c--link--NQlVc')
                        street = address_all[4].text

                        async with session.get(url_card, headers=headers) as card_room:
                            soup_room = BeautifulSoup(await card_room.text(), 'lxml')

                        await asyncio.sleep(2)

                        img = soup_room.find_all('li', class_='a10a3f92e9--container--Havpv')
                        img_1 = img[0].find('img', class_='a10a3f92e9--container--KIwW4 a10a3f92e9--container--contain--cYP76').get("src")
                        conditions = soup_room.find_all('div', class_='a10a3f92e9--item--n_zVq')
                        condit = conditions[-1].find_all('span', class_='a10a3f92e9--color_black_100--Ephi7 a10a3f92e9--lineHeight_5u--e6Sug a10a3f92e9--fontWeight_normal--JEG_c a10a3f92e9--fontSize_14px--reQMB a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY a10a3f92e9--text_letterSpacing__0--cQxU5 a10a3f92e9--text_whiteSpace__nowrap--hJYYl')
                        subway = soup_room.find('a', class_='a10a3f92e9--underground_link--VnUVj').text.replace(' ', '')
                        square_meter = condit[1].text
                        deal = f"Условия сделки: {condit[3].text}"
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

                            variable = characteristics[addition].find('span', class_='a10a3f92e9--color_gray60_100--mYFjS a10a3f92e9--lineHeight_4u--E1SPG a10a3f92e9--fontWeight_normal--JEG_c a10a3f92e9--fontSize_12px--pY5Xn a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY a10a3f92e9--text_letterSpacing__0--cQxU5').text

                            if variable in dict_addition:
                                dict_addition[variable] = characteristics[addition].find('span', class_='a10a3f92e9--color_black_100--Ephi7 a10a3f92e9--lineHeight_6u--cedXD a10a3f92e9--fontWeight_bold--BbhnX a10a3f92e9--fontSize_16px--QNYmt a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY').text

                            if variable not in dict_addition:
                                continue

                        for k, v in dict_addition.items():

                            if v is None:
                                dict_addition[k] = '-'
                            else:
                                continue

                        # square = characteristics[0].find('span', class_='a10a3f92e9--color_black_100--Ephi7 a10a3f92e9--lineHeight_6u--cedXD a10a3f92e9--fontWeight_bold--BbhnX a10a3f92e9--fontSize_16px--QNYmt a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY').text
                        # floor = characteristics[1].find('span', class_='a10a3f92e9--color_black_100--Ephi7 a10a3f92e9--lineHeight_6u--cedXD a10a3f92e9--fontWeight_bold--BbhnX a10a3f92e9--fontSize_16px--QNYmt a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY').text
                        # finishing = characteristics[3].find('span', class_='a10a3f92e9--color_black_100--Ephi7 a10a3f92e9--lineHeight_6u--cedXD a10a3f92e9--fontWeight_bold--BbhnX a10a3f92e9--fontSize_16px--QNYmt a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY').text
                        # square = re.sub(r'([А-Я ])', r' \1', characteristics[0].find('div', class_='a10a3f92e9--text--eplgM').text)
                        # floor = re.sub(r'([А-Я ])', r' \1', characteristics[1].find('div', class_='a10a3f92e9--text--eplgM').text)
                        # deadline = re.sub(r'([А-Я ])', r' \1', characteristics[2].find('div', class_='a10a3f92e9--text--eplgM').text)
                        # finishing = re.sub(r'([А-Я ])', r' \1', characteristics[3].find('div', class_='a10a3f92e9--text--eplgM').text)

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

                        # await publication(bot, img_1, name, street, rc_go, subway, price, deadline, square, floor, square_meter,
                        #                   deal, finishing, description)

                        await bot.send_message(-1002006923323, f"[🌇]({img_1}){name} {street}"
                                                               f"\n#ЖК{rc_go}"
                                                               f"\nⓂ️ #{subway}"
                                                               f"\n💰{price} Цена за кв.м² {square_meter}"
                                                               f"\n{deadline}"
                                                               f"\nОбщая площадь: {dict_addition['Общая площадь']}"
                                                               f"\nЖилая площадь: {dict_addition['Жилая площадь']}"
                                                               f"\nПлощадь кухни: {dict_addition['Площадь кухни']}"
                                                               f"\nЭтаж: {dict_addition['Этаж']} Дом: {dict_addition['Дом']}"
                                                               f"\nОтделка: {dict_addition['Отделка']}"
                                                               f"\n{deal}"
                                                               f"\n{description}"
                                                               f"\n{offer}", parse_mode="Markdown", reply_markup=markup)

                        await asyncio.sleep(900)

                        if count_base > 0:
                            continue

                        if count == len(card):
                            break

                    except Exception:
                        continue


