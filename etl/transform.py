import json
import pandas as pd

def transform_posts():
    with open("data/raw/posts.json") as f:
        posts = json.load(f)

    df = pd.DataFrame(posts)

    # Derived field
    df["title_length"] = df["title"].str.len()

    return df

def transform_users():
    with open("data/raw/users.json") as f:
        users = json.load(f)

    df = pd.DataFrame(users)

    return df

def transform_comments():
    with open("data/raw/comments.json") as f:
        comments = json.load(f)

    df = pd.DataFrame(comments)

    return df

def transform_todos():
    with open("data/raw/todos.json") as f:
        todos = json.load(f)

    df = pd.DataFrame(todos)

    return df

