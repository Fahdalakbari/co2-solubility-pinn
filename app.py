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

st.title("CO₂ Solubility Prediction using PINN")

st.markdown("""
Predict CO₂ solubility in brine using the trained
**Physics-Informed Neural Network (PINN)**.
""")

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

**{result:.6f} mol/kg**
"""
    )