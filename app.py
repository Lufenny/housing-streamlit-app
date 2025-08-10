import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Streamlit page config
st.set_page_config(page_title="Rent vs Buy Analysis", layout="wide")
st.title("🏠 Housing Affordability: Rent vs Buy Dashboard (Kuala Lumpur)")

# File path (same folder as app.py)
DATA_FILE = Path(__file__).parent / "Buy_vs_Rent_KL_FullModel.xlsx"

# Load data
@st.cache_data
def load_data(file_path):
    return pd.read_excel(file_path)

if DATA_FILE.exists():
    df = load_data(DATA_FILE)
else:
    st.error(f"❌ Data file not found: {DATA_FILE}")
    st.stop()

# Sidebar filters
st.sidebar.header("🔍 Filters")
years = sorted(df['Year'].unique())
selected_years = st.sidebar.slider(
    "Select Year Range",
    int(min(years)), int(max(years)),
    (int(min(years)), int(max(years)))
)
scenarios = df['Scenario'].unique() if 'Scenario' in df.columns else []
selected_scenarios = st.sidebar.multiselect(
    "Select Scenario(s)",
    scenarios,
    default=scenarios
)

# Filter data
df_filtered = df[
    (df['Year'] >= selected_years[0]) &
    (df['Year'] <= selected_years[1])
]
if 'Scenario' in df.columns:
    df_filtered = df_filtered[df_filtered['Scenario'].isin(selected_scenarios)]

# KPIs
col1, col2 = st.columns(2)
avg_rent = df_filtered['Rent Cost'].mean()
avg_buy = df_filtered['Buy Cost'].mean()
col1.metric("💰 Avg Rent Cost", f"RM {avg_rent:,.0f}")
col2.metric("🏡 Avg Buy Cost", f"RM {avg_buy:,.0f}")

# Interactive chart
fig = px.line(
    df_filtered,
    x="Year",
    y=["Rent Cost", "Buy Cost"],
    color_discrete_map={"Rent Cost": "#FF5733", "Buy Cost": "#33C1FF"},
    markers=True,
    title="Rent vs Buy Over Time"
)
fig.update_layout(legend_title_text='Cost Type', template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# Data table
st.subheader("📊 Detailed Data")
st.dataframe(df_filtered)

# Download button
csv = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    "⬇️ Download Filtered Data",
    csv,
    "rent_vs_buy_filtered.csv",
    "text/csv"
)
