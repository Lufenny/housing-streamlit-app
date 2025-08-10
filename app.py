import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Housing Affordability: Rent vs Buy Analysis")

# Example data
data = {
    'Year': list(range(2025, 2035)),
    'Rent Cost': [12000 * (1.03)**i for i in range(10)],
    'Buy Cost': [15000 + (i * 500) for i in range(10)]
}
df = pd.DataFrame(data)

# Display table
st.subheader("Cost Comparison Table")
st.dataframe(df)

# Chart
st.subheader("Cost Comparison Chart")
fig, ax = plt.subplots()
ax.plot(df['Year'], df['Rent Cost'], label='Rent', marker='o')
ax.plot(df['Year'], df['Buy Cost'], label='Buy', marker='o')
ax.set_xlabel('Year')
ax.set_ylabel('Annual Cost (USD)')
ax.legend()
st.pyplot(fig)
