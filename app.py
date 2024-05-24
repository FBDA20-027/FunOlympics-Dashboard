from dash import Dash, dcc, html, Input, Output
from dash_bootstrap_templates import load_figure_template
import pandas as pd
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc

templates = [
    "pulse"
]

load_figure_template(templates)


data = pd.read_csv("fun_olympics.csv")

# convert time column to datetime
data['time'] = pd.to_datetime(data['time'], format="mixed")

# sporting events aliases
sporting_events = {
    "/basketball": "Basketball",
    "/table-tennis": "Table Tennis",
    "/tennis": "Tennis",
    "/athletics/track": "Athletics - Track",
    "/athletics/field": "Athletics - Field",
    "/volleyball": "Volleyball",
    "/cycling": "Cycling",
    "/diving": "Diving",
    "/gymnastics": "Gymnastics",
    "/weightlifting": "Weightlifting",
    "/rowing": "Rowing",
    "/football": "Football",
    "/swimming": "Swimming",
    "/water-polo": "Water Polo",
    "/wrestling": "Wrestling",
    "/karate": "Karate",
    "/hockey": "Hockey"
}

# group data by sporting event
data['sporting_event'] = data['path'].map(sporting_events)
path_requests = data.groupby('sporting_event').size().reset_index(name='n')
path_requests = path_requests.drop(path_requests[path_requests['sporting_event'] == 'Other'].index)

# age groups
data['age_group'] = pd.cut(data['age'], bins=[0, 24, 34, 44, 54, 64, float('inf')],
                           labels=["16-24", "25-34", "35-44", "45-54", "55-64", "65+"])


# function to calculate peak viewing time
def calculate_peak_viewing_time(hourly_requests):
    peak_hour_index = np.argmax(hourly_requests['count'])
    peak_hour = hourly_requests.loc[peak_hour_index, 'time']
    return peak_hour


# function to calculate the most popular sporting event
def calculate_most_popular_sporting_event(filtered_data):
    event_counts = filtered_data['sporting_event'].value_counts()
    most_popular_event = event_counts.idxmax()
    return most_popular_event


# get unique continents and countries
continents = sorted(data['continent'].unique())
countries = sorted(data['country'].unique())


app = Dash(__name__, external_stylesheets=[dbc.themes.PULSE])

