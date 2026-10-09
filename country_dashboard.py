from dash import Dash, html, dcc, Input, Output

# 1. Create the Dash application
app = Dash(__name__)

# 2. Define the layout
app.layout = html.Div(
    style={
        "maxWidth": "900px",
        "margin": "30px auto",
        "padding": "25px",
        "fontFamily": "Arial",
        "backgroundColor": "#f4f6f9"
    },

    children=[

        # Main heading
        html.H1(
            "Country Data Dashboard",
            style={"textAlign": "center", "color": "#17365d"}
        ),

        html.P(
            "Learn Dash Core Components with an interactive example.",
            style={"textAlign": "center"}
        ),

        html.Hr(),

        # 3. Dropdown
        html.Label("Select a country:"),
        dcc.Dropdown(
            id="country-dropdown",
            options=[
                {"label": "Pakistan", "value": "Pakistan"},
                {"label": "India", "value": "India"},
                {"label": "Bangladesh", "value": "Bangladesh"}
            ],
            value="Pakistan",
            clearable=False
        ),

        html.Br(),

        # 4. Slider
        html.Label("Select a number:"),
        dcc.Slider(
            id="number-slider",
            min=0,
            max=100,
            step=10,
            value=50,
            marks={
                0: "0",
                20: "20",
                40: "40",
                60: "60",
                80: "80",
                100: "100"
            }
        ),

        html.Br(),

        # 5. Radio buttons
        html.Label("Select a region:"),
        dcc.RadioItems(
            id="region-radio",
            options=[
                {"label": "Asia", "value": "Asia"},
                {"label": "Europe", "value": "Europe"},
                {"label": "Africa", "value": "Africa"}
            ],
            value="Asia",
            inline=True
        ),

        html.Br(),

        # 6. Checklist
        html.Label("Select your interests:"),
        dcc.Checklist(
            id="interests-checklist",
            options=[
                {"label": "Python", "value": "Python"},
                {"label": "Pandas", "value": "Pandas"},
                {"label": "Data Visualization",
                 "value": "Data Visualization"}
            ],
            value=["Python"],
            inline=True
        ),

        html.Br(),

        # 7. Date picker
        html.Label("Select a date:"),
        dcc.DatePickerSingle(
            id="date-picker",
            date="2026-10-09",
            display_format="YYYY-MM-DD"
        ),

        html.Hr(),

        # 8. Display the interactive result
        html.H2("Your Selections"),

        html.Div(
            id="output-text",
            style={
                "backgroundColor": "white",
                "padding": "15px",
                "borderRadius": "8px",
                "lineHeight": "2"
            }
        ),

        html.Br(),

        # 9. Graph
        dcc.Graph(id="country-graph")

    ]
)


# 10. Callback: update the dashboard
@app.callback(
    Output("output-text", "children"),
    Output("country-graph", "figure"),

    Input("country-dropdown", "value"),
    Input("number-slider", "value"),
    Input("region-radio", "value"),
    Input("interests-checklist", "value"),
    Input("date-picker", "date")
)
def update_dashboard(country, number, region, interests, date):

    # Example data (not real country statistics)
    country_data = {
        "Pakistan": [20, 40, 60],
        "India": [30, 50, 70],
        "Bangladesh": [15, 35, 55]
    }

    # Change the chart values using the slider
    values = [
        value + number
        for value in country_data[country]
    ]

    # Create the summary
    summary = html.Div([
        html.P(f"Selected country: {country}"),
        html.P(f"Selected number: {number}"),
        html.P(f"Selected region: {region}"),
        html.P(
            "Selected interests: "
            + (", ".join(interests) if interests else "None")
        ),
        html.P(f"Selected date: {date}")
    ])

    # Create the chart
    figure = {
        "data": [
            {
                "x": ["January", "February", "March"],
                "y": values,
                "type": "bar",
                "name": country,
                "marker": {"color": "#2878b5"}
            }
        ],
        "layout": {
            "title": f"Example Data for {country}",
            "xaxis": {"title": "Month"},
            "yaxis": {"title": "Example Value"},
            "template": "plotly_white"
        }
    }

    return summary, figure


# 11. Run the application
if __name__ == "__main__":
    app.run(debug=True)

