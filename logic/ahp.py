import numpy as np

class AHPAnalyzer:
    def __init__(self, weights):
        """
        weights = {
            'grape': 0.4,
            'reg': 0.3,
            'spins': 0.2,
            'tokubi': 0.1
        }
        """
        self.weights = weights

        # 理論値（設定1〜6）
        self.grape_values = [5.90, 5.85, 5.80, 5.78, 5.76, 5.66]
        self.reg_values = [409.6, 385.5, 336.1, 290.1, 268.6, 229.1]

    def _normalize_distance(self, observed, targets, reverse=False):
        """
        observed: 実測値
        targets: 各設定の理論値（リスト）
        reverse: 値が小さいほど優秀な場合 True（ブドウとか）
        """
        distances = []
        for t in targets:
            diff = abs(observed - t)
            distances.append(diff)

        max_d = max(distances)
        scores = [1 - (d / max_d) if max_d != 0 else 1 for d in distances]
        return scores[::-1] if reverse else scores

    def evaluate(self, observed_data):
        """
        observed_data = {
            'grape': 6.0,
            'reg': 270.0,
            'spins': 3000,
            'tokubi': True
        }
        """

        grape_scores = self._normalize_distance(observed_data['grape'], self.grape_values, reverse=True)
        reg_scores = self._normalize_distance(observed_data['reg'], self.reg_values, reverse=True)

        # 回転数（多いほどよい）
        spins_scores = [min(observed_data['spins'] / 8000, 1.0)] * 6

        # 特定日（Trueで0.8固定、Falseなら0.5固定）
        tokubi_score = 0.8 if observed_data['tokubi'] else 0.5
        tokubi_scores = [tokubi_score] * 6

        final_scores = []
        for i in range(6):
            total = (
                grape_scores[i] * self.weights['grape'] +
                reg_scores[i] * self.weights['reg'] +
                spins_scores[i] * self.weights['spins'] +
                tokubi_scores[i] * self.weights['tokubi']
            )
            final_scores.append(total)

        max_score = max(final_scores)
        confidences = [(s / max_score) * 100 for s in final_scores]

        best_setting = np.argmax(final_scores) + 1
        best_confidence = round(confidences[best_setting - 1], 1)

        return {
            'setting_scores': confidences,
            'best_setting': best_setting,
            'confidence': best_confidence,
        }
