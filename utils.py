import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import joblib
import numpy as np
import torch

from pathlib import Path
from model import PINN




import joblib
import numpy as np
import torch

from model import PINN


# ==========================================================
# Load model and scalers
# ==========================================================

def load_model():

    # -----------------------------
    # Load scalers
    # -----------------------------
    scalers = joblib.load("scalers.pkl")

    # -----------------------------
    # Create model
    # -----------------------------
    model = PINN()

    model.load_state_dict(
        torch.load(
            "model_255000.pth",
            map_location=torch.device("cpu")
        )
    )

    model.eval()

    return model, scalers


# ==========================================================
# Prediction Function
# ==========================================================

def predict(
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
    MgSO4,
):

    # -----------------------------
    # Get scalers
    # -----------------------------
    scaler_T = scalers["T"]
    scaler_P = scalers["P"]
    scaler_CaCl2 = scalers["CaCl2"]
    scaler_NaCl = scalers["NaCl"]
    scaler_KCl = scalers["KCl"]
    scaler_MgCl2 = scalers["MgCl2"]
    scaler_Na2SO4 = scalers["Na2SO4"]
    scaler_K2SO4 = scalers["K2SO4"]
    scaler_MgSO4 = scalers["MgSO4"]
    scaler_Sol = scalers["Sol"]

    # -----------------------------
    # Normalize inputs
    # -----------------------------
    T_norm = scaler_T.transform(np.array([[T]], dtype=np.float32))
    P_norm = scaler_P.transform(np.array([[P]], dtype=np.float32))
    CaCl2_norm = scaler_CaCl2.transform(np.array([[CaCl2]], dtype=np.float32))
    NaCl_norm = scaler_NaCl.transform(np.array([[NaCl]], dtype=np.float32))
    KCl_norm = scaler_KCl.transform(np.array([[KCl]], dtype=np.float32))
    MgCl2_norm = scaler_MgCl2.transform(np.array([[MgCl2]], dtype=np.float32))
    Na2SO4_norm = scaler_Na2SO4.transform(np.array([[Na2SO4]], dtype=np.float32))
    K2SO4_norm = scaler_K2SO4.transform(np.array([[K2SO4]], dtype=np.float32))
    MgSO4_norm = scaler_MgSO4.transform(np.array([[MgSO4]], dtype=np.float32))

    # -----------------------------
    # Create model input
    # -----------------------------
    x = np.hstack([
        T_norm,
        P_norm,
        CaCl2_norm,
        NaCl_norm,
        KCl_norm,
        MgCl2_norm,
        Na2SO4_norm,
        K2SO4_norm,
        MgSO4_norm
    ])

    x = torch.tensor(
        x,
        dtype=torch.float32
    )

    # -----------------------------
    # Prediction
    # -----------------------------
    with torch.no_grad():

        y_norm = model(x)

    # -----------------------------
    # Back to original scale
    # -----------------------------
    y = scaler_Sol.inverse_transform(
        y_norm.detach().cpu().numpy()
    )

    return float(y[0, 0])