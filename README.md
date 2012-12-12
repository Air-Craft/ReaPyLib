Folder Structure
----------------

./*             - Functions wrapper for RPR_\* commands and RPR_Main_OnCommand macros. And Objects such as ReaperTrack
./actions/*     - Macros designed to be called directly from your ReaScript's .py file


Philosophy
----------------
Functions are for wrapping ReaScript commands and macros and maybe simple combinations.  
Anything that acts on, with or returns Reaper\* objects is contained within an object definition.  Eg.  
ReaperTrack.tracks_for_currently_selected(...) is a classmethod rather than a function.


Current Objects
----------------

tracks.ReaperTrack
items.ReaperItem





