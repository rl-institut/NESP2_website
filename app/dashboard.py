import json
import re
import plotly
import plotly.graph_objs as go


def create_plot(api_return):
    api_return = api_return.copy()
    # Create a trace
    x = []
    y = []
    for i in api_return["points"]:
        x.append(i["key"])
        y.append(i["value"])
    data = [go.Scatter(x=x, y=y, mode="lines")]

    return json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
