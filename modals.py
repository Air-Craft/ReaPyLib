#from Reaper.reaper_python import * # for autocomplete only
from reaper_python import *


def notice(msg, title="Notice"):
    RPR_ShowMessageBox(msg, title, 0)


def warn(msg):
    RPR_ShowMessageBox(msg, "Warning!", 0)
    
    
def warn_ok_cancel(msg):
    ''' Warn and prompt with OK/Cancel buttons
    @return: True if OK, False if Cancel
    '''
    
    res = RPR_ShowMessageBox(msg, "Warning!", 1)
    return (res == 1)


def warn_yes_no(msg):
    ''' Warn and prompt with Yes/No buttons
    @return: True if Yes, False if No
    '''
    
    res = RPR_ShowMessageBox(msg, "Warning!", 4)
    return (res == 6)