import requests
import pandas as pd
from playwright.async_api import async_playwright
from weather_config import LAT, LON, TIMEZONE

def get_weather_data():
    """
    Recupera os dados meteorológicos atuais da API Open-Meteo para uma localização
    específica, utilizando latitude, longitude e fuso horário previamente definidos.

    Dados obtidos:
        - Variáveis horárias: temperatura, sensação térmica, umidade relativa, 
          velocidade e direção do vento, probabilidade de precipitação e índice UV.
        - Variáveis diárias: temperaturas mínima e máxima, soma de precipitação, 
          velocidade e rajadas máximas do vento, radiação solar, nascer e pôr do sol.

    Retorna:
        Tuple[pd.DataFrame, pd.DataFrame]: Dois DataFrames, o primeiro contendo os dados 
        horários e o segundo contendo os dados diários.
    
    Levanta:
        HTTPError: Se a requisição à API falhar.
    """
    base_url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": LAT,
        "longitude": LON,
        "hourly": ",".join([
            "temperature_2m",
            "apparent_temperature",
            "relative_humidity_2m",
            "wind_speed_10m",
            "precipitation_probability",
            "uv_index",
            "wind_direction_10m"            
        ]),
        "daily": ",".join([
            "temperature_2m_min",
            "temperature_2m_max",
            "precipitation_sum",
            "windspeed_10m_max",
            "windgusts_10m_max",
            "shortwave_radiation_sum",
            "sunrise",
            "sunset"
        ]),
        "timezone": TIMEZONE
    }

    response = requests.get(base_url, params=params)
    response.raise_for_status()

    data = response.json()

    hourly = pd.DataFrame(data['hourly'])
    daily = pd.DataFrame(data['daily'])

    return hourly, daily

def deg_direction(deg):
    """
    Converte um valor angular (em graus) em uma direção cardinal simplificada.

    Parâmetros:
        deg (float or int): Valor em graus, representando a direção do vento.

    Retorna:
        str: Direção cardinal correspondente (ex: 'N', 'NE', 'E', ..., 'NW').

    Exemplo:
        >>> deg_direction(90)
        'E'
    """
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    ix = int((deg + 22.5) // 45) % 8
    return directions[ix]

def get_week_forecast():
    """
    Obtém a previsão diária de temperatura máxima e mínima para os próximos 7 dias
    a partir da API Open-Meteo, com base nas coordenadas e fuso horário definidos.

    Retorna:
        dict or None: Um dicionário contendo os dados diários de temperatura
        ("temperature_2m_max", "temperature_2m_min" e "time"), ou None caso a resposta
        da API não contenha a chave 'daily'.
    """   
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={LAT}&longitude={LON}"
        f"&daily=temperature_2m_max,temperature_2m_min"
        f"&timezone={TIMEZONE}"
    )
    response = requests.get(url)
    data = response.json()
    if "daily" not in data:
        print("Error: data not found.")
        return None
    return data["daily"]

def get_last_year_forecast(start, end):
    """
    Obtém dados históricos diários de temperatura máxima e mínima para o período especificado,
    utilizando a API de arquivos da Open-Meteo.

    Parâmetros:
        start (str): Data de início no formato 'YYYY-MM-DD'.
        end (str): Data de término no formato 'YYYY-MM-DD'.

    Retorna:
        dict or None: Um dicionário contendo os dados diários de temperatura
        ("temperature_2m_max", "temperature_2m_min" e "time"), ou None caso a resposta
        da API não contenha a chave 'daily'.
    """
    url = (
        "https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={LAT}&longitude={LON}"
        f"&start_date={start}&end_date={end}"
        f"&daily=temperature_2m_max,temperature_2m_min"
        f"&timezone={TIMEZONE}"
    )
    response = requests.get(url)
    data = response.json()
    if "daily" not in data:
        print("Error: data not found.")
        return None
    return data["daily"]

async def html_to_png(html_path, output_png):
    """
    Converte um arquivo HTML local em uma imagem PNG utilizando o Playwright.

    Parâmetros:
        html_path (str): Caminho absoluto para o arquivo HTML a ser renderizado.
        output_png (str): Caminho de saída onde a imagem PNG será salva.

    Retorna:
        None
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"file:///{html_path}")
        await page.wait_for_timeout(2000) 
        await page.screenshot(path=output_png, full_page=True)
        await browser.close()

def get_week_forecast():
    """
    Obtém a previsão diária de temperatura mínima e máxima para os próximos 7 dias
    a partir da API da Open-Meteo.

    Parâmetros:
        Nenhum

    Retorna:
        dict | None: Dicionário contendo os dados diários da previsão ou None 
        se os dados não estiverem disponíveis.
    """
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={LAT}&longitude={LON}"
        f"&daily=temperature_2m_max,temperature_2m_min"
        f"&timezone={TIMEZONE}"
    )
    response = requests.get(url)
    data = response.json()
    if "daily" not in data:
        print("Error: data not found.")
        return None
    return data["daily"]

def get_historical_data(start, end):
    """
    Obtém dados históricos de temperatura mínima e máxima para um intervalo de datas
    especificado, utilizando a API de histórico da Open-Meteo.

    Parâmetros:
        star (str): Data de início no formato 'YYYY-MM-DD'.
        end (str): Data de fim no formato 'YYYY-MM-DD'.

    Retorna:
        dict | None: Dicionário contendo os dados diários históricos ou None 
        se os dados não estiverem disponíveis.
    """
    url = (
        "https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={LAT}&longitude={LON}"
        f"&start_date={start}&end_date={end}"
        f"&daily=temperature_2m_max,temperature_2m_min"
        f"&timezone={TIMEZONE}"
    )
    response = requests.get(url)
    data = response.json()
    if "daily" not in data:
        print("Error: historical data not found.")
        return None
    return data["daily"]
