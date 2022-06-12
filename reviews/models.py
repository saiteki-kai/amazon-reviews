import subprocess

from reviews.config import asum_model_path


def asum(inputDir, outputDir, alpha, beta, gamma, nTopics, iterations="1000"):
    subprocess.call(
        [
            "java",
            "-jar",
            asum_model_path,
            "-a",
            alpha,
            "-b",
            beta,
            "-g",
            gamma,
            "-t",
            nTopics,
            "-th",
            "3",
            "-i",
            iterations,
            "-d",
            inputDir,
            "-o",
            outputDir,
        ]
    )
