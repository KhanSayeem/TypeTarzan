import json
import os
from datetime import date
class Storage:
    def __init__(self, filepath="data/scores.json"):
        self.filepath = filepath
        self._ensure_file()
    def _ensure_file(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            self._write(self._default_data())
    def _default_data(self):
        return {
            "wins": 0,
            "losses": 0,
            "best_wpm": 0,
            "high_scores": []
        }
    def _read(self):
        with open(self.filepath, "r") as f:
            return json.load(f)
    def _write(self, data):
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=4)
    def _add_result(self, wpm, difficulty, result):
        data = self._read()
        if result == "win":
            data["wins"] += 1
        else:
            data["losses"] += 1
        if wpm > data["best_wpm"]:
            data["best_wpm"] = wpm
        existing_ids = [s.get("id", 0) for s in data["high_scores"]]
        new_id = max(existing_ids, default=0) + 1
        data["high_scores"].append({
            "id": new_id,
            "wpm": wpm,
            "difficulty": difficulty,
            "result": result,
            "date": str(date.today())
        })
        data["high_scores"] = sorted(
            data["high_scores"], key=lambda x: x["wpm"], reverse=True
        )[:20]
        self._write(data)
    def get_high_scores(self):
        """Read — returns all stored scores."""
        return self._read()["high_scores"]
    def search_scores(self, difficulty=None, result=None):
        """Search + Filter — filter scores by difficulty and/or result."""
        scores = self.get_high_scores()
        if difficulty and difficulty != "all":
            scores = [s for s in scores if s["difficulty"] == difficulty]
        if result and result != "all":
            scores = [s for s in scores if s["result"] == result]
        return scores
    def sort_scores(self, scores, key="wpm", reverse=True):
        valid_keys = {"wpm", "date", "difficulty", "result"}
        if key not in valid_keys:
            key = "wpm"
        return sorted(scores, key=lambda x: x.get(key, 0), reverse=reverse)
    def delete_score(self, score_id):
        data = self._read()
        before = len(data["high_scores"])
        data["high_scores"] = [
            s for s in data["high_scores"] if s.get("id") != score_id
        ]
        if len(data["high_scores"]) == before:
            return False  # nothing was deleted
        data["wins"]     = sum(1 for s in data["high_scores"] if s["result"] == "win")
        data["losses"]   = sum(1 for s in data["high_scores"] if s["result"] == "loss")
        data["best_wpm"] = max((s["wpm"] for s in data["high_scores"]), default=0)
        self._write(data)
        return True
    def get_lifetime_stats(self):
        data   = self._read()
        scores = data["high_scores"]
        avg    = round(sum(s["wpm"] for s in scores) / len(scores)) if scores else 0
        return {
            "wins":     data["wins"],
            "losses":   data["losses"],
            "best_wpm": data["best_wpm"],
            "avg_wpm":  avg,
            "total":    len(scores)
        }