import pandas as pd

df = pd.read_csv("data/raw_posts.csv")
errors = []

# 1. Row count
if len(df) != 400:
    errors.append(f"Expected 400 rows, got {len(df)}")

# 2. No null post_ids
if df["post_id"].isnull().any():
    errors.append("Null post_ids found")

# 3. Reach must be positive
if (df["reach"] <= 0).any():
    errors.append("Zero or negative reach values found")

# 4. Engagement rate sanity check
bad_eng = df[df["engagement_rate"] > 50]
if len(bad_eng) > 0:
    errors.append(f"{len(bad_eng)} rows with eng_rate > 50%")

# 5. Both platforms present
platforms = df["platform"].unique().tolist()
if sorted(platforms) != ["meta", "tiktok"]:
    errors.append(f"Unexpected platforms: {platforms}")

# 6. Date range within last 90 days
df["post_date"] = pd.to_datetime(df["post_date"])
old = df[df["post_date"] < pd.Timestamp.now() - pd.Timedelta(days=91)]
if len(old) > 0:
    errors.append(f"{len(old)} posts older than 90 days")

if errors:
    print("VALIDATION FAILED:")
    for e in errors: print(f"  x {e}")
else:
    print("All validation checks passed.")
    print(f"  Rows: {len(df)}")
    print(f"  Platforms: {df.platform.value_counts().to_dict()}")
    print(f"  Formats: {df.format.nunique()} unique")
    print(f"  Avg eng rate: {df.engagement_rate.mean():.2f}%")