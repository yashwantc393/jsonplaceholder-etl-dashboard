import streamlit as st
import pandas as pd
import altair as alt

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="JSONPlaceholder Analytics",
    layout="wide"
)

st.title("📊 Users, Posts and Todos Analytics Dashboard")

# -----------------------------
# Load Parquet Data
# -----------------------------
users = pd.read_parquet("data/processed/users.parquet")
posts = pd.read_parquet("data/processed/posts.parquet")
comments = pd.read_parquet("data/processed/comments.parquet")
todos = pd.read_parquet("data/processed/todos.parquet")

# -----------------------------
# Pre-computations
# -----------------------------

# Comments per post
comments_per_post = (
    comments.groupby("postId")
    .size()
    .reset_index(name="total_comments")
)

posts_comments = posts.merge(
    comments_per_post,
    left_on="id",
    right_on="postId",
    how="left"
)

posts_comments["total_comments"] = posts_comments["total_comments"].fillna(0)

# Posts per user
posts_per_user = (
    posts.groupby("userId")
    .size()
    .reset_index(name="total_posts")
)

# -----------------------------
# KPI SECTION
# -----------------------------
st.subheader("🔢 Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Users", users["id"].nunique())

with col2:
    st.metric("Total Posts", posts["id"].nunique())

with col3:
    max_post = posts_comments.sort_values(
        "total_comments", ascending=False
    ).iloc[0]
    st.metric("Max Comments on a Post", int(max_post["total_comments"]))

# -----------------------------
# Post with Maximum Comments
# -----------------------------
st.subheader("🏆 Post with Maximum Comments")

st.success(
    f"""
    **Post ID:** {max_post['id']}  
    **Title:** {max_post['title']}  
    **Total Comments:** {int(max_post['total_comments'])}
    """
)

# -----------------------------
# Top 5 Posts by Comments
# -----------------------------
st.subheader("🔥 Top 5 Posts by Comments")

top_5_posts = posts_comments.sort_values(
    "total_comments", ascending=False
).head(5)

st.dataframe(
    top_5_posts[["title", "total_comments"]],
    use_container_width=True
)


# -----------------------------
# Posts per User (by User Name)
# -----------------------------
st.subheader("👤 Posts per User")

# Join posts with users to get user names
posts_users = posts.merge(
    users[["id", "name"]],
    left_on="userId",
    right_on="id",
    how="left"
)

posts_per_user_name = (
    posts_users
    .groupby("name")
    .size()
    .reset_index(name="total_posts")
)

st.bar_chart(
    posts_per_user_name.set_index("name")["total_posts"]
)

# -----------------------------
# Total Todos
# -----------------------------
st.subheader("📊 Todos Overview")

total_todos = len(todos)
st.metric("Total Todos", total_todos)

# -----------------------------
# Completed vs Pending
# -----------------------------
status_counts = (
    todos["completed"]
    .value_counts()
    .reset_index()
)

status_counts.columns = ["completed", "count"]

status_counts["status"] = status_counts["completed"].map({
    True: "Completed",
    False: "Pending"
})


status_chart = (
    alt.Chart(status_counts)
    .mark_bar()
    .encode(
        x=alt.X("status:N", title="Status"),
        y=alt.Y("count:Q", title="Number of Todos"),
        tooltip=["status", "count"]
    )
    .properties(height=300)
)

st.altair_chart(status_chart, use_container_width=True)

# -----------------------------
# Completion Rate (%)
# -----------------------------
completion_rate = round(
    (todos["completed"].sum() / total_todos) * 100, 2
)

st.metric("Overall Completion Rate (%)", f"{completion_rate}%")

# =====================================================
# ⭐ STRONG ANALYTICS
# =====================================================

# -----------------------------
# Completion Rate per User
# -----------------------------
todos_users = todos.merge(
    users[["id", "name"]],
    left_on="userId",
    right_on="id",
    how="left"
)

completion_per_user = (
    todos_users
    .groupby("name")["completed"]
    .mean()
    .reset_index()
)

completion_per_user["completion_rate"] = (
    completion_per_user["completed"] * 100
).round(2)

completion_chart = (
    alt.Chart(completion_per_user)
    .mark_bar(size=10)
    .encode(
        x=alt.X("name:N", sort="-y", title="User"),
        y=alt.Y("completion_rate:Q", title="Completion Rate (%)"),
        tooltip=["name", "completion_rate"]
    )
    .properties(height=400)
)

st.subheader("👤 Completion Rate per User")
st.altair_chart(completion_chart, use_container_width=True)

# -----------------------------
# Top 5 Users by Completion %
# -----------------------------
st.subheader("🏆 Top 5 Users by Completion Rate")

top_5_users = completion_per_user.sort_values(
    by="completion_rate",
    ascending=False
).head(5)

st.dataframe(
    top_5_users[["name", "completion_rate"]],
    use_container_width=True
)


