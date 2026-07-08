import streamlit as st
import pandas as pd
import os
from streamlit_geolocation import streamlit_geolocation

# Configuración de página
st.set_page_config(page_title="Coordenadas JOL", layout="wide")

DB_FILE = "MIC COORDENADAS.xlsx"

def cargar_db():
    if os.path.exists(DB_FILE):
        # Usamos engine='openpyxl' para archivos .xlsx modernos
        df = pd.read_excel(DB_FILE, engine='openpyxl', dtype=str)
        # Limpieza de nombres de columna
        df.columns = df.columns.str.strip().str.upper()
        # Asegurar que existan las columnas de coordenadas
        if "COORDENADA X" not in df.columns: df["COORDENADA X"] = "0.00"
        if "COORDENADA Y" not in df.columns: df["COORDENADA Y"] = "0.00"
        return df
    else:
        st.error(f"El archivo '{DB_FILE}' no se encuentra en la carpeta.")
        return pd.DataFrame()

df_maestra = cargar_db()

st.title("📍 Coordenadas JOL - Sistema de Gestión")

if not df_maestra.empty:
    asesor = st.selectbox("Seleccione asesor:", sorted(df_maestra['ASESOR'].unique()))
    df_asesor = df_maestra[df_maestra['ASESOR'].astype(str).str.strip() == asesor]
    
    st.dataframe(df_asesor, use_container_width=True)
    
    cliente = st.selectbox("Seleccionar cliente:", df_asesor['NOMBRE'].tolist())
    
    location = streamlit_geolocation()
    
    if location and location['latitude']:
        if st.button("Guardar Coordenadas GPS"):
            lat, lon = str(location['latitude']), str(location['longitude'])
            try:
                # Actualizar el DataFrame original
                idx = df_maestra[df_maestra['NOMBRE'] == cliente].index[0]
                df_maestra.at[idx, 'COORDENADA X'] = lat
                df_maestra.at[idx, 'COORDENADA Y'] = lon
                
                # Guardar en Excel
                df_maestra.to_excel(DB_FILE, index=False, engine='openpyxl')
                st.success(f"✅ Coordenadas guardadas para {cliente}")
                st.rerun()
            except Exception as e:
                st.error(f"Error al guardar: {e}. ¿Tienes el archivo Excel abierto?")
