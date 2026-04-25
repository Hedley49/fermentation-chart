import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load data
df = pd.read_csv("x1.txt", sep=r"\s+", header=None)
df.columns = ["time", "env", "beer", "ref", "color"]

# Parse time (gnuplot: "%m:%d:%h:%m:%s")
df["time"] = pd.to_datetime(df["time"], format="%m:%d:%H:%M:%S")

# ---- helper: parse gnuplot-style colors ----
def parse_color(c):
    c = str(c).strip()
    if c.startswith("0x"):
        return "#" + c[2:]
    return c  # already "#RRGGBB" or named

df["color_parsed"] = df["color"].apply(parse_color)

# ---- build figure ----
fig = go.Figure()

# --- env line (violet) ---
fig.add_trace(go.Scatter(
    x=df["time"],
    y=df["env"],
    mode="lines",
    line=dict(color="violet", width=2),
    name="env"
))

# --- beer line with per-segment color (gnuplot lc rgb variable) ---
for i in range(len(df) - 1):
    fig.add_trace(go.Scatter(
        x=[df["time"].iloc[i], df["time"].iloc[i+1]],
        y=[df["beer"].iloc[i], df["beer"].iloc[i+1]],
        mode="lines",
        line=dict(color=df["color_parsed"].iloc[i], width=2),
        showlegend=(i == 0),  # only show once in legend
        name="beer"
    ))

# --- reference line (dashed black) ---
fig.add_trace(go.Scatter(
    x=df["time"],
    y=df["ref"],
    mode="lines",
    line=dict(color="black", width=2, dash="dash"),
    name="68.0 f"
))

# ---- layout (match gnuplot formatting) ----
fig.update_layout(
    yaxis=dict(range=[60, 86], title="Value"),
    xaxis=dict(
        title="Time",
        tickformat="%M:%S\n%d/%b"
    ),
    legend=dict(orientation="h"),
    margin=dict(l=40, r=20, t=40, b=40)
)

# ---- render ----
st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        "displayModeBar": True,
        "modeBarButtonsToAdd": ["fullscreen"]
    }
)
