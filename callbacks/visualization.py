import numpy as np
from server import app
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import plotly.graph_objects as go
from math import log
from collections import defaultdict
import pandas as pd
from get_base_info import get_base_fig_info
from itertools import cycle

colors_cycle = []
for col_ix, col in enumerate(cycle(px.colors.qualitative.Plotly)):
    if col_ix > 500: break
    colors_cycle.append(col)

already_scored_df, fig, cat2lines, lang2lines, cat2traces, lang2traces = get_base_fig_info()

def draw_map(cats=None, langs=None):
    global fig
    # fig.update_traces(visible=False)
    if cats is None or not cats: cats = cat2traces.keys()
    if langs is None or not langs: langs = lang2traces.keys()
    

    fig.for_each_trace(
        lambda trace: trace.update(visible=False)
    )
    traces_to_show_cat = set()
    for cat in cats:
        for trace in cat2traces[cat]:
            traces_to_show_cat.add(trace.customdata[0].get("id"))
    
    traces_to_show_lang = set()
    for lang in langs:
        for trace in lang2traces[lang]:
            traces_to_show_lang.add(trace.customdata[0].get("id"))
    
    traces_to_show = traces_to_show_cat.intersection(traces_to_show_lang)
    traces_to_show_objs = []
    fig.for_each_trace(lambda trace: traces_to_show_objs.append(trace) if trace.customdata[0].get("id") in traces_to_show else ())
    traces_to_show = traces_to_show_objs
    langs_to_show = {lang for trace in traces_to_show for lang in trace.customdata[0].get("langs", [])}
    langs_to_show = sorted(langs_to_show)
    
    traces_to_show_ids = []
    cats_to_show = set()
    for trace in traces_to_show:
        traces_to_show_ids.append(trace.customdata[0]["id"])
        cats_to_show.update(trace.customdata[0]["cats"])
    cats_colors = {cat: color for color, cat in zip(colors_cycle, sorted(cats_to_show))}
    # print(traces_colors)

    
    def update_trace(trace):
        trace_id = trace.customdata[0].get("id")
        if trace_id not in traces_to_show_ids: return
        representative_cat = [cat for cat in trace.customdata[0]["cats"] if cat in cats][0]
        trace_color = cats_colors[representative_cat]
        trace.update(visible=True, marker={"color":trace_color})

    fig.for_each_trace(update_trace)

    return fig

@app.callback(Output('output-data', component_property='figure'),
              [Input('input-cat', 'value'),
              Input('input-lang', 'value'),])
def update_visualization(cats, langs):
    
    chart_layout = draw_map(cats, langs)
    return chart_layout

