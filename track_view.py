#from Reaper.reaper_python import * # for autocomplete only
from reaper_python import *


def select_time_range(start_time, end_time):
    RPR_GetSet_LoopTimeRange(True,          # isSet 
                             False,         # isLoop
                             start_time,
                             end_time,
                             False)         # allowautoseek
    
