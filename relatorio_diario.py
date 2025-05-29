import os
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Configurações de e-mail e localização
EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
SENHA_APP = os.getenv("SENHA_APP")
EMAIL_DESTINATARIO = os.getenv("EMAIL_DESTINATARIO")

LATITUDE = -22.8696
LONGITUDE = -43.3436
TIMEZONE = "America/Sao_Paulo"


def gerar_e_enviar_relatorio():
    """
    Gera o relatório meteorológico do dia utilizando a API Open-Meteo
    e envia o resultado por e-mail.
    """
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={LATITUDE}&longitude={LONGITUDE}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,"
        f"windspeed_10m_max,windgusts_10m_max,shortwave_radiation_sum,sunrise,sunset"
        f"&timezone={TIMEZONE}"
    )

    response = requests.get(url)
    data = response.json()

    if "daily" not in data:
        print("❌ Erro: dados meteorológicos não encontrados.")
        return

    daily = data["daily"]
    idx = 0  # Índice do dia atual

    relatorio = (
        f"📍 Previsão do Tempo para Hoje ({daily['time'][idx]}):\n"
        f"────────────────────────────────────────────\n"
        f"🌡️  Temperatura: {daily['temperature_2m_min'][idx]}°C mínima, "
        f"{daily['temperature_2m_max'][idx]}°C máxima\n"
        f"🌧️  Precipitação: {daily['precipitation_sum'][idx]} mm\n"
        f"💨 Vento: {daily['windspeed_10m_max'][idx]} km/h "
        f"(rajadas até {daily['windgusts_10m_max'][idx]} km/h)\n"
        f"🔆 Radiação solar: {daily['shortwave_radiation_sum'][idx]} MJ/m²\n"
        f"🌅 Nascer do sol: {datetime.fromisoformat(daily['sunrise'][idx]).strftime('%H:%M')}\n"
        f"🌇 Pôr do sol: {datetime.fromisoformat(daily['sunset'][idx]).strftime('%H:%M')}\n"
    )

    print("📤 Enviando e-mail com o relatório do tempo...")

    msg = MIMEText(relatorio, "plain", "utf-8")
    msg["Subject"] = "📅 Relatório do Tempo - Madureira (RJ)"
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = EMAIL_DESTINATARIO

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_REMETENTE, SENHA_APP)
            smtp.send_message(msg)
        print("✅ E-mail enviado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao enviar o e-mail: {e}")


if __name__ == '__main__':
    gerar_e_enviar_relatorio()
