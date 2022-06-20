import dash_html_components as html
import dash_core_components as dcc
from get_base_info import get_base_fig_info

already_scored_df, fig, cat2lines, lang2lines, cat2traces, lang2traces = get_base_fig_info()
cats = sorted(cat2traces.keys())
langs = sorted(lang2traces.keys())

layout_inputs = html.Div([
    html.H3("Inputs"),
    html.Div(children=[
        html.Div(children=[
            html.Label("Category"),
            # dcc.Input(id="input-mean", type="number", className="form-control", value="0")
            dcc.Dropdown(cats, id='input-cat',multi=True),
        ]),
    ], className="row"),
    html.Div(children=[
        html.Div(children=[
            html.Label("Language"),
            dcc.Dropdown(langs, id='input-lang', multi=True)
        ]),
    ], className="row"),
])
