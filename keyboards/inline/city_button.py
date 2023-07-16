import json
import requests
from requests import Timeout
from loguru import logger

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, List, Message
from config_data.config import RAPID_API_KEY, RAPID_API_HOST
from loader import bot


url = "https://hotels4.p.rapidapi.com/locations/v3/search"
headers = {
	"X-RapidAPI-Key": RAPID_API_KEY,
	"X-RapidAPI-Host": RAPID_API_HOST
}


def city_founding(city: str) -> List:

	"""
	Выполняет поиск города по его названию.

	:param city: Название города для поиска.
	:type city: Str
	:return: Список словарей с информацией о найденных городах.
	:rtype: List
	"""

	try:
		response = requests.get(url, headers=headers,
								params={'q': city, 'locale': 'en_EN',
								"langid": "1033", "siteid": "300000001"}, timeout=10)

		if response.status_code == requests.codes.ok:
			data = json.loads(response.text)
			cities = list()
			for i_data in data["sr"]:
				if i_data["type"] == "CITY":
					cities.append(dict(id=i_data["gaiaId"], region_name=i_data["regionNames"]["fullName"]))

				return cities

		else:
			print("Ошибка при выполнении запроса:", response.status_code)

	except Timeout:
		logger.info("Превышено время ожидания запроса")


def city_markup(text: str, message: Message) -> InlineKeyboardMarkup:

	"""
	Создает встроенную клавиатуру с найденными городами.
	Проверяет, есть ли в списке значения.
	В случае, если список пуст, просит ввести другой город.

	:param text: Название города для поиска.
	:type text: Str
	:param message: Объект сообщения от пользователя.
	:type message: Message
	:return: Встроенная клавиатура с найденными городами.
	:rtype: InlineKeyboardMarkup
	"""

	cities_list = city_founding(text)
	destinations = InlineKeyboardMarkup()

	if len(cities_list) == 0:
		bot.send_message(message.chat.id, "Совпадения не найдены. Попробуйте ввести другой город")
		raise SystemExit

	else:
		for city in cities_list:
			destinations.add(InlineKeyboardButton(text=city["region_name"], callback_data=city['id']))
		return destinations
