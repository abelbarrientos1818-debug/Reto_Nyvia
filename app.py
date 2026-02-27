import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración básica
st.set_page_config(page_title="Nyvia: Retail Intelligence", layout="wide")

st.title("Motor de Crecimiento de Ingresos - Retail MX")

# --- CARGA DE DATOS SEGURO ---
@st.cache_data
def load_data():
    # Cargamos el archivo que ya tienes en tu carpeta de Cursor
    df = pd.read_csv('online_retail_II.csv', encoding='ISO-8859-1')
    # Limpieza rápida para el MVP
    df = df.dropna(subset=['Customer ID'])
    df['TotalPrice'] = df['Quantity'] * df['Price']
    
    # Creamos un mini-resumen RFM manual para que no falle nada
    rfm_table = df.groupby('Customer ID').agg({
        'TotalPrice': 'sum',
        'Invoice': 'count'
    }).rename(columns={'TotalPrice': 'Monetary', 'Invoice': 'Frequency'})
    
    # Creamos clusters ficticios pero lógicos para la demo
    rfm_table['Cluster'] = pd.qcut(rfm_table['Monetary'], 4, labels=['Bronce', 'Plata', 'Oro', 'VIP'])
    return rfm_table

try:
    rfm = load_data()

    # --- SIDEBAR ---
    st.sidebar.header("Configuración de Campaña")
    porsentaje = st.sidebar.slider("% de clientes a recuperar", 0, 100, 15)

    # --- KPIs ---
    col1, col2, col3 = st.columns(3)
    total_rev = rfm['Monetary'].sum()
    
    with col1:
        st.metric("Facturación Analizada", f"${total_rev/1e6:.1f}M MXN")
    with col2:
        st.metric("Ticket Promedio", f"${rfm['Monetary'].mean():,.2f} MXN")
    with col3:
        # Impacto cuantificado (Estándar Nyvia)
        impacto = (total_rev * 0.03) * (porsentaje / 100)
        st.metric("Impacto Proyectado", f"+${impacto/1e6:.2f}M MXN", delta="ROI Estratégico")

    # --- GRÁFICO ---
    st.subheader("Segmentación Estratégica")
    fig = px.scatter(rfm.reset_index(), x="Frequency", y="Monetary", color="Cluster", 
                     log_x=True, log_y=True, title="Mapa de Valor de Clientes")
    st.plotly_chart(fig, use_container_width=True)

    st.success("Dashboard cargado con éxito. Listo para presentar a Dirección.")

except Exception as e:
    st.error(f"Error al cargar datos: {e}")
    st.info("Asegúrate de que el archivo 'online_retail_II.csv' esté en la misma carpeta que este script.")