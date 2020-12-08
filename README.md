# CovidCare
CovidCare is an attempt to helping to contain the disease (Covid-19) by finding out the Covid-19 status of people you have met along your days and the location of this meeting

![Logo](https://github.com/DiaaZiada/CovidCare-AndroidApp/blob/master/images/Screenshot%20from%202020-12-08%2015-04-29.png)

CovidCare System is consists of to part
* REST API Server9
* Mobile Application

# REST API Server 
this is the RESST API Server repo. You can find the Mobile App repo from [here](https://github.com/DiaaZiada/CovidCare-AndroidApp)

## Technologies
* Python Flask (REST API)

![flask](https://github.com/DiaaZiada/CovidCare-Server/blob/master/images/1_0G5zu7CnXdMT9pGbYUTQLQ.png)

* Neo4j Data Base (Graphical DataBase)

![neo4j](https://github.com/DiaaZiada/CovidCare-Server/blob/master/images/0_d2b2ohG7o_hnbYVx.png)

## How the App works
### LocationTime

The mobile app send an uuid (to identify it) and it's current location (latitude, logitude) and time whenever it's location changes
### Graphical DataBase
the server creates new node to the graphical database if it's first time to append the locationTime node to it

![node](https://github.com/DiaaZiada/CovidCare-Server/blob/master/images/IMG_20201208_160537.jpg)

![intersection](https://github.com/DiaaZiada/CovidCare-Server/blob/master/images/IMG_20201208_160520.jpg)


