from abc import ABC, abstractmethod


class BaseModel(ABC):
    def __init__(
        self,
        model_path: str,
        input_dir: str,
        output_dir: str,
    ):
        self.model_path = model_path
        self.input_dir = input_dir
        self.output_dir = output_dir

    @abstractmethod
    def estimate(
        self,
        alpha: float,
        beta: list[float],
        gamma: list[float],
        n_topics: int,
        iterations: int,
    ):
        pass
