from logic.utils.estimator import evaluate_setting_scores
from logic.ahp import AHPAnalyzer

def get_user_input():
    print("==== 後ヅモくん ====")
    big = int(input("BIG回数: "))
    reg = int(input("REG回数: "))
    spins = int(input("総回転数: "))
    diff = int(input("差枚数（マイナスもOK）: "))
    tokubi = input("今日は特定日ですか？ (y/n): ").strip().lower() == 'y'
    return big, reg, spins, diff, tokubi

def summarize_result(best_setting, confidence):
    if confidence >= 90:
        label = "打つ価値あり（かなり有望）"
    elif confidence >= 75:
        label = "まあまあアリ"
    elif confidence >= 60:
        label = "微妙…"
    else:
        label = "撤退推奨"

    return f"設定{best_setting} 最有力（信頼度{confidence:.1f}%） → {label}"

def main():
    big, reg, spins, diff, tokubi = get_user_input()

    if spins < 3000:
        print("⚠ 回転数が3000未満のため、信頼性が低く評価できません。")
        return

    setting_scores = evaluate_setting_scores(big, reg, spins, diff)

    # 実測データ抽出（設定ごとの平均は取らない）
    total_bonus = big + reg
    bonus_prob = spins / total_bonus if total_bonus > 0 else 999
    reg_prob = spins / reg if reg > 0 else 999
    grape_prob = 1 / setting_scores[1]['budou_score'] if setting_scores[1]['budou_score'] > 0 else 5.9

    # 重みの初期案
    weights = {
        'grape': 0.4,
        'reg': 0.3,
        'spins': 0.2,
        'tokubi': 0.1
    }

    analyzer = AHPAnalyzer(weights)
    result = analyzer.evaluate({
        'grape': grape_prob,
        'reg': reg_prob,
        'spins': spins,
        'tokubi': tokubi
    })

    print("=== 推定結果 ===")
    print(summarize_result(result['best_setting'], result['confidence']))

if __name__ == "__main__":
    main()
