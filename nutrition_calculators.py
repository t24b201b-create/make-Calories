# nutrition_calculators.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict
from nutrition_models import Person

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """BMI = weight_kg / (height_m)^2"""
    h_m = height_cm / 100.0
    if h_m <= 0:
        raise ValueError("height_cm must be > 0")
    return weight_kg / (h_m * h_m)

def classify_bmi_jp(bmi: float) -> str:
    """シンプル分類（必要なら日本肥満学会などに差し替え可能）"""
    if bmi < 18.5: return "underweight"
    if bmi < 25.0: return "normal"
    if bmi < 30.0: return "pre-obese"
    return "obese"

def estimate_tdee_kcal(person: Person) -> float:
    """簡易版（Mifflin-St Jeor相当のBMR→活動係数）。必要なら式を差し替え可能。"""
    # BMR
    if person.sex == "male":
        bmr = 10*person.weight_kg + 6.25*person.height_cm - 5*person.age_years + 5
    else:
        bmr = 10*person.weight_kg + 6.25*person.height_cm - 5*person.age_years - 161
    # 活動係数
    af = {
        "sedentary": 1.2, "light": 1.375, "moderate": 1.55,
        "active": 1.725, "very_active": 1.9
    }[person.activity_level]
    return bmr * af

@dataclass
class MacroTargets:
    energy_kcal: float
    protein_g: float
    fat_g: float
    carbs_g: float

def compute_macro_targets(person: Person, 
                          protein_g_per_kg: float = 1.2,
                          fat_ratio: float = 0.25) -> MacroTargets:
    """
    目安：
      - たんぱく質: 体重1kgあたり 1.2 g（用途に応じて1.0〜1.6に変更）
      - 脂質: 総エネルギーの25%（fat_ratioで変更可）
      - 炭水化物: 残りを充当
    """
    kcal = estimate_tdee_kcal(person)
    protein_g = person.weight_kg * protein_g_per_kg
    protein_kcal = protein_g * 4
    fat_kcal = kcal * fat_ratio
    fat_g = fat_kcal / 9
    carbs_kcal = max(kcal - protein_kcal - fat_kcal, 0.0)
    carbs_g = carbs_kcal / 4
    return MacroTargets(energy_kcal=kcal, protein_g=protein_g, fat_g=fat_g, carbs_g=carbs_g)

