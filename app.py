import streamlit as st
from utils import load_model, predict

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="CO₂ Solubility Prediction using PINN",
    page_icon="🧪",
    layout="centered"
)
##### css
st.markdown("""
<style>

/* ==========================
   Input Labels
   ========================== */
[data-testid="stWidgetLabel"] p {
    color: #1565C0 !important;      /* Blue */
    font-size: 22px !important;     /* Same size everywhere */
    font-weight: 800 !important;    /* Bold */
    font-family: "Segoe UI", sans-serif !important;
}

/* ==========================
   Input Values
   ========================== */
.stTextInput input {
    color: #0F9D58 !important;      /* Emerald Green */
    font-size: 22px !important;     /* Same size as labels */
    font-weight: 800 !important;    /* Bold */
    font-family: "Segoe UI", sans-serif !important;
}

/* ==========================
   Buttons
   ========================== */
.stButton > button {
    width: 100%;
    height: 65px !important;
    background: linear-gradient(90deg,#0F9D58,#087F5B) !important;
    border: none !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 12px rgba(15,157,88,0.35) !important;
}

.stButton > button p {
    color: white !important;
    font-size: 22px !important;     /* Same size */
    font-weight: 800 !important;
    font-family: "Segoe UI", sans-serif !important;
}

.stButton > button:hover {
    background: linear-gradient(90deg,#087F5B,#066A4B) !important;
}

/* ==========================
   Prediction Result
   ========================== */
[data-testid="stSuccess"] {
    font-size: 22px !important;
    font-weight: 800 !important;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# Load Model
# ==========================================================

@st.cache_resource
def initialize():
    return load_model()

model, scalers = initialize()

# ==========================================================
# Default Values
# ==========================================================

DEFAULTS = {
    "T": "323.15",
    "P": "5.0687",
    "CaCl2": "1.0",
    "NaCl": "0.0",
    "KCl": "0.0",
    "MgCl2": "0.0",
    "Na2SO4": "0.0",
    "K2SO4": "0.0",
    "MgSO4": "0.0",
}

DEFAULTS1 = {
    "T": "0.0",
    "P": "0.0",
    "CaCl2": "0.0",
    "NaCl": "0.0",
    "KCl": "0.0",
    "MgCl2": "0.0",
    "Na2SO4": "0.0",
    "K2SO4": "0.0",
    "MgSO4": "0.0",
}
# Initialize only once
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)

# ==========================================================
# Header
# ==========================================================

st.markdown(
    """
    <h1 style="
        text-align: center;
        color: #6A1B9A;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0.2em;
    ">
        CO₂ Solubility Prediction using Physics-Informed Neural Network
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="
        text-align: center;
        color: #0F9D58;
        font-size: 22px;
        font-weight: 700;
        margin-top: -10px;
        margin-bottom: 20px;
    ">
        Predict CO₂ solubility in brine using the trained Physics-Informed Neural Network (PINN).
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ==========================================================
# Inputs
# ==========================================================

col1, col2 = st.columns(2)

with col1:

    st.session_state["T"] = st.text_input(
        "Temperature (K)",
        value=st.session_state["T"]
    )

    st.session_state["CaCl2"] = st.text_input(
        "CaCl₂ (mol/kg)",
        value=st.session_state["CaCl2"]
    )

    st.session_state["KCl"] = st.text_input(
        "KCl (mol/kg)",
        value=st.session_state["KCl"]
    )

    st.session_state["Na2SO4"] = st.text_input(
        "Na₂SO₄ (mol/kg)",
        value=st.session_state["Na2SO4"]
    )

    st.session_state["MgSO4"] = st.text_input(
        "MgSO₄ (mol/kg)",
        value=st.session_state["MgSO4"]
    )

with col2:

    st.session_state["P"] = st.text_input(
        "Pressure (MPa)",
        value=st.session_state["P"]
    )

    st.session_state["NaCl"] = st.text_input(
        "NaCl (mol/kg)",
        value=st.session_state["NaCl"]
    )

    st.session_state["MgCl2"] = st.text_input(
        "MgCl₂ (mol/kg)",
        value=st.session_state["MgCl2"]
    )

    st.session_state["K2SO4"] = st.text_input(
        "K₂SO₄ (mol/kg)",
        value=st.session_state["K2SO4"]
    )

st.divider()

# ==========================================================
# Buttons
# ==========================================================

col1, col2 = st.columns(2)

with col1:
    predict_button = st.button(
        "Predict",
        use_container_width=True
    )

with col2:
    clear_button = st.button(
        "Clear",
        use_container_width=True
    )

# ==========================================================
# Clear
# ==========================================================

if clear_button:

    for key in DEFAULTS1.keys():
        st.session_state[key] = ""

    st.rerun()

# ==========================================================
# Prediction
# ==========================================================

if predict_button:

    try:

        T = float(st.session_state["T"])
        P = float(st.session_state["P"])
        CaCl2 = float(st.session_state["CaCl2"])
        NaCl = float(st.session_state["NaCl"])
        KCl = float(st.session_state["KCl"])
        MgCl2 = float(st.session_state["MgCl2"])
        Na2SO4 = float(st.session_state["Na2SO4"])
        K2SO4 = float(st.session_state["K2SO4"])
        MgSO4 = float(st.session_state["MgSO4"])

    except ValueError:

        st.error("Please enter numeric values in all fields.")
        st.stop()

    with st.spinner("Predicting..."):

        result = predict(
            model,
            scalers,
            T,
            P,
            CaCl2,
            NaCl,
            KCl,
            MgCl2,
            Na2SO4,
            K2SO4,
            MgSO4
        )

    st.divider()

    st.success(
        f"""
### Predicted CO₂ Solubility

### **{result:.6f} mol/kg**
"""
    )

