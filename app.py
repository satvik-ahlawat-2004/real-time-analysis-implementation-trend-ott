import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import time
import altair as alt
from PIL import Image
import io
from fpdf import FPDF
import base64

# Page configuration
st.set_page_config(
    page_title="OTT Analytics Dashboard",
    page_icon="📺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Base styling */
    .main {
        background: linear-gradient(135deg, #0E1117 0%, #1A1C26 100%);
        color: #E0E0E0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #8E2DE2 0%, #4A00E0 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    .main-header h1 {
        font-weight: 800;
        font-size: 3.2rem;
        background: linear-gradient(90deg, #FFFFFF 0%, #B8B8B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.85);
        max-width: 700px;
        margin: 0 auto;
    }
    
    /* Card styling */
    .card {
        background: rgba(17, 25, 40, 0.75);
        border-radius: 12px;
        padding: 1.5rem;
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.3);
        transition: all 0.3s ease;
        margin-bottom: 1.5rem;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px 0 rgba(31, 38, 135, 0.4);
    }
    
    .card h3 {
        color: white;
        font-weight: 600;
        margin-bottom: 1rem;
        font-size: 1.3rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 0.5rem;
    }
    
    /* Chart styling */
    .stPlotlyChart {
        background-color: rgba(17, 25, 40, 0.75);
        border-radius: 12px;
        padding: 1rem;
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.3);
    }
    
    /* Metric styling */
    .stMetric {
        background: rgba(17, 25, 40, 0.75);
        border-radius: 12px;
        padding: 1.5rem !important;
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.3);
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
    }
    
    div[data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        color: rgba(255, 255, 255, 0.75) !important;
    }
    
    /* Trending card styling */
    .trending-card {
        background: linear-gradient(135deg, rgba(59, 65, 138, 0.6) 0%, rgba(40, 48, 90, 0.6) 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .trending-card:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    .trending-card h3 {
        font-size: 1.5rem;
        margin: 0 0 10px 0;
        background: linear-gradient(90deg, #FFFFFF 0%, #B8B8B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Validation styling */
    .validation-info {
        background: linear-gradient(135deg, rgba(13, 110, 78, 0.25) 0%, rgba(11, 82, 91, 0.25) 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(26, 213, 152, 0.3);
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.2);
    }
    
    .validation-error {
        background: linear-gradient(135deg, rgba(190, 30, 45, 0.25) 0%, rgba(140, 20, 30, 0.25) 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 84, 84, 0.3);
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.2);
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: rgba(15, 17, 26, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1rem;
    }
    
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
        color: white;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #4A00E0 0%, #8E2DE2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 16px 0 rgba(31, 38, 135, 0.37) !important;
    }
    
    /* Hotspots styling */
    .hotspot-card {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .hotspot-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
    }
    
    .progress-container {
        background-color: rgba(30, 41, 59, 0.8);
        border-radius: 5px;
        height: 8px;
        margin-top: 5px;
        overflow: hidden;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #4A00E0 0%, #8E2DE2 100%);
        height: 100%;
        border-radius: 5px;
    }
    
    /* Map controls */
    .control-panel {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 12px;
        padding: 1.2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Custom selection styling */
    div[data-baseweb="select"] > div {
        background: rgba(30, 41, 59, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 17, 26, 0.95);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(90, 90, 90, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(110, 110, 110, 0.7);
    }
    
    /* Tooltip styling */
    div[data-testid="stTooltipIcon"] {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    /* General text styling */
    p, li, div {
        color: rgba(255, 255, 255, 0.85);
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Header with improved styling
st.markdown("""
<div class="main-header">
    <div style="display: flex; justify-content: flex-end; align-items: center; margin-bottom: 0.5rem;">
        <div style="font-size: 0.75rem; color: rgba(255, 255, 255, 0.8); 
                   letter-spacing: 1.5px; text-transform: uppercase; 
                   background: rgba(0,0,0,0.2); padding: 4px 12px; 
                   border-radius: 20px; backdrop-filter: blur(5px);
                   border: 1px solid rgba(255,255,255,0.1);">
            made by satvikkkkk
        </div>
    </div>
    <h1>🎬 OTT Analytics Dashboard</h1>
    <p>Real-time viewer analytics and engagement metrics with intelligent data validation</p>
</div>
""", unsafe_allow_html=True)

# Mock data generation function
def get_mock_data():
    """Generate mock data if no file is uploaded"""
    current_time = datetime.now()
    data = {
        'user_id': range(1, 1001),
        'content_id': np.random.choice(['Show_A', 'Show_B', 'Show_C', 'Show_D', 'Show_E'], 1000),
        'timestamp': [current_time - timedelta(minutes=np.random.randint(0, 60)) for _ in range(1000)],
        'watch_time': np.random.normal(30, 10, 1000),
        'device_type': np.random.choice(['mobile', 'tablet', 'tv', 'web'], 1000),
        'location': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'], 1000),
        'is_completed': np.random.choice([True, False], 1000, p=[0.7, 0.3])
    }
    return pd.DataFrame(data)

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False
if 'validated' not in st.session_state:
    st.session_state.validated = False
if 'validation_message' not in st.session_state:
    st.session_state.validation_message = ""

# Required columns for OTT analysis
REQUIRED_COLUMNS = {
    'content_id': ['content_id', 'content_title', 'show_name', 'title'],
    'watch_time': ['watch_time', 'duration', 'watch_duration', 'viewing_time'],
    'timestamp': ['timestamp', 'watch_timestamp', 'viewing_timestamp', 'date'],
    'device_type': ['device_type', 'device', 'platform'],
    'location': ['location', 'city', 'region', 'country'],
    'is_completed': ['is_completed', 'completed', 'finished']
}

def validate_columns(df):
    """Validate if the dataframe has the required columns"""
    found_columns = {}
    missing_columns = []
    
    for required_col, alternatives in REQUIRED_COLUMNS.items():
        found = False
        for alt in alternatives:
            if any(col.lower() == alt.lower() for col in df.columns):
                found = True
                # Store the actual column name that was found
                found_columns[required_col] = next(col for col in df.columns if col.lower() == alt.lower())
                break
        if not found:
            missing_columns.append(required_col)
    
    return found_columns, missing_columns

def analyze_dataset(df):
    """Analyze the dataset and return a summary"""
    num_rows = len(df)
    num_cols = len(df.columns)
    date_range = None
    if 'timestamp' in df.columns:
        try:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            date_range = f"{df['timestamp'].min().strftime('%Y-%m-%d')} to {df['timestamp'].max().strftime('%Y-%m-%d')}"
        except:
            date_range = "Unable to parse date range"
    
    return {
        'num_rows': num_rows,
        'num_cols': num_cols,
        'date_range': date_range
    }

# Sidebar
with st.sidebar:
    st.header("📊 Dashboard Controls")
    uploaded_file = st.file_uploader("Upload Viewer Data (CSV/Excel)", type=['csv', 'xlsx'])
    
    if uploaded_file is not None:
        try:
            # Read the file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Validate columns
            found_columns, missing_columns = validate_columns(df)
            
            if not missing_columns:
                # Analyze dataset
                analysis = analyze_dataset(df)
                
                # Show dataset summary
                st.markdown("""
                <div class="validation-info">
                    <h3>✅ Dataset Validated Successfully</h3>
                    <p>Records: {}</p>
                    <p>Columns: {}</p>
                    <p>Date Range: {}</p>
                </div>
                """.format(analysis['num_rows'], analysis['num_cols'], analysis['date_range']), 
                unsafe_allow_html=True)
                
                # Show sample data
                st.subheader("📋 Sample Data")
                st.dataframe(df.head(5))
                
                # Confirmation button
                if st.button("✅ Use This Dataset"):
                    # Rename columns to standard names
                    df = df.rename(columns={v: k for k, v in found_columns.items()})
                    
                    # Convert 'is_completed' column to boolean
                    is_completed_col = found_columns.get('is_completed')
                    if is_completed_col:
                        # Handle different formats of boolean values
                        if df[is_completed_col].dtype == 'object':
                            # Convert string TRUE/FALSE to boolean
                            df[is_completed_col] = df[is_completed_col].map({
                                'TRUE': True, 'True': True, 'true': True, '1': True, 1: True,
                                'FALSE': False, 'False': False, 'false': False, '0': False, 0: False
                            })
                    
                    st.session_state.data = df
                    st.session_state.validated = True
                    st.success("Dataset loaded successfully! The dashboard will now update.")
                    
            else:
                st.markdown(f"""
                <div class="validation-error">
                    <h3>❌ Validation Failed</h3>
                    <p>Missing required columns:</p>
                    <ul>{''.join([f'<li>{col}</li>' for col in missing_columns])}</ul>
                    <p>Please ensure your dataset includes these columns or their alternatives.</p>
                </div>
                """, unsafe_allow_html=True)
                st.session_state.validated = False
                
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            st.session_state.validated = False
    
    if st.session_state.validated:
        st.session_state.auto_refresh = st.toggle("Enable Auto-Refresh", st.session_state.auto_refresh)
        
        if st.button("Generate Report"):
            if st.session_state.data is not None:
                # Create PDF report using a different approach to avoid BytesIO error
                try:
                    # Create PDF report
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font('Arial', 'B', 16)
                    pdf.cell(0, 10, 'OTT Analytics Dashboard Report', ln=True, align='C')
                    pdf.set_font('Arial', '', 12)
                    
                    # Add timestamp
                    pdf.cell(0, 10, f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', ln=True)
                    
                    # Add summary statistics
                    pdf.ln(10)
                    pdf.set_font('Arial', 'B', 14)
                    pdf.cell(0, 10, 'Key Metrics', ln=True)
                    pdf.set_font('Arial', '', 12)
                    
                    # Calculate metrics for the PDF
                    total = len(df['user_id'].unique()) if 'user_id' in df.columns else len(df)
                    avg_time = df['watch_time'].mean()
                    completion = (df['is_completed'].astype(int).sum() / len(df)) * 100
                    
                    pdf.cell(0, 10, f'Total Viewers: {total}', ln=True)
                    pdf.cell(0, 10, f'Average Watch Time: {avg_time:.1f} minutes', ln=True)
                    pdf.cell(0, 10, f'Completion Rate: {completion:.1f}%', ln=True)
                    
                    # Add information about top content
                    top_content = df['content_id'].value_counts().nlargest(3)
                    pdf.ln(10)
                    pdf.set_font('Arial', 'B', 14)
                    pdf.cell(0, 10, 'Top Content', ln=True)
                    pdf.set_font('Arial', '', 12)
                    
                    for content, count in top_content.items():
                        pdf.cell(0, 10, f'{content}: {count} viewers', ln=True)
                    
                    # Save to bytes for download
                    pdf_bytes = pdf.output(dest='S').encode('latin-1')
                    
                    # Create download button
                    st.download_button(
                        label="Download PDF Report",
                        data=pdf_bytes,
                        file_name="ott_analytics_report.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")
                    st.info("Please try again or contact support if the issue persists.")

# Main content
if st.session_state.validated and st.session_state.data is not None:
    df = st.session_state.data
    
    # Auto-refresh logic
    if st.session_state.auto_refresh:
        if (datetime.now() - st.session_state.last_refresh).seconds >= 10:
            st.session_state.data = get_mock_data()
            st.session_state.last_refresh = datetime.now()
            st.rerun()
    
    # Ensure is_completed is boolean for calculations
    if 'is_completed' in df.columns and df['is_completed'].dtype != 'bool':
        df['is_completed'] = df['is_completed'].astype(bool)
    
    # Calculate metrics
    total_viewers = len(df['user_id'].unique()) if 'user_id' in df.columns else len(df)
    avg_watch_time = df['watch_time'].mean()
    completion_rate = (df['is_completed'].astype(int).sum() / len(df)) * 100
    
    # Display KPI metrics
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="font-size: 1.8rem; margin-bottom: 15px; font-weight: 600;">Key Performance Indicators</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Active Viewers", f"{total_viewers:,}")
    with col2:
        st.metric("Average Watch Time", f"{avg_watch_time:.1f} min")
    with col3:
        st.metric("Content Completion Rate", f"{completion_rate:.1f}%")
    
    # Create visualizations
    st.markdown("""
    <div style="margin: 30px 0 20px 0;">
        <h2 style="font-size: 1.8rem; margin-bottom: 15px; font-weight: 600;">Content & Device Analysis</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Active viewers by content (3D Donut Chart)
        content_viewers = df['content_id'].value_counts()
        fig_content = go.Figure(data=[go.Pie(
            labels=content_viewers.index,
            values=content_viewers.values,
            hole=0.5,
            textinfo='label+percent',
            marker=dict(
                colors=px.colors.sequential.Plasma,
                line=dict(color='rgba(255, 255, 255, 0.5)', width=1)
            )
        )])
        fig_content.update_layout(
            title="Active Viewers by Content",
            showlegend=False,
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_content, use_container_width=True)
        
    with col2:
        # Device usage breakdown (3D Pie Chart)
        device_usage = df['device_type'].value_counts()
        fig_devices = go.Figure(data=[go.Pie(
            labels=device_usage.index,
            values=device_usage.values,
            textinfo='label+percent',
            marker=dict(
                colors=px.colors.sequential.Viridis,
                line=dict(color='rgba(255, 255, 255, 0.5)', width=1)
            )
        )])
        fig_devices.update_layout(
            title="Device Usage Breakdown",
            showlegend=False,
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_devices, use_container_width=True)
    
    # Viewer drop-off analysis
    st.markdown("""
    <div style="margin: 30px 0 20px 0;">
        <h2 style="font-size: 1.8rem; margin-bottom: 5px; font-weight: 600;">📉 Viewer Drop-off Analysis</h2>
        <p style="opacity: 0.8; font-size: 0.9rem; margin-bottom: 15px;">How viewers engage with content over time</p>
    </div>
    """, unsafe_allow_html=True)
    
    df['minute_bucket'] = pd.qcut(df['watch_time'], q=10, labels=False)
    dropoff_data = df.groupby('minute_bucket').size()
    
    fig_dropoff = go.Figure()
    fig_dropoff.add_trace(go.Scatter(
        x=list(range(len(dropoff_data))),
        y=dropoff_data.values,
        mode='lines+markers',
        name='Viewers',
        line=dict(width=3, color='#4A00E0'),
        marker=dict(
            size=8,
            color=dropoff_data.values,
            colorscale='Viridis',
            line=dict(width=1, color='rgba(255, 255, 255, 0.5)')
        ),
        fill='tozeroy',
        fillcolor='rgba(74, 0, 224, 0.2)'
    ))
    fig_dropoff.update_layout(
        title=None,
        xaxis_title="Watch Time Percentile",
        yaxis_title="Number of Viewers",
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        margin=dict(l=20, r=20, t=10, b=20),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            showline=True,
            linecolor='rgba(255, 255, 255, 0.2)',
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255, 255, 255, 0.1)',
            showline=True,
            linecolor='rgba(255, 255, 255, 0.2)',
        )
    )
    st.plotly_chart(fig_dropoff, use_container_width=True)
    
    # Location-wise viewership
    st.subheader("🌎 Geographical Viewership")
    location_data = df['location'].value_counts().reset_index()
    location_data.columns = ['location', 'viewers']
    
    # Add geo-mapping utilities
    def detect_location_type(locations):
        """Determine if locations are likely US states, cities, or countries"""
        us_states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", 
                   "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", 
                   "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", 
                   "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", 
                   "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", 
                   "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", 
                   "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming",
                   "District of Columbia"]
        
        major_countries = ["United States", "Canada", "Mexico", "Brazil", "Argentina", "United Kingdom", 
                          "France", "Germany", "Italy", "Spain", "Russia", "China", "Japan", "India", 
                          "Australia", "New Zealand", "South Africa", "Nigeria", "Egypt", "Saudi Arabia"]
        
        # Check for state abbreviations like "NY", "CA"
        us_state_abbrevs = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", 
                           "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", 
                           "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", 
                           "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "DC"]
        
        # Major cities to check for
        major_cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", 
                       "San Diego", "Dallas", "San Jose", "London", "Paris", "Tokyo", "Mumbai", "Sydney", 
                       "Singapore", "Hong Kong", "Dubai", "Toronto", "Mexico City"]
        
        # Check for match patterns
        us_state_matches = sum(1 for loc in locations if loc in us_states or loc in us_state_abbrevs)
        country_matches = sum(1 for loc in locations if loc in major_countries)
        city_matches = sum(1 for loc in locations if loc in major_cities or 
                          any(city in loc for city in major_cities))
        
        # Calculate percentages
        total = len(locations)
        us_state_pct = us_state_matches / total if total > 0 else 0
        country_pct = country_matches / total if total > 0 else 0
        city_pct = city_matches / total if total > 0 else 0
        
        # Determine type based on highest percentage
        if us_state_pct > 0.3:
            return "usa-states"
        elif country_pct > 0.3:
            return "country"
        else:
            return "city"
    
    # Detect map type based on data
    location_type = detect_location_type(location_data['location'])
    
    # Create map scope selection
    map_options = {
        "Global": "world", 
        "North America": "north america",
        "Europe": "europe",
        "Asia": "asia", 
        "USA": "usa"
    }
    
    geo_col1, geo_col2 = st.columns([3, 1])
    
    with geo_col2:
        st.markdown("""
        <div class="control-panel">
            <h3 style="font-size: 1.2rem; margin-top: 0;">Map Controls</h3>
        </div>
        """, unsafe_allow_html=True)
        
        selected_scope = st.selectbox(
            "Select Region",
            options=list(map_options.keys()),
            index=0 if location_type == "country" else 4
        )
        
        # Map visualization type
        map_viz_type = st.radio(
            "Visualization Type",
            options=["Bubble Map", "Choropleth"],
            index=0
        )
        
        # Animation option
        enable_animation = st.checkbox("Enable Animation", value=False)
        
        if enable_animation:
            animation_speed = st.slider("Animation Speed", 
                                       min_value=500, 
                                       max_value=2000, 
                                       value=1000,
                                       step=100)
        
        # Add download map button
        if st.button("📥 Download Map"):
            st.info("Map image would be downloaded (feature in development)")

    with geo_col1:
        scope = map_options[selected_scope]
        
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 12px;">
            <h2 style="font-size: 1.8rem; margin-bottom: 5px;">Global Viewership Map</h2>
            <p style="opacity: 0.8; font-size: 0.9rem;">Showing data for {scope.title()} region</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Determine appropriate settings based on location type and scope
        if location_type == "usa-states" and scope == "usa":
            projection = "albers usa"
            locationmode = "USA-states"
        elif scope == "world" or scope in ["europe", "asia", "north america"]:
            projection = "natural earth"
            locationmode = "country names" if location_type == "country" else "ISO-3"
        else:
            projection = "mercator"
            locationmode = "country names" if location_type == "country" else "ISO-3"
        
        # Create the appropriate map based on user selection
        if map_viz_type == "Bubble Map":
            # For bubble map (scatter geo)
            fig_map = px.scatter_geo(
                location_data,
                locationmode=locationmode,
                locations='location',
                size='viewers',
                color='viewers',
                color_continuous_scale=px.colors.sequential.Plasma,
                scope=scope,
                projection=projection,
                title='Global Viewership Distribution',
                hover_name='location',
                hover_data={
                    'location': False,
                    'viewers': True,
                },
                size_max=50,
                animation_frame='location' if enable_animation else None,
                animation_group='location' if enable_animation else None,
            )
            
            if enable_animation:
                fig_map.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = animation_speed
        
        else:
            # For choropleth map
            if scope == "usa":
                # US State level choropleth
                fig_map = px.choropleth(
                    location_data,
                    locationmode=locationmode,
                    locations='location',
                    color='viewers',
                    scope=scope,
                    color_continuous_scale=px.colors.sequential.Plasma,
                    title='Viewership Density by Region',
                    hover_name='location',
                    hover_data={
                        'location': False,
                        'viewers': True,
                    },
                )
            else:
                # Country level choropleth
                fig_map = px.choropleth(
                    location_data,
                    locationmode=locationmode,
                    locations='location',
                    color='viewers',
                    scope=scope,
                    color_continuous_scale=px.colors.sequential.Plasma,
                    projection=projection,
                    title='Global Viewership Density',
                    hover_name='location',
                    hover_data={
                        'location': False,
                        'viewers': True,
                    },
                )
        
        # Enhance map styling
        fig_map.update_geos(
            showcoastlines=True, coastlinecolor="white",
            showland=True, landcolor="rgb(17, 17, 17)",
            showocean=True, oceancolor="rgb(10, 10, 30)",
            showlakes=True, lakecolor="rgb(17, 17, 17)",
            showrivers=True, rivercolor="rgb(17, 17, 17)",
            showcountries=True, countrycolor="white",
            showsubunits=True, subunitcolor="white",
            resolution=110,
            bgcolor="rgba(0,0,0,0)"
        )
        
        # Improve layout
        fig_map.update_layout(
            height=600,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=30, b=0),
            coloraxis_colorbar=dict(
                title="Viewers",
                thicknessmode="pixels", thickness=20,
                lenmode="pixels", len=400,
                yanchor="top", y=1,
                ticks="outside"
            ),
            geo=dict(
                bgcolor="rgba(0,0,0,0)",
            )
        )
        
        # Add city labels for top cities if using bubble map
        if map_viz_type == "Bubble Map":
            top_locations = location_data.nlargest(5, 'viewers')
            for idx, row in top_locations.iterrows():
                fig_map.add_annotation(
                    x=row['location'],
                    text=f"{row['location']}: {row['viewers']}",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor="white",
                    font=dict(size=14, color="white"),
                    bordercolor="white",
                    borderwidth=2,
                    borderpad=4,
                    bgcolor="rgba(50, 50, 50, 0.7)",
                    opacity=0.8
                )
        
        # Add an interactive element
        st.plotly_chart(fig_map, use_container_width=True)
    
    # Summary metrics below the map
    st.markdown("### Viewer Distribution Analysis")
    
    # Add region-based analysis below the map
    col1, col2 = st.columns(2)
    
    with col1:
        # Create a simple text-based "Viewership Hotspots" dashboard
        st.markdown("### 📍 Viewership Hotspots")
        top_locations = location_data.nlargest(5, 'viewers')
        for idx, row in top_locations.iterrows():
            percentage = (row['viewers'] / location_data['viewers'].sum()) * 100
            st.markdown(f"""
            <div class="hotspot-card">
                <h4>{row['location']}</h4>
                <div class="progress-container">
                    <div class="progress-bar" style="width: {percentage}%"></div>
                </div>
                <span>{percentage:.1f}% of total</span>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Define regional mapping based on detected location type
        if location_type == "usa-states":
            # Regional mapping for US states
            region_mapping = {
                "New York": "Northeast", "Massachusetts": "Northeast", "Rhode Island": "Northeast", 
                "Connecticut": "Northeast", "Vermont": "Northeast", "New Hampshire": "Northeast", 
                "Maine": "Northeast", "Pennsylvania": "Northeast", "New Jersey": "Northeast",
                "California": "West", "Washington": "West", "Oregon": "West", "Nevada": "West", 
                "Idaho": "West", "Montana": "West", "Wyoming": "West", "Utah": "West", 
                "Colorado": "West", "Alaska": "West", "Hawaii": "West", "Arizona": "Southwest", 
                "New Mexico": "Southwest", "Texas": "Southwest", "Oklahoma": "Southwest",
                "Illinois": "Midwest", "Ohio": "Midwest", "Michigan": "Midwest", "Indiana": "Midwest", 
                "Wisconsin": "Midwest", "Minnesota": "Midwest", "Iowa": "Midwest", 
                "Missouri": "Midwest", "North Dakota": "Midwest", "South Dakota": "Midwest", 
                "Nebraska": "Midwest", "Kansas": "Midwest",
                "Florida": "Southeast", "Georgia": "Southeast", "North Carolina": "Southeast", 
                "South Carolina": "Southeast", "Virginia": "Southeast", "West Virginia": "Southeast", 
                "Kentucky": "Southeast", "Tennessee": "Southeast", "Alabama": "Southeast", 
                "Mississippi": "Southeast", "Arkansas": "Southeast", "Louisiana": "Southeast", 
                "Delaware": "Southeast", "Maryland": "Southeast", "District of Columbia": "Southeast",
                "NY": "Northeast", "MA": "Northeast", "RI": "Northeast", "CT": "Northeast", 
                "VT": "Northeast", "NH": "Northeast", "ME": "Northeast", "PA": "Northeast", 
                "NJ": "Northeast", "CA": "West", "WA": "West", "OR": "West", "NV": "West", 
                "ID": "West", "MT": "West", "WY": "West", "UT": "West", "CO": "West", 
                "AK": "West", "HI": "West", "AZ": "Southwest", "NM": "Southwest", 
                "TX": "Southwest", "OK": "Southwest", "IL": "Midwest", "OH": "Midwest", 
                "MI": "Midwest", "IN": "Midwest", "WI": "Midwest", "MN": "Midwest", 
                "IA": "Midwest", "MO": "Midwest", "ND": "Midwest", "SD": "Midwest", 
                "NE": "Midwest", "KS": "Midwest", "FL": "Southeast", "GA": "Southeast", 
                "NC": "Southeast", "SC": "Southeast", "VA": "Southeast", "WV": "Southeast", 
                "KY": "Southeast", "TN": "Southeast", "AL": "Southeast", "MS": "Southeast", 
                "AR": "Southeast", "LA": "Southeast", "DE": "Southeast", "MD": "Southeast", 
                "DC": "Southeast"
            }
            region_title = "US Regional Distribution"
        
        elif location_type == "country":
            # Regional mapping for countries
            region_mapping = {
                "United States": "North America", "Canada": "North America", "Mexico": "North America",
                "Brazil": "South America", "Argentina": "South America", "Chile": "South America", 
                "Colombia": "South America", "Peru": "South America", "Venezuela": "South America",
                "United Kingdom": "Europe", "France": "Europe", "Germany": "Europe", "Italy": "Europe", 
                "Spain": "Europe", "Portugal": "Europe", "Netherlands": "Europe", "Belgium": "Europe", 
                "Switzerland": "Europe", "Austria": "Europe", "Sweden": "Europe", "Norway": "Europe", 
                "Denmark": "Europe", "Finland": "Europe", "Greece": "Europe", "Ireland": "Europe",
                "Russia": "Europe", "Ukraine": "Europe", "Poland": "Europe", "Romania": "Europe",
                "China": "Asia", "Japan": "Asia", "South Korea": "Asia", "North Korea": "Asia", 
                "India": "Asia", "Pakistan": "Asia", "Bangladesh": "Asia", "Indonesia": "Asia", 
                "Thailand": "Asia", "Vietnam": "Asia", "Malaysia": "Asia", "Singapore": "Asia", 
                "Philippines": "Asia", "Taiwan": "Asia", "Hong Kong": "Asia",
                "Australia": "Oceania", "New Zealand": "Oceania", 
                "Egypt": "Africa", "South Africa": "Africa", "Nigeria": "Africa", "Kenya": "Africa", 
                "Morocco": "Africa", "Algeria": "Africa", "Tunisia": "Africa", "Ghana": "Africa",
                "Saudi Arabia": "Middle East", "UAE": "Middle East", "Qatar": "Middle East", 
                "Israel": "Middle East", "Turkey": "Middle East", "Iran": "Middle East"
            }
            region_title = "Continental Distribution"
        
        else:
            # Default city-to-region mapping
            region_mapping = {
                'New York': 'East Coast',
                'Boston': 'East Coast',
                'Philadelphia': 'East Coast',
                'Los Angeles': 'West Coast',
                'San Francisco': 'West Coast',
                'Seattle': 'West Coast',
                'Portland': 'West Coast',
                'Chicago': 'Midwest',
                'Detroit': 'Midwest',
                'Minneapolis': 'Midwest',
                'Houston': 'South',
                'Dallas': 'South',
                'Miami': 'South',
                'Atlanta': 'South',
                'Phoenix': 'Southwest',
                'Denver': 'Southwest',
                'Las Vegas': 'Southwest',
                'London': 'Europe',
                'Paris': 'Europe',
                'Berlin': 'Europe',
                'Rome': 'Europe',
                'Madrid': 'Europe',
                'Tokyo': 'Asia',
                'Seoul': 'Asia',
                'Beijing': 'Asia',
                'Shanghai': 'Asia',
                'Mumbai': 'Asia',
                'Sydney': 'Australia',
                'Melbourne': 'Australia',
                'Auckland': 'Australia',
                'Toronto': 'Canada',
                'Vancouver': 'Canada',
                'Montreal': 'Canada',
                'Mexico City': 'Latin America',
                'São Paulo': 'Latin America',
                'Buenos Aires': 'Latin America'
            }
            region_title = "Regional Distribution"
        
        # Create region comparison visualization
        st.markdown(f"### 🗺️ {region_title}")
        
        # Map locations to regions and handle unmapped locations
        location_data['region'] = location_data['location'].map(
            lambda x: region_mapping.get(x, 'Other')
        )
        
        # Aggregate by region
        region_data = location_data.groupby('region')['viewers'].sum().reset_index()
        
        # Create a simple horizontal bar chart for regions
        fig_regions = px.bar(
            region_data.sort_values('viewers', ascending=True),
            y='region',
            x='viewers',
            orientation='h',
            color='viewers',
            color_continuous_scale=px.colors.sequential.Viridis,
            title=region_title
        )
        
        fig_regions.update_layout(
            height=300,
            xaxis_title="Number of Viewers",
            yaxis_title=None,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            margin=dict(l=0, r=0, t=30, b=0),
        )
        
        st.plotly_chart(fig_regions, use_container_width=True)
    
    # Trending Shows
    st.markdown("""
    <div style="margin: 30px 0 20px 0;">
        <h2 style="font-size: 1.8rem; margin-bottom: 15px; font-weight: 600;">🔥 Trending Content</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a safer aggregation that doesn't rely on user_id
    agg_dict = {
        'watch_time': 'mean',
        'is_completed': lambda x: x.astype(int).mean()
    }
    
    # Add a count metric (using a column we know exists)
    count_col = 'content_id'  # This column definitely exists since we're grouping by it
    
    trending_shows = df.groupby('content_id').agg(agg_dict)
    # Add count separately
    trending_shows['count'] = df.groupby('content_id').size()
    
    # Sort and get top 5
    trending_shows = trending_shows.sort_values('watch_time', ascending=False).head(5)
    
    # Create a row of trending cards
    trend_cols = st.columns(5)
    
    # Choose colors for each card
    card_colors = [
        "linear-gradient(135deg, #8E2DE2 0%, #4A00E0 100%)",
        "linear-gradient(135deg, #43CBFF 0%, #9708CC 100%)",
        "linear-gradient(135deg, #FDD819 0%, #E80505 100%)",
        "linear-gradient(135deg, #00C9FF 0%, #92FE9D 100%)",
        "linear-gradient(135deg, #FC466B 0%, #3F5EFB 100%)"
    ]
    
    # Icons for metrics
    icons = {
        "viewers": "👁️",
        "watch_time": "⏱️",
        "completion": "✅"
    }
    
    for idx, (show, col) in enumerate(zip(trending_shows.index, trend_cols)):
        with col:
            st.markdown(f"""
            <div style="background: {card_colors[idx % len(card_colors)]}; border-radius: 12px; padding: 1rem; height: 220px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);">
                <div>
                    <h3 style="font-size: 1.2rem; margin-bottom: 10px; color: white; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{show}</h3>
                    <div style="width: 100%; height: 3px; background: rgba(255,255,255,0.3); margin: 8px 0;"></div>
                </div>
                <div>
                    <div style="margin: 7px 0;">
                        <span style="font-size: 0.8rem; opacity: 0.9;">{icons["viewers"]} Viewers</span>
                        <div style="font-size: 1.2rem; font-weight: 600;">{trending_shows.loc[show, 'count']:,.0f}</div>
                    </div>
                    <div style="margin: 7px 0;">
                        <span style="font-size: 0.8rem; opacity: 0.9;">{icons["watch_time"]} Avg. Watch</span>
                        <div style="font-size: 1.2rem; font-weight: 600;">{trending_shows.loc[show, 'watch_time']:.1f} min</div>
                    </div>
                    <div style="margin: 7px 0;">
                        <span style="font-size: 0.8rem; opacity: 0.9;">{icons["completion"]} Completion</span>
                        <div style="font-size: 1.2rem; font-weight: 600;">{trending_shows.loc[show, 'is_completed']*100:.1f}%</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Warning for high drop-off
    if completion_rate < 40:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(255, 95, 109, 0.3) 0%, rgba(255, 195, 113, 0.3) 100%); border-radius: 12px; padding: 1rem; margin: 1.5rem 0; border-left: 4px solid #FF5F6D; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);">
            <h3 style="display: flex; align-items: center; font-size: 1.2rem; margin-bottom: 0.5rem;">
                <span style="margin-right: 10px; font-size: 1.5rem;">⚠️</span> Alert: Low Completion Rate
            </h3>
            <p>Overall completion rate is below 40%. Consider analyzing content quality and user experience.</p>
        </div>
        """, unsafe_allow_html=True)
        
    # Update footer
    st.markdown("""
    <div style="margin-top: 3rem; padding-top: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.1); text-align: center; color: rgba(255, 255, 255, 0.5);">
        <p>OTT Analytics Dashboard | Created with Streamlit | Data refreshes every 10 seconds when auto-refresh is enabled</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("👆 Please upload a compatible dataset using the sidebar to view analytics.", icon="ℹ️") 