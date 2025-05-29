import os
import requests
import smtplib
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Carrega variáveis de ambiente
load_dotenv()

EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
SENHA_APP = os.getenv("SENHA_APP")
EMAIL_DESTINATARIO = os.getenv("EMAIL_DESTINATARIO")

LATITUDE = -22.8696
LONGITUDE = -43.3436
TIMEZONE = "America/Sao_Paulo"

def obter_previsao_7_dias():
    """
    Obtém a previsão do tempo para os próximos 7 dias usando a API Open-Meteo.
    """
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={LATITUDE}&longitude={LONGITUDE}"
        f"&daily=temperature_2m_max,temperature_2m_min"
        f"&timezone={TIMEZONE}"
    )
    response = requests.get(url)
    data = response.json()

    if "daily" not in data:
        print("❌ Erro: dados meteorológicos não encontrados.")
        return None
    return data["daily"]

def obter_historico_ano_passado(inicio, fim):
    """
    Obtém dados históricos de temperatura do mesmo período no ano anterior.
    """
    url = (
        "https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={LATITUDE}&longitude={LONGITUDE}"
        f"&start_date={inicio}&end_date={fim}"
        f"&daily=temperature_2m_max,temperature_2m_min"
        f"&timezone={TIMEZONE}"
    )
    response = requests.get(url)
    data = response.json()

    if "daily" not in data:
        print("❌ Erro: dados históricos não encontrados.")
        return None
    return data["daily"]

def gerar_grafico_comparativo(previsao, historico, arquivo='comparacao_temperaturas.png'):
    """
    Gera e salva um gráfico comparativo entre a previsão atual e o histórico do ano passado.
    """
    datas = [datetime.fromisoformat(d).strftime('%d/%m') for d in previsao['time']]
    
    plt.figure(figsize=(10, 6))

    # Temperatura mínima
    plt.plot(datas, previsao['temperature_2m_min'], marker='o', label='Min - Este Ano', color='blue')
    plt.plot(datas, historico['temperature_2m_min'][:7], marker='o', linestyle='--', label='Min - Ano Passado', color='lightblue')

    # Temperatura máxima
    plt.plot(datas, previsao['temperature_2m_max'], marker='o', label='Max - Este Ano', color='red')
    plt.plot(datas, historico['temperature_2m_max'][:7], marker='o', linestyle='--', label='Max - Ano Passado', color='salmon')

    plt.title('Comparação de Temperaturas - Próximos 7 dias vs Ano Passado')
    plt.xlabel('Data')
    plt.ylabel('Temperatura (°C)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(arquivo)
    plt.close()

    print(f"✅ Gráfico gerado: {arquivo}")

def gerar_relatorio(previsao):
    """
    Gera um relatório textual da previsão dos próximos 7 dias.
    """
    relatorio = "📅 *Previsão do Tempo para os Próximos 7 Dias - Madureira (RJ)* 📅\n\n"

    for i in range(7):
        dia = datetime.fromisoformat(previsao['time'][i]).strftime('%d/%m/%Y')
        t_min = previsao['temperature_2m_min'][i]
        t_max = previsao['temperature_2m_max'][i]

        relatorio += (
            f"🗓️ {dia}\n"
            f"🌡️ Temp: {t_min}°C min / {t_max}°C max\n"
            "─────────────────────────────\n"
        )
    return relatorio

def enviar_email(mensagem, anexo='comparacao_temperaturas.png'):
    """
    Envia um e-mail com o relatório e o gráfico comparativo em anexo.
    """
    msg = MIMEMultipart()
    msg['Subject'] = "📅 Previsão do Tempo - Próximos 7 Dias + Comparação"
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = EMAIL_DESTINATARIO

    # Corpo do e-mail
    msg.attach(MIMEText(mensagem, "plain", "utf-8"))

    # Anexar arquivo
    try:
        with open(anexo, 'rb') as file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{anexo}"')
        msg.attach(part)
    except FileNotFoundError:
        print(f"⚠️ Arquivo {anexo} não encontrado para anexo.")

    # Envio
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_REMETENTE, SENHA_APP)
            smtp.send_message(msg)
        print("✅ E-mail enviado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao enviar o e-mail: {e}")

def main():
    """
    Função principal: obtém previsão e histórico, gera gráfico, relatório e envia por e-mail.
    """
    previsao = obter_previsao_7_dias()
    if not previsao:
        return

    hoje = datetime.now()
    inicio_passado = (hoje - timedelta(days=365)).strftime('%Y-%m-%d')
    fim_passado = (hoje - timedelta(days=359)).strftime('%Y-%m-%d')

    historico = obter_historico_ano_passado(inicio_passado, fim_passado)
    if not historico:
        return

    gerar_grafico_comparativo(previsao, historico)
    relatorio = gerar_relatorio(previsao)
    enviar_email(relatorio)

if __name__ == "__main__":
    main()
