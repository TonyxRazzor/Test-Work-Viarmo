import os
import json
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Загрузка ключа API из файла credentials.json
credentials = Credentials.from_authorized_user_file('credentials.json')

# Подключение к Google Sheets API
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

# ID таблицы Google, с которой будем работать
spreadsheet_id = 'your_spreadsheet_id'

# Чтение данных из столбца A таблицы
result = sheet.values().get(spreadsheetId=spreadsheet_id, range='A:A').execute()
values = result.get('values', [])

# Обработка каждой ссылки на товар
for row in values:
    url = row[0]
    
    # Переход по ссылке и получение HTML-кода страницы товара
    response = requests.get(url)
    html = response.text
    
    # Парсинг HTML-кода для извлечения характеристик товара
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('h1').text
    price = soup.find('span', {'class': 'price'}).text
    
    # Вставка характеристик товара в таблицу Google
    update_data = {
        'values': [[title, price]],
        'range': 'B' + str(row),
        'majorDimension': 'ROWS'
    }
    sheet.values().update(spreadsheetId=spreadsheet_id, range='Sheet1!B' + str(row), body=update_data, valueInputOption='RAW').execute()
