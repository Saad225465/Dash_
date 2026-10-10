from dash import Dash,html,dcc,Input,Output
import pandas as pd
import plotly.express as px
airline_data = pd.read_csv('airline_data.csv', encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 
                                   'Div1TailNum': str, 
                                   'Div2Airport': str, 
                                   'Div2TailNum': str})
app = Dash(__name__)
app.layout = html.Div(children=[ html.H1('Total number of flights to the destination state split by reporting airline',
                            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
                            html.Div(["Input Year: ", dcc.Input(id='input-year',value='2010',
                            type='number', style={'height':'50px', 'font-size': 35}),], 
                            style={'font-size': 40}),html.Br(), html.Br(),
                            html.Div(dcc.Graph(id='bar-plot')),])

@app.callback(Output(component_id='bar-plot',component_property='figure'),
              Input(component_id='input-year',component_property='value'))
def get_graph(enter_year):
    df = airline_data[airline_data['Year'] == int(enter_year)]
    bar_data = df.groupby('DestState')['Flights'].sum().reset_index()
    fig = px.bar(bar_data,x='DestState',y='Flights')
    fig.update_layout(title='Flights to Destination State', xaxis_title='DestState', yaxis_title='Flights')

    return  fig

if __name__ == '__main__':
    app.run()