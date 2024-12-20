from fastapi import FastAPI, HTTPException, Query
import os
from pyarrow.dataset import dataset
from pyarrow import dataset as ds_module
from .config import DATA_DIR, logger

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Search API running"}

@app.get("/search")
async def search(
    src_ip: str = Query(None),
    dst_ip: str = Query(None),
    src_port: int = Query(None),
    date: str = Query(None)
):
    parquet_dir = os.path.join(DATA_DIR, "parquet_data")
    if not os.path.exists(parquet_dir):
        raise HTTPException(status_code=404, detail="No Parquet data available")

    ds = dataset(parquet_dir, format="parquet")
    filter_expressions = []

    # Validate IPs if provided
    if src_ip and not validate_ip(src_ip):
        raise HTTPException(status_code=400, detail="Invalid SRC_IP format")
    if dst_ip and not validate_ip(dst_ip):
        raise HTTPException(status_code=400, detail="Invalid DST_IP format")

    # Build filter expressions for available columns
    if src_ip and "SRC_IP" in ds.schema.names:
        filter_expressions.append(ds_module.field("SRC_IP") == src_ip)
    if dst_ip and "DST_IP" in ds.schema.names:
        filter_expressions.append(ds_module.field("DST_IP") == dst_ip)
    if src_port is not None and "SRC_PORT" in ds.schema.names:
        filter_expressions.append(ds_module.field("SRC_PORT") == src_port)
    if date and "DATE" in ds.schema.names:
        filter_expressions.append(ds_module.field("DATE") == date)

    # Combine all filters with logical AND
    if filter_expressions:
        combined_filter = filter_expressions[0]
        for fexpr in filter_expressions[1:]:
            combined_filter = combined_filter & fexpr
        filtered = ds.to_table(filter=combined_filter)
    else:
        # No filter or columns not in schema: load all data
        filtered = ds.to_table()

    df = filtered.to_pandas()

    # Apply in-memory filtering if columns didn't exist in schema
    if src_ip and "SRC_IP" in df.columns:
        df = df[df["SRC_IP"] == src_ip]
    if dst_ip and "DST_IP" in df.columns:
        df = df[df["DST_IP"] == dst_ip]
    if src_port is not None and "SRC_PORT" in df.columns:
        df = df[df["SRC_PORT"] == src_port]
    if date and "DATE" in df.columns:
        df = df[df["DATE"] == date]

    results = df.to_dict('records')

    if not results:
        raise HTTPException(status_code=404, detail="No records found")

    return results

def validate_ip(ip):
    import re
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    return re.match(pattern, ip) is not None

