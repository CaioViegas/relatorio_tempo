import os
import requests
import asyncio
import pandas as pd
from telegram import Bot

# Configurações de API e localização
API_KEY = os.getenv("API_KEY")
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

LATITUDE = -22.8696
LONGITUDE = -43.3436

URL = (
    f"http://api.openweathermap.org/data/2.5/forecast?"
    f"lat={LATITUDE}&lon={LONGITUDE}&appid={API_KEY}&units=metric&lang=pt_br"
)


def obter_previsao():
    """
    Obtém a previsão do tempo a partir da API OpenWeatherMap.
    
    Returns:
        dict: Dados da previsão do tempo.
    
    Raises:
        Exception: Se a resposta da API for inválida.
    """
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro na API: {response.status_code}, {response.text}")


def processar_dados(data):
    """
    Processa os dados brutos da previsão e estrutura em DataFrame.
    
    Args:
        data (dict): Dados brutos da previsão.
    
    Returns:
        pd.DataFrame: DataFrame com as previsões estruturadas.
    """
    previsoes = []

    for item in data['list'][:3]:  # Apenas as próximas 3 previsões
        previsoes.append({
            'Data/Hora': item['dt_txt'],
            'Temperatura (°C)': item['main']['temp'],
            'Sensação Térmica (°C)': item['main']['feels_like'],
            'Pressão (hPa)': item['main']['pressure'],
            'Umidade (%)': item['main']['humidity'],
            'Condição': item['weather'][0]['main'],
            'Descrição': item['weather'][0]['description'],
            'Velocidade do Vento (m/s)': item['wind']['speed'],
            'Probabilidade de Precipitação': item.get('pop', 0),
            'Chuva (mm/3h)': item.get('rain', {}).get('3h', 0)
        })

    return pd.DataFrame(previsoes)


def formatar_mensagem(df):
    """
    Formata a mensagem de previsão do tempo para envio no Telegram.
    
    Args:
        df (pd.DataFrame): DataFrame com os dados de previsão.
    
    Returns:
        str: Mensagem formatada.
    """
    mensagem = "📊 *Relatório de Previsão do Tempo - Madureira* 📊\n\n"

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
    """
    Envia uma mensagem formatada via Telegram.
    
    Args:
        mensagem (str): Mensagem a ser enviada.
    """
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=mensagem, parse_mode='Markdown')


async def main():
    """
    Executa a coleta, processamento, formatação e envio da previsão.
    """
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
