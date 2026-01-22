from etl.transform import transform_posts
from etl.load import save_parquet

def main():
    df = transform_posts()
    save_parquet(df, "posts")

if __name__ == "__main__":
    main()
