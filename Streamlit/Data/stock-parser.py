import requests
import json
import pandas as pd
import aiohttp, asyncio

async def get_data(session, url, func_data):
    async with session.get(url, headers={
            "User-Agent": "Googlebot"
        }) as response:
        if not func_data['is_ok']:
            print("Ok")
            return
        print(f"Request to {url}")
        response_text = await response.text()
        data = json.loads(response_text)
        func_data['columns'] = data[func_data['what']]['columns']
        if len(response_text) < 500:
            print("len < 500")
            func_data['is_ok'] = False
            return
        func_data['list'].extend(data[func_data['what']]['data'])
        func_data['total_str'] += len(data[func_data['what']]['data'])


async def parse(func_information, ticker, maximum, step):
    url = "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{}/candles.json?start=".format(ticker)
    url += "{}"
    func_information["list"] = []
    func_information["total_str"] = 0
    func_information["is_ok"] = True
    func_information["what"] = "candles"
    print("Connecting to server")
    async with aiohttp.ClientSession() as session:
        tasks = [get_data(session, url.format(index), func_information) for index in range(1, maximum, step)]
        return await asyncio.gather(*tasks)

def get_ticker(ticker, filename, volume):
    func_info = {}
    asyncio.run(parse(func_info, ticker, volume, 500))
    df = pd.DataFrame(func_info["list"], columns=func_info['columns'])
    df["Date"] = pd.to_datetime(df["begin"])
    df = df.drop(["end", "begin"], axis=1)
    df.columns = df.columns.str.title()
    df.sort_values(by='Date', inplace=True)
    df.to_csv(filename, index=False)

get_ticker("GAZP", "GAZP.csv", 200000)
