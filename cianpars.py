import os
import re
import sqlite3 as sq
from bs4 import BeautifulSoup
import requests
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, executor
from fake_useragent import UserAgent
from datetime import datetime
from aiogram.contrib.fsm_storage.memory import MemoryStorage



load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())
ua = UserAgent()
# headers = {'User-agent': ua.random}
headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

proxies = {
    'https': 'http://47.56.110.204:8989'
}

# response = requests.get(url='https://2ip.ru', headers=headers, proxies=proxies)
# soup_response = BeautifulSoup(response.text, 'lxml')
# ip = soup_response.find('div', class_='ip').text.strip()
# print(ip)



@dp.message_handler(commands=['start'])
async def main(message: types.Message):




    await bot.send_message(message.from_user.id, 'Здравствуйте, {0.first_name}!'.format(message.from_user))

    btn_chat = types.InlineKeyboardButton(text='Напишите нашему эксперту в чат', url='https://t.me/EES_chat')
    markup = types.InlineKeyboardMarkup(inline_keyboard=[[btn_chat]])

    base = sq.connect('base.db')
    cur = base.cursor()
    base.execute('CREATE TABLE IF NOT EXISTS base(name TEXT)')

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
        session.proxies.update(proxies)
        # res_rooms = session.get(f"https://www.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&minprice=18000000&object_type%5B0%5D=2&offer_type=flat&p={page}&region=-1&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1")
        res_rooms = session.get('https://www.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&minprice=18000000&object_type%5B0%5D=2&offer_type=flat&p=1&region=-1&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1')
        print(res_rooms)
        soup_rooms = BeautifulSoup(res_rooms.text, 'lxml')
        # print(soup_rooms)
        card = soup_rooms.find_all('article', class_='_93444fe79c--container--Povoi _93444fe79c--cont--OzgVc')
        await asyncio.sleep(5)

        for j in card:

            # cur_datetime = datetime.now()
            # hour = cur_datetime.hour
            #
            # if 2 <= hour <= 5:
            #     await asyncio.sleep(14400)


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
                    rc = deadline_rc[0].find('a', class_='_93444fe79c--jk--dIktL').text.replace('ЖК', '') #ЖК «»
                    rc_go = ''.join(filter(str.isalnum, rc))
                    # time_to_metro = j.find('div', class_='_93444fe79c--remoteness--q8IXp').text
                    address_all = j.find_all('a', class_='_93444fe79c--link--NQlVc')
                    street = address_all[4].text
                    # num_haus = address_all[5].text
                    card_room = session.get(url_card)
                    soup_room = BeautifulSoup(card_room.text, 'lxml')
                    await asyncio.sleep(3)
                    img = soup_room.find_all('li', class_='a10a3f92e9--container--Havpv')
                    img_1 = img[0].find('img', class_='a10a3f92e9--container--KIwW4 a10a3f92e9--container--contain--cYP76').get("src")
                    conditions = soup_room.find_all('div', class_='a10a3f92e9--item--n_zVq')
                    condit = conditions[-1].find_all('span', class_='a10a3f92e9--color_black_100--Ephi7 a10a3f92e9--lineHeight_5u--e6Sug a10a3f92e9--fontWeight_normal--JEG_c a10a3f92e9--fontSize_14px--reQMB a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY a10a3f92e9--text_letterSpacing__0--cQxU5 a10a3f92e9--text_whiteSpace__nowrap--hJYYl')
                    price = soup_room.find('div', class_='a10a3f92e9--amount--ON6i1').text
                    subway = soup_room.find('a', class_='a10a3f92e9--underground_link--VnUVj').text
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
                    await asyncio.sleep(5) # 15 мин -1002006923323
                    await bot.send_message(message.from_user.id, f"[🌇]({img_1}){name} {street}"
                                                                 f"\n#ЖК{rc_go}"
                                                                 f"\nⓂ️ #{subway}"
                                                                 f"\n💰{price} {deadline} {square}"
                                                                 f"\n{floor} {square_meter}"
                                                                 f"\n{deal} {finishing}"
                                                                 f"\n{description}"
                                                                 f"\n{des}", parse_mode="Markdown", reply_markup=markup)

                if len(info) > 0:
                    continue

                if count == len(card):
                    break

            except Exception:
                continue



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)