#from Reaper.reaper_python import * # for autocomplete only
from reaper_python import *


def render_to_disk(prompt=True):
    if prompt:
        RPR_Main_OnCommand(40015, 0)
    else:
        RPR_Main_OnCommand(41824, 0)
    
    
