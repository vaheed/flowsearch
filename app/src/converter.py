import os
from .config import DATA_DIR, logger
from .utils import convert_csv_to_parquet

def convert_all_csv_in_directory(data_dir=DATA_DIR):
    """
    Convert all CSV files found in the directory and subdirectories to Parquet.
    Remove CSV after successful conversion.
    """
    logger.info("Starting CSV to Parquet conversion...")
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.csv'):
                csv_path = os.path.join(root, file)
                success = convert_csv_to_parquet(csv_path, data_dir)
                if success:
                    os.remove(csv_path)
                    logger.info(f"Removed original CSV: {csv_path}")
    logger.info("CSV to Parquet conversion completed.")

