import csv
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

@dataclass(frozen=True)
class Dish:
    dish_id: str
    name: str
    portion: str
    calories_kcal: float
    synonyms: Tuple[str, ...]

def load_menu(csv_path: str) -> Dict[str, Dish]:
    """cafeteria_menu.csv を読み込む"""
    dishes: Dict[str, Dish] = {}
    
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        if reader.fieldnames:
            reader.fieldnames = [h.strip().lstrip("\ufeff") for h in reader.fieldnames]

        for row in reader:
            
            row = {k.strip().lstrip("\ufeff"): v for k, v in row.items()}

            syns = tuple(s.strip() for s in (row.get("synonyms") or "").split(",") if s.strip())
            d = Dish(
                dish_id=row["dish_id"],
                name=row["name"],
                portion=row.get("portion", ""),
                calories_kcal=float(row["calories_kcal"]),
                synonyms=syns,
            )
            dishes[d.dish_id] = d
    return dishes

def build_alias_index(dishes: Dict[str, Dish]) -> Dict[str, str]:
    idx: Dict[str, str] = {}
    for did, dish in dishes.items():
        idx[dish.name] = did
        for s in dish.synonyms:
            idx[s] = did
    return idx

def find_dish_id(query: str, alias_index: Dict[str, str]) -> Optional[str]:
    q = (query or "").strip().lower()
    for key, did in alias_index.items():
        if q == key.lower():
            return did
    for key, did in alias_index.items():
        if q in key.lower():
            return did
    return None

def kcal_by_name(query: str, dishes: Dict[str, Dish]) -> Optional[float]:
    alias = build_alias_index(dishes)
    did = find_dish_id(query, alias)
    if did is None:
        return None
    return dishes[did].calories_kcal

def sum_kcal(order_items: List[Tuple[str, int]], dishes: Dict[str, Dish]) -> Tuple[float, List[Tuple[str, float, int]]]:
    """
    order_items: [("料理名または同義語", 数量), ...]
    return: (合計kcal, [(実際の料理名, kcal, 数量)])
    """
    alias = build_alias_index(dishes)
    total = 0.0
    breakdown: List[Tuple[str, float, int]] = []
    for name, qty in order_items:
        did = find_dish_id(name, alias)
        if did is None:
            continue
        d = dishes[did]
        total += d.calories_kcal * qty
        breakdown.append((d.name, d.calories_kcal, qty))
    return round(total, 1), breakdown
