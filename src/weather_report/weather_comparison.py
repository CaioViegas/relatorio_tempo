import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from weather_functions import get_last_year_forecast, get_historical_data, get_week_forecast

def comparison_graph(df_forecast: pd.DataFrame, df_hist_1y: pd.DataFrame, df_hist_2y: pd.DataFrame, datas_fmt: pd.Series) -> None:
    """
    Gera um gráfico comparativo das temperaturas mínimas e máximas previstas para os próximos 7 dias
    em relação aos dados históricos dos dois anos anteriores.

    Parâmetros:
    ----------
    df_forecast : pd.DataFrame
        DataFrame contendo as temperaturas previstas para o ano atual.
    df_hist_1y : pd.DataFrame
        DataFrame contendo as temperaturas históricas do ano passado.
    df_hist_2y : pd.DataFrame
        DataFrame contendo as temperaturas históricas de dois anos atrás.
    datas_fmt : pd.Series
        Série contendo as datas formatadas para os próximos 7 dias.

    Retorna:
    -------
    None
        Esta função não retorna valor, mas salva o gráfico gerado como um arquivo PNG.
    """
    plt.figure(figsize=(14, 6))
    sns.set(style="whitegrid")

    sns.lineplot(x=datas_fmt, y=df_forecast['temperature_2m_min'], label='Min - Este Ano', marker='o', color='royalblue')
    sns.lineplot(x=datas_fmt, y=df_hist_1y['temperature_2m_min'], label='Min - Ano Passado', marker='o', color='mediumturquoise', linestyle='--')
    sns.lineplot(x=datas_fmt, y=df_hist_2y['temperature_2m_min'], label='Min - Ano Retrasado', marker='o', color='seagreen', linestyle=':')

    sns.lineplot(x=datas_fmt, y=df_forecast['temperature_2m_max'], label='Max - Este Ano', marker='o', color='crimson')
    sns.lineplot(x=datas_fmt, y=df_hist_1y['temperature_2m_max'], label='Max - Ano Passado', marker='o', color='darkorange', linestyle='--')
    sns.lineplot(x=datas_fmt, y=df_hist_2y['temperature_2m_max'], label='Max - Ano Retrasado', marker='o', color='goldenrod', linestyle=':')

    plt.title('Comparação de Temperaturas (Máxima e Mínima) - Próximos 7 Dias vs Anos Anteriores', fontsize=14, weight='bold')
    plt.xlabel('Data', fontsize=12)
    plt.ylabel('Temperatura (°C)', fontsize=12)
    plt.xticks(rotation=0)
    plt.legend(title='Período', loc='lower center', bbox_to_anchor=(0.5, -0.5), ncol=3)
    plt.tight_layout()

    plt.savefig("data/outputs/comparative_graph.png", dpi=300)
    plt.close()

def comparison_main():
    """
    Executa o fluxo principal de comparação das temperaturas mínimas e máximas
    previstas para os próximos 7 dias com os dados históricos do mesmo período
    nos dois anos anteriores.

    Etapas:
        - Obtém a previsão semanal atual.
        - Converte os dados em DataFrame e formata as datas.
        - Define os intervalos de datas correspondentes dos anos anteriores.
        - Obtém os dados históricos de temperatura desses períodos.
        - Constrói os DataFrames históricos.
        - Gera e salva o gráfico comparativo chamando a função `comparison_graph`.

    Retorna:
        None
    """
    forecast = get_week_forecast()
    if forecast is None:
        return
    
    df_forecast = pd.DataFrame(forecast)
    df_forecast['time'] = pd.to_datetime(df_forecast['time'])
    dates_fmt = df_forecast['time'].dt.strftime('%d/%m')

    today = datetime.today().date()
    start_last_year = today - timedelta(days=365)
    end_last_year = start_last_year + timedelta(days=6)

    start_last_2y = today - timedelta(days=730)
    end_last_2y = start_last_2y + timedelta(days=6)

    historic_last_year = get_historical_data(start_last_year, end_last_year)
    historic_last_2y = get_last_year_forecast(start_last_2y, end_last_2y)

    if not historic_last_year or not historic_last_2y:
        return
    
    df_hist_1y = pd.DataFrame(historic_last_year)
    df_hist_2y = pd.DataFrame(historic_last_2y)

    comparison_graph(df_forecast, df_hist_1y, df_hist_2y, dates_fmt)
