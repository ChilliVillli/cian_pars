import os
import re
import sqlite3 as sq
import cianparser
from bs4 import BeautifulSoup
import requests
import asyncio
from dotenv import load_dotenv
from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher, types
from fake_useragent import UserAgent



load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()
ua = UserAgent()
headers = {'User-agent': ua.random}


# moscow_parser = cianparser.CianParser(location="Москва и область")
# data = moscow_parser.get_newobjects()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    # global cur, base

    await bot.send_message(message.from_user.id, 'Здравствуйте, {0.first_name}!'.format(message.from_user))

    base = sq.connect('base.db')
    cur = base.cursor()
    base.execute('CREATE TABLE IF NOT EXISTS base(name TEXT)')

    btn_chat = types.InlineKeyboardButton(text='Напишите нашему эксперту в чат', url='https://t.me/EES_chat')
    markup = types.InlineKeyboardMarkup(inline_keyboard=[[btn_chat]])

    page = 0

    while True:
        count = 0
        page += 1

    # for i in data:

        # url_cian = i['url']
        # url_cian = i
        # session = requests.Session()
        # session.headers.update(headers)
        # r = session.get(url_cian)
        # soup = BeautifulSoup(r.text, 'lxml')
        # url_rooms = soup.find('div', class_='_7a3fb80146--count--Ug9Tp').find('a').get("href")
        # res_rooms = session.get(url_rooms)
        # script_rooms = BeautifulSoup(res_rooms.text, 'html.parser')
        # script = script_rooms.find_all('script')
        # match = re.split(r'\W+', script[10].text)
        # res_rooms = session.get(f"https://www.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&minprice=18000000&newobject%5B0%5D={match[42]}&offer_type=flat&p={3}")

        session = requests.Session()
        session.headers.update(headers)
        res_rooms = session.get(f"https://www.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&minprice=18000000&object_type%5B0%5D=2&offer_type=flat&p={page}&region=-1&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1")
        soup_rooms = BeautifulSoup(res_rooms.text, 'lxml')
        card = soup_rooms.find_all('article', class_='_93444fe79c--container--Povoi _93444fe79c--cont--OzgVc')
        await asyncio.sleep(5)

        for j in card:

            if page == 54:
                page = 0

            count += 1

            try:

                name = j.find('div', class_='_93444fe79c--row--kEHOK').find('a', class_='_93444fe79c--link--VtWj6').find('span', class_='').text
                url_card = j.find('div', class_='_93444fe79c--row--kEHOK').find('a', class_='_93444fe79c--link--VtWj6').get("href")

                info = cur.execute('SELECT * FROM base WHERE name=?', (url_card,)).fetchone()

                if info is None:

                    cur.execute('INSERT INTO base (name) VALUES (?)', (url_card,))
                    base.commit()

                    deadline_rc = j.find_all('div', class_='_93444fe79c--container--aWzpE')
                    rc = deadline_rc[0].find('a', class_='_93444fe79c--jk--dIktL').text #цена за кв метр
                    time_to_metro = j.find('div', class_='_93444fe79c--remoteness--q8IXp').text
                    address_all = j.find_all('a', class_='_93444fe79c--link--NQlVc')
                    subway = address_all[3].text
                    street = address_all[4].text
                    num_haus = address_all[5].text
                    card_room = session.get(url_card)
                    soup_room = BeautifulSoup(card_room.text, 'lxml')
                    await asyncio.sleep(3)
                    img = soup_room.find_all('li', class_='a10a3f92e9--container--Havpv')
                    img_1 = img[0].find('img', class_='a10a3f92e9--container--KIwW4 a10a3f92e9--container--contain--cYP76').get("src")
                    conditions = soup_room.find_all('div', class_='a10a3f92e9--item--n_zVq')
                    condit = conditions[-1].find_all('span', class_='a10a3f92e9--color_black_100--Ephi7 a10a3f92e9--lineHeight_5u--e6Sug a10a3f92e9--fontWeight_normal--JEG_c a10a3f92e9--fontSize_14px--reQMB a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY a10a3f92e9--text_letterSpacing__0--cQxU5 a10a3f92e9--text_whiteSpace__nowrap--hJYYl')
                    price = soup_room.find('div', class_='a10a3f92e9--amount--ON6i1').text
                    square_meter = condit[1].text
                    deal = f"Условия сделки: {condit[3].text}"
                    characteristics = soup_room.find_all('div', class_='a10a3f92e9--item--Jp5Qv')
                    square = re.sub(r'([А-Я ])', r' \1', characteristics[0].find('div', class_='a10a3f92e9--text--eplgM').text)
                    floor = re.sub(r'([А-Я ])', r' \1', characteristics[1].find('div', class_='a10a3f92e9--text--eplgM').text)
                    deadline = re.sub(r'([А-Я ])', r' \1', characteristics[2].find('div', class_='a10a3f92e9--text--eplgM').text)
                    finishing = re.sub(r'([А-Я ])', r' \1', characteristics[3].find('div', class_='a10a3f92e9--text--eplgM').text)
                    description = soup_room.find('div', class_='a10a3f92e9--layout--BaqYw').text
                    des = '🌟 Понравилась квартира? Готовы к покупке?' \
                          '\nНапишите нашему эксперту в чат, и мы оперативно организуем показ объекта. ' \
                          '\nВаш новый дом ждет вас! 🏡💼'
                    await asyncio.sleep(5) # 2006923323
                    await bot.send_message(message.from_user.id, f"[🌇]({img_1}){name},{street}, {num_haus}"
                                                                 f"{subway} 🚶‍♂{time_to_metro} {finishing}" 
                                                                 f"\n💰{price} {deadline} {square}"
                                                                 f"\n{floor} {rc} {square_meter} {deal}"
                                                                 f"\n{description}"
                                                                 f"\n{des}", parse_mode="Markdown", reply_markup=markup)


                if len(info) > 0:
                    continue


            except Exception:
                continue

            if count == len(card):
                break


async def main():
    await dp.start_polling(bot)

asyncio.run(main())