import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuración de la App
st.set_page_config(page_title="Ariar Steel Control", layout="centered", page_icon="🏗️")

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { 
        width: 100%;
        background-color: #ff4b4b; 
        color: white; 
        border-radius: 8px; 
    }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS ---
DB_FILE = "horas_ariar.csv"

def cargar_datos():
    if not os.path.isfile(DB_FILE):
        df = pd.DataFrame(columns=["Fecha", "Empleado", "Ubicacion", "Horas"])
        df.to_csv(DB_FILE, index=False)
    return pd.read_csv(DB_FILE)

# --- PINS DE ACCESO ---
empleados_db = {
    "Melvin": "1234",
    "Edwin Lopez": "3909",
    "Luis": "5678",
    "Alexandra": "4321"
}

st.title("🏗️ PANEL DE CONTROL ARIAR STEEL")
st.write("---")

menu = ["👤 Ver Mis Horas (Empleado)", "🔑 Registrar Horas (Dueño)"]
choice = st.sidebar.selectbox("Seleccione Modo:", menu)

# --- MODO EMPLEADO ---
if choice == "👤 Ver Mis Horas (Empleado)":
    st.header("Consulta de Horas Personales")
    
    col1, col2 = st.columns(2)
    with col1:
        nombre_emp = st.selectbox("Selecciona tu nombre:", list(empleados_db.keys()))
    with col2:
        pin_check = st.text_input("PIN:", type="password")

    if pin_check == empleados_db.get(nombre_emp):
        df_horas = cargar_datos()
        mis_horas = df_horas[df_horas["Empleado"] == nombre_emp].copy()
        
        if not mis_horas.empty:
            st.metric("TOTAL DE HORAS ACUMULADAS", f"{mis_horas['Horas'].sum()} hrs")
            st.dataframe(mis_horas, use_container_width=True)
        else:
            st.info("No tienes horas registradas aún.")
    elif pin_check != "":
        st.error("⚠️ PIN Incorrecto.")

# --- MODO DUEÑO ---
elif choice == "🔑 Registrar Horas (Dueño)":
    st.header("Panel Administrativo")
    pin_admin = st.text_input("PIN de Dueño:", type="password")

    if pin_admin == "3909":
        with st.form("registro_ariar"):
            c1, c2 = st.columns(2)
            with c1:
                fecha = st.date_input("Fecha:", datetime.now())
                emp_reg = st.selectbox("Empleado:", list(empleados_db.keys()))
            with c2:
                lugar = st.text_input("Ubicación:", placeholder="Ej: Houston")
                hrs = st.number_input("Horas:", min_value=0.0, step=0.5)
            
            submit = st.form_submit_button("GUARDAR EN BASE DE DATOS")
            
            if submit and lugar:
                nueva_fila = pd.DataFrame([{"Fecha": fecha, "Empleado": emp_reg, "Ubicacion": lugar, "Horas": hrs}])
                df_ariar = cargar_datos()
                df_final = pd.concat([df_ariar, nueva_fila], ignore_index=True)
                df_final.to_csv(DB_FILE, index=False)
                st.success("Registrado!")
                st.rerun()

        st.write("---")
        df_completo = cargar_datos()
        
        if st.checkbox("Mostrar Base de Datos Completa"):
            st.dataframe(df_completo, use_container_width=True)
            
            # Botón para descargar reporte
            csv = df_completo.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Descargar Reporte CSV", data=csv, file_name="reporte_ariar_steel.csv", mime="text/csv")

            if st.button("🗑️ Borrar Último Registro"):
                if not df_completo.empty:
                    df_completo.drop(df_completo.tail(1).index, inplace=True)
                    df_completo.to_csv(DB_FILE, index=False)
                    st.rerun()

st.sidebar.caption("Ariar Steel Control v2.0")