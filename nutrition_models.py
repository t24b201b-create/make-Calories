# nutrition_models.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, Dict, Optional

Sex = Literal["male", "female"]
ActivityLevel = Literal["sedentary", "light", "moderate", "active", "very_active"]

@dataclass(frozen=True)
class Person:
    age_years: int
    sex: Sex
    height_cm: float
    weight_kg: float
    activity_level: ActivityLevel = "moderate"

@dataclass
class Nutrients:  # 食品1品 or 合計
    energy_kcal: Optional[float] = None
    protein_g: Optional[float] = None
    fat_g: Optional[float] = None
    carbs_g: Optional[float] = None
    salt_g: Optional[float] = None
    calcium_mg: Optional[float] = None
    vegetables_g: Optional[float] = None
    iron_mg: Optional[float] = None
    vitaminA_ugRAE: Optional[float] = None
    vitaminB1_mg: Optional[float] = None
    vitaminB2_mg: Optional[float] = None
    vitaminC_mg: Optional[float] = None

    def add_inplace(self, other: "Nutrients"):
        for k, v in other.__dict__.items():
            if v is None: 
                continue
            cur = getattr(self, k)
            setattr(self, k, (cur or 0.0) + float(v))
