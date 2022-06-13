import os
from pathlib import Path

root_dir = Path(os.path.dirname(os.path.realpath(__file__))).parent

bin_dir = root_dir / "bin"
data_dir = root_dir / "data"
out_dir = root_dir / "output"

raw_data_dir = data_dir / "raw"
processed_data_dir = data_dir / "processed"

asum_model_path = bin_dir / "ASUM.jar"

asum_input_dir = data_dir / "asum"
asum_output_dir = out_dir / "asum"
