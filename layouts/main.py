import dash_html_components as html
import dash_core_components as dcc
from layouts.inputs import layout_inputs
from layouts.visualization import layout_visualization

main_layout = html.Div([
    html.Div([
        html.Div([
            html.H1("Dashboard")
        ]),
    ], className="row"),
    html.Div([
        html.Div([
            layout_inputs
        ], className="col-3"),
        # html.Div([], className="col-1"),
        html.Div([
            layout_visualization
        ], className="col-9"),
    ], className="row"),
], className="container")
