import subprocess

from reviews.models.base import BaseModel


class ASUM(BaseModel):
    def __init__(self, model_path, input_dir, output_dir):
        super().__init__(
            model_path=model_path,
            input_dir=input_dir,
            output_dir=output_dir,
        )

    def estimate(self, alpha, beta, gamma, n_topics, iterations=1000):
        subprocess.call(
            [
                "java",
                "-jar",
                self.model_path,
                "-a",
                str(alpha),
                "-b",
                "/".join([str(x) for x in beta]),
                "-g",
                "/".join([str(x) for x in gamma]),
                "-th",
                "3",
                "-t",
                str(n_topics),
                "-i",
                str(iterations),
                "-d",
                self.input_dir,
                "-o",
                self.output_dir,
            ]
        )
