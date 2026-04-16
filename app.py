import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = "data/expenses.csv"

st.set_page_config(page_title="Expense Tracker", layout="wide")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        st.error("Run main.py first to generate dataset.")
        st.stop()

    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# -----------------------------
# 🔥 FIX MISSING COLUMNS (IMPORTANT)
# -----------------------------
if "month_num" not in df.columns:
    df["month_num"] = df["date"].dt.month

if "month" not in df.columns:
    df["month"] = df["date"].dt.month_name()

# -----------------------------
# HEADER
# -----------------------------
st.title("💰 Expense Tracker Dashboard")

# -----------------------------
# KPIs
# -----------------------------
total = df["amount"].sum()
avg = df["amount"].mean()
max_val = df["amount"].max()
top_cat = df.groupby("category")["amount"].sum().idxmax()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Spending", f"₹{total:,.0f}")
col2.metric("Average", f"₹{avg:,.0f}")
col3.metric("Max Expense", f"₹{max_val:,.0f}")
col4.metric("Top Category", top_cat)

st.divider()

# -----------------------------
# CATEGORY ANALYSIS
# -----------------------------
st.subheader("📊 Category Analysis")

cat_data = df.groupby("category")["amount"].sum().reset_index()

fig1, ax1 = plt.subplots()
sns.barplot(data=cat_data, x="category", y="amount", ax=ax1)
plt.xticks(rotation=45)
st.pyplot(fig1)

# -----------------------------
# MONTHLY TREND (FIXED)
# -----------------------------
st.subheader("📈 Monthly Trend")

month_data = (
    df.groupby(["month_num", "month"])["amount"]
    .sum()
    .reset_index()
    .sort_values("month_num")
)

fig2, ax2 = plt.subplots()
sns.lineplot(data=month_data, x="month", y="amount", marker="o", ax=ax2)
plt.xticks(rotation=45)
st.pyplot(fig2)

# -----------------------------
# PIE CHART
# -----------------------------
st.subheader("🥧 Expense Distribution")

fig3, ax3 = plt.subplots()
ax3.pie(cat_data["amount"], labels=cat_data["category"], autopct="%1.1f%%")
st.pyplot(fig3)

# -----------------------------
# TABLE
# -----------------------------
st.subheader("📄 Data Preview")
st.dataframe(df.head(20))

# -----------------------------
# INSIGHTS
# -----------------------------
st.subheader("💡 Insights")

st.write(f"Highest spending category: **{top_cat}**")

if cat_data["amount"].max() > 50000:
    st.warning("⚠️ Overspending detected!")
else:
    st.success("✅ Spending looks controlled!")