# define dashboard layout
app.layout = html.Div([
    html.H1("Payris 2024 FunOlympic Games Dashboard", style={'text-align': 'center', 'margin-bottom': '20px', 'margin-top': '20px',
                                                             'font-weight': 'bold'}),
    html.Div(className="container", children=[
        dcc.Tabs([
            dcc.Tab(label='Demographic Data', children=[
                html.Div(children=[
                    dbc.Row([
                        dbc.Col(
                            dbc.Card([
                                dbc.CardHeader(html.H5("Filters")),
                                dbc.CardBody([
                                    dbc.Row([
                                        dbc.Col(
                                            [
                                                html.Label("Select Sporting Event"),
                                                dcc.Dropdown(
                                                    id='sporting-event-dropdown',
                                                    options=[{'label': event, 'value': event} for event in path_requests['sporting_event']],
                                                    value=None,
                                                    multi=True,
                                                ),
                                            ],
                                            width=4
                                        ),

                                        dbc.Col(
                                            [
                                                html.Label("Select Continent"),
                                                dcc.Dropdown(
                                                    id='continent-dropdown',
                                                    options=[{'label': continent, 'value': continent} for continent in continents],
                                                    value=None,
                                                    multi=True,
                                                ),
                                            ],
                                            width=4
                                        ),

                                        dbc.Col(
                                            [
                                                html.Label("Select Country"),
                                                dcc.Dropdown(
                                                    id='country-dropdown',
                                                    value=None,
                                                    multi=True,
                                                ),
                                            ],
                                            width=4
                                        ),
                                    ])
                                ])
                            ], className="mb-3"),
                            width=12
                        ),
                    ]),
                    dbc.Row([
                        dbc.Col(
                            dbc.Card([
                                dbc.CardHeader(html.H5("Viewership by Country")),
                                dbc.CardBody([
                                    dcc.Graph(id='country-requests'),
                                ])
                            ], className="mb-3"),
                            width=7
                        ),
                        dbc.Col(
                            dbc.Card([
                                dbc.CardHeader(html.H5("Average Viewership by Income Status")),
                                dbc.CardBody([
                                    dcc.Graph(id='income-requests'),
                                ])
                            ], className="mb-3"),
                            width=5
                        )]),
                    dbc.Row([
                        dbc.Col(
                            dbc.Card([
                                dbc.CardHeader(html.H5("Average Viewership by Age Group")),
                                dbc.CardBody([
                                    dcc.Graph(id='age-requests'),
                                ])
                            ], className="mb-3"),
                            width=6
                        ),
                        dbc.Col(
                            dbc.Card([
                                dbc.CardHeader(html.H5("Average Viewership by Gender")),
                                dbc.CardBody([
                                    dcc.Graph(id='gender-requests'),
                                ])
                            ], className="mb-3"),
                            width=6
                        )
                    ]),
                ])
            ]),
            dcc.Tab(label='Viewership Statistics', children=[
                html.Div( children=[
                    dbc.Row([
                        dbc.Col(
                            dbc.Card([
                                dbc.CardHeader(html.H5("Filters")),
                                dbc.CardBody([
                                    dbc.Row([
                                        dbc.Col(
                                            [
                                                html.Label("Select Sporting Event"),
                                                dcc.Dropdown(
                                                    id='sporting-event-dropdown-home',
                                                    options=[{'label': event, 'value': event} for event in path_requests['sporting_event']],
                                                    value=None,
                                                    multi=True,
                                                ),
                                            ],
                                            width=4
                                        ),

                                        dbc.Col(
                                            [
                                                html.Label("Select Continent"),
                                                dcc.Dropdown(
                                                    id='continent-dropdown-home',
                                                    options=[{'label': continent, 'value': continent} for continent in continents],
                                                    value=None,
                                                    multi=True,
                                                ),
                                            ],
                                            width=4
                                        ),

                                        dbc.Col(
                                            [
                                                html.Label("Select Country"),
                                                dcc.Dropdown(
                                                    id='country-dropdown-home',
                                                    value=None,
                                                    multi=True,
                                                ),
                                            ],
                                            width=4
                                        ),
                                    ])
                                ])
                            ], className="mb-3"),
                            width=12
                        ),
                    ]),

                    dbc.Row([
                        dbc.Col(
                            dbc.Card([
                                dbc.CardHeader(html.H5("Total Website Visit Count")),
                                dbc.CardBody([
                                    html.H2(id='total-requests-value', children="Placeholder"),
                                ])
                            ], className="mb-3", style={'background-color': '#f8d7da', 'color': '#721c24', 'border-color': '#f5c6cb'}),
                            width=4
                        ),
                        dbc.Col(
                            dbc.Card([
                                dbc.CardHeader(html.H5("Peak Viewing Time")),
                                dbc.CardBody([
                                    html.H2(id='peak-viewing-time', children="Placeholder"),
                                ])
                            ], className="mb-3", style={'background-color': '#f8d7da', 'color': '#721c24', 'border-color': '#f5c6cb'}),
                            width=4
                        ),
                        dbc.Col(
                            dbc.Card([
                                dbc.CardHeader(html.H5("Most Popular Sporting Event")),
                                dbc.CardBody([
                                    html.H2(id='most-popular-sporting-event', children="Placeholder"),
                                ])
                            ], className="mb-3", style={'background-color': '#f8d7da', 'color': '#721c24', 'border-color': '#f5c6cb'}),
                            width=4
                        ),
                    ]),

                    dbc.Row([
                        dbc.Col(
                            dbc.Card([
                                dbc.CardHeader(html.H5("Average Viewership at Each Time of Day")),
                                dbc.CardBody([
                                    dcc.Graph(id='hourly-requests'),
                                ])
                            ], className="mb-3"),
                            width=7
                        ),
                        dbc.Col(
                            dbc.Card([
                                dbc.CardHeader(html.H5("Number of Visits per Sporting Event")),
                                dbc.CardBody([
                                    dcc.Graph(id='sporting-event-requests'),
                                ])
                            ], className="mb-3"),
                            width=5
                        )
                    ]),
                    dbc.Row([
                        dbc.Col(
                            dbc.Card([
                                dbc.CardHeader(html.H5("Viewership of Concurrently Running Sporting Events")),
                                dbc.CardBody([
                                    dcc.Graph(id='concurrent-sporting-events'),
                                ])
                            ], className="mb-3"),
                            width=12
                        ),
                    ]),
                ])
            ]),
        ])
    ])
])

