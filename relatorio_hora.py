import requests
import asyncio
import os
import pandas as pd
from telegram import Bot

API_KEY = os.getenv("API_KEY")
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

latitude = -22.8696
longitude = -43.3436

URL = f"http://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&appid={API_KEY}&units=metric&lang=pt_br"

def obter_previsao():
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception(f"Erro na API: {response.status_code}, {response.text}")

def processar_dados(data):
    previsoes = []
    
    for item in data['list'][:2]:  
        dt_txt = item['dt_txt']
        temp = item['main']['temp']
        feels_like = item['main']['feels_like']
        pressure = item['main']['pressure']
        humidity = item['main']['humidity']
        weather_main = item['weather'][0]['main']
        weather_desc = item['weather'][0]['description']
        wind_speed = item['wind']['speed']
        pop = item.get('pop', 0)
        chuva = item.get('rain', {}).get('3h', 0)

        previsoes.append({
            'Data/Hora': dt_txt,
            'Temperatura (°C)': temp,
            'Sensação Térmica (°C)': feels_like,
            'Pressão (hPa)': pressure,
            'Umidade (%)': humidity,
            'Condição': weather_main,
            'Descrição': weather_desc,
            'Velocidade do Vento (m/s)': wind_speed,
            'Probabilidade de Precipitação': pop,
            'Chuva (mm/3h)': chuva
        })
    
    df = pd.DataFrame(previsoes)
    return df

def formatar_mensagem(df):
    mensagem = f"📊 *Relatório de Previsão do Tempo - Madureira* 📊\n\n"
    
    for _, row in df.iterrows():
        mensagem += (
            f"🕒 {row['Data/Hora']}\n"
            f"🌡️ Temp: {row['Temperatura (°C)']}°C | Sensação: {row['Sensação Térmica (°C)']}°C\n"
            f"💨 Vento: {row['Velocidade do Vento (m/s)']} m/s\n"
            f"🌧️ Chuva: {row['Chuva (mm/3h)']} mm | POP: {row['Probabilidade de Precipitação']*100:.0f}%\n"
            f"🔵 Umidade: {row['Umidade (%)']}%\n"
            f"🔴 Pressão: {row['Pressão (hPa)']} hPa\n"
            f"🌤️ Condição: {row['Condição']} - {row['Descrição']}\n\n"
        )
    return mensagem

async def enviar_mensagem_telegram(mensagem):
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=mensagem, parse_mode='Markdown')

async def main():
    try:
        dados = obter_previsao()
        df = processar_dados(dados)
        mensagem = formatar_mensagem(df)
        await enviar_mensagem_telegram(mensagem)
        print("✅ Mensagem enviada com sucesso via Telegram!")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == '__main__':
    asyncio.run(main())