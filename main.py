import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go 
def db():
    conn = sqlite3.connect('nse.db')
        
    sdate = st.date_input("Select a start date", pd.to_datetime('2022-01-14'))
    edate = st.date_input("Select an end date", pd.to_datetime('2022-03-10'))
    query = """    
    SELECT DISTINCT date, open, high, low, close, volume, oi
    FROM nse
    WHERE date BETWEEN ? AND ?
    """
        
    df1 = pd.read_sql_query(query, conn, params=(sdate, edate))
    
    # Create subplots with both line and bar plots
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Price", "Volume and OI"))

    # Add line plots
    for col in ["open", "high", "low", "close"]:
        fig.add_trace(go.Scatter(x=df1["date"], y=df1[col], mode='lines', name=col), row=1, col=1)

    # Add bar plots
    for col in ["volume", "oi"]:
        fig.add_trace(go.Bar(x=df1["date"], y=df1[col], name=col), row=2, col=1)

    fig.update_layout(title="NSE Data Viewer")
    st.plotly_chart(fig)
    conn.close()

st.title("NSE Data Viewer")
db()
