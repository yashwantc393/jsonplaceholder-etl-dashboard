import os
from etl.transform import (
    transform_posts,
    transform_users,
    transform_comments,
    transform_todos
)

def save_all_parquet():
    os.makedirs("data/processed", exist_ok=True)

    transform_posts().to_parquet(
        "data/processed/posts.parquet", index=False
    )

    transform_users().to_parquet(
        "data/processed/users.parquet", index=False
    )

    transform_comments().to_parquet(
        "data/processed/comments.parquet", index=False
    )

    transform_todos().to_parquet(
        "data/processed/todos.parquet", index=False
    )

if __name__ == "__main__":
    save_all_parquet()
