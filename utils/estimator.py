# 設定推定ロジック（簡易）
def estimate_setting(game_count, big, reg, diff):
    reg_rate = game_count / (reg + 1e-5)
    if reg_rate <= 229:
        return 6
    elif reg_rate <= 268:
        return 5
    elif reg_rate <= 290:
        return 4
    elif reg_rate <= 336:
        return 3
    elif reg_rate <= 385:
        return 2
    else:
        return 1
