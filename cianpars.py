import time
import re
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


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Здравствуйте, {0.first_name}!'.format(message.from_user))
    await asyncio.sleep(5)

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
        # card = soup_rooms.find_all('div', class_='_93444fe79c--card--ibP42 _93444fe79c--wide--gEKNN')
        card = soup_rooms.find_all('article', class_='_93444fe79c--container--Povoi _93444fe79c--cont--OzgVc')

        for j in card:
            name = j.find('div', class_='_93444fe79c--row--kEHOK').find('a', class_='_93444fe79c--link--VtWj6').find('span', class_='').text
            url_card = j.find('div', class_='_93444fe79c--row--kEHOK').find('a', class_='_93444fe79c--link--VtWj6').get("href")
            print(url_card)
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
            square = re.sub(r'([А-Я])', r' \1', characteristics[0].find('div', class_='a10a3f92e9--text--eplgM').text)
            floor = re.sub(r'([А-Я])', r' \1', characteristics[1].find('div', class_='a10a3f92e9--text--eplgM').text)
            deadline = re.sub(r'([А-Я])', r' \1', characteristics[2].find('div', class_='a10a3f92e9--text--eplgM').text)
            finishing = re.sub(r'([А-Я])', r' \1', characteristics[3].find('div', class_='a10a3f92e9--text--eplgM').text)
            description = soup_room.find('div', class_='a10a3f92e9--layout--BaqYw').text

            await asyncio.sleep(5)
            await bot.send_message(message.from_user.id, f"[🌇]({img_1}){name},{street}{num_haus}{subway}🚶‍♂{time_to_metro}"
                                                         f"\n💰{price}{deadline}{finishing}{square}"
                                                         f"\n{floor}{rc}{square_meter}{deal}"
                                                         f"\n{description}", parse_mode="Markdown")


async def main():
    await dp.start_polling(bot)

asyncio.run(main())

