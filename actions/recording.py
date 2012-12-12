#from Reaper.reaper_python import * # for autocomplete only
from reaper_python import *
from fifteencc.reaper import transport, tracks
from fifteencc.reaper.tracks import ReaperTrack
from fifteencc.reaper.modals import warn


def record_next_track():
    # Enforce 1 track selected
    if tracks.selected_count() != 1:
        warn("A track (and only 1) must be selected first!")
    else:
        
        # Clear solo/record
        transport.stop()
        transport.rewind()
        tracks.unsolo_all()
        tracks.record_unarm_all()
        
        # Select next track that isn't a folder and arm for recording
        tr = ReaperTrack.track_for_currently_selected()
        tr = tr.next_track(allow_folder=False)
        
        
        if not tr:
            warn("No more tracks!")
        else:
            tr.solo_in_place().record_arm().select_only()
            transport.record()
    
