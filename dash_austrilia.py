from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# ----------------------------------
# 1. Load and prepare the dataset
# ----------------------------------

df = pd.read_csv("Historical_Wildfires.csv")

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Remove rows with invalid dates
df = df.dropna(subset=["Date"]).copy()

# Create Year and Month columns
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month_name()
df["Month_Number"] = df["Date"].dt.month

# Remove missing region values
df = df.dropna(subset=["Region"]).copy()

# ----------------------------------
# 2. Create the Dash application
# ----------------------------------

app = Dash(__name__)

app.layout = html.Div(
    children=[
        # Dashboard heading
        html.H1(
            "Australia Wildfire Dashboard",
            style={
                "color": "#503D36",
                "textAlign": "center",
                "fontSize": "30px",
                "marginBottom": "25px"
            }
        ),

        # Region selection
        html.Div(
            [
                html.Label(
                    "Select Region:",
                    style={
                        "fontSize": "18px",
                        "fontWeight": "bold",
                        "marginBottom": "10px"
                    }
                ),

                dcc.RadioItems(
                    id="region",
                    options=[
                        {"label": "New South Wales", "value": "NSW"},
                        {"label": "Northern Territory", "value": "NT"},
                        {"label": "Queensland", "value": "QL"},
                        {"label": "South Australia", "value": "SA"},
                        {"label": "Tasmania", "value": "TA"},
                        {"label": "Victoria", "value": "VI"},
                        {"label": "Western Australia", "value": "WA"}
                    ],
                    value="NSW",
                    inline=True,
                    labelStyle={
                        "display": "inline-block",
                        "marginRight": "18px",
                        "marginBottom": "10px"
                    }
                )
            ],
            style={"marginBottom": "25px"}
        ),

        # Year selection
        html.Div(
            [
                html.Label(
                    "Select Year:",
                    style={
                        "fontSize": "18px",
                        "fontWeight": "bold"
                    }
                ),

                dcc.Dropdown(
                    id="year",
                    options=[
                        {"label": str(year), "value": int(year)}
                        for year in sorted(df["Year"].dropna().unique())
                    ],
                    value=(
                        2005
                        if 2005 in df["Year"].values
                        else int(df["Year"].min())
                    ),
                    clearable=False,
                    style={"width": "250px", "marginTop": "10px"}
                )
            ],
            style={"marginBottom": "30px"}
        ),

        # Graphs
        html.Div(
            [
                html.Div(
                    id="plot1",
                    style={"width": "50%", "padding": "10px"}
                ),

                html.Div(
                    id="plot2",
                    style={"width": "50%", "padding": "10px"}
                )
            ],
            style={
                "display": "flex",
                "flexWrap": "wrap",
                "width": "100%"
            }
        ),

        # Error or information messages
        html.Div(
            id="message",
            style={
                "color": "#B22222",
                "textAlign": "center",
                "marginTop": "15px"
            }
        )
    ],
    style={
        "fontFamily": "Arial, sans-serif",
        "padding": "20px",
        "backgroundColor": "#F7F7F7",
        "minHeight": "100vh"
    }
)

# ----------------------------------
# 3. Callback to update the graphs
# ----------------------------------

@app.callback(
    [
        Output("plot1", "children"),
        Output("plot2", "children"),
        Output("message", "children")
    ],
    [
        Input("region", "value"),
        Input("year", "value")
    ]
)
def reg_year_display(input_region, input_year):

    # Filter data by selected region and year
    region_data = df[df["Region"] == input_region]

    y_r_data = region_data[
        region_data["Year"] == input_year
    ].copy()

    # Check whether data exists
    if y_r_data.empty:
        return (
            html.Div(),
            html.Div(),
            f"No wildfire data found for {input_region} in {input_year}."
        )

    # Check required numerical columns
    required_columns = ["Estimated_fire_area", "Count"]

    if not all(col in y_r_data.columns for col in required_columns):
        return (
            html.Div(),
            html.Div(),
            "The dataset is missing Estimated_fire_area or Count."
        )

    # ----------------------------------
    # 4. Prepare pie chart data
    # ----------------------------------

    est_data = (
        y_r_data.groupby(
            ["Month_Number", "Month"],
            as_index=False
        )["Estimated_fire_area"]
        .mean()
        .sort_values("Month_Number")
    )

    est_data = est_data.dropna(subset=["Estimated_fire_area"])

    if est_data.empty:
        fig1 = None
        graph1 = html.Div("No estimated fire-area data available.")
    else:
        fig1 = px.pie(
            est_data,
            values="Estimated_fire_area",
            names="Month",
            title=(
                f"{input_region}: Monthly Average "
                f"Estimated Fire Area in {input_year}"
            ),
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        fig1.update_layout(
            title_x=0.5,
            template="plotly_white",
            height=450,
            margin=dict(l=20, r=20, t=70, b=20)
        )

        graph1 = dcc.Graph(
            figure=fig1,
            config={"responsive": True}
        )

    # ----------------------------------
    # 5. Prepare bar chart data
    # ----------------------------------

    veg_data = (
        y_r_data.groupby(
            ["Month_Number", "Month"],
            as_index=False
        )["Count"]
        .mean()
        .sort_values("Month_Number")
    )

    veg_data = veg_data.dropna(subset=["Count"])

    if veg_data.empty:
        graph2 = html.Div("No vegetation-fire count data available.")
    else:
        fig2 = px.bar(
            veg_data,
            x="Month",
            y="Count",
            title=(
                f"{input_region}: Average Count of Pixels "
                f"for Presumed Vegetation Fires in {input_year}"
            ),
            labels={
                "Month": "Month",
                "Count": "Average Fire Pixel Count"
            },
            color="Count",
            color_continuous_scale="OrRd"
        )

        fig2.update_layout(
            title_x=0.5,
            template="plotly_white",
            height=450,
            xaxis_title="Month",
            yaxis_title="Average Pixel Count",
            margin=dict(l=40, r=20, t=70, b=50)
        )

        graph2 = dcc.Graph(
            figure=fig2,
            config={"responsive": True}
        )

    return graph1, graph2, ""


# ----------------------------------
# 6. Run the application
# ----------------------------------

if __name__ == "__main__":
    app.run(debug=True)

