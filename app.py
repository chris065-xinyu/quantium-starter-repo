import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


# ---------- Load & prep data ----------
df = pd.read_csv("data/pink_morsels_sales.csv")

# Ensure correct dtypes
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
df["Region"] = df["Region"].astype(str).str.strip().str.lower()

df = df.dropna(subset=["Date", "Sales", "Region"])


def make_figure(selected_region):

    if selected_region != "all":
        dff = df[df["Region"] == selected_region]
    else:
        dff = df

    daily_sales = (
        dff.groupby("Date")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Date")
    )

  
    fig = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        title="Pink Morsel Daily Sales Over Time"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Total Sales"
    )

    price_change_date = pd.Timestamp("2021-01-15")

    fig.add_vline(
        x=price_change_date,
        line_width=2,
        line_dash="dash",
    )

    fig.add_annotation(
        x=price_change_date,
        y=1,
        xref="x",
        yref="paper",
        text="Price increase (2021-01-15)",
        showarrow=False,
        xanchor="left",
        yanchor="top",
        yshift=-5,
    )

    return fig


# ---------- App ----------
app = Dash(__name__)
app.title = "Pink Morsel Sales Dashboard"

app.layout = html.Div(
    style={
        "maxWidth": "1100px",
        "margin": "0 auto",
        "padding": "24px 16px",
        "fontFamily": "-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial",
        "backgroundColor": "#fafafa",
    },
    children=[
        html.Div(
            style={
                "backgroundColor": "white",
                "borderRadius": "14px",
                "padding": "18px 18px 10px 18px",
                "boxShadow": "0 6px 18px rgba(0,0,0,0.08)",
                "marginBottom": "16px",
            },
            children=[
                html.H1(
                    "Impact of Pink Morsel Price Increase on Sales",
                    style={"margin": "0 0 6px 0", "color": "#1f2937"},
                ),
                html.P(
                    "Filter by region to explore sales trends. The dashed line marks the price increase on 2021-01-15.",
                    style={"margin": "0 0 14px 0", "color": "#4b5563"},
                ),
                html.Div(
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "gap": "12px",
                        "flexWrap": "wrap",
                    },
                    children=[
                        html.Span("Region:", style={"color": "#374151", "fontWeight": 600}),
                        dcc.RadioItems(
                            id="region-filter",
                            options=[
                                {"label": "All", "value": "all"},
                                {"label": "North", "value": "north"},
                                {"label": "East", "value": "east"},
                                {"label": "South", "value": "south"},
                                {"label": "West", "value": "west"},
                            ],
                            value="all",
                            inline=True,
                            style={"color": "#374151"},
                            inputStyle={"marginRight": "6px"},
                            labelStyle={"marginRight": "14px"},
                        ),
                    ],
                ),
            ],
        ),

        html.Div(
            style={
                "backgroundColor": "white",
                "borderRadius": "14px",
                "padding": "12px 12px 6px 12px",
                "boxShadow": "0 6px 18px rgba(0,0,0,0.08)",
            },
            children=[
                dcc.Graph(
                    id="sales-chart",
                    figure=make_figure("all"),
                    config={"displayModeBar": True},
                ),
            ],
        ),
    ],
)


@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value"),
)
def update_chart(selected_region):
    return make_figure(selected_region)


if __name__ == "__main__":
    app.run(debug=True)