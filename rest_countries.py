import requests
from openpyxl import Workbook
from tqdm import tqdm
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# URL API
URL = "https://restcountries.com/v3.1/all"

# Запрос к API
try:
    logging.info("Запрос к API...")
    response = requests.get(URL)
    response.raise_for_status()
    countries = response.json()
    logging.info(f"Успешно получено {len(countries)} стран.")
except requests.RequestException as e:
    logging.error(f"Ошибка при запросе: {e}")
    exit(1)

# Создание Excel-файла
wb = Workbook()
ws = wb.active
ws.title = "Страны мира"

# Заголовки
headers = [
    "Название (англ.)", "Офиц. название", "Регион", "Подрегион",
    "Население", "Площадь (км²)", "Столица",
    "Валюта", "Языки", "Флаг (emoji)", "Геолокация (lat, lng)"
]
ws.append(headers)

# Обработка данных
for country in tqdm(countries, desc="Обработка стран"):
    name_common = country.get("name", {}).get("common", "—")
    name_official = country.get("name", {}).get("official", "—")
    region = country.get("region", "—")
    subregion = country.get("subregion", "—")
    population = country.get("population", 0)
    area = country.get("area", 0)
    capital = country.get("capital", ["—"])[0]
    flag = country.get("flag", "—")

    # Валюты (ключи)
    currencies = country.get("currencies", {})
    currency_list = ', '.join(currencies.keys()) if currencies else "—"

    # Языки (значения)
    languages = country.get("languages", {})
    languages_list = ', '.join(languages.values()) if languages else "—"

    # Геолокация
    latlng = country.get("latlng", ["—", "—"])
    geolocation = f"{latlng[0]}, {latlng[1]}" if len(latlng) == 2 else "—"

    ws.append([
        name_common, name_official, region, subregion,
        population, area, capital,
        currency_list, languages_list, flag, geolocation
    ])

# Сохранение
output_filename = "countries_data.xlsx"
wb.save(output_filename)
logging.info(f"Файл успешно сохранён как '{output_filename}'")
