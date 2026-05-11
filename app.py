import streamlit as st
import ollama
import json

# ==========================================
# 1. BASE DE CONOCIMIENTO
# ==========================================
base_conocimiento = {
    "dominio": "Astronomía Profesional y Observatorios en Chile",
    "por_que_chile": "El norte de Chile ofrece más de 300 noches despejadas al año, atmósfera seca y gran altitud, condiciones ideales para la observación astronómica.",
    "normativa_legal": {
        "ley_principal": "Decreto 43 del Ministerio del Medio Ambiente.",
        "objetivo": "Regula la contaminación lumínica en las regiones de Antofagasta, Atacama y Coquimbo para proteger los cielos astronómicos."
    },
    "observatorios_radioastronomia": [
        {
            "nombre": "ALMA (Atacama Large Millimeter/submillimeter Array)",
            "ubicacion": "Llano de Chajnantor, Región de Antofagasta",
            "altitud": "5.050 msnm",
            "tecnologia": "Interferómetro con 66 antenas de alta precisión (54 de 12m y 12 de 7m).",
            "hitos_historicos": "Captura de la primera imagen de un agujero negro supermasivo (M87*) en 2019.",
            "consorcio": "ESO (Europa), NSF (EE.UU.), NINS (Japón) en cooperación con Chile."
        },
        {
            "nombre": "APEX (Atacama Pathfinder Experiment)",
            "ubicacion": "Llano de Chajnantor",
            "altitud": "5.100 msnm",
            "tecnologia": "Antena única de 12 metros de diámetro.",
            "especialidad": "Estudio del polvo frío y gas molecular en el universo."
        }
    ],
    "observatorios_opticos_infrarrojos": [
        {
            "nombre": "VLT (Very Large Telescope)",
            "ubicacion": "Cerro Paranal, Región de Antofagasta",
            "altitud": "2.635 msnm",
            "tecnologia": "4 Unidades de Telescopio (UT) de 8.2m de diámetro y 4 Telescopios Auxiliares (AT) de 1.8m móviles.",
            "nombres_telescopios_mapudungun": ["Antu (Sol)", "Kueyen (Luna)", "Melipal (Cruz del Sur)", "Yepun (Venus/Lucero)" ],
            "instrumentos_clave": "MUSE, ESPRESSO, SPHERE",
            "hitos_historicos": "Primera imagen directa de un exoplaneta (2M1207b) y comprobación de la Relatividad General orbitando el agujero negro Sgr A*."
        },
        {
            "nombre": "Observatorio Interamericano Cerro Tololo (CTIO)",
            "ubicacion": "Valle del Elqui, Región de Coquimbo",
            "altitud": "2.200 msnm",
            "tecnologia": "Telescopio Víctor M. Blanco de 4 metros.",
            "instrumento_clave": "DECam (Dark Energy Camera) de 570 megapíxeles.",
            "hitos_historicos": "Proveyó los datos clave para descubrir la expansión acelerada del universo (Premio Nobel de Física 2011)."
        },
        {
            "nombre": "Gemini Sur",
            "ubicacion": "Cerro Pachón, Región de Coquimbo",
            "altitud": "2.722 msnm",
            "tecnologia": "Telescopio óptico/infrarrojo de 8.1 metros con sistema de óptica adaptativa.",
            "gemelo": "Tiene un observatorio gemelo en Mauna Kea, Hawái (Gemini Norte)."
        },
        {
            "nombre": "Observatorio de La Silla",
            "ubicacion": "Desierto de Atacama, Región de Coquimbo",
            "altitud": "2.400 msnm",
            "tecnologia": "Telescopio de 3.6 metros y el NTT (New Technology Telescope).",
            "instrumento_clave": "HARPS (High Accuracy Radial velocity Planet Searcher), el cazador de exoplanetas más exitoso."
        }
    ],
    "megatelescopios_en_construccion": [
        {
            "nombre": "ELT (Extremely Large Telescope)",
            "ubicacion": "Cerro Armazones",
            "fecha_estimada": "Finales de la década de 2020",
            "tecnologia": "Espejo primario de 39.3 metros compuesto por 798 segmentos hexagonales.",
            "objetivo": "Buscar biomarcadores (vida) en atmósferas de exoplanetas."
        },
        {
            "nombre": "Vera C. Rubin Observatory (antiguo LSST)",
            "ubicacion": "Cerro Pachón",
            "fecha_estimada": "2025",
            "tecnologia": "Cámara digital más grande del mundo (3.200 megapíxeles).",
            "objetivo": "Escaneará todo el cielo visible del sur cada pocos días, generando 20 Terabytes de datos por noche."
        },
        {
            "nombre": "GMT (Giant Magellan Telescope)",
            "ubicacion": "Observatorio Las Campanas",
            "fecha_estimada": "Inicios de la década de 2030",
            "tecnologia": "Siete espejos monolíticos gigantes que formarán un diámetro equivalente a 24.5 metros."
        }
    ]
}

