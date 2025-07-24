from pathlib import Path
from weather_functions import get_weather_data
from weather_dashboard import generate_weather_dashboard
from weather_comparison import comparison_main
from report_creator import daily_report
from email_sender import send_email

def main():
    base_dir = Path(__file__).resolve().parents[2]
    outputs_dir = base_dir / "data" / "outputs"

    outputs_dir.mkdir(parents=True, exist_ok=True)

    dashboard_png = outputs_dir / "weather_dashboard.png"
    comparison_png = outputs_dir / "comparative_graph.png"

    generate_weather_dashboard() 
    comparison_main()             

    _, daily = get_weather_data()
    report = daily_report(daily)

    files = [str(dashboard_png), str(comparison_png)]
    send_email(report, files)

if __name__ == "__main__":
    main()
