from dash import Dash, html,dcc,Input,Output
import datetime as dt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# data
df = pd.read_csv('Historical_Wildfires.csv')
df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
df['Year'] = pd.to_datetime(df['Date']).dt.year



app =Dash(__name__)

app.layout = html.Div(children=[
    html.H1('Austrilia Wildfire Dashboard',style={'color' : '#503D36','text-align':'center','font-size':26}),

    html.Div([
                  
        # html.Div([
        #     html.H2('Select Region:', style={'margin-right': '2em'}),
        #      #Radio items to select the region
        #      dcc.RadioItems(['NSW','QL','SA','TA','VI','WA'], 'NSW', id='region',inline=True)]),
        #OR you can use labels:value pair a well in raioditems as below
			#Radio items to select the region
                    dcc.RadioItems([{"label":"New South Wales","value": "NSW"},
                                    {"label":"Northern Territory","value": "NT"},
                                    {"label":"Queensland","value": "QL"},
                                    {"label":"South Australia","value": "SA"},
                                    {"label":"Tasmania","value": "TA"},
                                    {"label":"Victoria","value": "VI"},
                                    {"label":"Western Australia","value": "WA"}],value="NSW", id='region',inline=True)]),
                    html.Div([
                        html.H2('Select Year:', style={'margin-right': '2em'}),
                        dcc.Dropdown(df.Year.unique(), value = 2005,id='year')
                        #notice the use of unique() from pandas to fetch the values of year from the dataframe for dropdown
                    ]),
                    html.Div([
                
                        html.Div([ ], id='plot1'),
                        html.Div([ ], id='plot2')

                    ], style={'display':'flex'}),

])
    
@app.callback([Output(component_id='plot1', component_property='children'),
               Output(component_id='plot2', component_property='children')],
               [Input(component_id='region', component_property='value'),
                Input(component_id='year', component_property='value')])
def reg_year_display(input_region,input_year):
    region_data = df[df['Region'] == input_region]
    y_r_data = region_data[region_data['Year'] == input_year]

    est_data = y_r_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    fig1 = px.pie(est_data,values='Estimated_fire_area',names='Month',title=f'{input_region} : Monthly Average Estimated Fire Area in year {input_year}')

    veg_data = y_r_data.groupby('Month')['Count'].mean().reset_index()
    fig2 = px.bar(veg_data,x='Month',y='Count',title=f'{input_region} : Average Count of Pixels for Presumed Vegetation Fires in year {input_year}')

    return [dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2)]




if __name__ == "__main__":
    app.run()