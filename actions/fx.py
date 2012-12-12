#from Reaper.reaper_python import * # for autocomplete only
from reaper_python import *
from fifteencc import reaper
from fifteencc.reaper.modals import warn
from fifteencc.reaper.tracks import ReaperTrack

'''
def export_selected_items_rendered_through_topmost_parent_folder(export_folder_path="./Renders"):
    
    for each in items:
        tr = item track
        tr.solo_only()
        par_tr = tr.parent_tracks[0]    # topmost folder
        par_tr.freeze()
        rendered_item = par_tr.items[0]
        copy rendered_item.source_file export_folder_path
        par_tr.unfreeze()
        rendered_item.delete(delete_source=True) 
        
        item.unselect()
    '''
    

     