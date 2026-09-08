import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

# --- 1. CONFIGURACIÓN VISUAL Y FUENTE (CSS) ---
st.set_page_config(page_title="Portal Legal - Seguros", page_icon="⚖️")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    html, body, p, h1, h2, h3, h4, h5, h6, div[class*="stText"] {
        font-family: 'Inter', sans-serif !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("Sistema de Liquidación de Siniestros")
st.markdown("Plataforma interna de evaluación normativa (Motor Gemini).")

# --- 2. CONFIGURACIÓN DEL ENTORNO ---
google_api_key = st.text_input("Credenciales de acceso (Google Gemini API Key)", type="password")

if google_api_key:
    os.environ["GOOGLE_API_KEY"] = google_api_key
    
    # Instanciamos el modelo oficial y gratuito de Google vía LangChain
    llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0.1)

    # --- 3. CONTEXTO SIMULADO ---
    contexto_poliza = """
    ARTÍCULO 1: La aseguradora cubrirá los daños por robo total del vehículo.
    ARTÍCULO 2: Se excluye expresamente el robo de accesorios removibles, incluyendo radios, espejos y equipamiento no original.
    ARTÍCULO 3: En caso de choque, se cubrirán daños a terceros hasta por un tope de $10,000 dólares.
    """
    
    with st.expander("Consultar Póliza Vigente"):
        st.info(contexto_poliza)

    # --- 4. PANEL DE EVALUACIÓN ---
    st.subheader("Ingreso de Siniestro")
    pregunta = st.selectbox(
        "Seleccione el reporte ingresado por el cliente:",
        [
            "¿Me cubren si me roban la radio del auto mientras estaba estacionado en el mall?",
            "Choqué por accidente y le causé daños al otro auto por $5,000. ¿Está cubierto?",
            "Me robaron el auto completo anoche fuera de mi casa. ¿Qué aplica aquí?"
        ]
    )

    if st.button("Generar Minuta Legal"):
        with st.spinner("Procesando expediente con Gemini..."):
            
            # --- 5. PROMPT DEL SISTEMA ---
            prompt_sistema = f"""Eres un liquidador de seguros senior dictaminando un caso. 
Redacta tu minuta de forma directa, corporativa y humana. 
PROHIBIDO usar frases típicas de IA como "Basado en el contexto", "Aquí tienes la respuesta", o "Como modelo de lenguaje".
Ve directo al grano con lenguaje jurídico y técnico.

Póliza vigente:
{contexto_poliza}

Estructura tu minuta exactamente así:
- ANÁLISIS TÉCNICO: [Tu razonamiento breve y directo pensando paso a paso]
- RESOLUCIÓN FINAL: [Aprobado / Rechazado]
- FUNDAMENTO LEGAL: [Artículo aplicable]

Si el siniestro no está tipificado en la póliza, responde únicamente: "Caso no tipificado. Requiere escalamiento."
"""
            
            try:
                mensajes = [
                    SystemMessage(content=prompt_sistema),
                    HumanMessage(content=pregunta)
                ]
                
                # Ejecutamos la invocación con LangChain
                respuesta = llm.invoke(mensajes)
                
                # Saneamiento y limpieza de la respuesta para evitar bloques de datos crudos
                texto_limpio = respuesta.content if hasattr(respuesta, 'content') else str(respuesta)
                if isinstance(texto_limpio, list):
                    texto_limpio = "".join([item.get('text', '') if isinstance(item, dict) else str(item) for item in texto_limpio])
                
                st.success("Expediente procesado correctamente.")
                st.markdown("### Minuta de Resolución")
                st.markdown(texto_limpio)
                
            except Exception as e:
                st.error(f"Error de conexión con el servidor: {e}")
else:
    st.warning("Ingrese su API Key de Google AI Studio para continuar.")