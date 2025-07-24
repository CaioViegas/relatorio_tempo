import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from weather_functions import get_weather_data, deg_direction

def generate_weather_dashboard():
    """
    Gera um dashboard meteorológico com gráficos de temperatura, sensação térmica, umidade relativa, velocidade do vento, probabilidade de precipitação e índice UV, 
    além de mostrar a temperatura máxima, mínima e a direção e velocidade do vento nos próximos 24 horas.

    Retorna:
        None
    """
    hourly_df, daily_df = get_weather_data()
    hourly_df['time'] = pd.to_datetime(hourly_df['time'])
    daily_df['time'] = pd.to_datetime(daily_df['time'])

    current_time = datetime.now()
    df_24h = hourly_df[
        (hourly_df['time'] >= current_time) & 
        (hourly_df['time'] <= current_time + timedelta(hours=24))
    ]

    max_temp = df_24h['temperature_2m'].max()
    min_temp = df_24h['temperature_2m'].min()
    wind_speed = df_24h['wind_speed_10m'].mean().round(1)
    wind_dir = deg_direction(df_24h['wind_direction_10m'].mode()[0])

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    fig.suptitle('Dashboard Meteorológico - 24 Horas', fontsize=18)

    sns.lineplot(ax=axes[0, 0], x=df_24h['time'].dt.strftime('%H'), y=df_24h['temperature_2m'], label='Temperatura (°C)', color='#1f77b4')
    sns.lineplot(ax=axes[0, 0], x=df_24h['time'].dt.strftime('%H'), y=df_24h['apparent_temperature'], label='Sensação (°C)', color='#ff7f0e', linestyle='--')
    axes[0, 0].set_title('Temperatura vs. Sensação Térmica')
    axes[0, 0].set_ylabel('°C')
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid(True)
    
    sns.lineplot(ax=axes[0, 1], x=df_24h['time'].dt.strftime('%H'), y=df_24h['relative_humidity_2m'], color='#2ca02c')
    axes[0, 1].set_title('Umidade Relativa (%)')
    axes[0, 1].set_ylabel('%')
    axes[0, 1].tick_params(axis='x', rotation=45)
    axes[0, 1].grid(True)

    sns.lineplot(ax=axes[0, 2], x=df_24h['time'].dt.strftime('%H'), y=df_24h['wind_speed_10m'], color='#9467bd')
    axes[0, 2].set_title('Velocidade do Vento (Km/h)')
    axes[0, 2].set_ylabel('Km/h')
    axes[0, 2].tick_params(axis='x', rotation=45)
    axes[0, 2].grid(True)

    sns.barplot(ax=axes[1, 0], x=df_24h['time'].dt.strftime('%H'), y=df_24h['precipitation_probability'], color='#17becf')
    axes[1, 0].set_title('Probabilidade de Precipitação')
    axes[1, 0].set_ylabel('%')
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].grid(True)

    sns.barplot(ax=axes[1, 1], x=df_24h['time'].dt.strftime('%H'), y=df_24h['uv_index'], color='#e377c2')
    axes[1, 1].set_title('Índice UV')
    axes[1, 1].set_ylabel('UV')
    axes[1, 1].tick_params(axis='x', rotation=45)
    axes[1, 1].axhspan(6, 8, color='orange', alpha=0.2)
    axes[1, 1].grid(True)

    axes[1, 2].axis('off')

    axes[1, 2].text(0.5, 0.85, "MÁXIMA:", color='red', fontsize=14, ha='center', weight='bold')
    axes[1, 2].text(0.5, 0.75, f"{max_temp}°C", color='black', fontsize=14, ha='center')

    axes[1, 2].text(0.5, 0.60, "MÍNIMA:", color='blue', fontsize=14, ha='center', weight='bold')
    axes[1, 2].text(0.5, 0.50, f"{min_temp}°C", color='black', fontsize=14, ha='center')

    axes[1, 2].text(0.5, 0.35, "VENTOS:", color='green', fontsize=14, ha='center', weight='bold')
    axes[1, 2].text(0.5, 0.25, f"{wind_dir} | {wind_speed} km/h", color='black', fontsize=14, ha='center')

    axes[1, 2].set_facecolor('whitesmoke')
    for spine in axes[1, 2].spines.values():
        spine.set_edgecolor('gray')
        spine.set_linewidth(1)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig('data/outputs/weather_dashboard.png', dpi=300)
    plt.close()