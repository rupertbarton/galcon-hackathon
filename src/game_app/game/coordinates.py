class Coordinates:
    def __init__(
        self,
        x: float,
        y: float,
    ):
        self.x = x
        self.y = y

    def to_json(self):
        return {"x": round(self.x, 3), "y": round(self.y, 3)}
