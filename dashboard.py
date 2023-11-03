import pandas as pd
import numpy as np
import matplotlib.pyplot as  plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style="dark")


def create_customer_bystate_df(df):
    customer_bystate_df = df.groupby("customer_state").customer_id.nunique().reset_index()
    customer_bystate_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)

    return customer_bystate_df

def create_seller_bystate_df(df):
    seller_bystate_df = df.groupby("seller_state").seller_id.nunique().reset_index()
    seller_bystate_df.rename(columns={
        "seller_id": "seller_count"
    }, inplace=True)

    return seller_bystate_df

def create_seller_revenue_df(df):
    seller_revenues_df = df.groupby("seller_id").price.sum().reset_index()
    seller_revenues_df.rename(columns={
        "price": "revenue"
    }, inplace=True)

    return seller_revenues_df

def create_product_category_df(df):
    product_categories_df = df.groupby("product_category_name_english").order_id.nunique().reset_index()
    product_categories_df.rename(columns={
        "product_category_name_english": "product_category_name",
        "order_id": "quantity"
    }, inplace=True)

    return product_categories_df

def create_monthly_order_df(df):
    monthly_order_df = df.resample(rule="M", on="order_purchase_timestamp").agg({
        "order_id": "nunique",
        "price": "sum",
        "review_score": "mean"
    }).reset_index()
    monthly_order_df.rename(columns={
        "order_id": "order_count",
        "price": "seller_revenue"
    }, inplace=True)

    return monthly_order_df

def create_cluster_byseller_df(df):
    cluster_byseller_df = df.groupby("seller_id").agg({
        "order_id": "nunique",
        "price": "sum",
        "review_score": "mean"
    }).reset_index()
    cluster_byseller_df.rename(columns={
        "order_id": "order_count",
        "price": "seller_revenue",
    }, inplace=True)

    return cluster_byseller_df

# read all csv
all_df = pd.read_csv("all_df.csv")

# change datetime column to datetime format
datetime_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "review_creation_date",
    "review_answer_timestamp",
    "shipping_limit_date"
]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column], format="mixed")

# find min and max order date
min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    st.title("Stackware E-Commerce")
    # make a filter by date
    start_date, end_date = st.date_input(
        label="Time Span",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# apply date filter
main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & (all_df["order_purchase_timestamp"] <= str(end_date))]

# initial all dataframe
customer_bystate_df = create_customer_bystate_df(main_df)
seller_bystate_df = create_seller_bystate_df(main_df)
seller_revenue_df = create_seller_revenue_df(main_df)
product_category_df = create_product_category_df(main_df)
monthly_order_df = create_monthly_order_df(main_df)
cluster_byseller_df = create_cluster_byseller_df(main_df)

# create header
st.header("Stackware E-Commerce Dashboard")

# MONTHLY ALL SELLER ORDERS
st.subheader("Monthly All Seller Orders")

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Seller Order", value=monthly_order_df.order_count.sum())

with col2:
    total_revenue = format_currency(monthly_order_df.seller_revenue.sum(), "USD", locale="en_US")
    st.metric("Total Seller Revenue", value=total_revenue)

# make monthly order visualization
fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(monthly_order_df["order_purchase_timestamp"], monthly_order_df["order_count"], marker="o", linewidth=2, color="#006e87")
ax.tick_params(axis="x", labelsize=15)
ax.tick_params(axis="y", labelsize=20)

st.pyplot(fig)

# HIGHEST & LOWEST PROFITED SELLERS
st.subheader("Highest & Lowest Profited Sellers")

# shortened the seller name to 3  digit unique id
seller_revenue_df["seller_id"] = seller_revenue_df["seller_id"].apply(lambda x: x[0:3])

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35,15))
colors = ["#006e87", "#00c6f2", "#00c6f2", "#00c6f2", "#00c6f2"]

# highest profited seller
sns.barplot(y="revenue", x="seller_id", data=seller_revenue_df.sort_values(by="revenue", ascending=False).head(5), palette=colors, hue=colors, legend=False, ax=ax[0])
ax[0].set_title("Sellers With The Highest Profits", loc="center", fontsize=50)
ax[0].set_xlabel("Seller id", fontsize=30)
ax[0].set_ylabel(None)
ax[0].tick_params(axis="y", labelsize=35)
ax[0].tick_params(axis="x", labelsize=30)

# lowest profited seller
sns.barplot(y="revenue", x="seller_id", data=seller_revenue_df.sort_values(by="revenue", ascending=True).head(5), palette=colors, hue=colors, legend=False, ax=ax[1])
ax[1].set_title("Sellers With The Lowest Profits", loc="center", fontsize=50)
ax[1].set_xlabel("Seller id", fontsize=30)
ax[1].set_ylabel(None)
ax[0].tick_params(axis="y", labelsize=35)
ax[0].tick_params(axis="x", labelsize=30)

st.pyplot(fig)

# BEST AND WORST PERFORMING PRODUCTS
st.subheader("Best & Worst Performing Products")

# make visualization
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
colors = ["#006e87", "#00c6f2", "#00c6f2", "#00c6f2", "#00c6f2"]

