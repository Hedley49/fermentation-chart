import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("x1.txt", sep=r"\s+", header=None)
df.columns = ["time", "env", "beer", "ref", "color"]

# Parse time
df["time"] = pd.to_datetime(df["time"], format="%m:%d:%H:%M:%S")

# Set index for plotting
df = df.set_index("time")

# Basic line chart
st.line_chart(df[["env", "beer", "ref"]])