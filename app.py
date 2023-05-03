import dash
from dash import html
import plotly.graph_objects as go
from dash import dcc
from dash.dependencies import Input, Output, State
import pandas as pd
from utils.neo4j_util import Neo4jQuery
from utils.mongodb_util import MongoQuery
from utils.sql_util import SqlQuery
import dash_cytoscape as cyto


external_stylesheets = [
    {
        'href': 'https://fonts.googleapis.com/css?family=Open+Sans&display=swap',
        'rel': 'stylesheet'
    },
    {
        'href': 'https://fonts.googleapis.com/css?family=Montserrat&display=swap',
        'rel': 'stylesheet'
    },
    {
        'href': 'https://fonts.googleapis.com/css?family=Roboto&display=swap',
        'rel': 'stylesheet'
    }
]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
institutes = pd.read_csv('doc/institutes.csv')
keywords = pd.read_csv('doc/keywords.csv')
app.layout = html.Div(id = 'parent', children = [
        html.H1(id = 'H00', children = 'Computer Science Academic World Web Application', style = {'textAlign':'center',\
                    'font-family': 'Roboto, sans-serif','marginTop':40,'marginBottom':40,}),

        html.H2(id = 'H6', children = 'Popularity Trend', style = {'textAlign':'center',\
                     'font-family': 'Open Sans, sans-serif','marginTop':40,'marginBottom':40}),
        html.Div(
            id='description6',
            children=["In this panel, you can find out the overall trend of a given topic. "],
            style={'font-family': 'Arial'}
        ),
        dcc.Dropdown( id = 'dropdown3',
        options = [{'label': row['name'], 'value': row['name']} for index, row in keywords.iterrows()],
        value = 'algorithm'),
        dcc.Graph(id = 'time_plot'),


        html.H2(id = 'H1', children = 'Query University', style = {'textAlign':'center',\
                        'font-family': 'Open Sans, sans-serif','marginTop':40,'marginBottom':40}),
        html.Div(
            id='description1',
            children=["In this panel, you can find out the universities with the most professors studying a given research topic. "],
            style={'font-family': 'Arial'}
        ),
        html.Label('Enter a keyword:'),
        dcc.Input(id='input-keyword-1', type='text', value='machine learning'),
        html.Button('Generate Query', id='button-query-1'),
        html.Div(id='output-query-1'),

        html.H2(id = 'H4', children = 'Top Research Topics', style = {'textAlign':'center',\
                        'font-family': 'Open Sans, sans-serif','marginTop':40,'marginBottom':40}),
        html.Div(
            id='description4',
            children=["In this panel, you can find out the top ten research topics in a university. "],
            style={'font-family': 'Arial'}
        ),
        dcc.Dropdown( id = 'dropdown1',
        options = [{'label': row['name'], 'value': row['name']} for index, row in institutes.iterrows()],
        value = 'American University'),
        dcc.Graph(id = 'bar_plot'),
  

        html.H2(id = 'H5', children = 'Collaboration network', style = {'textAlign':'center',\
                        'font-family': 'Open Sans, sans-serif','marginTop':40,'marginBottom':40}),
        html.Div(
            id='description5',
            children=["In this panel, you can find out the colloration network in a university. "],
            style={'font-family': 'Arial'}
        ),
        dcc.Dropdown( id = 'dropdown2',
        options = [{'label': row['name'], 'value': row['name']} for index, row in institutes.iterrows()],
        value = 'American University'),
        cyto.Cytoscape(
            id='cytoscape',
            layout={'name': 'circle'},
        style={
            'width': '100%',
            'height': '500px',
            'edge-text-rotation': 'autorotate',
            'text-outline-width': 2,
            'text-outline-color': '#fff',
            'text-outline-opacity': 1,
            'font-size': 12,
            'label': 'data(label)',
            'text-valign': 'center',
            'text-halign': 'center'
        },
        elements=[]
        ),



        html.H2(id = 'H2', children = 'Query Faculty', style = {'textAlign':'center',\
                        'font-family': 'Open Sans, sans-serif','marginTop':40,'marginBottom':40}),
        html.Div(
            id='description2',
            children=["In this panel, you can find out the faculties with the highest keyword related citations given a research topic. "],
            style={'font-family': 'Arial'}
        ),

        html.Label('Enter a keyword:'),
        dcc.Input(id='input-keyword-2', type='text', value='machine learning'),
        html.Button('Generate Query', id='button-query-2'),
        html.Div(id='output-query-2'),


        html.H2(id = 'H3', children = 'Faculty Reserch Trend', style = {'textAlign':'center',\
                        'font-family': 'Open Sans, sans-serif','marginTop':40,'marginBottom':40}),
        html.Div(
            id='description3',
            children=["In this panel, you can find trend of a given topic studied by a professor. "],
            style={'font-family': 'Arial'}
        ),
        html.Label('Enter a keyword:'),
        dcc.Input(id='input-keyword-3-1', type='text', value='data'),
        html.Label('Enter faculty name:'),
        dcc.Input(id='input-keyword-3-2', type='text', value='Elisa Bertino'),
        html.Button('Generate Query', id='button-query-3'),
        html.Div(id='output-query-3'),







        ##update
        html.H3(id = 'H01', children = 'Update University', style = {'textAlign':'left',\
                    'font-family': 'Montserrat, sans-serif','marginTop':40,'marginBottom':40,}),
        html.Div(
            id='description01',
            children=["You can update the photo url of universities here. Enter the university name below, example: Columbia University."],
            style={'font-family': 'Arial'}
        ),
        dcc.Input(id='input10', type='text', placeholder='University Name'),
        dcc.Input(id='input20', type='text', placeholder='Photo_url'),
        html.Button('Update Record', id='button-update0'),
        html.Div(id='output-update0'),


        html.H3(id = 'H02', children = 'Update Faculty', style = {'textAlign':'left',\
                    'font-family': 'Montserrat, sans-serif', 'marginTop':40,'marginBottom':40}),
        html.Div(
            id='description02',
            children=["You can update email, phone, and url of faculties here. Enter the faculty name below, example: Michael L. Littman."],
            style={'font-family': 'Arial'}
        ),
        dcc.Input(id='input1', type='text', placeholder='Name'),
        dcc.Input(id='input2', type='text', placeholder='Enter email'),
        dcc.Input(id='input3', type='text', placeholder='Enter phone'),
        dcc.Input(id='input4', type='text', placeholder='Enter photo url'),
        html.Button('Update Record', id='button-update'),
        html.Div(id='output-update'),

    ])






