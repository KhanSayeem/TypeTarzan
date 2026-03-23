import json 
import os
from datetime import date
class Storage:
    def __init__(self, filepath = "date/scores.json"):
        self.filepath = filepath
        self._file_exists()
    
    def _file_exists(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok = True)
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
    
    def _write(self, data ):
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent = 4 )
  

    def _add_result(self, result, difficulty, wpm):
        data = self._read()

        if result == "win":
            data[wins] += 1
        else:
            data[losses] += 1

        if wpm > data["best_wpm"]:
            data[best_wpm] = wpm
        
        data[high_scores].append({
            "wpm": wpm,
            "difficulty": difficulty,
            "result": result,
            "date": str(date.today())
        })
    
        data["high_scores"] = sorted(
            data["high_scores"] , key = lambda x: x["wpm"], reverse = True
        )[:10]
        
        self._write(data)

        def get_stats(self):
            data = self._read()
            return{
                "wins": data["wins"],
                "losses": data["losses"],
                "best_wpm": data["best_wpm"]
            }
        
        def get_highscores(self):
            data = self._read()
            return data["high_scores"]