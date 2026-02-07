from flask import Blueprint, render_template, current_app
from ..analyzers.ai_engine import AIEngine
from ..analyzers.scoring_engine import ScoringEngine

analysis_bp = Blueprint("analysis", __name__)

@analysis_bp.route("/analysis_dummy", methods=["GET"])
def analysis_dummy():
    return "OK"

def run_analysis(resume_text, jd_text):
    cfg = current_app.config
    ai = AIEngine(cfg)
    scorer = ScoringEngine(cfg)

    raw = ai.analyze(resume_text, jd_text)
    scored = scorer.apply_weights(raw)
    matrix = scorer.to_matrix(scored)

    return render_template("index.html", analysis=scored, matrix=matrix)
