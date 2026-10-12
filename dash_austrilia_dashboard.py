
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd

import plotly.express as px


# Load the automobile sales data
data = pd.read_csv(
    # 'automobile_sales.csv'
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv"
)




# Initialize the Dash application
app = dash.Dash(__name__)
app.title = "Automobile Sales Statistics Dashboard"

# Dropdown options
dropdown_options = [
    {
        "label": "Yearly Statistics",
        "value": "Yearly Statistics"
    },
    {
        "label": "Recession Period Statistics",
        "value": "Recession Period Statistics"
    }
]

# List of years
year_list = [i for i in range(1980, 2024)]

# Create the dashboard layout
app.layout = html.Div([
    # TASK 2.1: Dashboard title
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={
            "textAlign": "center",
            "color": "#503D36",
            "fontSize": "24px"
        }
    ),

    # TASK 2.2: Report type dropdown
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id="dropdown-statistics",
            options=dropdown_options,
            value="Select Statistics",
            placeholder="Select a report type",
            style={
                "width": "80%",
                "padding": "3px",
                "fontSize": "20px",
                "textAlignLast": "center"
            }
        )
    ]),

    # Year dropdown
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id="select-year",
            options=[
                {"label": i, "value": i}
                for i in year_list
            ],
            value="Select-year",
            placeholder="Select-year",
            disabled=True
        )
    ]),

    # TASK 2.3: Output container
    html.Div([
        html.Div(
            id="output-container",
            className="chart-grid",
            style={"display": "flex", "flexDirection": "column"}
        )
    ])
])


# TASK 2.4: Enable/disable the year dropdown
@app.callback(
    Output("select-year", "disabled"),
    Input("dropdown-statistics", "value")
)
def update_input_container(selected_statistics):

    if selected_statistics == "Yearly Statistics":
        return False
    else:
        return True


# Callback to display the selected report
@app.callback(
    Output("output-container", "children"),
    [
        Input("dropdown-statistics", "value"),
        Input("select-year", "value")
    ]
)
def update_output_container(selected_statistics, input_year):

    # =====================================================
    # TASK 2.5: Recession Period Statistics
    # =====================================================
    if selected_statistics == "Recession Period Statistics":

        # Filter recession-period data
        recession_data = data[data["Recession"] == 1]

        # Plot 1: Average automobile sales by year
        yearly_rec = (
            recession_data.groupby("Year")["Automobile_Sales"]
            .mean()
            .reset_index()
        )

        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x="Year",
                y="Automobile_Sales",
                title="Average Automobile Sales During Recession"
            )
        )

        # Plot 2: Average sales by vehicle type
        average_sales = (
            recession_data.groupby("Vehicle_Type")["Automobile_Sales"]
            .mean()
            .reset_index()
        )

        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title="Average Automobile Sales by Vehicle Type During Recession",
                labels={
                    "Vehicle_Type": "Vehicle Type",
                    "Automobile_Sales": "Average Automobile Sales"
                }
            )
        )

        # Plot 3: Advertising expenditure share by vehicle type
        exp_rec = (
            recession_data.groupby("Vehicle_Type")[
                "Advertising_Expenditure"
            ]
            .sum()
            .reset_index()
        )

        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title="Advertising Expenditure Share by Vehicle Type During Recession"
            )
        )

        # Plot 4: Effect of unemployment on vehicle sales
        unemp_data = (
            recession_data.groupby(
                ["unemployment_rate", "Vehicle_Type"]
            )["Automobile_Sales"]
            .mean()
            .reset_index()
        )

        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x="unemployment_rate",
                y="Automobile_Sales",
                color="Vehicle_Type",
                labels={
                    "unemployment_rate": "Unemployment Rate",
                    "Automobile_Sales": "Average Automobile Sales",
                    "Vehicle_Type": "Vehicle Type"
                },
                title="Effect of Unemployment Rate on Vehicle Type and Sales"
            )
        )

        # Return all four recession graphs
        return [
            html.Div(
                className="chart-item",
                children=[R_chart1, R_chart2],
                style={"display": "flex", "flexWrap": "wrap"}
            ),
            html.Div(
                className="chart-item",
                children=[R_chart3, R_chart4],
                style={"display": "flex", "flexWrap": "wrap"}
            )
        ]

    # =====================================================
    # TASK 2.6: Yearly Statistics
    # =====================================================
    elif (
        input_year is not None
        and selected_statistics == "Yearly Statistics"
        and input_year in year_list
    ):

        # Filter data for the selected year
        yearly_data = data[data["Year"] == input_year]

        # Plot 1: Automobile sales over the entire period
        yas = (
            data.groupby("Year")["Automobile_Sales"]
            .mean()
            .reset_index()
        )

        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x="Year",
                y="Automobile_Sales",
                title="Average Automobile Sales Over the Years"
            )
        )

        # Plot 2: Total monthly automobile sales
        mas = (
            yearly_data.groupby("Month")["Automobile_Sales"]
            .sum()
            .reset_index()
        )

        # Ensure months appear in calendar order
        month_order = [
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ]

        mas["Month"] = pd.Categorical(
            mas["Month"],
            categories=month_order,
            ordered=True
        )

        mas = mas.sort_values("Month")

        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x="Month",
                y="Automobile_Sales",
                title="Total Monthly Automobile Sales"
            )
        )

        # Plot 3: Average sales by vehicle type in selected year
        avr_vdata = (
            yearly_data.groupby("Vehicle_Type")["Automobile_Sales"]
            .mean()
            .reset_index()
        )

        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title=(
                    "Average Vehicles Sold by Vehicle Type "
                    f"in the Year {input_year}"
                ),
                labels={
                    "Vehicle_Type": "Vehicle Type",
                    "Automobile_Sales": "Average Automobile Sales"
                }
            )
        )

        # Plot 4: Advertising expenditure by vehicle type
        exp_data = (
            yearly_data.groupby("Vehicle_Type")[
                "Advertising_Expenditure"
            ]
            .sum()
            .reset_index()
        )

        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title="Total Advertising Expenditure for Each Vehicle"
            )
        )

        # Return all four yearly graphs
        return [
            html.Div(
                className="chart-item",
                children=[Y_chart1, Y_chart2],
                style={"display": "flex", "flexWrap": "wrap"}
            ),
            html.Div(
                className="chart-item",
                children=[Y_chart3, Y_chart4],
                style={"display": "flex", "flexWrap": "wrap"}
            )
        ]

    # No report selected yet
    return None


# Run the Dash application
if __name__ == "__main__":
    app.run(debug=True)