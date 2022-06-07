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

launch_site_list = list(spacex_df['Launch Site'].unique())
launch_site_options = []
for site in launch_site_list:
    launch_site_options.append({'label': site, 'value': site})

#print (launch_site_options)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                
                                dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                {'label': 'All Sites', 'value': 'ALL'}
                                            ] + launch_site_options,
                                            value='ALL',
                                            placeholder="Select a Launch Site here",
                                            searchable=True
                                ),
                                
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                        2500: '2500',
                                                        5000: '5000',
                                                        7500: '7500',
                                                        10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df

    if entered_site == 'ALL':
        data = filtered_df

        fig = px.pie(data, values='class', 
        names='Launch Site', 
        title='Total Successful Launch by Site')
        return fig
    else:
        data = filtered_df[['Launch Site','class']][filtered_df['Launch Site'] == entered_site]
        
        #print (data)
        data = data.groupby(['class']).count().reset_index()

        #print (data)

        fig = px.pie(data, values='Launch Site', 
        names='class', 
        title='Total Successful Launch by Site')
        return fig
        # return the outcomes piechart for a selected site


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'), 
    Input(component_id="payload-slider", component_property="value"))
def update_chart(site_dropdown, payload_slider):
    filtered_df = spacex_df

    #print (f"task 4 - {site_dropdown} and {payload_slider}")
    if site_dropdown == 'ALL':
        data = filtered_df
        mask = (data['Payload Mass (kg)'] > payload_slider[0]) & (data['Payload Mass (kg)'] < payload_slider[1])
        data = data[mask]

        fig = px.scatter(data, 
                        x='Payload Mass (kg)', 
                        y='class',
                        color="Booster Version Category", 
                        title='Correlation between Payload and Success for all Sites')

        
        return fig
    else:
        data = filtered_df
        mask = (data['Payload Mass (kg)'] > payload_slider[0]) & (data['Payload Mass (kg)'] < payload_slider[1]) & (data['Launch Site'] == site_dropdown)
        data = data[mask]

        fig = px.scatter(data, 
                        x='Payload Mass (kg)', 
                        y='class',
                        color="Booster Version Category", 
                        title='Correlation between Payload and Success for all Sites')

        
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
