from pathlib import Path

bin_dir = Path('../bin')
data_dir = Path('../data')
out_dir = Path('../output')

raw_data_dir = data_dir / 'raw'
processed_data_dir = data_dir / 'processed'

asum_model_path = bin_dir / 'ASUM.jar'

asum_input_dir =  data_dir / "asum"
asum_output_dir = out_dir / "asum"