# update country dropdown options based on selected continent - Viewership Statistics page
@app.callback(
    Output('country-dropdown-home', 'options'),
    [Input('continent-dropdown-home', 'value')]
)
def update_country_options(selected_continents):
    if selected_continents:
        filtered_data = data[data['continent'].isin(selected_continents)]
        countries_in_selected_continents = sorted(filtered_data['country'].unique())
        return [{'label': country, 'value': country} for country in countries_in_selected_continents]
    else:
        return [{'label': country, 'value': country} for country in countries]

# update continent dropdown options based on selected country - Viewership Statistics page
@app.callback(
    Output('continent-dropdown-home', 'options'),
    [Input('country-dropdown-home', 'value')]
)
def update_continent_options(selected_countries):
    if selected_countries:
        filtered_data = data[data['country'].isin(selected_countries)]
        continents_of_selected_countries = sorted(filtered_data['continent'].unique())
        return [{'label': continent, 'value': continent} for continent in continents_of_selected_countries]
    else:
        return [{'label': continent, 'value': continent} for continent in continents]


# update country dropdown options based on selected continent - Demographic Data page
@app.callback(
    Output('country-dropdown', 'options'),
    [Input('continent-dropdown', 'value')]
)
def update_country_options(selected_continents):
    if selected_continents:
        filtered_data = data[data['continent'].isin(selected_continents)]
        countries_in_selected_continents = sorted(filtered_data['country'].unique())
        return [{'label': country, 'value': country} for country in countries_in_selected_continents]
    else:
        return [{'label': country, 'value': country} for country in countries]

# update continent dropdown options based on selected country - Demographic Data page
@app.callback(
    Output('continent-dropdown', 'options'),
    [Input('country-dropdown', 'value')]
)
def update_continent_options(selected_countries):
    if selected_countries:
        filtered_data = data[data['country'].isin(selected_countries)]
        continents_of_selected_countries = sorted(filtered_data['continent'].unique())
        return [{'label': continent, 'value': continent} for continent in continents_of_selected_countries]
    else:
        return [{'label': continent, 'value': continent} for continent in continents]

# callback to update the total website visits value
@app.callback(
    Output('total-requests-value', 'children'),
    [Input('sporting-event-dropdown-home', 'value'),
     Input('country-dropdown-home', 'value'),
     Input('continent-dropdown-home', 'value')]
)
def update_total_requests(selected_sporting_events, selected_countries, selected_continents):
    filtered_data = data.copy()

    if selected_sporting_events:
        filtered_data = filtered_data[filtered_data['sporting_event'].isin(selected_sporting_events)]
    if selected_countries:
        filtered_data = filtered_data[filtered_data['country'].isin(selected_countries)]
    if selected_continents:
        filtered_data = filtered_data[filtered_data['continent'].isin(selected_continents)]

    total_requests = len(filtered_data)
    return total_requests

