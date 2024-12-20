import os
import logging

# Configuration values
DATA_DIR = os.getenv("DATA_DIR", "/nfacct/data")

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger("nfacct_app")
