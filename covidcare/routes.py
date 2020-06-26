import random
from flask import Flask, request, jsonify, Blueprint
from sqlalchemy import or_, and_

from covidcare.models import AppInfo

routes = Blueprint('routes', __name__)

@routes.route("/", methods=['GET', 'POST'])
def home():
    return jsonify({"msg":"sfasdf"})

@routes.route("/requestid", methods=["POST","GET"])
def request_id():
    app_id = request.json["appId"]
    app = AppInfo(app_id, "Healthy")
    app.register()
    return jsonify({"appId":app.get_id()})
   
@routes.route("/updatestatus", methods=["POST"])
def update_status():
    app_id = request.json["appId"]
    status = request.json["status"]   
    appInfo =  AppInfo(app_id, status)
    appInfo.register()
    appInfo.update_status()
    return jsonify({"appId":appInfo.get_id(), "status":appInfo.get_status()})

@routes.route("/sendlocationtime", methods=["POST"])
def send_location_time():   
    app = request.json[0]
    appInfo = AppInfo(app["appId"])
    appInfo.register()
    for app in request.json:
        time = app["time"]
        latitude = app["latitude"]
        longitude = app["longitude"]
        appInfo.add_location_time(latitude,longitude,time)
    if random.randint(0, 10000) >9999:
        AppInfo.clear_appinfo()
    return jsonify({"appId":appInfo.get_id()})


@routes.route("/getmeetings", methods=["POST"])
def get_meetings():
    app_id = request.json["appId"]
    appInfo = AppInfo(app_id)
    appInfo.register()
    apps = appInfo.get_apps()
    apps.sort(key=lambda dic: dic["hash"].split(',')[-1], reverse=True)
    return jsonify(apps)

@routes.route("/clear", methods=["GET"])
def clear():
    AppInfo.clear_location_time()
    AppInfo.clear_appinfo()
    return "done"

