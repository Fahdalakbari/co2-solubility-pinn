import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch
import torch.nn as nn


# ==========================
# Hyperparameters
# ==========================
acti1 = nn.Tanh
acti2 = nn.Tanh
acti3 = nn.Tanh

neu1 = 350
neu2 = 230
neu3 = 230


# ==========================
# PINN Model
# ==========================
class PINN(nn.Module):

    def __init__(self):

        super(PINN, self).__init__()

        # Neural Network
        self.net = nn.Sequential(

            nn.Linear(9, neu1),
            acti1(),

            nn.Linear(neu1, neu2),
            acti2(),

            nn.Linear(neu2, neu3),
            acti3(),

            nn.Linear(neu3, 1)

        )

        # =====================================================
        # Fugacity Parameters
        # =====================================================

        # Temperature (15)
        for i in range(1, 16):
            setattr(self, f"ct{i}", nn.Parameter(torch.tensor(1.0)))

        # Pressure (15)
        for i in range(1, 16):
            setattr(self, f"cp{i}", nn.Parameter(torch.tensor(1.0)))

        # =====================================================
        # Salt-Out Parameters
        # =====================================================

        # ---------- Temperature ----------

        # Cation
        for salt in range(1, 5):
            for p in [2,3,4,5,7,8,9,10,11]:
                setattr(
                    self,
                    f"Cct{p}_{salt}",
                    nn.Parameter(torch.tensor(1.0))
                )

        # Anion
        for salt in range(1,3):
            for p in [2,3,4,5,7,8,9,10,11]:
                setattr(
                    self,
                    f"Cnt{p}_{salt}",
                    nn.Parameter(torch.tensor(1.0))
                )

        # Ternary
        for salt in range(1,8):
            for p in [2,3,4,5,7,8,9,10,11]:
                setattr(
                    self,
                    f"Ctt{p}_{salt}",
                    nn.Parameter(torch.tensor(1.0))
                )

        # ---------- Pressure ----------

        # Cation
        for salt in range(1,5):
            for p in [6,7,8,9,10,11]:
                setattr(
                    self,
                    f"Ccp{p}_{salt}",
                    nn.Parameter(torch.tensor(1.0))
                )

        # Anion
        for salt in range(1,3):
            for p in [6,7,8,9,10,11]:
                setattr(
                    self,
                    f"Cnp{p}_{salt}",
                    nn.Parameter(torch.tensor(1.0))
                )

        # Ternary
        for salt in range(1,8):
            for p in [6,7,8,9,10,11]:
                setattr(
                    self,
                    f"Ctp{p}_{salt}",
                    nn.Parameter(torch.tensor(1.0))
                )

        # =====================================================
        # Chemical Potential
        # =====================================================

        for p in [2,3,4,5,7,8,9,10,11]:
            setattr(
                self,
                f"Ckt{p}",
                nn.Parameter(torch.tensor(1.0))
            )

        for p in [6,7,8,9,10,11]:
            setattr(
                self,
                f"Ckp{p}",
                nn.Parameter(torch.tensor(1.0))
            )

        # =====================================================
        # dγ/dSalt
        # =====================================================

        # CaCl2
        self.Cs1_1 = nn.Parameter(torch.tensor(1.0))
        self.Cs2_1 = nn.Parameter(torch.tensor(1.0))
        self.Cs3_1 = nn.Parameter(torch.tensor(1.0))

        # NaCl
        self.Cs1_2 = nn.Parameter(torch.tensor(1.0))
        self.Cs2_2 = nn.Parameter(torch.tensor(1.0))

        # KCl
        self.Cs1_3 = nn.Parameter(torch.tensor(1.0))
        self.Cs2_3 = nn.Parameter(torch.tensor(1.0))

        # MgCl2
        self.Cs1_4 = nn.Parameter(torch.tensor(1.0))
        self.Cs2_4 = nn.Parameter(torch.tensor(1.0))
        self.Cs3_4 = nn.Parameter(torch.tensor(1.0))

        # Na2SO4
        self.Cs1_5 = nn.Parameter(torch.tensor(1.0))
        self.Cs2_5 = nn.Parameter(torch.tensor(1.0))
        self.Cs3_5 = nn.Parameter(torch.tensor(1.0))

        # K2SO4
        self.Cs1_6 = nn.Parameter(torch.tensor(1.0))
        self.Cs2_6 = nn.Parameter(torch.tensor(1.0))
        self.Cs3_6 = nn.Parameter(torch.tensor(1.0))

        # MgSO4
        self.Cs1_7 = nn.Parameter(torch.tensor(1.0))
        self.Cs2_7 = nn.Parameter(torch.tensor(1.0))
        self.Cs3_7 = nn.Parameter(torch.tensor(1.0))

    # ==========================================================
    # Forward
    # ==========================================================

    def forward(self, x):

        return torch.abs(self.net(x))