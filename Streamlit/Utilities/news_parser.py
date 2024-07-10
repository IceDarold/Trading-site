import asyncio
import csv
from datetime import date, timedelta
from bs4 import BeautifulSoup
import aiohttp
import dateparser

def daterange(start_date, end_date):
    delta = timedelta(days=1)
    while start_date <= end_date:
        yield start_date
        start_date += delta
        
async def fetch(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            return await response.text()
        else:
            return None

async def get_data(session, date):
    url = f"https://lenta.ru/{date.strftime('%Y/%m/%d')}/page/"
    url += "{}"
    count = 1
    data = {}
    while True:
        print(f"Making request for {url.format(count)}")
        page_content = await fetch(session, url.format(count))
        if page_content and len(page_content) > 32000:
            data[count] = page_content
            print(f"Success {date.strftime('%Y/%m/%d')} {count} {len(page_content)}")
            count += 1
        else:
            print(f"Failed {url.format(count)}")
            break
    return data

async def get_all_articles_links(pages, date):
    tasks = []
    for page in pages.values():
        soup = BeautifulSoup(page, 'html.parser')
        news = soup.find_all('li', class_="archive-page__item _news")
        for n in news:
            date_time = n.find('a').div.time.text
            formatted_date = dateparser.parse(date_time, languages=['ru']).strftime('%Y-%m-%d %H:%M:%S')
            title = n.find('a').h3.text
            link = n.find('a')['href']
            tasks.append((formatted_date, title, link))
    return tasks

async def main(start_date, end_date, filename):
    async with aiohttp.ClientSession() as session:
        for current_date in daterange(start_date, end_date):
            day_pages = await get_data(session, current_date)
            articles = await get_all_articles_links(day_pages, current_date)
    
    # Запись в CSV файл
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(tasks)
    
    # Открываем файл в режиме чтения и читаем его содержимое
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Добавляем новую строку в начало содержимого
    new_content = text + '\n' + content
    
    # Открываем файл в режиме записи и записываем обновленное содержимое
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(new_content)

async def run(start_date, end_date, filename):
    await main(start_date, end_date, filename)

def parse(start_date, end_date, filename):
    asyncio.run(run(start_date, end_date, filename))