# ==========================================
# 2. CONFIGURACIÓN DE LA INTERFAZ 
# ==========================================
st.set_page_config(page_title="AstroBot Chile | Fase 2", page_icon="🔭", layout="wide")

# Barra lateral 
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/ESO-VLT-Laser-phot-33a-07.jpg/800px-ESO-VLT-Laser-phot-33a-07.jpg", caption="VLT en Cerro Paranal")
    st.header("🌌 Base de Datos Cargada")
    st.success("Conectado al LLM Local (Llama 3)")
    st.write("**Entidades Modeladas:**")
    st.markdown("- 2 Radiotelescopios\n- 4 Observatorios Ópticos\n- 3 Megatelescopios futuros\n- 1 Ley de Protección\n- Hitos Históricos (Premios Nobel)")
    st.info("Desarrollo Fase 2 - Sistema con Inyección de Contexto Estructurado (JSON).")

st.title("🔭 AstroBot: Sistema Experto en Astronomía de Chile")
st.markdown("Este chatbot utiliza un modelo de lenguaje abierto para responder consultas basándose estrictamente en una base de conocimientos sobre los observatorios instalados en territorio nacional.")
st.markdown("---")

# ==========================================
# 3. LÓGICA DEL LLM Y CHAT
# ==========================================
# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Prompt del sistema
SYSTEM_PROMPT = f"""
Eres un asistente científico avanzado especializado en Astronomía en Chile. 
Tu única fuente de información es este JSON proporcionado:
{json.dumps(base_conocimiento, ensure_ascii=False)}

REGLAS ESTRICTAS:
1. Responde preguntas usando SOLO la información del JSON.
2. Si el usuario pregunta algo que NO está en el JSON, debes responder exactamente: "Lo siento, esa información no está en mi base de datos de observatorios chilenos."
3. Sé claro, conciso y profesional.
4. Si te preguntan sobre tecnología, menciona el tamaño de los espejos o cámaras.
"""

# Captura de input del usuario
if prompt := st.chat_input("Ej: ¿Qué observatorio ganó un Premio Nobel? o ¿Cuál es la ley que protege los cielos?"):
    # Agregar mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Llamada al modelo local usando Ollama
    with st.chat_message("assistant"):
        with st.spinner("Procesando en LLM local..."):
            try:
                response = ollama.chat(model='llama3', messages=[
                    {'role': 'system', 'content': SYSTEM_PROMPT},
                    {'role': 'user', 'content': prompt},
                ])
                respuesta = response['message']['content']
                st.markdown(respuesta)
                # Guardar respuesta en el historial
                st.session_state.messages.append({"role": "assistant", "content": respuesta})
            except Exception as e:
                st.error(f"Error de conexión con Ollama. Asegúrate de tenerlo abierto. Detalles: {e}")