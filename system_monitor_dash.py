#!/usr/bin/env python3

import psutil
from datetime import datetime
import logging
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

# Set up logging
logging.basicConfig(
    filename='system_metrics.log',
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

app = Dash(__name__)

# Initial state for logging toggle
logging_on = True

# Dashboard layout
app.layout = html.Div([
    html.H1("System Resource Monitor"),
    html.Div(id='alert-banner', style={'color': 'red', 'fontWeight': 'bold'}),
    dcc.Graph(id='live-graph'),
    html.Table(id='data-table', style={'width': '100%', 'borderCollapse': 'collapse'}),
    html.Button('Toggle Logging', id='toggle-button', n_clicks=0),
    html.Div(id='logging-status'),
    dcc.Interval(id='interval-component', interval=5*1000, n_intervals=0)  # 5 seconds
])

# Data storage
data_points = []

def get_metrics():
    """Fetch system metrics with error handling."""
    try:
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return {'timestamp': timestamp, 'CPU': cpu, 'Memory': memory, 'Disk': disk}
    except Exception as e:
        logger.error(f"Error fetching metrics: {e}")
        return None

# Callback to update graph, table, and alerts
@app.callback(
    [Output('live-graph', 'figure'),
     Output('data-table', 'children'),
     Output('alert-banner', 'children')],
    Input('interval-component', 'n_intervals')
)
def update_dashboard(n):
    global data_points, logging_on
    metrics = get_metrics()
    
    if metrics and logging_on:
        data_points.append(metrics)
        logger.info(f"CPU: {metrics['CPU']}%, Memory: {metrics['Memory']}%, Disk: {metrics['Disk']}%")
    
    # Limit data points to last 20 for performance
    if len(data_points) > 20:
        data_points.pop(0)
    
    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[d['timestamp'] for d in data_points],
        y=[d['CPU'] for d in data_points],
        name='CPU',
        mode='lines+markers',
        hovertemplate='%{y:.1f}% @ %{x}<br>'
    ))
    fig.add_trace(go.Scatter(
        x=[d['timestamp'] for d in data_points],
        y=[d['Memory'] for d in data_points],
        name='Memory',
        mode='lines+markers',
        hovertemplate='%{y:.1f}% @ %{x}<br>'
    ))
    fig.add_trace(go.Scatter(
        x=[d['timestamp'] for d in data_points],
        y=[d['Disk'] for d in data_points],
        name='Disk',
        mode='lines+markers',
        hovertemplate='%{y:.1f}% @ %{x}<br>'
    ))
    fig.update_layout(
        title='System Resources',
        xaxis_title='Time',
        yaxis_title='Usage (%)',
        yaxis_range=[0, 100]
    )

    # Create table
    table = [
        html.Tr([html.Th(col) for col in ['Timestamp', 'CPU (%)', 'Memory (%)', 'Disk (%)']]),
        *[html.Tr([html.Td(d[col]) for col in ['timestamp', 'CPU', 'Memory', 'Disk']]) for d in data_points[-5:]]  # Last 5 entries
    ]

    # Check for alerts
    alert = ''
    if metrics:
        if metrics['CPU'] > 90:
            alert = 'ALERT: CPU Usage > 90%'
        elif metrics['Memory'] > 90:
            alert = 'ALERT: Memory Usage > 90%'
        elif metrics['Disk'] > 95:
            alert = 'ALERT: Disk Usage > 95%'

    return fig, table, alert

# Callback for toggling logging
@app.callback(
    Output('logging-status', 'children'),
    Input('toggle-button', 'n_clicks')
)
def toggle_logging(n_clicks):
    global logging_on
    logging_on = not logging_on
    logger.info(f"Logging toggled to {'ON' if logging_on else 'OFF'}")
    return f"Logging: {'ON' if logging_on else 'OFF'}"

if __name__ == '__main__':
    app.run(debug=True)