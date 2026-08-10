from src.feature_pipeline.hopsworks_client import raw_hourly_fs

df = raw_hourly_fs.read()
print(df.shape[0])