from dash import Dash, html

app = Dash(__name__)

app.layout = html.Div([
    html.H1("My Dashboard"),
    html.H2("Welcome"),
    html.P("This is my Dash application."),

    html.Label("Name:"),
    html.Br(),

    html.Button("Click Me"),
    html.Br(),

    html.Img(src="https://example.com/image.jpg"),
    html.Br(),

    html.A("Visit Google", href="https://www.google.com")
])

app.run(debug=True)