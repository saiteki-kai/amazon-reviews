import subprocess
from pathlib import Path
from sys import platform

from reviews.models.base import BaseModel


class JST(BaseModel):
    def __init__(self, model_path, input_dir, output_dir):
        super().__init__(
            model_path=model_path,
            input_dir=input_dir,
            output_dir=output_dir,
        )

    def estimate(self, alpha, beta, gamma, n_topics, iterations=1000):
        filename = "jst" if platform == "linux" else "jst.exe"

        subprocess.call(
            [
                Path(self.model_path) / filename,
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
                "-datasetFile",
                "docs.dat",
                "-nsentiLabs",
                "2",
                "-sentiFile",
                Path(self.input_dir) / "sentiwords.txt",
            ],
        )
