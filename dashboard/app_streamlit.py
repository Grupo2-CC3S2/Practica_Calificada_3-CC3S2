import streamlit as st
from metrics import load_snapshots, throughput, wip, velocity, cycle_time, slip_rate

st.set_page_config(page_title="Scrum Dashboard", layout="wide")
st.title("Dashboard Métricas Scrum")

df = load_snapshots()
st.write("Tareas totales:", len(df))

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Throughput", throughput(df))
col2.metric("In progress", wip(df))
col3.metric("Velocity", velocity(df))
col4.metric("Cycle Time", f"{cycle_time(df):.2f}" if cycle_time(df) else "N/A")
col5.metric("Slip Rate", f"{slip_rate(df)*100:.1f}%" if slip_rate(df) else "N/A")

st.subheader("Datos crudos")
st.dataframe(df)


# Ejecucion
# streamlit run dashboard/app_streamlit.py 
# Desde la raiz del proyecto