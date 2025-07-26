import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="ROI to Million Simulator", layout="centered")

st.title("💰 ROI Trade Simulator")
st.caption("Simulate how many trades it takes to reach your financial goal by compounding profits")

# User Inputs
col1, col2 = st.columns(2)
with col1:
    starting_capital = st.number_input("Starting Capital ($)", value=25.0, min_value=1.0)
with col2:
    roi_percent = st.number_input("ROI per Trade (%)", value=200.0, min_value=1.0)

target_amount = st.number_input("Target Amount ($)", value=1_000_000.0, min_value=100.0)

# Core Logic
roi_multiplier = 1 + roi_percent / 100
capital = starting_capital
data = []
trade = 0

while capital < target_amount:
    trade += 1
    capital *= roi_multiplier
    data.append({"Trade #": trade, "Capital ($)": round(capital, 2)})

df = pd.DataFrame(data)

# Output
st.success(f"🎯 You'll reach **${int(capital):,}** in **{trade} trades** with {roi_percent}% ROI per trade.")

# Table
st.subheader("📊 Capital Growth Table")
st.dataframe(df, use_container_width=True)

# Plotly Chart
fig = px.line(df, x="Trade #", y="Capital ($)", title="Capital Growth Over Trades",
              markers=True, template="plotly_white")
fig.add_hline(y=target_amount, line_dash="dash", line_color="red", annotation_text="Target")
st.plotly_chart(fig, use_container_width=True)

# Download Option
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("📥 Download CSV", data=csv, file_name="roi_growth_simulation.csv", mime="text/csv")
