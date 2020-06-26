from py2neo import Graph, Node, Relationship
from passlib.hash import bcrypt
from datetime import datetime
import os
import uuid

url = os.environ.get('GRAPHENEDB_URL', 'http://localhost:7474')
username = "neo4j"#os.environ.get('NEO4J_USERNAME')
password = ""#os.environ.get('NEO4J_PASSWORD')

graph = Graph(url + '/db/data/', username=username, password=password)

class AppInfo:  
    def __init__(self, id, status="Healthy"):
        self.id = id
        self.status = status

    def get_id(self):
        return self.id 
    def get_status(self):
        return self.status
        
    def find_app(self):
        app = graph.find_one("AppInfo","id", str(self.id))
        return app
    
    def register(self):
        if not self.find_app():
            if self.id == "-1":
                self.id = str(uuid.uuid4())
            app = Node('AppInfo', id=self.id, status=self.status)
            graph.create(app)
            return True
        return False

    def find_location_time(self,hash): 
        return graph.find_one("LocationTime", "hash", hash)

    def add_location_time(self, latitude, longitude, time):

        ymd, hms = time.split(" ")
        ymd = ymd.split("/")
        hms = hms.split(":")
        s = hms[-1]
        if len(s)==1:
            s = "0"
        else:
            s = s[0]
        hms[-1] = s
        datetime = []
        datetime.extend(ymd)
        datetime.extend(hms)
        datetime = "-".join(datetime)
        datetime = datetime

        app = self.find_app()

        n,f = str(latitude).split(".")
        # if len(f) < 5:
        latitude = n+"."+f[:4]
        # else:
        #     latitude = n+"."+f[:4]+ ("0" if int(f[4]) < 5 else "1")
        
        n,f = str(longitude).split(".")
        # if len(f) < 5:
        longitude = n+"."+f[:4]
        # else:
            # longitude = n+"."+f[:4] + ("0" if int(f[4]) < 5 else "1")

        hash = str(latitude)+','+str(longitude)+','+datetime
        location_time = self.find_location_time(hash)
        if not location_time:     
            location_time = Node("LocationTime",hash=hash)
            graph.create(location_time)
        
        rel = Relationship(app, 'WAS_THERE', location_time)
        graph.create(rel)
        rel = Relationship(location_time, 'WAS_HERE', app)
        graph.create(rel)
    
    def update_status(self):
        graph.run(
        "MERGE (n:AppInfo {id: {id}}) SET n.status = {status}",
        {"id": self.get_id(), "status": self.status}
        )
    def get_locationtime(self):
        query = """
        MATCH (app:AppInfo)-[:WAS_THERE]->(locationtime:LocationTime)
        WHERE app.id = {id}
        RETURN locationtime
        """
        locationtime = graph.run(query, id=self.id)
        locationtime = list(locationtime)
        hashs = [hash["locationtime"]["hash"] for hash  in locationtime]        
        return hashs

    def _get_apps(self, hash):
        query = """
        MATCH (locationtime:LocationTime)-[:WAS_HERE]->(app:AppInfo)
        WHERE locationtime.hash = {hash}
        RETURN app
        """
        apps = graph.run(query, hash=hash)
        appsList = []
        # lat, lon, time = hash.split(',')
        for app in apps:
            if app["app"]['id'] in self.ids:
                continue
            appsList.append({"status":app["app"]["status"],"id":app["app"]["id"],"hash":hash})   
            self.ids.append(app["app"]["id"])
        return appsList
    def get_apps(self):
        hashs = self.get_locationtime()
        apps = []
        self.ids = [self.id]
        for hash in hashs:
            apps.extend(self._get_apps(hash))
        return apps
    
    @staticmethod
    def clear_location_time():
        query = """
        MATCH (appinfo:AppInfo)-[rel1:WAS_THERE]->(lt:LocationTime),(lt:LocationTime)-[rel2:WAS_HERE]->(:AppInfo)
        WITH appinfo, rel1, lt, rel2, [item in split(lt.hash,",")] as hashcomponents
        WITH appinfo, rel1, lt, rel2, [item in split(hashcomponents[2], "-") | toInteger(item)] AS dateComponents
        WITH appinfo, rel1, lt, rel2, datetime({year: dateComponents[0], month: dateComponents[1], day: dateComponents[2], hour:dateComponents[3], minute:dateComponents[4]}) as dat
        WHERE duration.inDays(dat, datetime()).days < 10
        DELETE rel1, rel2
        DELETE lt
        """
        graph.run(query)
    
    @staticmethod
    def clear_appinfo():
        query="""
        MATCH (appinfo:AppInfo)
        WHERE size((appinfo)--())=0
        DELETE (appinfo)
        """
        graph.run(query)

"""
MATCH (appifo:AppInfo)-[rel1:WAS_THERE]->(lt:LocationTime),(lt:LocationTime)-[rel2:WAS_HERE]->(:AppInfo)
WHERE lt.hash = {hash}'x,29.5454654,2020/12/16 01:12:16' 
DELETE rel1, rel2
DELETE lt

"""

"""
WITH [item in split("2020-12-16-01-12-16", "-") | toInteger(item)] AS dateComponents
WITH datetime({year: dateComponents[0], month: dateComponents[1], day: dateComponents[2], hour:dateComponents[3], minute:dateComponents[4]}) as date

"""

"""
WITH [item in split(.hash,",")] as hashcomponents
WITH [item in split(hashcomponents[2], "-") | toInteger(item)] AS dateComponents
WITH datetime({year: dateComponents[0], month: dateComponents[1], day: dateComponents[2], hour:dateComponents[3], minute:dateComponents[4]}) as dat
return duration.inDays(dat, datetime()).days
"""

""""
MATCH (appifo:AppInfo)-[rel1:WAS_THERE]->(lt:LocationTime),(lt:LocationTime)-[rel2:WAS_HERE]->(:AppInfo)
WITH [item in split(lt.hash,",")] as hashcomponents
WITH [item in split(hashcomponents[2], "-") | toInteger(item)] AS dateComponents
WITH datetime({year: dateComponents[0], month: dateComponents[1], day: dateComponents[2], hour:dateComponents[3], minute:dateComponents[4]}) as dat
WHERE duration.inDays(dat, datetime()).days > 1
DELETE rel1, rel2
DELETE lt
"""

"""
MATCH (appinfo:AppInfo)-[rel1:WAS_THERE]->(lt:LocationTime),(lt:LocationTime)-[rel2:WAS_HERE]->(:AppInfo)
WITH appinfo, rel1, lt, rel2, [item in split(lt.hash,",")] as hashcomponents
WITH appinfo, rel1, lt, rel2, [item in split(hashcomponents[2], "-") | toInteger(item)] AS dateComponents
WITH appinfo, rel1, lt, rel2, datetime({year: dateComponents[0], month: dateComponents[1], day: dateComponents[2], hour:dateComponents[3], minute:dateComponents[4]}) as dat
WHERE duration.inDays(dat, datetime()).days > 1
DELETE rel1, rel2
DELETE lt
"""

"""
MATCH (appinfo:AppInfo)
WHERE size((appinfo)--())=0
DELETE (appinfo)
"""