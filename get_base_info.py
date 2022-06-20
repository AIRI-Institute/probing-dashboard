import numpy as np
from server import app
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import plotly.graph_objects as go
from math import log
from collections import defaultdict
import pandas as pd

def get_base_fig_info():
    already_scored_df = pd.read_csv("already_scored.csv")
    fig = go.Figure()

    cat2lines, lang2lines = defaultdict(list), defaultdict(list)
    cat2traces, lang2traces = defaultdict(list), defaultdict(list)
    cat2markers, lang2markers = defaultdict(list), defaultdict(list)
    enumix = 0
    added_markers = set()

    for ix, row in already_scored_df.iterrows():
        if row['frechet'] > 0.1: continue
        geo = go.Scattergeo(
            lon = [row["left:longitude"],row["right:longitude"]],
            lat = [row["left:latitude"], row["right:latitude"]],
            mode = 'lines',
            text= [row["left:language"], row["right:language"]],
            name = f"{row['left:task_category']}\t{row['right:task_category']}\t{row['frechet']}",
            hoverinfo="text+name",
            line ={"width": 2-2*row["frechet"]},
            customdata=[{"type": "line", "id": enumix, 
                         "langs":[row["right:language"], row["left:language"]],
                         "cats": [row['left:task_category'], row['right:task_category']]}])
        markerl = go.Scattergeo(
            lon = [row["left:longitude"]],
            lat = [row["left:latitude"]],
            mode = 'markers',
            name= row["left:language"],
            hoverinfo="text",
            customdata=[{"type": "lang"}])
        markerr = go.Scattergeo(
            lon = [row["right:longitude"]],
            lat = [row["right:latitude"]],
            mode = 'markers',
            name= row["right:language"],
            hoverinfo="text",
            customdata=[{"type": "lang"}])
        fig.add_trace(geo)
        if (row["right:longitude"], row["right:latitude"]) not in added_markers: fig.add_trace(markerr)
        if (row["left:longitude"], row["left:latitude"]) not in added_markers: fig.add_trace(markerl)
        added_markers.update(((markerr.lon, markerr.lat), (markerl.lon, markerl.lat)))
        

        cat2traces[row['left:task_category']].append(geo)
        cat2traces[row['right:task_category']].append(geo)
        lang2traces[row['left:language']].append(geo)
        lang2traces[row['right:language']].append(geo)

        enumix+=1
    fig.update_layout(showlegend=False,  margin=dict(l=0,r=0,b=0,t=0), width=500, height=500)
    return already_scored_df, fig, cat2lines, lang2lines, cat2traces, lang2traces