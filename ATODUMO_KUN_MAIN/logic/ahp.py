import numpy as np

class AHPAnalyzer:
    def __init__(self, weights):
        self.weights = weights
        self.grape_values = [5.90, 5.85, 5.80, 5.78, 5.76, 5.66]
        self.reg_values = [409.6, 385.5, 336.1, 290.1, 268.6, 229.1]

    def _normalize_distance(self, observed, targets, reverse=False):
        distances = [abs(observed - t) for t in targets]
        max_d = max(distances)
        scores = [1 - (d / max_d) if max_d != 0 else 1 for d in distances]
        return scores[::-1] if reverse else scores

    def _interpret_confidence(self, setting, confidence):
        if confidence >= 80:
            verdict = "打つ価値あり！"
        elif confidence >= 60:
            verdict = "微妙…"
        else:
            verdict = "撤退推奨"
        return f"設定{setting}濃厚（{confidence:.1f}%） → {verdict}"

    def evaluate(self, observed_data):
        grape_scores = self._normalize_distance(observed_data['grape'], self.grape_values, reverse=True)
        reg_scores = self._normalize_distance(observed_data['reg'], self.reg_values, reverse=True)
        spins_scores = [min(observed_data['spins'] / 8000, 1.0)] * 6
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
        c
