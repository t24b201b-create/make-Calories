# -*- coding: utf-8 -*-
"""
test_backend.py
学食メニューCSVを読み込み、検索/表示/集計を行う簡易CLI。
- CSVは test_backend.py と同じディレクトリの
  'niigata_univ_dai1_shokudo_nutrition.csv' を自動参照
- 使い方の例はファイル末尾を参照
"""

from __future__ import annotations
from pathlib import Path
import argparse
import sys
from typing import List

from cafeteria_menu_helpers import (
    load_menu,
    search as search_dishes,
    get_by_name,
    summarize_total,
)

CSV_PATH = Path(__file__).with_name("niigata_univ_dai1_shokudo_nutrition.csv")


def ensure_csv_exists(csv_path: Path) -> None:
    if not csv_path.exists():
        sys.stderr.write(f"[ERROR] CSV not found: {csv_path}\n")
        sys.stderr.write("       ファイルの位置を確認するか、ファイル名を揃えてください。\n")
        sys.exit(1)


def fmt_price(yen):
    return f"¥{yen}" if isinstance(yen, int) else "-"


def fmt_num(x):
    return "-" if x is None else (str(int(x)) if float(x).is_integer() else f"{x}")


def cmd_stats(args):
    """件数と代表的な項目を表示"""
    ensure_csv_exists(CSV_PATH)
    dishes = load_menu(CSV_PATH)
    print(f"件数: {len(dishes)}")
    # 最初の数件だけ表示
    for d in dishes[: min(5, len(dishes))]:
        print(f"- {d.name} | {fmt_price(d.price_yen)} | kcal={fmt_num(d.get('energy_kcal'))}")


def cmd_search(args):
    """キーワード検索して上位N件を表示"""
    ensure_csv_exists(CSV_PATH)
    dishes = load_menu(CSV_PATH)
    results = search_dishes(dishes, args.keyword)
    if not results:
        print("該当なし")
        return
    print(f"ヒット: {len(results)} 件（先頭 {args.limit} 件）")
    for d in results[: args.limit]:
        kcal = fmt_num(d.get("energy_kcal"))
        protein = fmt_num(d.get("protein_g"))
        fat = fmt_num(d.get("fat_g"))
        carb = fmt_num(d.get("carbs_g"))
        print(f"- {d.name} | {fmt_price(d.price_yen)} | kcal={kcal} P={protein}g F={fat}g C={carb}g")


def cmd_show(args):
    """完全一致で1件表示"""
    ensure_csv_exists(CSV_PATH)
    dishes = load_menu(CSV_PATH)
    d = get_by_name(dishes, args.name)
    if not d:
        print("見つかりませんでした。まずは search で候補を確認してください。")
        return
    print(f"[{d.name}]")
    print(f"価格: {fmt_price(d.price_yen)}")
    print(f"URL : {d.url or '-'}")
    print("栄養素:")
    for k in [
        "energy_kcal",
        "protein_g",
        "fat_g",
        "carbs_g",
        "salt_g",
        "calcium_mg",
        "vegetables_g",
        "iron_mg",
        "vitaminA_ugRAE",
        "vitaminB1_mg",
        "vitaminB2_mg",
        "vitaminC_mg",
    ]:
        v = d.get(k)
        print(f"  - {k}: {fmt_num(v)}")


def cmd_sum(args):
    """キーワード部分一致の集合を合計（セット計算向け）"""
    ensure_csv_exists(CSV_PATH)
    dishes = load_menu(CSV_PATH)
    target = [d for d in dishes if args.keyword in d.name]
    if not target:
        print("該当なし")
        return
    total = summarize_total(target)
    print(f"対象件数: {len(target)}")
    print("合計値:")
    for k in [
        "energy_kcal",
        "protein_g",
        "fat_g",
        "carbs_g",
        "salt_g",
        "calcium_mg",
        "vegetables_g",
        "iron_mg",
        "vitaminA_ugRAE",
        "vitaminB1_mg",
        "vitaminB2_mg",
        "vitaminC_mg",
    ]:
        print(f"  - {k}: {fmt_num(total.get(k))}")


def cmd_topkcal(args):
    """kcalの高い順 上位N件を表示"""
    ensure_csv_exists(CSV_PATH)
    dishes = load_menu(CSV_PATH)
    ds = [d for d in dishes if d.get("energy_kcal") is not None]
    ds.sort(key=lambda d: d.get("energy_kcal"), reverse=True)
    print(f"kcal上位 {args.n} 件")
    for d in ds[: args.n]:
        print(f"- {d.name} | {fmt_price(d.price_yen)} | kcal={fmt_num(d.get('energy_kcal'))}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="学食メニューCSV テスト用CLI")
    sub = p.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("stats", help="件数とサンプル表示")
    sp.set_defaults(func=cmd_stats)

    sp = sub.add_parser("search", help="キーワード検索（部分一致/前方一致）")
    sp.add_argument("keyword", type=str, help="検索キーワード（例: ラーメン）")
    sp.add_argument("-n", "--limit", type=int, default=10, help="表示件数")
    sp.set_defaults(func=cmd_search)

    sp = sub.add_parser("show", help="完全一致で1件表示（まずは search で名称確認推奨）")
    sp.add_argument("name", type=str, help="メニュー完全名")
    sp.set_defaults(func=cmd_show)

    sp = sub.add_parser("sum", help="名前に含むキーワードで絞って合計（セット計算など）")
    sp.add_argument("keyword", type=str, help="例: カレー")
    sp.set_defaults(func=cmd_sum)

    sp = sub.add_parser("topkcal", help="kcal上位N件を表示")
    sp.add_argument("-n", type=int, default=10)
    sp.set_defaults(func=cmd_topkcal)

    return p


def main(argv: List[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
