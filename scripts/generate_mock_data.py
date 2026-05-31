import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()
np.random.seed(42)

def gen_posts(platform, n=200):
    formats = {
        "tiktok": ["video", "live", "stitch", "duet"],
        "meta":   ["reel", "carousel", "story", "image", "text"]
    }
    topics = ["product_launch", "ugc", "tutorial",
              "trend", "creator_collab", "brand_campaign"]
    rows = []
    for _ in range(n):
        reach = np.random.randint(1000, 500000)
        fmt   = random.choice(formats[platform])
        creator = random.random() < 0.4
        if creator:
            reach = int(reach * random.uniform(1.2, 2.5))
        rows.append({
            "post_id":        fake.uuid4(),
            "platform":       platform,
            "format":         fmt,
            "topic":          random.choice(topics),
            "post_date":      fake.date_between("-90d", "today"),
            "reach":          reach,
            "impressions":    int(reach * random.uniform(1.1, 2.5)),
            "likes":          int(reach * random.uniform(0.02, 0.18)),
            "comments":       int(reach * random.uniform(0.001, 0.03)),
            "shares":         int(reach * random.uniform(0.001, 0.05)),
            "saves":          int(reach * random.uniform(0.005, 0.04)),
            "video_views":    int(reach * random.uniform(0.3, 0.9))
                              if fmt in ["video","reel","live"] else 0,
            "creator_post":   creator,
            "brand":          "UrbanWear NL",
            "week":           None
        })
    df = pd.DataFrame(rows)
    df["post_date"] = pd.to_datetime(df["post_date"])
    df["week"]      = df["post_date"].dt.to_period("W").astype(str)
    df["engagement_rate"] = (
        (df.likes + df.comments + df.shares + df.saves)
        / df.reach * 100
    ).round(2)
    return df

tiktok_df = gen_posts("tiktok", 200)
meta_df   = gen_posts("meta",   200)
df = pd.concat([tiktok_df, meta_df], ignore_index=True)

df.to_csv("data/raw_posts.csv", index=False)
print(f"Generated {len(df)} rows")
print(df[["platform","format","reach","engagement_rate"]].describe().round(2))