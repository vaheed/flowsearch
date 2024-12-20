import os
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
from datetime import datetime
from .config import logger
import dask.dataframe as dd

def convert_csv_to_parquet(csv_path, output_base_dir):
    """
    Convert a CSV file to a Parquet file, partitioning by date.
    """
    try:
        # Read as Dask DataFrame
        ddf = dd.read_csv(csv_path)
        # Convert to Pandas DataFrame before Pandas operations
        df = ddf.compute()

        # Ensure TIMESTAMP_START is parsed as datetime if needed
        if 'TIMESTAMP_START' in df.columns:
            df['TIMESTAMP_START'] = pd.to_datetime(df['TIMESTAMP_START'], errors='coerce')

        # Derive date partition from TIMESTAMP_START
        if 'TIMESTAMP_START' in df.columns and not df['TIMESTAMP_START'].isna().all():
            df['DATE'] = df['TIMESTAMP_START'].dt.date.astype(str)
        else:
            # fallback if missing or invalid
            df['DATE'] = 'unknown_date'

        table = pa.Table.from_pandas(df)
        dataset_dir = os.path.join(output_base_dir, "parquet_data")

        # Write in a partitioned manner by DATE
        pq.write_to_dataset(
            table,
            root_path=dataset_dir,
            partition_cols=["DATE"],
            use_dictionary=True,
            compression='snappy'
        )
        logger.info(f"Converted {csv_path} to Parquet and partitioned by DATE.")
        return True
    except Exception as e:
        logger.error(f"Error converting {csv_path} to Parquet: {e}")
        return False

