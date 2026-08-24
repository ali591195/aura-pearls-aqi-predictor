from pathlib import Path

from src.common.hopsworks_client import engineered_daily_fs

# The output path
OUTPUT_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "engineered_features.parquet"
)

def main():
    # Getting all engineered data
    df = engineered_daily_fs.read()

    # Storing to parquet for reuse
    df.to_parquet(OUTPUT_PATH, index=False)

if __name__ == "__main__":
    main()