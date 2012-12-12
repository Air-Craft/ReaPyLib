#from Reaper.reaper_python import * # for autocomplete only
from reaper_python import *


class ReaperItem(object):
    def __init__(self, rpr_media_item):
        self._rpr_media_item = rpr_media_item;    
        
    @property
    def position(self):
        return RPR_GetMediaItemInfo_Value(self._rpr_media_item, "D_POSITION")
    
    @property
    def length(self):
        return RPR_GetMediaItemInfo_Value(self._rpr_media_item, "D_LENGTH")
    
    @property
    def start_time(self):
        '''Alias for position'''
        return self.position 

    @property
    def end_time(self):
        return self.position + self.length 
    
    
        