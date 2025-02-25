import pandas as pd
import networkx as nx
import streamlit as st
import altair as alt
from typing import List, Dict, Any
import sqlite3
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime, timedelta

def generate_memory_timeline(conn: sqlite3.Connection) -> alt.Chart:
    """Generate a timeline visualization of memory entries."""
    # Query memory data
    df = pd.read_sql_query("""
        SELECT 
            timestamp, 
            query,
            SUBSTR(answer, 1, 100) as short_answer,
            model,
            latency,
            input_tokens,
            output_tokens
        FROM long_term_memory
        ORDER BY timestamp
    """, conn)
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Add date column for grouping
    df['date'] = df['timestamp'].dt.date
    
    # Create timeline chart
    timeline = alt.Chart(df).mark_circle().encode(
        x='timestamp:T',
        y='latency:Q',
        size='output_tokens:Q',
        color='model:N',
        tooltip=['timestamp', 'query', 'short_answer', 'model', 'latency', 'input_tokens', 'output_tokens']
    ).properties(
        width=700,
        height=400,
        title='Memory Timeline'
    ).interactive()
    
    return timeline
    
def generate_memory_graph(conn: sqlite3.Connection, limit: int = 20) -> str:
    """Generate a graph visualization of memory connections."""
    # Query memory data
    df = pd.read_sql_query(f"""
        SELECT id, timestamp, query, SUBSTR(answer, 1, 100) as short_answer
        FROM long_term_memory
        ORDER BY timestamp DESC
        LIMIT {limit}
    """, conn)
    
    # Create graph
    G = nx.Graph()
    
    # Add memory nodes
    for _, row in df.iterrows():
        G.add_node(row['id'], 
                   label=f"Q: {row['query'][:30]}...",
                   title=f"ID: {row['id']}\nQ: {row['query']}\nA: {row['short_answer']}",
                   timestamp=row['timestamp'])
    
    # Add edges based on keyword similarity
    for i, row_i in df.iterrows():
        words_i = set(row_i['query'].lower().split())
        for j, row_j in df.iterrows():
            if i < j:  # Avoid duplicate edges
                words_j = set(row_j['query'].lower().split())
                common_words = words_i.intersection(words_j)
                
                # If they share at least 2 significant words, add an edge
                if len(common_words) >= 2:
                    G.add_edge(row_i['id'], row_j['id'], 
                               weight=len(common_words),
                               title=f"Common: {', '.join(common_words)}")
    
    # Draw graph
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=700, alpha=0.8)
    
    # Draw edges with varying width based on weight
    edges = G.edges(data=True)
    weights = [data['weight'] for _, _, data in edges]
    nx.draw_networkx_edges(G, pos, width=weights, alpha=0.5)
    
    # Draw labels
    labels = {node: data['label'] for node, data in G.nodes(data=True)}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8)
    
    # Save figure to bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    plt.close()
    
    # Convert to base64 for embedding in HTML
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"data:image/png;base64,{data}"
    
def generate_model_performance_chart(conn: sqlite3.Connection) -> alt.Chart:
    """Generate a chart comparing model performance."""
    # Query model performance data
    df = pd.read_sql_query("""
        SELECT 
            model,
            AVG(latency) as avg_latency,
            AVG(output_tokens) as avg_output_tokens,
            COUNT(*) as query_count
        FROM long_term_memory
        WHERE model IS NOT NULL
        GROUP BY model
    """, conn)
    
    # Create chart
    base = alt.Chart(df).encode(
        x='model:N'
    )
    
    bars = base.mark_bar().encode(
        y='avg_latency:Q',
        color='model:N',
        tooltip=['model', 'avg_latency', 'avg_output_tokens', 'query_count']
    )
    
    text = bars.mark_text(
        align='center',
        baseline='bottom',
        dy=-5
    ).encode(
        text=alt.Text('avg_latency:Q', format='.2f')
    )
    
    chart = (bars + text).properties(
        width=600,
        height=400,
        title='Average Latency by Model'
    )
    
    return chart
    
def display_memory_visualizations(conn: sqlite3.Connection):
    """Display memory visualizations in Streamlit."""
    st.subheader("Memory Visualizations")
    
    tab1, tab2, tab3 = st.tabs(["Timeline", "Connections", "Model Performance"])
    
    with tab1:
        st.write("This timeline shows when memories were created, with the size indicating output token count.")
        timeline = generate_memory_timeline(conn)
        st.altair_chart(timeline, use_container_width=True)
        
        # Add time range selector
        st.write("Filter by time range:")
        days = st.slider("Days to include", 1, 30, 7)
        
        # Get filtered data
        cutoff_date = datetime.now() - timedelta(days=days)
        df_filtered = pd.read_sql_query(f"""
            SELECT 
                timestamp, 
                model,
                latency,
                input_tokens,
                output_tokens
            FROM long_term_memory
            WHERE timestamp > '{cutoff_date.isoformat()}'
            ORDER BY timestamp
        """, conn)
        
        if not df_filtered.empty:
            df_filtered['timestamp'] = pd.to_datetime(df_filtered['timestamp'])
            df_filtered['date'] = df_filtered['timestamp'].dt.date
            
            # Daily summary chart
            daily_summary = alt.Chart(df_filtered).mark_bar().encode(
                x='date:T',
                y='count():Q',
                tooltip=['date', 'count()']
            ).properties(
                width=600,
                height=200,
                title=f'Queries per Day (Last {days} days)'
            )
            
            st.altair_chart(daily_summary, use_container_width=True)
        else:
            st.write("No data available for the selected time range.")
    
    with tab2:
        st.write("This graph shows connections between related memories based on keyword similarity.")
        max_nodes = st.slider("Number of memories to include", 5, 50, 20)
        graph_image = generate_memory_graph(conn, limit=max_nodes)
        st.image(graph_image)
        
    with tab3:
        st.write("This chart compares the performance of different models.")
        performance_chart = generate_model_performance_chart(conn)
        st.altair_chart(performance_chart, use_container_width=True)
        
        # Token efficiency chart
        token_df = pd.read_sql_query("""
            SELECT 
                model,
                SUM(input_tokens) as total_input,
                SUM(output_tokens) as total_output
            FROM long_term_memory
            WHERE model IS NOT NULL AND input_tokens > 0
            GROUP BY model
        """, conn)
        
        if not token_df.empty:
            token_df['tokens_ratio'] = token_df['total_output'] / token_df['total_input']
            
            ratio_chart = alt.Chart(token_df).mark_bar().encode(
                x='model:N',
                y='tokens_ratio:Q',
                color='model:N',
                tooltip=['model', 'total_input', 'total_output', 'tokens_ratio']
            ).properties(
                width=600,
                height=300,
                title='Output/Input Token Ratio by Model'
            )
            
            st.altair_chart(ratio_chart, use_container_width=True) 