# callback for updating the choropleth map based on selected sporting events
@app.callback(
    Output('country-requests', 'figure'),
    [Input('sporting-event-dropdown', 'value')]
)
def update_country_requests(selected_sporting_events):
    filtered_data = data.copy()

    if selected_sporting_events:
        filtered_data = filtered_data[filtered_data['sporting_event'].isin(selected_sporting_events)]

    country_requests = filtered_data.groupby('country').size().reset_index(name='count')

    fig = px.choropleth(country_requests, locations='country', locationmode='country names', color='count',
                        color_continuous_scale='Viridis', range_color=(0, max(country_requests['count'])),
                        labels={'count': 'Visits'})
    fig.update_layout(geo=dict(showcoastlines=True))
    return fig

# callback for updating viewership time graph
@app.callback(
    Output('hourly-requests', 'figure'),
    [Input('sporting-event-dropdown-home', 'value'),
     Input('country-dropdown-home', 'value'),
     Input('continent-dropdown-home', 'value')]
)
def update_hourly_requests(selected_sporting_events, selected_countries, selected_continents):
    filtered_data = data.copy()

    if selected_sporting_events:
        filtered_data = filtered_data[filtered_data['sporting_event'].isin(selected_sporting_events)]
    if selected_countries:
        filtered_data = filtered_data[filtered_data['country'].isin(selected_countries)]
    if selected_continents:
        filtered_data = filtered_data[filtered_data['continent'].isin(selected_continents)]

    hourly_requests = filtered_data.groupby(pd.Grouper(key='time', freq='h')).size().reset_index(name='count')

    fig = px.line(hourly_requests, x='time', y='count', labels={'count': 'Visits', 'time': 'Time'})
    return fig


