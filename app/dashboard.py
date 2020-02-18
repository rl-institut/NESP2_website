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


CATEGORIES = {
    "Social": ["peopleConnected", "communitiesConnected"],
    "Technical": ["installedRenewableEnergyCapacity", "electricityConsumed"],
    "Financial": ["totalInvestment", "averagetarif"],
}


VALUES = [{"key": 2017, "value": 1}, {"key": 2018, "value": 2}, {"key": 2019, "value": 3}, {"key": 2020, "value": 4}]
DUMMY_RETURN = {
    "peopleConnected": {
        "unitOfMeasure": "",
        "trendValue": 0,
        "value": 0,
        "points": VALUES,
    },
    "communitiesConnected": {
        "unitOfMeasure": "",
        "trendValue": 0,
        "value": 0,
        "points": VALUES,
    },
    "installedRenewableEnergyCapacity": {
        "unitOfMeasure": "kW",
        "trendValue": 0,
        "value": 0,
        "points": VALUES,
    },
    "electricityConsumed": {
        "unitOfMeasure": "kWh",
        "trendValue": 0,
        "value": 0,
        "points": VALUES,
    },
    "totalInvestment": {
        "unitOfMeasure": "USD",
        "trendValue": 0,
        "value": 0,
        "points": VALUES,
    },
    "averagetarif": {
        "unitOfMeasure": "USD/kWh",
        "trendValue": 0,
        "value": 0,
        "points": VALUES,
    },
}
