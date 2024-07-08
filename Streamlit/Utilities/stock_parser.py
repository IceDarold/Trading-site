import requests
import json
import pandas as pd
import aiohttp, asyncio, time

async def get_data(session, url, func_data):
    try:
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
    except TimeoutError:
        print("Timeout error. Wait for 10 seconds...")
        await asyncio.sleep(10)
        return await get_data(session, url, func_data)
    except aiohttp.client_exceptions.ClientConnectorError:
        print("ClientConnectorError. Wait for 10 seconds...")
        await asyncio.sleep(10)
        return await get_data(session, url, func_data)
    except aiohttp.client_exceptions.ClientOSError:
        print("ClientOSError. Wait for 10 seconds...")
        await asyncio.sleep(10)
        return await get_data(session, url, func_data)
    except aiohttp.client_exceptions.ClientPayloadError:
        print("ClientPayloadError. Wait for 10 seconds...")
        await asyncio.sleep(10)
        return await get_data(session, url, func_data)



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

def get_ticker(ticker, filename, volume) -> pd.DataFrame:
    func_info = {}
    asyncio.run(parse(func_info, ticker, volume, 500))
    df = pd.DataFrame(func_info["list"], columns=func_info['columns'])
    df["Date"] = pd.to_datetime(df["begin"])
    df = df.drop(["end", "begin"], axis=1)
    df.columns = df.columns.str.title()
    df.sort_values(by='Date', inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.to_csv(filename, index=False)
    return df

def get_volume(ticker, volume=5000, left_border=0, right_border=10000, kill=False):
    print(f"{ticker}: {left_border}:{volume}:{right_border}")
    if abs(right_border - left_border) <= 500:
        return volume
    url = "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{}/candles.json?start=".format(ticker)
    url += "{}"
    url = url.format(volume)
    try:
        req_len = len(requests.get(url).content)
    except TimeoutError:
        print("Timeout error. Wait for 10 seconds...")
        time.sleep(10)
        return get_volume(ticker, volume, left_border, right_border, kill)
    except aiohttp.client_exceptions.ClientConnectorError:
        print("ClientConnectorError. Wait for 10 seconds...")
        time.sleep(10)
        return get_volume(ticker, volume, left_border, right_border, kill)
    except aiohttp.client_exceptions.ClientOSError:
        print("ClientOSError. Wait for 10 seconds...")
        time.sleep(10)
        return get_volume(ticker, volume, left_border, right_border, kill)

    except aiohttp.client_exceptions.ClientPayloadError:
        print("ClientPayloadError. Wait for 10 seconds...")
        time.sleep(10)
        return get_volume(ticker, volume, left_border, right_border, kill)
    if req_len < 500:
        return get_volume(ticker, (volume + left_border) // 2, left_border, volume, True)
    else:
        if not kill and (volume * 2 + 2) > right_border:   
            return get_volume(ticker, volume * 2, left_border * 2, right_border * 2, kill)
        return get_volume(ticker, (right_border + volume) // 2, volume, right_border, kill)

def parse_ticker(ticker) -> pd.DataFrame:
    return get_ticker(ticker, f"Data/{ticker}.csv", get_volume(ticker))

def ticker_exists(ticker):
    try:
        url = "https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{}/candles.json?start="
        if len(requests.get(url.format(ticker)).content) > 500:
            return True
        else:
            return False
    except Exception:
        return None