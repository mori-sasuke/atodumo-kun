# メインスクリプト
from logic.ahp import calculate_trust
from utils.estimator import estimate_setting
import json
import os

def main():
    print("後ヅモくん 起動中...")
    game_count = int(input("ゲーム数: "))
    big = int(input("BIG回数: "))
    reg = int(input("REG回数: "))
    diff = int(input("差枚数: "))
    is_special_day = input("特定日ですか？ (y/n): ").lower() == 'y'

    if game_count < 3000:
        print("回転数不足。まだ打つのはやめておきましょう。")
        return

    setting = estimate_setting(game_count, big, reg, diff)
    trust = calculate_trust(game_count, big, reg, diff, is_special_day)

    print(f"設定{setting}最有力（信頼度: {trust:.1f}%）")

if __name__ == "__main__":
    main()
