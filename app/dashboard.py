from dash import Dash
import dash_core_components as dcc
import dash_html_components as html

def add_dash(server):
    """Create Dash app."""
    # external_stylesheets = ['/static/dist/css/style.css']
    # external_scripts = ['/static/dist/js/includes/jquery.min.js',
    #                 '/static/dist/js/main.js']

    dash_app = Dash(server=server,
                    # external_stylesheets=external_stylesheets,
                    # external_scripts=external_scripts,
                    routes_pathname_prefix='/commands/')

    # Create Dash Layout
    dash_app.layout = html.Div(id='dash-container', children="dash app")

    return dash_app.server