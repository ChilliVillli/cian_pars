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

data = ['https://zhk-poklonnaya-9-i.cian.ru/', 'https://zhk-rezidencii-skolkovo-odintsovo-i.cian.ru/']



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
        name = soup.find('h1', class_='_7a3fb80146--color_white_100--d9peM _7a3fb80146--lineHeight_46px--MDC6G _7a3fb80146--fontWeight_bold--BbhnX _7a3fb80146--fontSize_38px--_LK5X _7a3fb80146--display_block--KYb25 _7a3fb80146--text--e4SBY _7a3fb80146--text_letterSpacing__normal--tfToq').text
        address = soup.find('span', class_='_7a3fb80146--color_black_100--Ephi7 _7a3fb80146--lineHeight_36px--K6dvk _7a3fb80146--fontWeight_bold--BbhnX _7a3fb80146--fontSize_28px--P1gR4 _7a3fb80146--display_block--KYb25 _7a3fb80146--text--e4SBY _7a3fb80146--text_letterSpacing__normal--tfToq').text
        subway = soup.find('span', class_='_7a3fb80146--color_black_100--Ephi7 _7a3fb80146--lineHeight_20px--fX7_V _7a3fb80146--fontWeight_normal--JEG_c _7a3fb80146--fontSize_14px--reQMB _7a3fb80146--display_inline--ySCqY _7a3fb80146--text--e4SBY _7a3fb80146--text_letterSpacing__normal--tfToq').text
        time_to_metro = soup.find('div', class_='_7a3fb80146--underground-distance--ecEdF').find('span').text
        price = soup.find('span', class_='_7a3fb80146--color_white_100--d9peM _7a3fb80146--lineHeight_22px--FdvaW _7a3fb80146--fontWeight_normal--JEG_c _7a3fb80146--fontSize_16px--QNYmt _7a3fb80146--display_inline--ySCqY _7a3fb80146--text--e4SBY _7a3fb80146--text_letterSpacing__normal--tfToq').text
        img = soup.find_all('img', class_='_7a3fb80146--image--XmJ9Z')
        img_1 = img[1].get('src')
        img_2 = img[2].get('src')
        img_3 = img[3].get('src')
        description = soup.find('div', class_='_7a3fb80146--text--SnsX_').text
        characteristics = soup.find_all('div', class_='_7a3fb80146--value--wcB9F')
        deadline = f"Срок сдачи: {characteristics[0].text}"
        class_hause = f"Класс: {characteristics[1].text}"
        floor = f"Этажность: {characteristics[2].text}"
        frame = f"Корпусов: {characteristics[3].text}"
        house_type = f"Тип дома: {characteristics[4].text}"
        ceiling = f"Высота потолков: {characteristics[5].text}"
        finishing = f"Варианты отделки: {characteristics[6].text}"
        parking = f"Парковка: {characteristics[7].text}"
        # media = types.MediaGroup()
        # media.attach_photo(img_1)
        # media.attach_photo(img_2)
        # media.attach_photo(img_3)
        await asyncio.sleep(5)
        # await bot.send_media_group(message.from_user.id, media=media)
        await bot.send_message(message.from_user.id, f"[.]({img_2}){name},{address}🚇{subway}🚶‍♂{time_to_metro}"
                                                     f"\n💰{price}{deadline}{class_hause}"
                                                     f"\n{floor}{frame}{house_type}"
                                                     f"\n{ceiling}{finishing}{parking}{description}", parse_mode="Markdown")


async def main():
    await dp.start_polling(bot)

asyncio.run(main())

