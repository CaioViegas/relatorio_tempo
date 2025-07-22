import asyncio
from pathlib import Path
from weather_functions import html_to_png, get_weather_data
from weather_dashboard import generate_weather_dashboard
from weather_comparison import comparison_main
from report_creator import daily_report
from email_sender import send_email

def main():
    base_dir = Path(__file__).resolve().parents[2]
    html_dir = base_dir / "data" / "outputs"
    img_dir = base_dir / "data" / "images" 

    html_dir.mkdir(parents=True, exist_ok=True)
    img_dir.mkdir(parents=True, exist_ok=True)

    dashboard_html = html_dir / "weather_dashboard.html"
    dashboard_png = img_dir / "weather_dashboard.png"

    comparison_html = html_dir / "comparative_graph.html"
    comparison_png = img_dir / "comparative_graph.png"

    fig = generate_weather_dashboard()
    fig.write_html(dashboard_html)
    comparison_main()

    asyncio.run(html_to_png(str(dashboard_html), output_png=str(dashboard_png)))
    asyncio.run(html_to_png(str(comparison_html), output_png=str(comparison_png)))

    _, daily = get_weather_data()
    report = daily_report(daily)

    files = [str(dashboard_png), str(comparison_png)]
    send_email(report, files)

if __name__ == "__main__":
    main()
