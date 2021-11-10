import os
from utils import get_filename
import pandas as pd 
import plotly.express as px


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# @TODO
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def graph_csv(path_csv, path_html, filename, key_header, value_header, scatter=False):

    wd = get_filename(path_csv, filename)
    df = pd.read_csv(wd)

    if not scatter:
        fig = px.line(df, x=key_header, y=value_header, title='')
    else: 
        fig = px.scatter(df, x=key_header, y=value_header, title='')
  
    fig.write_html(get_filename(path_html, filename))
   
    return fig 

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
