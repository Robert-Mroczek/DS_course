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
unique_sites = spacex_df['Launch Site'].unique()
option_list = [{'label': 'All Sites', 'value': 'ALL'}]
for site in unique_sites: 
    option_list.append({'label':site,'value': site})
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',  options= option_list,
                                value= 'ALL',
                                placeholder = 'Select a Launch Site here', 
                                searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min = 0,
                                max = 10000,
                                step = 1000,
                                value = [min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id = 'success-pie-chart',component_property = 'figure'),
Input(component_id = 'site-dropdown', component_property = 'value'))

def get_pie_chart(entered_site): 
    filtered_df = spacex_df
    if entered_site == 'ALL':
        filtered_df = filtered_df[filtered_df['class']==1]
        grouped = filtered_df.groupby(['Launch Site'],as_index = False)['class'].count() 
        fig = px.pie(grouped,values = 'class',
        names = 'Launch Site',
        title = 'Total succes launches by site')
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site] 
        grouped = filtered_df.groupby(['class'],as_index = False)['Launch Site'].count()
        fig = px.pie(grouped,values = 'Launch Site',
        names = 'class',
        title = f'Total succes launches for {entered_site} site')
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id = 'success-payload-scatter-chart',component_property = 'figure'),
Input(component_id = 'payload-slider',component_property = 'value'),
Input(component_id='site-dropdown', component_property='value'))

def get_payload_succes(payload_value,entered_site): 
    if entered_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_value[0])&(spacex_df['Payload Mass (kg)'] <= payload_value[1])]
        fig = px.scatter(filtered_df, x = 'Payload Mass (kg)', y = 'class',
        color = 'Booster Version Category',
        title = 'Corellation Payload vs Succes all sites')
    else: 
        filtered_df = spacex_df[(spacex_df['Launch Site']== entered_site)&(spacex_df['Payload Mass (kg)'] >= payload_value[0])&(spacex_df['Payload Mass (kg)'] <= payload_value[1])]
        fig = px.scatter(filtered_df, x = 'Payload Mass (kg)', y = 'class',
        color = 'Booster Version Category',
        title = f'Corellation Payload vs Succes {entered_site} site')
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
