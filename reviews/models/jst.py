import subprocess
from pathlib import Path

from reviews.models.base import BaseModel


class JST(BaseModel):
    def __init__(self, model_path, input_dir, output_dir):
        super().__init__(
            model_path=model_path,
            input_dir=input_dir,
            output_dir=output_dir,
        )

    def estimate(self, alpha, beta, gamma, n_topics, iterations=1000):
        subprocess.call(
            [
                Path(self.model_path) / "jst",
                "-est",
                "-alpha",
                str(alpha),
                "-beta",
                str(beta),
                "-gamma",
                str(gamma),
                "-ntopics",
                str(n_topics),
                "-niters",
                str(iterations),
                "-result_dir",
                self.output_dir,
                "-data_dir",
                self.input_dir,
            ],
        )
