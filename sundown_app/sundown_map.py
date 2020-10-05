from urllib.request import urlopen
import json
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go  # or plotly.express as px

from .about_us import about_us_html


def county2fips_fct(x):
    if x in county2fips:
        return str(int(county2fips[x]))
    else:
        return np.nan


# define data dir
data_dir = "../data"
data_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), data_dir)

counties_with_latlong = pd.read_csv(
    os.path.join(data_filepath, "counties.txt"), dtype={"GEOID": str}, sep="\t"
)

# get sundown town data
df = pd.read_csv(os.path.join(data_filepath, "sundown_with_counties.csv"), encoding="latin-1")
df["County_no_states"] = df.county.str.split(",").apply(lambda x: x[0])
county_long_names = []
for i in df.county.values:
    x = i.split(",")
    if len(x) == 2:
        county_long_names.append(x[0] + " " + x[1])
    else:
        county_long_names.append(x)
df["county_long_names"] = county_long_names

# get fips data
fips_codes = pd.read_csv(os.path.join(data_filepath, "county_fips_master.csv"), encoding="latin-1")
county2fips = dict(fips_codes[["county_name", "fips"]].values)

county_sundown_counts = pd.DataFrame(df.groupby(by="County_no_states").size())
county_sundown_counts = county_sundown_counts.reset_index()
county_sundown_counts = county_sundown_counts.rename(columns={"County_no_states": "County", 0: "#"})
county_sundown_counts["fips"] = county_sundown_counts.County.apply(lambda x: county2fips_fct(x))
county_sundown_counts = county_sundown_counts[county_sundown_counts.fips.notnull()]

with urlopen(
    "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
) as response:
    counties = json.load(response)

df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
    dtype={"fips": str},
)

fig = px.choropleth_mapbox(
    county_sundown_counts,
    geojson=counties,
    locations="fips",
    color="#",
    color_continuous_scale="Viridis",
    range_color=(0, 12),
    mapbox_style="carto-positron",
    zoom=3,
    center={"lat": 37.0902, "lon": -95.7129},
    opacity=0.5,
    labels={"#": "# of Sundown Towns"},
)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
# fig.show()


sundown_map_html = html.Div(
    children=[
        html.Div(
            [
                dcc.Markdown(""" # List of sundown towns across the country """),
                html.Pre(id="click-data"),
            ]
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id="sundown-county",
                    options=[
                        {"label": c, "value": fips}
                        for c, fips in zip(
                            county_sundown_counts.County.values, county_sundown_counts.fips.values
                        )
                    ],
                    value="Counties",
                )
            ]
        ),
        dcc.Graph(id="sundown-map", figure=fig),
    ]
)
