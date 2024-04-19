from datetime import datetime
from pythonosc import dispatcher
from pythonosc import osc_server

from tinydb import TinyDB, Query
db = TinyDB('db.json')

ip = "192.168.1.223"
port = 5000

def getData():
    allvalues = db.all()
    print(allvalues[0])
    return allvalues[0]

def handleData(electrodeOne, electrodeTwo):
    db.truncate()
    db.insert({
        'elec1': electrodeOne, 
        'elec2': electrodeTwo})

    getData()

def eeg_handler(address: str,*args):
    global electrodeOne
    electrodeOne = args[0]
    electrodeTwo = args[1]
    electrodeThree = args[2]
    electrodeFour = args[3]
    
    dummyArray = [
        electrodeOne, electrodeTwo, electrodeThree, electrodeFour
    ]

    print(dummyArray)
    handleData(electrodeOne, electrodeTwo)
    
if __name__ == "__main__":
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/muse/eeg", eeg_handler)

    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    print("Listening on UDP port "+str(port))
    server.serve_forever()

