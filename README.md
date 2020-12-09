
# CovidCare
CovidCare is an attempt to help contain the disease (Covid-19) by finding out the Covid-19 status of people you have come to contact within your day and the location of these contacts.

![Logo](https://github.com/DiaaZiada/CovidCare-AndroidApp/blob/master/images/Screenshot%20from%202020-12-08%2015-04-29.png)

CovidCare system consists of
* REST API Server9
* Mobile Application

# REST API Server 
This repo is about the server, you can find the mobile app repo at [here](https://github.com/DiaaZiada/CovidCare-AndroidApp)

## Technologies
* Python flask

![flask](https://github.com/DiaaZiada/CovidCare-Server/blob/master/images/1_0G5zu7CnXdMT9pGbYUTQLQ.png)

* Neo4j DataBase (Graphical DataBase)

![neo4j](https://github.com/DiaaZiada/CovidCare-Server/blob/master/images/0_d2b2ohG7o_hnbYVx.png)
## Run
`$python run.py`
## How the app works

### Location and time

The mobile app sends a UUID (to identify it) and the current location (latitude, longitude) and time whenever it's location changes.

After that the 

### Graphical DataBase
#### Storing the location and time
The server creates a new node to the graphical database if it's the first time to append the location and time node to it, the purple part is the UUID of the device and the yellow parts are all the locations and times stored for that UUID
![node](https://github.com/DiaaZiada/CovidCare-Server/blob/master/images/IMG_20201208_160537.jpg)

#### Getting the location and time
When the user requests information about the people he came to contact with the server applies BFS for the 2nd level from the user UUID node (The purple node). The result is the UUIDs of the people who have the same location and time.

![intersection](https://github.com/DiaaZiada/CovidCare-Server/blob/master/images/IMG_20201208_160520.jpg)
