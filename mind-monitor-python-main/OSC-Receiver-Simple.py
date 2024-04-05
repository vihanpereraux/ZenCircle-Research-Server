"""
Mind Monitor - Minimal EEG OSC Receiver
Coded: James Clutterbuck (2021)
Requires: pip install python-osc
"""
from datetime import datetime
from pythonosc import dispatcher # type: ignore
from pythonosc import osc_server # type: ignore

ip = "192.168.1.223"
port = 5000

def eeg_handler(address: str,*args):
    dateTimeObj = datetime.now()
    printStr = ''
    for arg in args:
        printStr += ","+str(arg)
    print(printStr)
    
if __name__ == "__main__":
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/muse/elements/alpha_absolute", eeg_handler)

    server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)
    print("Listening on UDP port "+str(port))
    server.serve_forever()



    # 789.7435913085938, 790.952392578125, 826.4102783203125, 795.7875366210938, 807.87548828125

    # 2024-04-05 19:48:51.978960, 746.6300659179688, 794.1758422851562, 799.010986328125, 748.6447143554688, 626.556762695312