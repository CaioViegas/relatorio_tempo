import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from weather_functions import get_weather_data, deg_direction

def generate_weather_dashboard():
    """
    Gera um dashboard interativo em Plotly contendo gráficos meteorológicos 
    para as próximas 24 horas com base em dados climáticos horários e diários.

    O dashboard inclui:
        - Temperatura vs. Sensação Térmica
        - Umidade relativa do ar
        - Velocidade do vento
        - Probabilidade de precipitação
        - Índice UV
        - Anotações com temperatura máxima, mínima e direção/velocidade média do vento

    Returns:
        plotly.graph_objects.Figure: Objeto de figura contendo o dashboard gerado.
    """
    hourly_df, daily_df = get_weather_data()
    hourly_df['time'] = pd.to_datetime(hourly_df['time'])
    daily_df['time'] = pd.to_datetime(daily_df['time'])

    current_time = datetime.now()
    df_24h = hourly_df[(hourly_df['time'] >= current_time) & (hourly_df['time'] <= current_time + timedelta(hours=24))]

    fig = make_subplots(
        rows=2, cols=3,
        subplot_titles=(
            'Temperatura vs. Sensação Térmica',
            'Umidade Relativa (%)',
            'Velocidade do Vento (Km/h)',
            'Probabilidade de Precipitação',
            'Índice UV',
            'Máxima / Mínima / Direção do Vento'
        ),
        vertical_spacing=0.2,
        horizontal_spacing=0.1,
        specs=[
            [{"type": "xy"}, {"type": "xy"}, {"type": "xy"}],  
            [{"type": "xy"}, {"type": "xy"}, {"type": "domain"}]          
        ]
    )

    fig.add_trace(go.Scatter(
        x=df_24h['time'], y=df_24h['temperature_2m'],
        name='Temperatura (°C)',
        line=dict(color='#1f77b4', width=3),
        mode='lines+markers',
        hovertemplate='%{x|%H:%M}<br>Temperatura: %{y:.1f}°C'
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=df_24h['time'], y=df_24h['apparent_temperature'],
        name='Sensacao (°C)',
        line=dict(color='#ff7f0e', width=3, dash='dot'),
        mode='lines+markers',
        hovertemplate='%{x|%H:%M}<br>Sensacao: %{y:.1f}°C'
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=df_24h['time'], y=df_24h['relative_humidity_2m'],
        name='Umidade (%)',
        line=dict(color='#2ca02c', width=3),
        hovertemplate='%{x|%H:%M}<br>Umidade: %{y:.1f}%'
    ), row=1, col=2)

    fig.add_trace(go.Scatter(
        x=df_24h['time'], y=df_24h['wind_speed_10m'],
        name='Vento (km/h)',
        line=dict(color='#9467bd', width=3),
        hovertemplate='%{x|%H:%M}<br>Vento: %{y:.1f} km/h'
    ), row=1, col=3)

    fig.add_trace(go.Bar(
        x=df_24h['time'], y=df_24h['precipitation_probability'],
        name='Chuva (%)',
        marker=dict(color='#17becf', opacity=0.7)
    ), row=2, col=1)

    fig.add_trace(go.Bar(
        x=df_24h['time'], y=df_24h['uv_index'],
        name='Índice UV',
        marker=dict(color='#e377c2', opacity=0.7)
    ), row=2, col=2)

    fig.add_shape(
        type="rect",
        xref="x domain", yref="y",
        x0=0, x1=1, y0=6, y1=8,
        fillcolor="orange", opacity=0.2,
        line_width=0, row=2, col=2
    )

    max_temp = df_24h['temperature_2m'].max()
    min_temp = df_24h['temperature_2m'].min()
    wind_speed = df_24h['wind_speed_10m'].mean().round(1)
    wind_dir = deg_direction(df_24h['wind_direction_10m'].mode()[0])

    deslocamento = 0.02
    y_top = 0.25
    y_bottom = 0.12
    x_max = 0.84 + deslocamento
    x_min = 0.92 + deslocamento
    x_ventos = 0.895 + deslocamento

    fig.add_annotation(
        text=f"<b>MÁXIMA</b><br>{max_temp}°C",
        xref="paper", yref="paper",
        x=x_max, y=y_top,
        showarrow=False,
        font=dict(size=20, color='#d62728'),
        align='center',
        bordercolor='#d62728',
        borderwidth=2,
        borderpad=10,
        bgcolor='#f9f9f9'
    )

    fig.add_annotation(
        text=f"<b>MÍNIMA</b><br>{min_temp}°C",
        xref="paper", yref="paper",
        x=x_min, y=y_top,
        showarrow=False,
        font=dict(size=20, color='#1f77b4'),
        align='center',
        bordercolor='#1f77b4',
        borderwidth=2,
        borderpad=10,
        bgcolor='#f9f9f9'
    )

    fig.add_annotation(
        text=f"<b>VENTOS</b><br>{wind_dir} | {wind_speed} km/h",
        xref="paper", yref="paper",
        x=x_ventos, y=y_bottom,
        showarrow=False,
        font=dict(size=20, color='#2ca02c'),
        align='center',
        bordercolor='#2ca02c',
        borderwidth=2,
        borderpad=10,
        bgcolor='#f9f9f9'
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGrey')

    fig.update_layout(
        title_text='Dashboard Meteorológico - 24 Horas',
        title_font=dict(size=24),
        height=800,
        width=2000,
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=True,
        margin=dict(l=50, r=50, t=100, b=50)
    )

    fig.update_yaxes(title_text='Temperatura (°C)', row=1, col=1)
    fig.update_yaxes(title_text='Umidade (%)', row=1, col=2)
    fig.update_yaxes(title_text='Velocidade (km/h)', row=1, col=3)
    fig.update_yaxes(title_text='Probabilidade (%)', row=2, col=1)
    fig.update_yaxes(title_text='UV Index', row=2, col=2)

    for row in [1, 2]:
        for col in [1, 2]:
            fig.update_xaxes(
                row=row, col=col,
                tickformat='%H', dtick=7200000
            )
        if row == 1:
            fig.update_xaxes(
                row=row, col=3,
                tickformat='%H', dtick=7200000
            )

    return fig