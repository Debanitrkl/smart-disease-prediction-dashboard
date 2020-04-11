import sys
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from web_app.app import app
from web_app.apps import india_dashboard, world_dashboard

sys.path.append("/mnt/data/Events/CODE19/smart-disease-prediction-dashboard/")

app.layout = html.Div([
    dcc.Location(id='url', refresh=False, pathname='/apps/india_dashboard'),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    print(pathname)
    if pathname == '/apps/india_dashboard':
        return india_dashboard.layout
    elif pathname == '/apps/world_dashboard':
        return world_dashboard.layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=False)
