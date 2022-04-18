# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites','value': 'ALL'},
                                        {'label': 'CCAFS LC-40','value': 'CCAFS LC-40'},
                                        {'label': 'VAFB SLC-4E','value': 'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A','value': 'KSC LC-39A'},
                                        {'label': 'CCAFS SLC-40','value': 'CCAFS SLC-40'},
                                    ],
                                    value='ALL',
                                    placeholder='Select a Launch Site here',
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
                                    id='payload-slider', 
                                    min=0, 
                                    max=10000, 
                                    step=1000, 
                                    marks={0: '0', 2500: '2500', 5000:'5000', 7500:'7500', 10000:'10000'}, 
                                    value=[min_payload, max_payload]
                                    
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart' ,component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)

def getChart(inputSite):

    df = spacex_df.copy()

    if inputSite == 'ALL':

        print(inputSite)

        fig = px.pie(
        df, 
        values='class',
        names='Launch Site',
        title='Total Success Launches By Site'
        )

        return fig

    else:

        df = df[df['Launch Site'] == inputSite]['class'].value_counts()

        print(inputSite)
        print(df)

        ratio = [0, 1]

        fig = px.pie(
        df, 
        values='class',
        names=ratio,
        title=f'Total Success Launches for site {inputSite}'
        )

        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')]
)
def getScatter(inputSite, sliderValue):

    df2 = spacex_df.copy()

    low, high = sliderValue
    mask = (df2['Payload Mass (kg)'] > low) & (df2['Payload Mass (kg)'] < high)

    if inputSite == 'ALL':

        print(sliderValue)

        figure = px.scatter(
            df2[mask],
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
        )

        return figure

    else:

        df2 = df2[df2['Launch Site'] == inputSite]

        print(inputSite)
        print(df2)

        figure = px.scatter(
            df2[mask],
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
        )

        return figure

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