# callback for updating viewership by age graph
@app.callback(
    Output('age-requests', 'figure'),
    [Input('sporting-event-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('continent-dropdown', 'value')]
)
def update_age_requests(selected_sporting_events, selected_countries, selected_continents):
    filtered_data = data.copy()

    if selected_sporting_events:
        filtered_data = filtered_data[filtered_data['sporting_event'].isin(selected_sporting_events)]
    if selected_countries:
        filtered_data = filtered_data[filtered_data['country'].isin(selected_countries)]
    if selected_continents:
        filtered_data = filtered_data[filtered_data['continent'].isin(selected_continents)]

    age_requests = filtered_data.groupby('age_group', observed=True).size().reset_index(name='count')

    fig = px.bar(age_requests, x='age_group', y='count', labels={'count': 'Visits', 'age_group': 'Age Group'})
    return fig


# callback for updating viewership by gender graph
@app.callback(
    Output('gender-requests', 'figure'),
    [Input('sporting-event-dropdown', 'value'),
     Input('country-dropdown', 'value'),
     Input('continent-dropdown', 'value')]
)
def update_gender_requests(selected_sporting_events, selected_countries, selected_continents):
    filtered_data = data.copy()

    if selected_sporting_events:
        filtered_data = filtered_data[filtered_data['sporting_event'].isin(selected_sporting_events)]
    if selected_countries:
        filtered_data = filtered_data[filtered_data['country'].isin(selected_countries)]
    if selected_continents:
        filtered_data = filtered_data[filtered_data['continent'].isin(selected_continents)]

    gender_requests = filtered_data.groupby('gender', observed=True).size().reset_index(name='count')

    fig = px.pie(gender_requests, values='count', names='gender', hole=0.3)
    return fig


# callback for updating viewership by income status graph
@app.callback(
    Output('income-requests', 'figure'),
    [Input('sporting-event-dropdown', 'value'),
    Input('country-dropdown', 'value'),
    Input('continent-dropdown', 'value')]
)
def update_income_requests(selected_sporting_events, selected_countries, selected_continents):
    filtered_data = data.copy()

    if selected_sporting_events:
        filtered_data = filtered_data[filtered_data['sporting_event'].isin(selected_sporting_events)]
    if selected_countries:
        filtered_data = filtered_data[filtered_data['country'].isin(selected_countries)]
    if selected_continents:
        filtered_data = filtered_data[filtered_data['continent'].isin(selected_continents)]

    income_requests = filtered_data.groupby('income_status', observed=True).size().reset_index(name='count')

    fig = px.pie(income_requests, values='count', names='income_status', hole=0.3)
    return fig


# callback for updating the pie chart based on selected sporting events
@app.callback(
    Output('sporting-event-requests', 'figure'),
    [Input('country-dropdown-home', 'value'),
     Input('continent-dropdown-home', 'value')]
)
def update_sporting_event_requests(selected_countries, selected_continents):
    filtered_data = data.copy()

    if selected_countries:
        filtered_data = filtered_data[filtered_data['country'].isin(selected_countries)]
    if selected_continents:
        filtered_data = filtered_data[filtered_data['continent'].isin(selected_continents)]

    sporting_event_requests = filtered_data['sporting_event'].value_counts().reset_index()
    sporting_event_requests.columns = ['Sporting Event', 'Requests']

    fig = px.pie(sporting_event_requests, values='Requests', names='Sporting Event')
    return fig


# callback for updating the heatmap based on selected sporting events
@app.callback(
    Output('concurrent-sporting-events', 'figure'),
    [Input('sporting-event-dropdown-home', 'value'),
     Input('country-dropdown-home', 'value'),
     Input('continent-dropdown-home', 'value')]
)
def update_concurrent_sporting_events(selected_sporting_events, selected_countries, selected_continents):
    filtered_data = data.copy()

    if selected_sporting_events:
        filtered_data = filtered_data[filtered_data['sporting_event'].isin(selected_sporting_events)]
    if selected_countries:
        filtered_data = filtered_data[filtered_data['country'].isin(selected_countries)]
    if selected_continents:
        filtered_data = filtered_data[filtered_data['continent'].isin(selected_continents)]

    concurrent_sporting_events = filtered_data.groupby(['time', 'sporting_event']).size().reset_index(name='visits')

    fig = px.density_heatmap(concurrent_sporting_events, x="time", y="sporting_event", z="visits",
                             color_continuous_scale="balance")
    fig.update_layout(xaxis_title="Time",  
                      yaxis_title="Sporting Event", 
                      coloraxis_colorbar_title="Visits") 
    fig.update_layout(xaxis_nticks=24)  
    return fig


# callback for updating the peak viewing time value
@app.callback(
    Output('peak-viewing-time', 'children'),
    [Input('sporting-event-dropdown-home', 'value'),
     Input('country-dropdown-home', 'value'),
     Input('continent-dropdown-home', 'value')]
)
def update_peak_viewing_time(selected_sporting_events, selected_countries, selected_continents):
    filtered_data = data.copy()

    if selected_sporting_events:
        filtered_data = filtered_data[filtered_data['sporting_event'].isin(selected_sporting_events)]
    if selected_countries:
        filtered_data = filtered_data[filtered_data['country'].isin(selected_countries)]
    if selected_continents:
        filtered_data = filtered_data[filtered_data['continent'].isin(selected_continents)]

    hourly_requests = filtered_data.groupby(pd.Grouper(key='time', freq='h')).size().reset_index(name='count')

    peak_viewing_time = calculate_peak_viewing_time(hourly_requests)
    return peak_viewing_time.strftime('%H:%M')


# callback for updating the most popular sporting event value
@app.callback(
    Output('most-popular-sporting-event', 'children'),
    [Input('country-dropdown-home', 'value'),
     Input('continent-dropdown-home', 'value')]
)
def update_most_popular_sporting_event(selected_countries, selected_continents):
    filtered_data = data.copy()

    if selected_countries:
        filtered_data = filtered_data[filtered_data['country'].isin(selected_countries)]
    if selected_continents:
        filtered_data = filtered_data[filtered_data['continent'].isin(selected_continents)]

    most_popular_event = calculate_most_popular_sporting_event(filtered_data)
    return most_popular_event


if __name__ == '__main__':
    app.run_server(debug=True)
