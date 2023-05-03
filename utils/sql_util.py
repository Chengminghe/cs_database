import pandas as pd
from mysql import connector
import numpy as np
from dash import html
from dash import dcc
import plotly.graph_objects as go

styles = {
    'table': {
        'borderCollapse': 'collapse',
        'borderSpacing': '0',
        'width': '100%',
        'border': '1px solid #ddd',
        'fontFamily': 'Arial, sans-serif',
        'fontSize': '12px'
    },
    'th': {
        'textAlign': 'left',
        'padding': '8px',
        'backgroundColor': '#f2f2f2',
        'fontWeight': 'bold',
        'border': '1px solid #ddd',
    },
    'td': {
        'textAlign': 'left',
        'padding': '8px',
        'border': '1px solid #ddd',
    },
    'tr:hover': {
        'backgroundColor': '#f5f5f5'
    }
}




class SqlQuery():
    def __init__(self,host,user,password,database,port=3306,connection_timeout=60):
        self.host=host
        self.user=user
        self.password=password
        self.database=database
        self.port=port
        self.connection_timeout=connection_timeout

    def query_university(self,value):
        query = \
            f"SELECT university.name AS UniversityName, COUNT(faculty.name) AS NumberOFProfessor \
            FROM university, faculty WHERE university.id = faculty.university_id \
            AND university.id IN \
            (SELECT faculty.university_id FROM faculty WHERE faculty.id IN \
            (SELECT faculty_keyword.faculty_id FROM faculty_keyword WHERE faculty_keyword.keyword_id IN \
            (SELECT keyword.id FROM keyword WHERE keyword.name = '{value}'))) \
            GROUP BY university.id \
            ORDER BY COUNT(faculty.name) DESC \
            LIMIT 10;"
        cnx = connector.connect(host=self.host,user=self.user,password=self.password,
                                database=self.database,port=self.port,connection_timeout=self.connection_timeout)

        cursor = cnx.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=[column[0] for column in cursor.description])
        cursor.close()
        cnx.close()
        table_contents = [    html.Tr([        html.Th(col, style=styles['th']) for col in df.columns
            ])
        ] + [    html.Tr([        html.Td(df.iloc[i][col], style=styles['td']) for col in df.columns
            ]) for i in range(len(df))
        ]

        table = html.Table(table_contents, style=styles['table'])

        return table


    def query_faculty(self,value):
        query = \
            f"SELECT faculty.name, SUM(publication.num_citations * publication_keyword.score) \
            AS KRC FROM faculty_publication, publication, publication_keyword, faculty \
            WHERE publication.id IN (SELECT publication_id FROM publication_keyword \
            WHERE keyword_id = (SELECT id FROM keyword WHERE name = '{value}')) \
            AND publication_keyword.keyword_id = (SELECT id FROM keyword WHERE name = '{value}') \
            AND publication_keyword.publication_id = publication.id \
            AND publication.id = faculty_publication.publication_id \
            AND faculty_publication.faculty_id = faculty.id \
            GROUP BY faculty.id ORDER BY KRC DESC LIMIT 10"
        cnx = connector.connect(host=self.host,user=self.user,password=self.password,
                                database=self.database,port=self.port,connection_timeout=self.connection_timeout)

        cursor = cnx.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=[column[0] for column in cursor.description])
        cursor.close()
        cnx.close()
        # return df


        table_contents = [    html.Tr([        html.Th(col, style=styles['th']) for col in df.columns
            ])
        ] + [    html.Tr([        html.Td(df.iloc[i][col], style=styles['td']) for col in df.columns
            ]) for i in range(len(df))
        ]

        table = html.Table(table_contents, style=styles['table'])

        return table
        

    def query_faculty_keyword(self, value1, value2):
    
        years = [year for year in range(2000, 2021)]

        query_change_year = [
                f"SELECT COUNT(faculty_publication.publication_id) AS NumberOfPublication\
                FROM faculty_publication, faculty\
                WHERE faculty_publication.publication_id IN \
                (SELECT id FROM publication WHERE year = '{year}')\
                AND faculty_publication.publication_id IN \
                (SELECT publication_keyword.publication_id FROM publication_keyword \
                WHERE publication_keyword.keyword_id IN \
                (SELECT keyword.id FROM keyword WHERE keyword.name LIKE '%{value1}%'))\
                AND faculty_publication.faculty_id = (SELECT faculty.id WHERE faculty.name = '{value2}')\
                GROUP BY faculty.name" for year in years]
            # Execute the query and store the results in a Pandas DataFrame
        cnx = connector.connect(host=self.host,user=self.user,password=self.password,
                                database=self.database,port=self.port,connection_timeout=self.connection_timeout)

        cursor = cnx.cursor()
        dfs=[]
        for q in query_change_year:
            cursor.execute(q)
            results = cursor.fetchall()
            df = pd.DataFrame(results, columns=[column[0] for column in cursor.description])
            dfs.append(df)
        cursor.close()
        cnx.close()

        
        return html.Div([
                html.Div(),
                dcc.Graph(figure = go.Figure(data = 
                                go.Scatter(x= years, 
                                           y= np.array([df['NumberOfPublication'][0] if len(df['NumberOfPublication'])!=0
                                            else 0 for df in dfs ]).flatten())))
                ])

    def update_faculty(self, name, email=None, phone=None,url=None):

        cnx = connector.connect(host=self.host,user=self.user,password=self.password,
                                database=self.database,port=self.port,
                                connection_timeout=self.connection_timeout,autocommit=True)

        cursor = cnx.cursor()
        cursor.execute("SELECT name FROM faculty WHERE name = '{}'".format(name))
        result = cursor.fetchall()
        if result:       
            update_query = "UPDATE faculty SET {}='{}' WHERE NAME='{}'"
            code = [False]*3
            if email is not None:
                cursor.execute(update_query.format('email',email,name))
                code[0]=(cursor.rowcount != 0)
            if phone is not None:
                cursor.execute(update_query.format('phone',phone, name))
                code[1]=(cursor.rowcount != 0)
            if url is not None:
                cursor.execute(update_query.format('url', url, name))
                code[2]=(cursor.rowcount != 0)
            cursor.close()
            cnx.close()
            message = "Email updated: {}\t Phone updated: {}\t URL updated: {}".format(*code)
            return html.Div(message)
        else:
            cursor.close()
            cnx.close()
            message = "{} does not exist!".format(name)
            return html.Div(message)           

    def update_university(self, name,url=None):

        cnx = connector.connect(host=self.host,user=self.user,password=self.password,
                                database=self.database,port=self.port,
                                connection_timeout=self.connection_timeout,autocommit=True)

        cursor = cnx.cursor()
        cursor.execute("SELECT name FROM university WHERE name = '{}'".format(name))
        result = cursor.fetchall()
        if result:       
            update_query = "UPDATE university SET photo_url='{}' WHERE NAME='{}'"
            if url is not None:
                cursor.execute(update_query.format(url, name))
                code = (cursor.rowcount != 0)
            cursor.close()
            cnx.close()
            message = "Photo URL updated: {}".format(code)
            return html.Div(message)
        else:
            cursor.close()
            cnx.close()
            message = "{} does not exist!".format(name)
            return html.Div(message) 










