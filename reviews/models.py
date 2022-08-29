from operator import sub
from pickle import TRUE
import subprocess

from reviews.config import asum_input_dir, asum_model_path, asum_output_dir


def asum(alpha, beta, gamma, n_topics, iterations="1000"):
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
            n_topics,
            "-th",
            "3",
            "-i",
            iterations,
            "-d",
            asum_input_dir,
            "-o",
            asum_output_dir,
        ]
    )

def jst(config_file_path):
    subprocess.call("jst -est -config "+config_file_path)