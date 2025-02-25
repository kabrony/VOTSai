"""
Visualizations Component for TRILOGY Brain

Provides terminal-styled data visualizations for analytics.
"""
import streamlit as st
from typing import Dict, Any, List, Optional
import json

class VisualizationsComponent:
    """
    Terminal-styled visualizations for data representation
    
    Features:
    - ASCII charts and graphs
    - Matrix-styled data visualizations
    - Terminal-themed Plotly wrappers
    """
    
    def __init__(self, 
                theme_colors: Optional[Dict[str, str]] = None,
                component_id: str = "viz"):
        """
        Initialize the visualizations component
        
        Args:
            theme_colors: Dictionary with primary, background, and text colors
            component_id: Unique ID for this component instance
        """
        self.theme_colors = theme_colors or {
            "primary": "#00ff41",
            "background": "#0d0d0d",
            "text": "#00ff41"
        }
        self.component_id = component_id
        self._setup_css()
    
    def _setup_css(self):
        """Initialize visualizations CSS"""
        st.markdown(f"""
        <style>
        .viz-container-{self.component_id} {{
            background-color: {self.theme_colors["background"]};
            border: 1px solid {self.theme_colors["primary"]};
            border-radius: 6px;
            padding: 15px;
            font-family: 'Courier New', monospace;
            color: {self.theme_colors["text"]};
            margin-bottom: 20px;
            position: relative;
            overflow: hidden;
        }}
        
        .viz-title-{self.component_id} {{
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 15px;
            padding-bottom: 5px;
            border-bottom: 1px solid {self.theme_colors["primary"]};
        }}
        
        .viz-content-{self.component_id} {{
            overflow-x: auto;
        }}
        
        /* ASCII visualization styles */
        .ascii-chart-{self.component_id} {{
            font-family: monospace;
            white-space: pre;
            line-height: 1.2;
            font-size: 14px;
        }}
        
        /* Terminal grid background */
        .viz-container-{self.component_id}::before {{
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
        
        /* Node-link graph styles */
        .node-{self.component_id} {{
            fill: {self.theme_colors["primary"]};
            stroke: rgba(255, 255, 255, 0.7);
            stroke-width: 1px;
        }}
        
        .link-{self.component_id} {{
            stroke: rgba(0, 255, 65, 0.5);
            stroke-opacity: 0.6;
        }}
        
        .node-label-{self.component_id} {{
            font-family: monospace;
            font-size: 10px;
            fill: white;
            pointer-events: none;
        }}
        </style>
        """, unsafe_allow_html=True)
    
    def render_ascii_bar_chart(self, 
                              title: str, 
                              values: List[float], 
                              labels: List[str],
                              max_width: int = 40):
        """
        Render an ASCII bar chart
        
        Args:
            title: Chart title
            values: List of values for bars
            labels: List of labels for bars
            max_width: Maximum width of bars in characters
        """
        if not values or not labels:
            st.warning("No data to display")
            return
            
        # Create ASCII chart
        chart = self._generate_ascii_bar_chart(values, labels, max_width, title)
        
        # Render container
        st.markdown(f"""
        <div class="viz-container-{self.component_id}">
            <div class="viz-title-{self.component_id}">{title}</div>
            <div class="viz-content-{self.component_id}">
                <div class="ascii-chart-{self.component_id}">
                    <pre>{chart}</pre>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def _generate_ascii_bar_chart(self, 
                                 values: List[float], 
                                 labels: List[str], 
                                 max_width: int = 40, 
                                 title: str = ""):
        """
        Generate ASCII bar chart text
        
        Args:
            values: List of values for bars
            labels: List of labels for bars
            max_width: Maximum width of bars in characters
            title: Chart title
            
        Returns:
            ASCII chart text
        """
        if not values:
            return "No data available"
            
        max_value = max(values)
        max_label_len = max(len(label) for label in labels)
        
        # Create chart header
        header = f"{'=' * (max_label_len + max_width + 10)}\n"
        header += f"{title.center(max_label_len + max_width + 10)}\n"
        header += f"{'=' * (max_label_len + max_width + 10)}\n\n"
        
        # Create bars
        chart = header
        for i, (value, label) in enumerate(zip(values, labels)):
            # Calculate bar width proportional to value
            bar_width = int((value / max_value) * max_width) if max_value > 0 else 0
            
            # Format the label with padding to align bars
            padded_label = label.ljust(max_label_len)
            
            # Add bar with value
            chart += f"{padded_label} │{'█' * bar_width} {value:.2f}\n"
        
        return chart
    
    def render_force_directed_graph(self, 
                                   title: str, 
                                   nodes: List[Dict[str, Any]], 
                                   links: List[Dict[str, Any]],
                                   width: int = 600,
                                   height: int = 400):
        """
        Render a force-directed graph visualization
        
        Args:
            title: Graph title
            nodes: List of node objects with id and optional properties
            links: List of link objects with source and target
            width: Visualization width
            height: Visualization height
        """
        if not nodes or not links:
            st.warning("No graph data to display")
            return
            
        # Create a unique ID for this graph
        graph_id = f"graph_{self.component_id}_{id(nodes)}"
        
        # Create graph data
        graph_data = {
            "nodes": nodes,
            "links": links
        }
        
        # Render container with D3.js visualization
        st.markdown(f"""
        <div class="viz-container-{self.component_id}">
            <div class="viz-title-{self.component_id}">{title}</div>
            <div class="viz-content-{self.component_id}">
                <div id="{graph_id}" style="width: 100%; height: {height}px;"></div>
            </div>
        </div>
        
        <script src="https://d3js.org/d3.v7.min.js"></script>
        <script>
        // Wait for D3.js to load
        (function() {{
            // Check if D3 is loaded
            function waitForD3() {{
                if (window.d3) {{
                    createGraph();
                }} else {{
                    setTimeout(waitForD3, 100);
                }}
            }}
            
            waitForD3();
            
            function createGraph() {{
                // Graph data
                const graph = {json.dumps(graph_data)};
                
                // Create SVG
                const svg = d3.select("#{graph_id}")
                    .append("svg")
                    .attr("width", "100%")
                    .attr("height", "{height}")
                    .attr("viewBox", [0, 0, {width}, {height}]);
                
                // Create force simulation
                const simulation = d3.forceSimulation(graph.nodes)
                    .force("link", d3.forceLink(graph.links).id(d => d.id).distance(100))
                    .force("charge", d3.forceManyBody().strength(-200))
                    .force("center", d3.forceCenter({width/2}, {height/2}));
                
                // Create links
                const link = svg.append("g")
                    .selectAll("line")
                    .data(graph.links)
                    .enter().append("line")
                    .attr("class", "link-{self.component_id}")
                    .attr("stroke-width", d => Math.sqrt(d.value || 1));
                
                // Create nodes
                const node = svg.append("g")
                    .selectAll("circle")
                    .data(graph.nodes)
                    .enter().append("circle")
                    .attr("class", "node-{self.component_id}")
                    .attr("r", 5)
                    .call(d3.drag()
                        .on("start", dragstarted)
                        .on("drag", dragged)
                        .on("end", dragended));
                
                // Add labels if specified
                if (graph.nodes.some(d => d.label)) {{
                    const labels = svg.append("g")
                        .selectAll("text")
                        .data(graph.nodes)
                        .enter().append("text")
                        .attr("class", "node-label-{self.component_id}")
                        .attr("dx", 8)
                        .attr("dy", ".35em")
                        .text(d => d.label || d.id);
                }}
                
                // Add tooltips
                node.append("title")
                    .text(d => d.id);
                
                // Update positions on simulation tick
                simulation.on("tick", () => {{
                    link
                        .attr("x1", d => d.source.x)
                        .attr("y1", d => d.source.y)
                        .attr("x2", d => d.target.x)
                        .attr("y2", d => d.target.y);
                    
                    node
                        .attr("cx", d => d.x)
                        .attr("cy", d => d.y);
                    
                    // Update labels if they exist
                    svg.selectAll(".node-label-{self.component_id}")
                        .attr("x", d => d.x)
                        .attr("y", d => d.y);
                }});
                
                // Drag functions
                function dragstarted(event, d) {{
                    if (!event.active) simulation.alphaTarget(0.3).restart();
                    d.fx = d.x;
                    d.fy = d.y;
                }}
                
                function dragged(event, d) {{
                    d.fx = event.x;
                    d.fy = event.y;
                }}
                
                function dragended(event, d) {{
                    if (!event.active) simulation.alphaTarget(0);
                    d.fx = null;
                    d.fy = null;
                }}
            }}
        }})();
        </script>
        """, unsafe_allow_html=True)
    
    def style_plotly_chart(self, fig):
        """
        Apply terminal styling to a Plotly figure
        
        Args:
            fig: Plotly figure to style
            
        Returns:
            Styled Plotly figure
        """
        # Apply terminal styling to the figure
        fig.update_layout(
            paper_bgcolor=self.theme_colors["background"],
            plot_bgcolor="rgba(0,0,0,0)",
            font_family="Courier New, monospace",
            font_color=self.theme_colors["text"],
            title_font_family="Courier New, monospace",
            title_font_color=self.theme_colors["primary"],
            legend_title_font_color=self.theme_colors["primary"],
            legend_title_font_family="Courier New, monospace",
        )
        
        # Style axes
        fig.update_xaxes(
            gridcolor="rgba(0, 255, 65, 0.1)",
            showline=True,
            linewidth=1,
            linecolor=self.theme_colors["primary"],
            title_font=dict(family="Courier New, monospace", color=self.theme_colors["primary"])
        )
        
        fig.update_yaxes(
            gridcolor="rgba(0, 255, 65, 0.1)",
            showline=True,
            linewidth=1,
            linecolor=self.theme_colors["primary"],
            title_font=dict(family="Courier New, monospace", color=self.theme_colors["primary"])
        )
        
        return fig
    
    def render_table(self, 
                    title: str, 
                    data: List[Dict[str, Any]], 
                    columns: Optional[List[str]] = None):
        """
        Render an ASCII-style data table
        
        Args:
            title: Table title
            data: List of data dictionaries
            columns: Optional list of columns to include (defaults to all keys)
        """
        if not data:
            st.warning("No data to display")
            return
            
        # Determine columns if not specified
        if not columns:
            columns = list(data[0].keys())
            
        # Calculate column widths
        col_widths = {}
        for col in columns:
            # Get max width of column name and values
            col_widths[col] = max(
                len(str(col)),
                max(len(str(row.get(col, ""))) for row in data)
            )
            
        # Create table header
        header = "+" + "+".join("-" * (col_widths[col] + 2) for col in columns) + "+\n"
        header += "|" + "|".join(f" {col.ljust(col_widths[col])} " for col in columns) + "|\n"
        header += "+" + "+".join("=" * (col_widths[col] + 2) for col in columns) + "+\n"
        
        # Create table rows
        rows = ""
        for row in data:
            rows += "|" + "|".join(f" {str(row.get(col, '')).ljust(col_widths[col])} " for col in columns) + "|\n"
            rows += "+" + "+".join("-" * (col_widths[col] + 2) for col in columns) + "+\n"
            
        table = header + rows
        
        # Render the table
        st.markdown(f"""
        <div class="viz-container-{self.component_id}">
            <div class="viz-title-{self.component_id}">{title}</div>
            <div class="viz-content-{self.component_id}">
                <div class="ascii-chart-{self.component_id}">
                    <pre>{table}</pre>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def set_theme(self, theme_colors: Dict[str, str]):
        """
        Update the visualization theme colors
        
        Args:
            theme_colors: Dictionary with primary, background, and text colors
        """
        self.theme_colors = theme_colors
        self._setup_css() 