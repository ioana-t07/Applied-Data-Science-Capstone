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
                                dcc.Dropdown(id='site-dropdown', 
                                            options=[
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': 'site1', 'value': 'site1'}],
                                            value='ALL',
                                            placeholder="Select a Launch Site here",
                                            searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart', 
                                                   figure = px.pie(data, values='class',
                                                        names='pie chart names', title= 'title'))),

                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 100: '100'},
                                                value=[min_value, max_value])

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart', 
                                                   (fig = px.scatter(data, x='Payload Mass (kg)', y='class', 
                                                        color="Booster Version Category",
                                                        labels={'class': 'Landing outcome', 'Payload Mass (kg)': 'Payload Mass (kg)'},
                                                        legend = (["Booster Version Category"]),
                                                        title='title'),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    succes_launch = spacex_df.groupby('Launch Site')[spacex_df['class'] ==1].sum().reset_index()
    site_launch = spacex_df.groupby('class')[spacex_df['Launch Site'] == entered_site].sum().reset_index()
    if entered_site == 'ALL':
        fig = px.pie(succes_launch, values='class', names='class', 
            legend = (["Launch Site"]),
            title='Total Successful launches for all sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        fig = px.pie(site_launch, values='class', names='class',
            legend = (["class"]),
            title="Total launches for site {}".format(enter_site))
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
       
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            [Input(component_id='site-dropdown', component_property='value'), 
            Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site):
    filtered_df = spacex_df.['Launch Site'] == entered_site
    if entered_site == 'ALL':
        fig = px.scatter(spacex_df, x='Payload Mass (kg)', y='class', 
            color="Booster Version Category",
            labels={'class': 'Landing outcome', 'Payload Mass (kg)': 'Payload Mass (kg)'},
            legend = (["Booster Version Category"]),
            title='Correlation between Payload and succces for all sites ')
        return fig
                
    else:        
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
            color="Booster Version Category",
            labels={'class': 'Landing outcome', 'Payload Mass (kg)': 'Payload Mass'},
            legend = (["Booster Version Category"]),
            title= "Correlation between Payload and succces for site {}".format(enter_site))
        return fig



# Run the app
if __name__ == '__main__':
    app.run_server()

