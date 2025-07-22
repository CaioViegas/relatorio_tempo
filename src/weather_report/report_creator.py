from datetime import datetime

def daily_report(daily: dict, idx: int = 0) -> str:
    """
    Gera um resumo textual da previsão meteorológica diária.

    Esta função recebe um dicionário com dados meteorológicos diários e retorna
    uma string formatada com as principais informações do dia, como temperatura,
    precipitação, vento, radiação solar, e horários do nascer e pôr do sol.

    Parâmetros:
    ----------
    daily : dict
        Dicionário contendo as previsões meteorológicas diárias. Espera-se que possua
        as chaves: 'time', 'temperature_2m_min', 'temperature_2m_max',
        'precipitation_sum', 'windspeed_10m_max', 'windgusts_10m_max',
        'shortwave_radiation_sum', 'sunrise' e 'sunset'.

    idx : int, opcional
        Índice do dia no dicionário para gerar o relatório. Por padrão, considera o primeiro dia (0).

    Retorna:
    -------
    str
        String com a previsão do tempo formatada para o dia selecionado.

    Exemplo de uso:
    --------------
    >>> report = daily_report(daily_data, idx=0)
    >>> print(report)
    📍 Previsão do Tempo para Hoje (2025-07-21):
    ────────────────────────────────────────────
    🌡️  Temperatura: 18°C mínima, 28°C máxima
    🌧️  Precipitação: 2.3 mm
    💨 Vento: 15 km/h (rajadas até 28 km/h)
    🔆 Radiação solar: 22.1 MJ/m²
    🌅 Nascer do sol: 06:23
    🌇 Pôr do sol: 17:48
    """
    return (
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
