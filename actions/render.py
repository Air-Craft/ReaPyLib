#from Reaper.reaper_python import * # for autocomplete only
import os
from reaper_python import *
from fifteencc import reaper
from fifteencc.reaper.modals import *
from fifteencc.reaper.tracks import ReaperTrack
from fifteencc.reaper.items import ReaperItem

def export_selected_tracks_through_master(export_folder_path='./Renders'):
    '''
    Renders the selected tracks through the main rendering engine naming 
    their files with the hyphenated combo of their parent tracks' names plus its name.  
    
    Useful for sample exports.  Requires setting specific Render settings on the first export which
    the macro will then use to copy out and rename the file. 
    
    @param export_folder_path: Defaults to "./Renders". Appends to project (audio) path if relative 
    '''
    EXPORT_FILE_NAME_PLACEHOLDER = "REAPER_EXPORT_TMP"
    
    
    sel_tracks = ReaperTrack.tracks_for_currently_selected()
    
    # Sanitise path, prepend project folder if not absolute
    if not os.path.isabs(export_folder_path):
        (proj_path, i) = RPR_GetProjectPath("", 1024)
        export_folder_path = os.path.abspath(os.path.join(proj_path, export_folder_path))
    
    # Don't care if it exists.  Render will create it
    
    # Loop through selected tracks
    is_first = True
    export_cnt = 0 
    for track in sel_tracks:
        
        # No items? Continue...
        if not len(track.items):
            continue
        
        # Solo this track and select time range for the track's items
        track.solo_exclusive()
        reaper.track_view.select_time_range(track.items[0].start_time, track.items[-1].end_time)
     
        # Prompt for render settings for the first export.  Then do it silently for the rest 
        if is_first:
            warn("You'll be prompted for render settings for the first item." 
                 "For this to work you MUST make these settings:\n\n"
                 "Render: Master Mix\n"
                 "Render Bounds: Time Selection\n"
                 "Directory: {}\n"
                 "File name: {}\n"
                    .format(export_folder_path, 
                            EXPORT_FILE_NAME_PLACEHOLDER))
            reaper.render.render_to_disk(prompt=True)
            is_first = False
            if not warn_ok_cancel("WAIT! Click OK when once first export is done or Cancel to abort (Reaper wait hack)..."):
                return
        else:
            reaper.render.render_to_disk(prompt=False)
        
        # Find the full exported filepath. We only know its basename... 
        src_filepath = None
        (dirpath, dirnames, filenames) = os.walk(export_folder_path).next()
        for f in filenames:
            if -1 != f.find(EXPORT_FILE_NAME_PLACEHOLDER):
                src_filepath = os.path.join(export_folder_path, f)
                break
            
        # Allow abort if not found error...
        if not src_filepath:
            if not warn_yes_no("Could not find exported file {}.*.  Continue?".format(os.path.join(export_folder_path, EXPORT_FILE_NAME_PLACEHOLDER))):
                return
                
        # Otherwise rename it to the name derived from the track name and parent folders  
        dum, ext = os.path.splitext(src_filepath)
        names = [tr.name for tr in track.parent_tracks]
        names.append(track.name)
        dest_basename = "-".join(names) 
        dest_filepath = os.path.join(export_folder_path, dest_basename + ext)
        
        # Rename, overwriting
        if os.path.exists(dest_filepath):
            os.remove(dest_filepath)
        os.rename(src_filepath, dest_filepath)
        
        export_cnt += 1
        
    notice("Exported {} files to {}".format(export_cnt, export_folder_path), "Success!")
                
'''
def render_child_track_items_with_selected_folders_fx_chains():
    Renders the child items with a parent folders FX chain and removes the chain from 
    
    # Confirm >= 1 tracks selected
    if tracks.selected_count() < 1:
        warn("No tracks selected.")

    # 
    source_tracks = ReaperTrack.tracks_for_currently_selected()
    
    for parent_track in source_tracks:
        # If not parent or has no FX then warn
        if not parent_track.is_folder():
            warn("ReaperTrack '{}' is not a folder track (click OK to continue)".format(parent_track.name))
            continue
        
        if parent_track.fx_count < 1:
            warn("ReaperTrack '{}' has no FX (click OK to continue)".format(parent_track.name))
            continue
        
        # Get effects chain cut
        parent_track.select_only()
        tracks.cut_fx_chain_from_selected()
        
        
        
        
    # Restore selection state
    for tr in source_tracks:
        tr.select()
'''
    