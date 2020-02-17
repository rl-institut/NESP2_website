import numpy as np
import json
import plotly
import plotly.graph_objs as go


def create_plot():

    N = 1000
    random_x = np.random.randn(N)
    random_y = np.random.randn(N)

    # Create a trace
    data = [go.Scatter(
        x=random_x,
        y=random_y,
        mode='markers'
    )]

    return json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
