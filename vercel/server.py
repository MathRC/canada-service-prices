import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import geopandas as gpd
from pathlib import Path
import os

# Load processed data - updated paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
aespi = pd.read_csv(os.path.join(BASE_DIR, "data/processed/aespi_clean.csv"))

# Load and preprocess regions
regions = gpd.read_file(os.path.join(BASE_DIR, "data/processed/canada_regions.geojson"))
regions = regions.to_crs(epsg=4326)
regions['geometry'] = regions.geometry.clip_by_rect(-141, 41.7, -52.6, 83.1)
regions['geometry'] = regions.geometry.simplify(0.02)

# Convert dates
aespi['Date'] = pd.to_datetime(aespi['Date'])
aespi['Year'] = aespi['Date'].dt.year
all_dates = aespi['Date'].unique()
min_date = min(all_dates)
max_date = max(all_dates)

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Canadian Architectural & Engineering Services Price Index"),
    
    html.Div([
        # Region Selector
        html.Div([
            html.Label("Select Regions:", className="filter-label"),
            dcc.Dropdown(
                id='region-selector',
                options=[{'label': r, 'value': r} for r in sorted(aespi['Region'].unique())],
                value=['Canada', 'Ontario', 'Quebec'],
                multi=True,
                className="dropdown"
            )
        ], className="filter-column"),
        
        # Service Selector
        html.Div([
            html.Label("Select Service Category:", className="filter-label"),
            dcc.Dropdown(
                id='service-selector',
                options=[{'label': s, 'value': s} for s in sorted(aespi['Service Category'].unique())],
                value=aespi['Service Category'].unique()[0],
                multi=False,
                className="dropdown"
            )
        ], className="filter-column"),
        
            # Date Range Slider
            html.Div([
                html.Label("Date Range:", className="filter-label"),
                dcc.RangeSlider(
                    id='date-slider',
                    min=int(min_date.timestamp()),
                    max=int(max_date.timestamp()),
                    value=[int(min_date.timestamp()), int(max_date.timestamp())],
                    marks={
                        int(pd.Timestamp(year=y, month=1, day=1).timestamp()): {'label': str(y)}
                        for y in range(min_date.year, max_date.year + 1)
                    },
                    step=86400,  # 1-day precision
                    tooltip=None,
                    className="slider"
                )
            ], className="filter-column")
    ], className="filters-row"),
    
    dcc.Graph(id='time-series-plot', className="graph-container"),
    html.Div([
        dcc.Graph(id='choropleth-plot', className="graph-container"),
        dcc.Graph(id='change-plot', className="graph-container")
    ], className="row")
], className="dashboard-container")

@app.callback(
    Output('time-series-plot', 'figure'),
    [Input('region-selector', 'value'),
     Input('service-selector', 'value'),
     Input('date-slider', 'value')]
)
def update_time_series(selected_regions, selected_service, timestamp_range):
    start_date = pd.to_datetime(timestamp_range[0], unit='s')
    end_date = pd.to_datetime(timestamp_range[1], unit='s')
    
    filtered = aespi[
        (aespi['Region'].isin(selected_regions)) & 
        (aespi['Service Category'] == selected_service) &
        (aespi['Date'].between(start_date, end_date))
    ]
    
    if filtered.empty:
        return px.line(title="No data available for selected filters")
    
    fig = px.line(filtered, x='Date', y='Index Value', color='Region',
                 title=f"<b>{selected_service}</b> Price Trends Over Time")
    fig.update_layout(
        hovermode="x unified",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

@app.callback(
    Output('choropleth-plot', 'figure'),
    [Input('service-selector', 'value'),
     Input('date-slider', 'value')]
)
def update_choropleth(selected_service, timestamp_range):
    start_date = pd.to_datetime(timestamp_range[0], unit='s')
    end_date = pd.to_datetime(timestamp_range[1], unit='s')
    
    filtered = aespi[
        (aespi['Service Category'] == selected_service) &
        (aespi['Date'].between(start_date, end_date))
    ]
    
    if filtered.empty:
        return px.choropleth(title="No data available for selected filters")
    
    regional_avg = filtered.groupby('Region')['Index Value'].mean().reset_index()
    merged = regions.merge(regional_avg, left_on='region', right_on='Region')
    
    fig = px.choropleth(
        merged,
        geojson=merged.geometry.__geo_interface__,
        locations=merged.index,
        color='Index Value',
        hover_name='region',
        title=f"<b>{selected_service}</b> Regional Averages",
        color_continuous_scale='Viridis',
        height=500
    )
    fig.update_geos(
        visible=False,
        projection_type="conic conformal",
        projection_rotation=dict(lon=-95, lat=60),
        lataxis_range=[40, 70],
        lonaxis_range=[-140, -50]
    )
    fig.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

@app.callback(
    Output('change-plot', 'figure'),
    [Input('region-selector', 'value'),
     Input('service-selector', 'value'),
     Input('date-slider', 'value')]
)
def update_change_plot(selected_regions, selected_service, timestamp_range):
    start_date = pd.to_datetime(timestamp_range[0], unit='s')
    end_date = pd.to_datetime(timestamp_range[1], unit='s')
    
    filtered = aespi[
        (aespi['Region'].isin(selected_regions)) & 
        (aespi['Service Category'] == selected_service) &
        (aespi['Date'].between(start_date, end_date))
    ]
    
    if filtered.empty:
        return px.bar(title="No data available for selected filters")
    
    annual_avg = filtered.groupby(['Region', 'Year'])['Index Value'].mean().reset_index()
    annual_avg['Yearly Change (%)'] = annual_avg.groupby('Region')['Index Value'].pct_change() * 100
    
    fig = px.bar(annual_avg.dropna(),
                x='Year', y='Yearly Change (%)',
                color='Region',
                barmode='group',
                title="<b>Annual Percentage Changes</b>",
                text_auto='.2f')
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside")
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
