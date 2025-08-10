import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page settings
st.set_page_config(page_title="Housing Affordability Dashboard", page_icon="🏡", layout="wide")

st.title("🏡 Housing Affordability: Rent vs Buy Analysis")
st.markdown("### Compare the long-term cost of renting vs buying based on your assumptions.")

# Sidebar for inputs
st.sidebar.header("Adjust Your Assumptions")

house_price = st.sidebar.number_input("House Price (USD)", 50000, 2000000, 300000)
down_payment_pct = st.sidebar.slider("Down Payment (%)", 0, 100, 20)
mortgage_rate = st.sidebar.number_input("Mortgage Interest Rate (%)", 0.0, 15.0, 4.0)
loan_term = st.sidebar.slider("Loan Term (Years)", 5, 40, 30)

annual_rent = st.sidebar.number_input("Annual Rent (USD)", 1000, 100000, 15000)
rent_increase = st.sidebar.slider("Annual Rent Increase (%)", 0.0, 10.0, 3.0)

years = st.sidebar.slider("Projection Years", 1, 40, 10)

# Calculations
down_payment = house_price * (down_payment_pct / 100)
loan_amount = house_price - down_payment
annual_mortgage_payment = (loan_amount * (mortgage_rate / 100)) / (1 - (1 + mortgage_rate / 100) ** (-loan_term))

data = []
for year in range(1, years + 1):
    rent_cost = annual_rent * ((1 + rent_increase / 100) ** (year - 1))
    if year <= loan_term:
        buy_cost = annual_mortgage_payment
    else:
        buy_cost = 0
    data.append({"Year": year, "Rent Cost": rent_cost, "Buy Cost": buy_cost})

df = pd.DataFrame(data)

# Cumulative costs
df["Cumulative Rent"] = df["Rent Cost"].cumsum()
df["Cumulative Buy"] = df["Buy Cost"].cumsum()

# Layout: split into two columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Annual Cost Comparison")
    fig, ax = plt.subplots()
    ax.plot(df["Year"], df["Rent Cost"], label="Rent", marker='o', color="orange")
    ax.plot(df["Year"], df["Buy Cost"], label="Buy", marker='o', color="green")
    ax.set_xlabel("Year")
    ax.set_ylabel("Annual Cost (USD)")
    ax.legend()
    st.pyplot(fig)

with col2:
    st.subheader("💰 Cumulative Cost Over Time")
    fig2, ax2 = plt.subplots()
    ax2.plot(df["Year"], df["Cumulative Rent"], label="Cumulative Rent", marker='o', color="red")
    ax2.plot(df["Year"], df["Cumulative Buy"], label="Cumulative Buy", marker='o', color="blue")
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Total Cost (USD)")
    ax2.legend()
    st.pyplot(fig2)

# Table
st.subheader("📄 Detailed Projection Table")
st.dataframe(df.style.format("{:,.0f}"))
