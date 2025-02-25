"""
Dashboard Components for TRILOGY Brain Terminal

Provides specialized dashboard widgets for the terminal interface.
"""
import streamlit as st
from typing import Dict, Any, List, Optional
from datetime import datetime

class SystemMonitor:
    """Terminal-styled system resource monitor component"""
    
    def __init__(self, theme_colors: Dict[str, str]):
        self.theme_colors = theme_colors
        self._setup_css()
    
    def _setup_css(self):
        st.markdown(f"""
        <style>
        .sys-monitor {{
            background-color: {self.theme_colors["background"]};
            border: 1px solid {self.theme_colors["primary"]};
            border-radius: 4px;
            padding: 10px;
            font-family: 'Courier New', monospace;
            margin-bottom: 15px;
        }}
        
        .sys-monitor-title {{
            color: {self.theme_colors["primary"]};
            font-weight: bold;
            border-bottom: 1px solid {self.theme_colors["primary"]};
            padding-bottom: 5px;
            margin-bottom: 10px;
            font-size: 14px;
            text-transform: uppercase;
        }}
        
        .sys-monitor-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
        }}
        
        .sys-monitor-metric {{
            text-align: center;
            padding: 8px;
            background-color: rgba(0,0,0,0.3);
            border-radius: 4px;
        }}
        
        .sys-monitor-value {{
            font-size: 24px;
            font-weight: bold;
            color: {self.theme_colors["primary"]};
        }}
        
        .sys-monitor-label {{
            font-size: 12px;
            opacity: 0.8;
        }}
        
        .sys-monitor-badge {{
            display: inline-block;
            padding: 3px 6px;
            border-radius: 10px;
            font-size: 10px;
            margin-left: 5px;
        }}
        
        .sys-monitor-badge-success {{
            background-color: rgba(0, 255, 0, 0.2);
            color: #00ff00;
        }}
        
        .sys-monitor-badge-warning {{
            background-color: rgba(255, 255, 0, 0.2);
            color: #ffff00;
        }}
        
        .sys-monitor-badge-error {{
            background-color: rgba(255, 0, 0, 0.2);
            color: #ff4444;
        }}
        </style>
        """, unsafe_allow_html=True)
    
    def render_system_metrics(self, metrics: List[Dict[str, Any]]):
        """
        Render system metrics in a grid
        
        Args:
            metrics: List of metrics with value, label, status (optional)
        """
        st.markdown("""
        <div class="sys-monitor">
            <div class="sys-monitor-title">System Monitor</div>
            <div class="sys-monitor-grid">
        """, unsafe_allow_html=True)
        
        for metric in metrics:
            status_badge = ""
            if "status" in metric:
                status_class = f"sys-monitor-badge-{metric['status']}"
                status_badge = f'<span class="sys-monitor-badge {status_class}">{metric["status"]}</span>'
                
            st.markdown(f"""
            <div class="sys-monitor-metric">
                <div class="sys-monitor-value">{metric["value"]}{status_badge}</div>
                <div class="sys-monitor-label">{metric["label"]}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div></div>", unsafe_allow_html=True)

class TerminalLog:
    """Terminal-styled log display component"""
    
    def __init__(self, theme_colors: Dict[str, str]):
        self.theme_colors = theme_colors
        self._setup_css()
    
    def _setup_css(self):
        st.markdown(f"""
        <style>
        .term-log {{
            background-color: {self.theme_colors["background"]};
            border: 1px solid {self.theme_colors["primary"]};
            border-radius: 4px;
            padding: 10px;
            font-family: 'Courier New', monospace;
            height: 300px;
            overflow-y: auto;
            margin-bottom: 15px;
        }}
        
        .term-log-title {{
            color: {self.theme_colors["primary"]};
            font-weight: bold;
            border-bottom: 1px solid {self.theme_colors["primary"]};
            padding-bottom: 5px;
            margin-bottom: 10px;
            font-size: 14px;
            text-transform: uppercase;
            display: flex;
            justify-content: space-between;
        }}
        
        .term-log-entry {{
            margin-bottom: 5px;
            font-size: 12px;
            line-height: 1.4;
            white-space: pre-wrap;
            word-break: break-word;
        }}
        
        .term-log-time {{
            color: #888;
            margin-right: 8px;
        }}
        
        .term-log-info {{
            color: {self.theme_colors["text"]};
        }}
        
        .term-log-warning {{
            color: #ffcc00;
        }}
        
        .term-log-error {{
            color: #ff4444;
        }}
        
        .term-log-success {{
            color: #00ff00;
        }}
        </style>
        """, unsafe_allow_html=True)
    
    def render_log(self, log_entries: List[Dict[str, Any]], title: str = "System Log"):
        """
        Render terminal log
        
        Args:
            log_entries: List of log entries with timestamp, level, message
            title: Log title
        """
        st.markdown(f"""
        <div class="term-log">
            <div class="term-log-title">
                <span>{title}</span>
                <span>{datetime.now().strftime('%H:%M:%S')}</span>
            </div>
        """, unsafe_allow_html=True)
        
        for entry in log_entries:
            level = entry.get("level", "info").lower()
            timestamp = entry.get("timestamp", datetime.now().strftime("%H:%M:%S"))
            message = entry.get("message", "")
            
            st.markdown(f"""
            <div class="term-log-entry">
                <span class="term-log-time">[{timestamp}]</span>
                <span class="term-log-{level}">{message}</span>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

class ActiveProcesses:
    """Terminal-styled active processes component"""
    
    def __init__(self, theme_colors: Dict[str, str]):
        self.theme_colors = theme_colors
        self._setup_css()
    
    def _setup_css(self):
        st.markdown(f"""
        <style>
        .processes {{
            background-color: {self.theme_colors["background"]};
            border: 1px solid {self.theme_colors["primary"]};
            border-radius: 4px;
            padding: 10px;
            font-family: 'Courier New', monospace;
            margin-bottom: 15px;
        }}
        
        .processes-title {{
            color: {self.theme_colors["primary"]};
            font-weight: bold;
            border-bottom: 1px solid {self.theme_colors["primary"]};
            padding-bottom: 5px;
            margin-bottom: 10px;
            font-size: 14px;
            text-transform: uppercase;
        }}
        
        .processes-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
        }}
        
        .processes-table th {{
            text-align: left;
            padding: 5px;
            color: {self.theme_colors["primary"]};
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        
        .processes-table td {{
            padding: 5px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}
        
        .processes-table tr:last-child td {{
            border-bottom: none;
        }}
        
        .processes-status {{
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 5px;
        }}
        
        .processes-status-active {{
            background-color: #00ff00;
            box-shadow: 0 0 5px #00ff00;
        }}
        
        .processes-status-idle {{
            background-color: #ffcc00;
        }}
        
        .processes-status-stopped {{
            background-color: #ff4444;
        }}
        
        .processes-progress {{
            height: 5px;
            background-color: rgba(255,255,255,0.1);
            border-radius: 3px;
            overflow: hidden;
            margin-top: 3px;
        }}
        
        .processes-progress-bar {{
            height: 100%;
            background-color: {self.theme_colors["primary"]};
        }}
        </style>
        """, unsafe_allow_html=True)
    
    def render_processes(self, processes: List[Dict[str, Any]], title: str = "Active Processes"):
        """
        Render active processes
        
        Args:
            processes: List of processes with name, status, cpu, memory, progress
            title: Component title
        """
        st.markdown(f"""
        <div class="processes">
            <div class="processes-title">{title}</div>
            <table class="processes-table">
                <tr>
                    <th>Process</th>
                    <th>Status</th>
                    <th>CPU</th>
                    <th>Memory</th>
                    <th>Progress</th>
                </tr>
        """, unsafe_allow_html=True)
        
        for proc in processes:
            name = proc.get("name", "Unknown")
            status = proc.get("status", "active")
            cpu = proc.get("cpu", "0%")
            memory = proc.get("memory", "0MB")
            progress = proc.get("progress", 0)
            
            st.markdown(f"""
            <tr>
                <td>
                    <span class="processes-status processes-status-{status}"></span>
                    {name}
                </td>
                <td>{status}</td>
                <td>{cpu}</td>
                <td>{memory}</td>
                <td>
                    <div class="processes-progress">
                        <div class="processes-progress-bar" style="width: {progress}%;"></div>
                    </div>
                </td>
            </tr>
            """, unsafe_allow_html=True)
            
        st.markdown("</table></div>", unsafe_allow_html=True) 