# OTT Analytics Dashboard

A real-time viewer analytics dashboard for OTT/media platforms built with Streamlit. This dashboard provides interactive 3D visualizations and live insights from viewer activity data.

## Features

- 📊 Real-time data visualization with auto-refresh
- 📈 Interactive 3D charts and animations
- 🌍 Geographical viewership analysis
- 📱 Device usage breakdown
- 🎯 Viewer engagement metrics
- 📄 PDF/Image report generation
- 🌙 Modern UI with dark theme

## Setup

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the application:
```bash
streamlit run app.py
```

## Data Format

Upload a CSV file with the following columns:
- user_id: Unique identifier for each viewer
- content_id: Show/movie identifier
- timestamp: Viewing timestamp
- watch_time: Duration watched (minutes)
- device_type: Viewing device (mobile/tablet/tv/web)
- location: City or region
- is_completed: Whether content was fully watched (true/false)

## Features

- Real-time metrics updates every 10 seconds
- Interactive 3D visualizations using Plotly
- Automatic trend detection
- Downloadable reports
- Responsive design for all screen sizes

## License

MIT License 