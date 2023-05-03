from neo4j import GraphDatabase
import neo4j
import pandas as pd

class Neo4jQuery():
    def __init__(self,uri,database,auth):
        self.uri=uri
        self.database=database
        self.auth=auth
        self.driver = GraphDatabase.driver(uri, auth=auth)
    def query_research_topics(self,input):
        query = """MATCH (i:INSTITUTE {{name: "{}"}})<-[:AFFILIATION_WITH]-(f:FACULTY)-[interested_in:INTERESTED_IN]->(k:KEYWORD)
                WITH k, sum(interested_in.score) AS total_score
                ORDER BY total_score DESC
                RETURN k.name as name, total_score
                LIMIT 10""".format(input)
        with self.driver.session(database=self.database) as session:
            result = session.run(query)
            df = pd.DataFrame([r.values() for r in result], columns=result.keys())
        return df
    def query_collaborations(self,input):
        query =  """MATCH (p:PUBLICATION)<-[:PUBLISH]-(f:FACULTY)-[:AFFILIATION_WITH]->(i:INSTITUTE {{name: '{}'}})
                    WITH f,p
                    MATCH (f)-[:AFFILIATION_WITH]->(i)<-[:AFFILIATION_WITH]-(f2:FACULTY)-[:PUBLISH]->(p2:PUBLICATION)-[:LABEL_BY]->(k:KEYWORD)
                    WHERE f.name < f2.name AND p.id=p2.id
                    WITH f, f2, k.name AS keyword, count(*) AS collab_count
                    ORDER BY collab_count DESC
                    WITH f.name AS name1, f2.name AS name2, collect(keyword) AS top_keywords
                    RETURN name1, name2, top_keywords
                    ORDER BY name1, name2
                    LIMIT 30""".format(input)
        with self.driver.session(database=self.database) as session:
            result = session.run(query)
            df = pd.DataFrame([r.values() for r in result], columns=result.keys())
        return df



