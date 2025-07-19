# logic/utils/estimator.py

JUGGLER_DATA = {
    "bonus": {
        1: 1 / 163.8,
        2: 1 / 159.1,
        3: 1 / 148.6,
        4: 1 / 135.2,
        5: 1 / 126.8,
        6: 1 / 114.6,
    },
    "reg": {
        1: 1 / 409.6,
        2: 1 / 385.5,
        3: 1 / 336.1,
        4: 1 / 290.1,
        5: 1 / 268.6,
        6: 1 / 229.1,
    },
    "budou": {
        1: 1 / 5.90,
        2: 1 / 5.85,
        3: 1 / 5.80,
        4: 1 / 5.78,
        5: 1 / 5.76,
        6: 1 / 5.66,
    }
}


def estimate_budou_prob(spin_count: int, total_bonus: int, diff_medals: int) -> float:
    """
    差枚数とボーナス、回転数からブドウ確率を推定（ざっくり）
    """
    # 消化したメダルを推定
    used_medals = spin_count * 3  # 1回転 = 3枚ベース
    got_medals = diff_medals + (total_bonus * 100)  # 100枚/ボーナスで仮定

    net_used = used_medals - got_medals
    if net_used <= 0:
        return 1 / 5.5  # 出過ぎた場合は高設定寄り仮定

    estimated_budou_count = net_used / 8  # ブドウ1回あたり8枚仮定
    return spin_count / estimated_budou_count


def get_score(actual: float, expected: float) -> float:
    """
    実測値と期待値のズレをスコア化（差の絶対値）
    値が小さいほど良い（近い）
    """
    return abs(actual - expected)


def evaluate_setting_scores(big: int, reg: int, spins: int, diff: int) -> dict:
    """
    各設定のスコアを計算して返す
    """
    result = {}
    total_bonus = big + reg
    actual_bonus_prob = spins / total_bonus if total_bonus > 0 else 999
    actual_reg_prob = spins / reg if reg > 0 else 999
    actual_budou_prob = estimate_budou_prob(spins, total_bonus, diff)

    for setting in range(1, 7):
        s_bonus = JUGGLER_DATA["bonus"][setting]
        s_reg = JUGGLER_DATA["reg"][setting]
        s_budou = JUGGLER_DATA["budou"][setting]

        score_bonus = get_score(1 / actual_bonus_prob, s_bonus)
        score_reg = get_score(1 / actual_reg_prob, s_reg)
        score_budou = get_score(actual_budou_prob, s_budou)

        result[setting] = {
            "bonus_score": score_bonus,
            "reg_score": score_reg,
            "budou_score": score_budou
        }

    return result
