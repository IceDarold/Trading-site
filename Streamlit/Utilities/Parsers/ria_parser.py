import asyncio
import csv
from datetime import date, timedelta, datetime, time
from bs4 import BeautifulSoup
import aiohttp
import dateparser
import pandas as pd

def daterange(start_date, end_date, revert=False):
    if not revert:
      delta = timedelta(days=1)
      while start_date <= end_date:
          yield start_date
          start_date += delta
    else:
      delta = timedelta(days=1)
      while start_date <= end_date:
          yield end_date
          end_date -= delta
        
async def fetch(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                return None
    except TimeoutError:
        print("Timeout error. Wait for 10 seconds...")
        await asyncio.sleep(10)
        return await fetch(session, url)
    except aiohttp.client_exceptions.ClientConnectorError:
        print("ClientConnectorError. Wait for 10 seconds...")
        await asyncio.sleep(10)
        return await fetch(session, url)
    except aiohttp.client_exceptions.ClientOSError:
        print("ClientOSError")
        await asyncio.sleep(10)
        return await fetch(session, url)

async def get_data(session, date):
    url = f"https://ria.ru/services/lenta/more.html?date={date.strftime('%Y%m%d')}T"
    url += "{}"
    news_l = []
    current_time = time(23, 59, 59)
    formatted_time = current_time.strftime("%H%M%S")
    is_yesterday = False
    while True:
        link = url.format(formatted_time)
        print(f"Making request for {link}")
        page_content = await fetch(session, link)
        if page_content:
            soup = BeautifulSoup(page_content, 'html.parser')
            news = soup.find_all('div', class_="list-item")
            for n in news:
                title = n.find('div', class_="list-item__content").find('a', class_="list-item__title color-font-hover-only").text
                article_url = n.find('div', class_="list-item__content").find('a', class_="list-item__title color-font-hover-only")['href']
                a_time = n.find('div', class_="list-item__info").find('div', class_="list-item__date").text
                try:
                    is_yesterday = int(a_time[0]) != date.day
                except ValueError:
                    print("ValueError")
                    is_yesterday = a_time.split(",") == 2
                if is_yesterday:
                    break
                splitted = a_time.replace(" ", "").split(',')
                date_time = datetime.combine(date, datetime.strptime(splitted[1] if len(splitted) == 2 else splitted[0], "%H:%M").time())
                formatted_date = date_time.strftime('%Y-%m-%d %H:%M:%S')
                news_l.append(",".join([formatted_date, title, article_url]) + "\n")
            print(f"Success {date.strftime('%Y/%m/%d')} {len(news)} {len(page_content)}")
        else:
            print(f"Failed {url.format(link)}")
            continue
        if is_yesterday:
           break
        else:
            formatted_time = date_time.strftime("%H%M%S")

    return news_l
    

async def main(start_date, end_date, file_path):
    async with aiohttp.ClientSession() as session:
        for current_date in daterange(start_date, end_date, True):
            articles = await get_data(session, current_date)
            with open(file_path, mode='a', newline='', encoding='utf-8') as file:
                print("Saving to file")
                file.writelines(articles)

def parse(start_date, end_date, file_path):
    asyncio.run(main(start_date, end_date, file_path))
    with open(file_path, "r", encoding='utf-8') as f:
        print("Checking everything")
        df = f.readlines()
    article_l = []
    for line in df[1:]:
        comma_index = line.find(',', line.find(',')+1)
        ria = line[line.find(','):comma_index]
        slash_index = line.find('https://')
        title = line[comma_index + 1:slash_index-1]
        url = line[slash_index:]
        article_l.append([ria.strip(), title.strip(), url.strip()])
    df = pd.DataFrame(article_l, columns=["datetime", "title", "url"])
    df = df.drop_duplicates()
    df["datetime"] = pd.to_datetime(df["datetime"])
    df.sort_values(by="datetime", inplace=True)
    df.to_csv(file_path, index=False)
parse(datetime.now() - timedelta(1), datetime.now(), "Data/News/ria.csv")