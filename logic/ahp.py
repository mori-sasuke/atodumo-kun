# AHPベースの信頼度算出
def calculate_trust(game_count, big, reg, diff, is_special_day):
    weight_game = 0.3
    weight_reg = 0.3
    weight_grape = 0.3
    weight_special = 0.1

    grape_rate = (big + reg) * 6  # 推定ぶどう回数
    expected_grape = game_count / 5.8
    grape_score = min(grape_rate / expected_grape, 1.0)

    reg_rate = game_count / (reg + 1e-5)
    reg_score = max(0, min(1, (1/290.1) / (1/reg_rate)))

    game_score = min(game_count / 6000, 1.0)
    special_score = 1.0 if is_special_day else 0.7

    trust = 100 * (weight_game * game_score + weight_reg * reg_score +
                   weight_grape * grape_score + weight_special * special_score)
    return trust
