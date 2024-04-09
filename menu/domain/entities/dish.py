import dataclasses

@dataclasses.dataclass
class Dish:
    id: int
    name: str
    description: str
    price: float

    @classmethod
    def from_dict(self,d):
        return self(**d)

    def to_dict(self):
        return dataclasses.asdict(self)
