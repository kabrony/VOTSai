"""
Dashboard UI Component for TRILOGY Brain

Provides terminal-styled dashboard widgets and visualizations.
"""
import streamlit as st
from typing import Dict, Any, List, Optional
from datetime import datetime

class DashboardComponent:
    """
    Terminal-styled dashboard component for system monitoring
    
    Features:
    - System status widgets
    - Resource monitors
    - Activity logs
    - Terminal styling
    """
    
    def __init__(self, 
                theme_colors: Optional[Dict[str, str]] = None,
                dashboard_id: str = "main"):
        """
        Initialize the dashboard component
        
        Args:
            theme_colors: Dictionary with primary, background, and text colors
            dashboard_id: Unique ID for this dashboard instance
        """
        self.theme_colors = theme_colors or {
            "primary": "#00ff41",
            "background": "#0d0d0d",
            "text": "#00ff41"
        }
        self.dashboard_id = dashboard_id
        self._setup_css()
        
    def _setup_css(self):
        """Initialize dashboard CSS"""
        st.markdown(f"""
        <style>
        .system-dashboard-{self.dashboard_id} {{
            background-color: {self.theme_colors["background"]};
            border: 1px solid {self.theme_colors["primary"]};
            border-radius: 6px;
            padding: 15px;
            font-family: 'Courier New', monospace;
            color: {self.theme_colors["text"]};
            position: relative;
            margin-bottom: 20px;
            box-shadow: 0 0 15px rgba(0, 255, 65, 0.3);
            overflow: hidden;
        }}
        
        .dashboard-header-{self.dashboard_id} {{
            border-bottom: 1px solid {self.theme_colors["primary"]};
            padding-bottom: 10px;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-between;
        }}
        
        .dashboard-title-{self.dashboard_id} {{
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        .dashboard-controls-{self.dashboard_id} {{
            display: flex;
        }}
        
        .dashboard-content-{self.dashboard_id} {{
            position: relative;
        }}
        
        .widget-container-{self.dashboard_id} {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin-top: 10px;
        }}
        
        .widget-{self.dashboard_id} {{
            background-color: rgba(0, 0, 0, 0.3);
            border: 1px solid {self.theme_colors["primary"]};
            border-radius: 4px;
            padding: 10px;
            flex: 1;
            min-width: 200px;
        }}
        
        .widget-title-{self.dashboard_id} {{
            font-size: 14px;
            text-transform: uppercase;
            margin-bottom: 10px;
            color: {self.theme_colors["primary"]};
            border-bottom: 1px solid {self.theme_colors["primary"]};
            padding-bottom: 5px;
        }}
        
        .widget-content-{self.dashboard_id} {{
            font-size: 13px;
            line-height: 1.4;
        }}
        
        .progress-bar-{self.dashboard_id} {{
            height: 15px;
            background-color: rgba(0, 255, 65, 0.1);
            margin-bottom: 10px;
            position: relative;
        }}
        
        .progress-bar-fill-{self.dashboard_id} {{
            height: 100%;
            background-color: {self.theme_colors["primary"]};
            transition: width 0.5s ease-in-out;
        }}
        
        .progress-bar-text-{self.dashboard_id} {{
            position: absolute;
            top: 0;
            right: 5px;
            font-size: 12px;
            line-height: 15px;
        }}
        
        /* Terminal-style grid background */
        .system-dashboard-{self.dashboard_id}::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                linear-gradient(rgba(0, 255, 65, 0.1) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 65, 0.1) 1px, transparent 1px);
            background-size: 20px 20px;
            z-index: -1;
            opacity: 0.2;
            pointer-events: none;
        }}
        
        /* Log styling */
        .log-container-{self.dashboard_id} {{
            font-family: 'Courier New', monospace;
            font-size: 12px;
            line-height: 1.4;
            max-height: 200px;
            overflow-y: auto;
            background-color: rgba(0, 0, 0, 0.5);
            padding: 5px;
            border-radius: 3px;
        }}
        
        .log-entry-{self.dashboard_id} {{
            margin-bottom: 3px;
            border-bottom: 1px solid rgba(0, 255, 65, 0.1);
            padding-bottom: 3px;
        }}
        
        .log-timestamp-{self.dashboard_id} {{
            color: #888;
            margin-right: 5px;
        }}
        
        .log-level-info-{self.dashboard_id} {{
            color: {self.theme_colors["text"]};
        }}
        
        .log-level-warning-{self.dashboard_id} {{
            color: #ffcc00;
        }}
        
        .log-level-error-{self.dashboard_id} {{
            color: #ff5f56;
        }}
        </style>
        """, unsafe_allow_html=True)
        
    def render_dashboard(self, title: str = "SYSTEM MONITOR"):
        """
        Render the dashboard container
        
        Args:
            title: Title for the dashboard
            
        Returns:
            Dashboard content container
        """
        # Dashboard container
        st.markdown(f"""
        <div class="system-dashboard-{self.dashboard_id}">
            <div class="dashboard-header-{self.dashboard_id}">
                <div class="dashboard-title-{self.dashboard_id}">{title}</div>
                <div class="dashboard-controls-{self.dashboard_id}">
                    <span style="margin-right: 10px;">⚡ LIVE</span>
                    <span>{datetime.now().strftime('%H:%M:%S')}</span>
                </div>
            </div>
            <div class="dashboard-content-{self.dashboard_id}" id="dashboard-content-{self.dashboard_id}">
                <!-- Dashboard content goes here -->
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Return a container for the dashboard content
        return st.container()
    
    def render_widget_row(self, num_widgets: int = 3):
        """
        Render a row of widgets
        
        Args:
            num_widgets: Number of widgets in the row
            
        Returns:
            List of containers for each widget
        """
        st.markdown(f'<div class="widget-container-{self.dashboard_id}" id="widget-row-{id(self)}"></div>', unsafe_allow_html=True)
        
        # Create columns for each widget
        return st.columns(num_widgets)
    
    def render_widget(self, 
                     title: str, 
                     content: str = "",
                     progress: Optional[float] = None,
                     progress_text: Optional[str] = None,
                     container: Optional[Any] = None):
        """
        Render a dashboard widget
        
        Args:
            title: Widget title
            content: Widget HTML content
            progress: Optional progress value (0-100)
            progress_text: Optional text to show on progress bar
            container: Optional container to render the widget in
        """
        # Create widget HTML
        widget_html = f"""
        <div class="widget-{self.dashboard_id}">
            <div class="widget-title-{self.dashboard_id}">{title}</div>
        """
        
        # Add progress bar if specified
        if progress is not None:
            progress_width = max(0, min(100, progress))
            widget_html += f"""
            <div class="progress-bar-{self.dashboard_id}">
                <div class="progress-bar-fill-{self.dashboard_id}" style="width: {progress_width}%;"></div>
                <div class="progress-bar-text-{self.dashboard_id}">{progress_text or f"{progress_width:.1f}%"}</div>
            </div>
            """
            
        # Add content and close widget
        widget_html += f"""
            <div class="widget-content-{self.dashboard_id}">{content}</div>
        </div>
        """
        
        # Render in the appropriate container
        if container:
            container.markdown(widget_html, unsafe_allow_html=True)
        else:
            st.markdown(widget_html, unsafe_allow_html=True)
    
    def render_log_widget(self, 
                         title: str, 
                         logs: List[Dict[str, Any]],
                         container: Optional[Any] = None):
        """
        Render a log widget with entries
        
        Args:
            title: Widget title
            logs: List of log entries with timestamp, level, and message
            container: Optional container to render the widget in
        """
        # Start widget HTML
        widget_html = f"""
        <div class="widget-{self.dashboard_id}">
            <div class="widget-title-{self.dashboard_id}">{title}</div>
            <div class="log-container-{self.dashboard_id}">
        """
        
        # Add log entries
        for log in logs:
            timestamp = log.get("timestamp", datetime.now().strftime("%H:%M:%S"))
            level = log.get("level", "info").lower()
            message = log.get("message", "")
            
            widget_html += f"""
            <div class="log-entry-{self.dashboard_id}">
                <span class="log-timestamp-{self.dashboard_id}">[{timestamp}]</span>
                <span class="log-level-{level}-{self.dashboard_id}">{message}</span>
            </div>
            """
            
        # Close widget
        widget_html += """
            </div>
        </div>
        """
        
        # Render in the appropriate container
        if container:
            container.markdown(widget_html, unsafe_allow_html=True)
        else:
            st.markdown(widget_html, unsafe_allow_html=True)
    
    def render_ascii_chart(self, 
                          title: str, 
                          data: List[float], 
                          labels: List[str] = None,
                          container: Optional[Any] = None):
        """
        Render a simple ASCII bar chart
        
        Args:
            title: Chart title
            data: List of values
            labels: Optional list of labels (defaults to indices)
            container: Optional container to render the chart in
        """
        if not data:
            return
            
        # Generate labels if not provided
        if not labels:
            labels = [str(i) for i in range(len(data))]
            
        # Normalize data to fit in display
        max_value = max(data)
        max_bar_width = 20
        
        # Create ASCII chart
        chart = ""
        for i, value in enumerate(data):
            bar_width = int((value / max_value) * max_bar_width) if max_value > 0 else 0
            label = labels[i] if i < len(labels) else str(i)
            
            # Pad label to align bars
            padded_label = label.ljust(10)
            
            # Add bar with value
            chart += f"{padded_label} | {'█' * bar_width} {value:.2f}\n"
            
        # Create widget with the chart
        widget_html = f"""
        <div class="widget-{self.dashboard_id}">
            <div class="widget-title-{self.dashboard_id}">{title}</div>
            <div class="widget-content-{self.dashboard_id}">
                <pre>{chart}</pre>
            </div>
        </div>
        """
        
        # Render in the appropriate container
        if container:
            container.markdown(widget_html, unsafe_allow_html=True)
        else:
            st.markdown(widget_html, unsafe_allow_html=True)
    
    def set_theme(self, theme_colors: Dict[str, str]):
        """
        Update the dashboard theme colors
        
        Args:
            theme_colors: Dictionary with primary, background, and text colors
        """
        self.theme_colors = theme_colors
        self._setup_css() 