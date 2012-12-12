ReaPyLib
===============

An object model, function library, and collaborative macro collection for Reaper's ReaScript. 
Say goodbye to C-based `RPR_*` confusion and hallelujah to Pythonic OO sweetness 


Folder Structure
----------------

./*             - Functions wrapper for `RPR_*` commands and `RPR_Main_OnCommand` macros. Class defs such as ReaperTrack
./actions/*     - Macros designed to be called directly from your ReaScript's .py file


Instructions
------------
1. Place the repo in your Python's path.  
2. Create your own ReaScript file (eg my_macro.py) in a separate directory
3. Import relavant functions from `action.*` and call directory in your .py file
4. Add your .py to Reaper via the actions window

If you make you own custom actions, contribute by forking the repo, adding them to the 
relevant actions/*.py file and issuing a pull request.  Go on, it's easy


Philosophy
----------------
Functions are for wrapping ReaScript commands and macros and simple combinations of them.  
Anything that acts on, with or returns Reaper\* objects is contained within an object definition.  Eg.  
ReaperTrack.tracks_for_currently_selected(...) is a class method rather than a function as it returns


Current Objects
----------------

tracks.ReaperTrack
items.ReaperItem





