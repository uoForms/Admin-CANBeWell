import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_core_components as dcc

df = pd.read_csv("export.csv", parse_dates = ['date'])

df_def = df.describe()

df_pageviewtime = df\
            .groupby(['role', 'gender', 'navigation', 'item'])\
            .pageviewtime.agg(['mean', 'min', 'max'])\
            .reset_index()

# create table layout
def generate_table(dataframe, max_rows=100):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H3(children='CANBeWell Data visualization'),
        
        html.Label('Select gender'),
        html.Div([
            dcc.Dropdown(
                id='gender',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value=['gender'],
                multi=True
            )
            ],style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='navigation-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value=['navigation'],
                multi = True
            )],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    )],

        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
        ),
    
        html.Div([
            html.H4(chhildren='Data overall description'),
            generate_table(df_def)
        )],
        generate_table(df_pageviewtime),

        dcc.Slider(
            id='time--slider',
            min=df['date'].min(),
            max=df['date'].max(),
            value=df['date'].max(),
            marks={str(date): str(date) for date in df['date'].unique()},
            step=None
    )
])


@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)