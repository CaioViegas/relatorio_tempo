import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from weather_functions import get_last_year_forecast, get_historical_data, get_week_forecast

def comparison_graph(df_forecast: pd.DataFrame, df_hist_1y: pd.DataFrame, df_hist_2y: pd.DataFrame, datas_fmt: pd.Series) -> go.Figure:
    """
    Gera um gráfico interativo comparando as temperaturas mínimas e máximas
    previstas para os próximos 7 dias com os dados históricos dos dois anos anteriores.

    Args:
        df_forecast (pd.DataFrame): DataFrame contendo as temperaturas mínimas e máximas previstas.
        df_hist_1y (pd.DataFrame): DataFrame com as temperaturas mínimas e máximas do mesmo período no ano anterior.
        df_hist_2y (pd.DataFrame): DataFrame com as temperaturas mínimas e máximas do mesmo período há dois anos.
        datas_fmt (pd.Series): Série com as datas formatadas para o eixo X.

    Returns:
        go.Figure: Figura do Plotly com os dados comparativos renderizados.

    Observação:
        O gráfico também é salvo automaticamente como arquivo HTML em
        'data/outputs/comparative_graph.html'.
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=datas_fmt, y=df_forecast['temperature_2m_min'],
        mode='lines+markers', name='Min - Este Ano',
        line=dict(color='royalblue', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=datas_fmt, y=df_hist_1y['temperature_2m_min'],
        mode='lines+markers', name='Min - Ano Passado',
        line=dict(color='mediumturquoise', dash='dash')
    ))
    fig.add_trace(go.Scatter(
        x=datas_fmt, y=df_hist_2y['temperature_2m_min'],
        mode='lines+markers', name='Min - Ano Retrasado',
        line=dict(color='seagreen', dash='dot')
    ))

    fig.add_trace(go.Scatter(
        x=datas_fmt, y=df_forecast['temperature_2m_max'],
        mode='lines+markers', name='Max - Este Ano',
        line=dict(color='crimson', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=datas_fmt, y=df_hist_1y['temperature_2m_max'],
        mode='lines+markers', name='Max - Ano Passado',
        line=dict(color='darkorange', dash='dash')
    ))
    fig.add_trace(go.Scatter(
        x=datas_fmt, y=df_hist_2y['temperature_2m_max'],
        mode='lines+markers', name='Max - Ano Retrasado',
        line=dict(color='goldenrod', dash='dot')
    ))

    fig.update_layout(
        title='📈 Comparação de Temperaturas (Máxima e Mínima) - Próximos 7 Dias vs Anos Anteriores',
        xaxis_title='Data',
        yaxis_title='Temperatura (°C)',
        template='plotly_white',
        height=520,
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(title='Período', orientation='h', y=1.02, x=0.5, xanchor='center')
    )

    fig.write_html("data/outputs/comparative_graph.html")

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