@app.callback(Output(component_id='bar_plot', component_property= 'figure'),
              [Input(component_id='dropdown1', component_property= 'value')])
def graph_update(dropdown_value1):
    print(dropdown_value1)
    df = Neo4j.query_research_topics(dropdown_value1)
    fig = go.Figure(
        data=[go.Bar(x=df['name'], y=df['total_score'])],
        layout_title_text="Sample Bar Chart"
    )
    
    fig.update_layout(title = 'Top 10 research topics',
                      xaxis_title = 'Topics',
                      yaxis_title = 'Total Scores'
                      )
    return fig  


@app.callback(Output(component_id='cytoscape', component_property= 'elements'),
              [Input(component_id='dropdown2', component_property= 'value')])
def graph_update(dropdown_value2):
    print(dropdown_value2)
    df = Neo4j.query_collaborations(dropdown_value2)
    name_set = set(df[['name1', 'name2']].values.flatten())

    nodes = [{"data":{"id":name,"label":name}} for index,name in enumerate(name_set)]
    edges = [{"data":{"source":row["name1"],"target":row["name2"]}} for index, row in df.iterrows()]
    # layout = {"name": "grid"}
    # print(nodes+edges)
    return nodes+edges 

@app.callback(Output(component_id='time_plot', component_property= 'figure'),
              [Input(component_id='dropdown3', component_property= 'value')])
def graph_update(dropdown3):
    print(dropdown3)
    df = Mongo.query_topic_trend(dropdown3)
    fig = go.Figure(
        data=[go.Bar(x=df['year'], y=df['count'])],
        layout_title_text="Sample Bar Chart"
    )
    
    fig.update_layout(title = 'Trend Plot',
                      xaxis_title = 'Total number of publications',
                      yaxis_title = 'Year'
                      )
    return fig  

@app.callback(
    Output('output-query-1', 'children'),
    [Input('button-query-1', 'n_clicks')],
    [State('input-keyword-1', 'value')])
def graph_update(n_clicks, value):
    print(value)
    return Sql.query_university(value) 

@app.callback(
    Output('output-query-2', 'children'),
    [Input('button-query-2', 'n_clicks')],
    [State('input-keyword-2', 'value')])
def graph_update(n_clicks,value):
    print(value)
    return Sql.query_faculty(value)

@app.callback(
    Output('output-query-3', 'children'),
    [Input('button-query-3', 'n_clicks')],
    [State('input-keyword-3-1', 'value'),
     State('input-keyword-3-2', 'value')])
def graph_update(n_clicks, value1, value2):
    print(value1,value2)
    return Sql.query_faculty_keyword(value1,value2)

@app.callback(
    Output('output-update', 'children'),
    [Input('button-update', 'n_clicks')],
    [State('input1', 'value'),State('input2', 'value'), State('input3', 'value'), State('input4', 'value')]
)
def update_record(n_clicks, name, email=None, phone=None,url=None):
    return Sql.update_faculty(name,email,phone,url)

@app.callback(
    Output('output-update0', 'children'),
    [Input('button-update0', 'n_clicks')],
    [State('input10', 'value'),State('input20', 'value')]
)
def update_record(n_clicks, name, url=None):
    return Sql.update_university(name,url)

if __name__ == '__main__':
    sql_host = input("Please enter sql host: ")
    sql_usr = input("Please enter sql user name: ")
    sql_pswd  = input("Please enter sql password: ")

    neo_uri = input("Please enter Neo4j uri: ")
    neo_usr  = input("Please enter Neo4j user name: ")
    neo_pswd = input("Please enter Neo4j password: ")

    mongo_uri = input("Please enter MongoDB uri: ")

    Sql = SqlQuery(sql_host,sql_usr,sql_pswd,"academicworld")
    Neo4j = Neo4jQuery(neo_uri,'academicworld',(neo_usr,neo_pswd))
    Mongo = MongoQuery(mongo_uri,"academicworld","publications")
    app.run_server()

