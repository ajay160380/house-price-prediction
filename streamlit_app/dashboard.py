import plotly.graph_objects as go
import plotly.express as px
import streamlit as st


def create_score_gauge(value: float, title: str, color: str) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={"font": {"color": "white", "size": 28}, "suffix": "/10"},
        gauge={
            "axis": {"range": [0, 10], "tickcolor": "#999aaf", "tickfont": {"color": "#999aaf"}},
            "bar": {"color": color, "thickness": 0.3},
            "bgcolor": "rgba(255,255,255,0.05)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 3], "color": "rgba(255,60,60,0.15)"},
                {"range": [3, 6], "color": "rgba(255,200,50,0.15)"},
                {"range": [6, 8], "color": "rgba(50,200,255,0.15)"},
                {"range": [8, 10], "color": "rgba(50,255,100,0.15)"},
            ],
            "threshold": {
                "line": {"color": "white", "width": 2},
                "thickness": 0.5,
                "value": value,
            },
        },
    ))
    fig.update_layout(
        height=200,
        margin=dict(l=10, r=10, t=40, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#e8e8f0"},
        title={"text": title, "font": {"size": 13, "color": "#999aaf"}, "x": 0.5},
    )
    return fig


def create_radar_chart(scores: dict[str, float]) -> go.Figure:
    categories = ["Education", "Healthcare", "Transport", "Lifestyle", "Overall"]
    values = [scores.get("education", 0), scores.get("healthcare", 0),
              scores.get("transport", 0), scores.get("lifestyle", 0),
              scores.get("overall", 0)]

    fig = go.Figure(data=go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill="toself",
        line=dict(color="#667eea", width=2),
        marker=dict(color="#00d4ff", size=4),
        fillcolor="rgba(102,126,234,0.15)",
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickfont={"color": "#999aaf", "size": 9},
                gridcolor="rgba(255,255,255,0.06)",
            ),
            angularaxis=dict(
                tickfont={"color": "#e8e8f0", "size": 10},
                gridcolor="rgba(255,255,255,0.06)",
            ),
            bgcolor="rgba(0,0,0,0)",
        ),
        height=300,
        margin=dict(l=60, r=60, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#e8e8f0"},
    )
    return fig


def create_amenity_bar_chart(amenities: dict) -> go.Figure:
    labels = []
    values = []
    for cat, items in amenities.items():
        display_name = {
            "school": "Schools", "hospital": "Hospitals", "metro": "Metro",
            "park": "Parks", "restaurant": "Restaurants", "mall": "Malls",
            "bus_stop": "Bus Stops",
        }.get(cat, cat)
        labels.append(display_name)
        values.append(len(items))

    colors = ["#667eea", "#764ba2", "#00d4ff", "#28a745", "#ff6b6b", "#ffd93d", "#6c5ce7"]

    fig = go.Figure(data=[
        go.Bar(
            x=labels,
            y=values,
            marker=dict(color=colors[:len(labels)], line=dict(color="rgba(255,255,255,0.1)", width=1)),
            text=values,
            textposition="outside",
            textfont={"color": "#e8e8f0", "size": 12},
            hovertemplate="<b>%{x}</b>: %{y}<extra></extra>",
        )
    ])
    fig.update_layout(
        height=280,
        margin=dict(l=10, r=10, t=10, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#e8e8f0"},
        xaxis=dict(
            tickfont={"color": "#999aaf", "size": 10},
            gridcolor="rgba(255,255,255,0.03)",
        ),
        yaxis=dict(
            tickfont={"color": "#999aaf", "size": 10},
            gridcolor="rgba(255,255,255,0.03)",
            showticklabels=False,
        ),
        bargap=0.4,
    )
    return fig


def create_price_range_chart(low: float, base: float, high: float) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Price Range"],
        y=[high],
        marker=dict(color="rgba(102,126,234,0.2)"),
        showlegend=False,
        hoverinfo="skip",
    ))
    fig.add_trace(go.Bar(
        x=["Price Range"],
        y=[base - low],
        base=low,
        marker=dict(color="rgba(102,126,234,0.5)"),
        name="Estimated Range",
        text=[f"₹{low:.1f}L - ₹{high:.1f}L"],
        textposition="inside",
        textfont={"color": "white", "size": 12},
    ))
    fig.add_trace(go.Scatter(
        x=["Price Range"],
        y=[base],
        mode="markers+text",
        marker=dict(color="#00d4ff", size=14, symbol="diamond"),
        text=[f"₹{base:.1f}L"],
        textposition="top center",
        textfont={"color": "#00d4ff", "size": 13, "weight": 700},
        name="Predicted Price",
    ))
    fig.update_layout(
        height=200,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#e8e8f0"},
        xaxis=dict(showticklabels=False, gridcolor="rgba(255,255,255,0.03)"),
        yaxis=dict(tickfont={"color": "#999aaf", "size": 10}, gridcolor="rgba(255,255,255,0.03)"),
        barmode="overlay",
        showlegend=False,
    )
    return fig


def create_comparison_chart(data1: dict, data2: dict, label1: str, label2: str) -> go.Figure:
    categories = ["Locality Score", "Education", "Healthcare", "Transport", "Lifestyle"]
    vals1 = [data1.get("overall", 0), data1.get("education", 0),
             data1.get("healthcare", 0), data1.get("transport", 0),
             data1.get("lifestyle", 0)]
    vals2 = [data2.get("overall", 0), data2.get("education", 0),
             data2.get("healthcare", 0), data2.get("transport", 0),
             data2.get("lifestyle", 0)]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name=label1,
        x=categories,
        y=vals1,
        marker=dict(color="#667eea", line=dict(color="rgba(255,255,255,0.1)", width=1)),
        text=[f"{v}/10" for v in vals1],
        textposition="outside",
        textfont={"color": "#667eea", "size": 10},
    ))
    fig.add_trace(go.Bar(
        name=label2,
        x=categories,
        y=vals2,
        marker=dict(color="#00d4ff", line=dict(color="rgba(255,255,255,0.1)", width=1)),
        text=[f"{v}/10" for v in vals2],
        textposition="outside",
        textfont={"color": "#00d4ff", "size": 10},
    ))
    fig.update_layout(
        barmode="group",
        height=350,
        margin=dict(l=10, r=10, t=20, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#e8e8f0"},
        legend={"font": {"color": "#999aaf"}, "orientation": "h", "y": 1.05},
        xaxis=dict(tickfont={"color": "#999aaf", "size": 10}, gridcolor="rgba(255,255,255,0.03)"),
        yaxis=dict(tickfont={"color": "#999aaf", "size": 10}, gridcolor="rgba(255,255,255,0.03)",
                   range=[0, 10]),
    )
    return fig
