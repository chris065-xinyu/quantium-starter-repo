import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

# 读取数据
df = pd.read_csv("data/pink_morsels_sales.csv")

# 日期格式化
df["Date"] = pd.to_datetime(df["Date"])

# 按日期汇总每日总销售额
daily_sales = df.groupby("Date")["Sales"].sum().reset_index()

# 按日期排序
daily_sales = daily_sales.sort_values("Date")

# 创建图表
fig = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    title="Pink Morsels Daily Sales Over Time"
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Total Sales",
)

# 创建 Dash 应用
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Impact of Pink Morsel Price Increase on Sales"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)