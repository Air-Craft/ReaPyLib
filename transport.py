from reaper_python import *
#from Reaper.reaper_python import * # for autocomplete only

def rewind():
    RPR_Main_OnCommand(40042, 0)
     
def stop():
    RPR_Main_OnCommand(1016, 0)
         
def record():
    RPR_Main_OnCommand(1013, 0)