# best performing product category
sns.barplot(x="quantity", y="product_category_name", data=product_category_df.sort_values(by="quantity", ascending=False).head(5), palette=colors, ax=ax[0])
ax[0].set_xlabel(None)
ax[0].set_ylabel(None)
ax[0].set_title("Best Performing Product Category", loc="center", fontsize=50)
ax[0].tick_params(axis="y", labelsize=35)
ax[0].tick_params(axis="x", labelsize=30)

# worst performing product category
sns.barplot(x="quantity", y="product_category_name", data=product_category_df.sort_values(by="quantity", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_xlabel(None)
ax[1].set_ylabel(None)
ax[1].set_title("Worst Performing Product Category", loc="center", fontsize=50)
ax[1].tick_params(axis="y", labelsize=35)
ax[1].tick_params(axis="x", labelsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()

st.pyplot(fig)

# CUSTOMER DEMOGRAPHICS
st.subheader("Customers & Sellers Demographics")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
colors = ["#006e87", "#00c6f2", "#00c6f2", "#00c6f2", "#00c6f2"]

sns.barplot(y="customer_state", x="customer_count", data=customer_bystate_df.sort_values(by="customer_count" ,ascending=False).head(5), palette=colors, ax=ax[0])
ax[0].set_title("Number Of Customer By State", loc="center", fontsize=50)
ax[0].set_xlabel(None)
ax[0].set_ylabel(None)
ax[0].tick_params(axis="y", labelsize=35)
ax[0].tick_params(axis="x", labelsize=30)

sns.barplot(y="seller_state", x="seller_count", data=seller_bystate_df.sort_values(by="seller_count" ,ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_title("Number Of Seller By State", loc="center", fontsize=50)
ax[1].set_xlabel(None)
ax[1].set_ylabel(None)
ax[1].tick_params(axis="y", labelsize=35)
ax[1].tick_params(axis="x", labelsize=30)

st.pyplot(plt)

# CLUSTER ANALYSIS per seller
st.subheader("Revenue Cluster Analysis Per Seller")

fig, ax = plt.subplots(ncols=2, nrows=1, figsize=(35, 10))

# watch the relationship between revenue and order
sns.scatterplot(data=cluster_byseller_df, y="order_count", x="seller_revenue", ax=ax[0])
ax[0].set_xlabel("Seller Revenue", fontsize=30)
ax[0].set_ylabel("Order Count", fontsize=30)
ax[0].set_title("Relationship between Order & Revenue", fontsize=50)
ax[0].tick_params(axis="y", labelsize=35)
ax[0].tick_params(axis="x", labelsize=30)

# watch relation between order and review score
sns.scatterplot(data=cluster_byseller_df, y="order_count", x="review_score", ax=ax[1])
ax[1].set_xlabel("Review Score", fontsize=30)
ax[1].set_ylabel("Order Count", fontsize=30)
ax[1].set_title("Relationship between Review & Order", fontsize=50)
ax[1].tick_params(axis="y", labelsize=35)
ax[1].tick_params(axis="x", labelsize=30)

st.pyplot(plt)

fig, ax = plt.subplots(figsize=(10, 5))
# watch relation between seller_revenue and review score
sns.scatterplot(data=cluster_byseller_df, y="seller_revenue", x="review_score", ax=ax)
ax.set_xlabel("Review Score", fontsize=15)
ax.set_ylabel("Seller Revenue", fontsize=15)
ax.set_title("Relationship between Review & Revenue", fontsize=15)
ax.tick_params(axis="y", labelsize=15)
ax.tick_params(axis="x", labelsize=20)

st.pyplot(plt)

# REVENUE CLUSTER ANALYSIS PER MONTH
st.subheader("Revenue Cluster Analysis Per Seller")

fig, ax = plt.subplots(ncols=2, nrows=1, figsize=(35, 10))

# watch the relationship between revenue and order
sns.scatterplot(data=monthly_order_df, y="order_count", x="seller_revenue", ax=ax[0])
ax[0].set_xlabel("Seller Revenue", fontsize=30)
ax[0].set_ylabel("Order Count", fontsize=30)
ax[0].set_title("Relationship between Order & Revenue", fontsize=50)
ax[0].tick_params(axis="y", labelsize=35)
ax[0].tick_params(axis="x", labelsize=30)

# watch relation between order and review score
sns.scatterplot(data=monthly_order_df, y="order_count", x="review_score", ax=ax[1])
ax[1].set_xlabel("Review Score", fontsize=30)
ax[1].set_ylabel("Order Count", fontsize=30)
ax[1].set_title("Relationship between Review & Order", fontsize=50)
ax[1].tick_params(axis="y", labelsize=35)
ax[1].tick_params(axis="x", labelsize=30)

st.pyplot(plt)

fig, ax = plt.subplots(figsize=(10, 5))

# watch relation between seller_revenue and review score
sns.scatterplot(data=monthly_order_df, y="seller_revenue", x="review_score", ax=ax)
ax.set_xlabel("Review Score", fontsize=15)
ax.set_ylabel("Seller Revenue", fontsize=15)
ax.set_title("Relationship between Review & Revenue", fontsize=15)
ax.tick_params(axis="y", labelsize=15)
ax.tick_params(axis="x", labelsize=20)

st.pyplot(plt)
