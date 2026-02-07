class ScoringEngine:
    def __init__(self, config):
        self.weights = config.SCORING_WEIGHTS

    def apply_weights(self, analysis):
        total = 0.0
        for key, param in analysis["parameters"].items():
            w = self.weights.get(key, 0)
            s = param.get("score", 0)
            ws = (s * w) / 100.0
            param["weight"] = w
            param["weighted_score"] = round(ws, 2)
            total += ws
        analysis["overall_score"] = round(total, 2)
        if total >= 85:
            rec = "Strong Match"
        elif total >= 70:
            rec = "Good Match"
        elif total >= 55:
            rec = "Moderate Match"
        elif total >= 40:
            rec = "Weak Match"
        else:
            rec = "Poor Match"
        analysis["recommendation"] = rec
        return analysis

    def to_matrix(self, analysis):
        rows = []
        for name, param in analysis["parameters"].items():
            rows.append(
                {
                    "parameter": name.replace("_", " ").title(),
                    "score": param["score"],
                    "weight": param["weight"],
                    "weighted_score": param["weighted_score"],
                    "rationale": param["rationale"],
                    "examples": param["examples"],
                }
            )
        rows.sort(key=lambda r: r["weight"], reverse=True)
        return rows
