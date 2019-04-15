import pandas as pd
from constant import GAME_RECORDS_PATH


class Record:
    """
        records: [
            {
                "name": "Player-001",
                "score": 26,
                "datetime": "2019-04-15 22:29:47",
            }
        ]
    """
    def __init__(self, records_path=GAME_RECORDS_PATH):
        self.records_path = records_path
        try:
            self.df = pd.read_json(records_path)
        except Exception:
            self.df = pd.DataFrame([])

    def add(self, record):
        self.df = self.df.append(pd.DataFrame([record]), ignore_index=True)
        self.df.to_json(self.records_path, orient='records')
