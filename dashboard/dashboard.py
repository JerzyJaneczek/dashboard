import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import pandas as pd
import plotly.express as px

app = dash.Dash(external_stylesheets=[
                dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server


# Data
data = pd.read_csv("dataset.csv", sep="\t")
data = data.dropna()
Y = data["AcceptedCmp1"] + data["AcceptedCmp2"] + data["AcceptedCmp3"] + \
    data["AcceptedCmp4"] + data["AcceptedCmp5"] + data["Response"]
df = data

##Components##
myGraph = dcc.Graph(id="graph", figure={})
dropdown = dcc.Dropdown(options=["Bar", "Scatter", "Boxplot"],
                        value="Bar",
                        clearable=False,
                        id="graph_type")

columnDropdown = dcc.Dropdown(options=[
    {'label': i, 'value': i} for i in df.columns
],
    value="ID",
    clearable=False,
    id="data_variable")


app.layout = dbc.Container(
    [
        html.H1("ML Dashboard"),
        dbc.Tabs(
            [
                dbc.Tab(label="Q1", tab_id="q1"),
                dbc.Tab(label="Q4", tab_id="q4"),
                dbc.Tab(label="Q6", tab_id="q6"),
            ],
            id="tabs",
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)

# Images
image1 = html.Img(src='', id='image1')
image2 = html.Img(src='', id='image2')
image3 = html.Img(src='', id='image3')
image4 = html.Img(src='', id='image4')
image5 = html.Img(src='', id='image5')
image6 = html.Img(src='', id='image6', style={"width": '70%'})


@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab")],
)
def render_tab_content(active_tab):
    if active_tab:
        if active_tab == "q1":
            return html.Div([dropdown, columnDropdown, myGraph])
        elif active_tab == "q4":
            return html.Div([image1, image2, image3, image4])
        elif active_tab == "q6":
            return html.Div([image5, image6])

    return "No tab selected"


@app.callback(
    Output("image1", "src"),
    Output("image2", "src"),
    Output("image3", "src"),
    Output("image4", "src"),
    Input("tabs", "active_tab"),
)
def renderImage(active_tab):
    if active_tab == "q4":
        image_path1 = 'https://newdashboard.onrender.com/assets/figure1.png'
        image_path2 = './assets/figure2.png'
        image_path3 = './assets/figure3.png'
        image_path4 = './assets/figure4.png'
        return image_path1, image_path2, image_path3, image_path4


@app.callback(
    Output("image5", "src"),
    Output("image6", "src"),
    Input("tabs", "active_tab"),
)
def renderImage(active_tab):
    if active_tab == "q6":
        image_path5 = './assets/Shap.png'
        image_path6 = './assets/ShapAnalysis.png'
        return image_path5, image_path6


@app.callback(Output("graph", "figure"),
              Input("graph_type", "value"),
              Input("data_variable", "value"),)
def update_graph(graph_type, data_variable):
    # Check if the column is of type int64 or float64
    if graph_type == "Bar":
        fig = px.histogram(data_frame=df, x=df[data_variable],
                           title="Bar Chart of " + data_variable)

    elif graph_type == "Scatter":
        fig = px.scatter(data_frame=df, x=df[data_variable], y=Y,
                         title="Scatter Plot of " + data_variable)

    elif graph_type == "Boxplot":
        fig = px.box(data_frame=df, y=df[data_variable],
                     title="Scatter Plot of " + data_variable)

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
