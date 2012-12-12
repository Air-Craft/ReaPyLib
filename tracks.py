#from Reaper.reaper_python import * # for autocomplete only
from reaper_python import *
from items import ReaperItem
from modals import *

def track_count(proj_idx = 0):
    return RPR_CountTracks(proj_idx)

def unsolo_all():
    RPR_Main_OnCommand(40340, 0)
    
def solo_selected():
    RPR_Main_OnCommand(11, 0)
    
def record_unarm_all():
    RPR_Main_OnCommand(40491, 0)
    
def record_arm_selected():
    '''(SWS) Record arm selected tracks
    '''
    RPR_Main_OnCommand(RPR_NamedCommandLookup("_XENAKIOS_SELTRAX_RECARMED"), 0)


####################################
# TRACK SELECTION
####################################

def selected_count(proj_idx = 0):
    return RPR_CountSelectedTracks(proj_idx)

def save_selection_state():
    RPR_Main_OnCommand(RPR_NamedCommandLookup("_SWS_SAVESEL"), 0)
    
def restore_selection_state():
    RPR_Main_OnCommand(RPR_NamedCommandLookup("_SWS_RESTORESEL"), 0)

def toggle_saved_selection_state():
    RPR_Main_OnCommand(RPR_NamedCommandLookup("_SWS_TOGSAVESEL"), 0)

def select_next():
    '''(SWS) Select next track(s) unselecting current
    Returns:    MediaTrack *
    '''
    RPR_Main_OnCommand(RPR_NamedCommandLookup("_XENAKIOS_SELNEXTTRACK"), 0)
    return RPR_GetSelectedTrack(0, 0);  # first 0 is current project
    
def select_next_appending():
    '''(SWS) Select next track(s) keeping the current one(s) selected
    '''
    RPR_Main_OnCommand(RPR_NamedCommandLookup("_XENAKIOS_SELNEXTTRACKKEEP"), 0)

def select_parent():
    '''(SWS) Select parent(s) of selected track(s).  Unselects the original track
    '''
    RPR_Main_OnCommand(RPR_NamedCommandLookup("_SWS_SELPARENTS"), 0)

def select_parent_appending():
    '''(SWS) Select parent(s) of selected track(s) while keep this current track selection
    '''
    RPR_Main_OnCommand(RPR_NamedCommandLookup("_SWS_SELPARENTS2"), 0)


##############################################################################

class ReaperTrack:
    def __init__(self, rpr_track, project_idx=0):
        self._rpr_track = rpr_track;
        self._rpr_project = project_idx
    
    
    #######################################
    # CLASS METHODS
    #######################################
    
    @classmethod
    def track_for_currently_selected(cls, project_idx=0, selected_idx=0):
        '''
        @return: None if none selected else object with selected track
        ''' 
        if RPR_CountSelectedTracks(project_idx) == 0:
            return None
        return cls(RPR_GetSelectedTrack(project_idx, selected_idx))
    
    @classmethod
    def tracks_for_currently_selected(cls, project_idx=0):
        '''
        @return: None if none selected else list of ReaperTrack objects
        '''
        sel_cnt = RPR_CountSelectedTracks(project_idx) 
        if sel_cnt == 0:
            return None
        
        return [ cls(RPR_GetSelectedTrack(project_idx, selected_idx)) for selected_idx in range(sel_cnt) ]
    
    
    #######################################
    # PROPERTIES
    #######################################
    
    @property 
    def is_folder(self):
        (trackname, tr, flags) = RPR_GetTrackState(self._rpr_track, 0)
        return flags & 1
    
    @property
    def name(self):
        (trackname, tr, flags) = RPR_GetTrackState(self._rpr_track, 0)
        return trackname
    
    @property
    def next_track(self, allow_folder=True):
        '''Returns ReaperTrack object for next track by idx
        @todo: Safety checks and alerts (> 1 tracks?)
        @todo: Visible tracks only
        @return: ReaperTrack object of next or none if last track 
        ''' 
        
        # Loop through until we find a match
        track_cnt = track_count()
        tr = RPR_GetTrack(self._rpr_project, 0)
        i = 1
        while i < track_cnt and tr != self._rpr_track:
            tr = RPR_GetTrack(self._rpr_project, i)
            i+=1
        
        # Return None if end encountered
        if i == track_cnt:
            return None
        
        # Now loop through until we find a non-folder if specified
        tr = RPR_GetTrack(self._rpr_project, i)
        trObj = self.__class__(tr)
        
        # if allow_folder = True then this will exit straight away    
        while i < track_cnt and (not allow_folder and trObj.is_folder()):
            tr = RPR_GetTrack(self._rpr_project, i)
            trObj = self.__class__(tr)
            i+=1
        
        if i == RPR_CountTracks(self._rpr_project):
            return None
        
        return trObj
    
    @property
    def parent_track(self):
        '''
        Returns the ReaperTrack object for the next outermost parent folder or None if none.
        Warning! This utilises the SWS "save/restore selection".
        '''
        save_selection_state()
        self.select_only()
        select_parent()
        p_tr = ReaperTrack.track_for_currently_selected(self._rpr_project)
        restore_selection_state()
        return p_tr
    
    
    @property
    def parent_tracks(self):
        '''
        Returns a list of all parents in order from top down
        Warning! This utilises the SWS "save/restore selection".
        '''
        save_selection_state()
        self.select_only()
        p_tracks = []
        i=0
        while i < 10:
            i+=1
            select_parent()
            tr = ReaperTrack.track_for_currently_selected(self._rpr_project)
            if tr == None:
                break
            p_tracks.append(tr)
        
        restore_selection_state()
        p_tracks.reverse()
        return p_tracks
    
    @property
    def items(self):
        '''
        @return: List of ReaperItem's or empty list if none
        '''
        cnt = RPR_CountTrackMediaItems(self._rpr_track)
        items = []
        for idx in range(cnt):
            items.append(ReaperItem(RPR_GetTrackMediaItem(self._rpr_track, idx)))
        return items
    
    #######################################
    # RETURNS SELF
    #######################################
    
    def select_appending(self):
        RPR_SetTrackSelected(self._rpr_track, 1)
        return self
        
    def unselect(self):
        RPR_SetTrackSelected(self._rpr_track, 0)
        return self
        
    def select_only(self):
        RPR_SetOnlyTrackSelected(self._rpr_track)
        return self
    
    
    def solo(self, state=1):
        '''
        @param state: 0=unsolo, 1=solo, 2=solo in place (ie through track, not through master)
        '''
        RPR_SetMediaTrackInfo_Value(self._rpr_track, 'I_SOLO', state)
        return self
    
    def unsolo(self):
        self.solo(state=0)
        return self
        
    def solo_in_place(self):
        '''Solo through the immediate track or parent only.  Not through master
        '''
        self.solo(state=2)
        return self
    
    def solo_exclusive(self):
        '''Unsolo all, solo this track
        ''' 
        unsolo_all()
        self.solo()
    
    def mute(self, state=True):
        RPR_SetMediaTrackInfo_Value(self._rpr_track, 'B_MUTE', state)
        return self
    
    def unmute(self):
        self.mute(state=False)
        return self
    
    def record_arm(self, state=1):
        RPR_SetMediaTrackInfo_Value(self._rpr_track, 'I_RECARM', state)
        return self
    
    def record_unarm(self):
        self.record_arm(state=0) 
        return self
    
    #######################################
    # PRIVATE
    #######################################
        