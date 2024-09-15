import os
from panda3d.core import WindowProperties
import json

from constants.settings import GAME_SETTINGS

def load_config(path):
    
    if not os.path.isfile(path):
        # Volume values default to 1
        # Default to windowed in given dimensions
        setup_windowed() 
        # no config file
        return
    
    with open(path) as config_file:
        config = json.load(config_file)
    
    if "sfx_volume" in config:
       set_sfx_volume(config["sfx_volume"]) 
       
    if "music_volume" in config:
       set_music_volume(config["music_volume"]) 
    
    if "fullscreen" in config:
        if config["fullscreen"]:
            set_fullscreen_value(config["fullscreen"])
        else:
            setup_windowed()
    else:
      setup_windowed() 
      
    if "show_fps" in config:
        base.setFrameRateMeter(config["show_fps"])
        
def setup_windowed():
    wp = WindowProperties(base.win.getProperties()) 
    wp.set_fullscreen(False)
    wp.set_size(GAME_SETTINGS.DEFAULT_WINDOW_WIDTH, GAME_SETTINGS.DEFAULT_WINDOW_HEIGHT)
    wp.set_origin(-2, -2)
    base.win.requestProperties(wp) 
            
def save_config(path):
    config = {"sfx_volume": float(get_sfx_volume()), "music_volume": float(get_music_volume()), "fullscreen": get_fullscreen_value(), "show_fps": True }
    
    with open(path, "w+") as config_file:
        config_file.write(json.dumps(config))

def get_sfx_volume():
    # This assumes that all sfx managers have the same volume
    return base.sfxManagerList[0].getVolume() 
    
def set_sfx_volume(value):
    for manager in base.sfxManagerList:
        manager.setVolume(value)
        
def get_music_volume():
    return base.musicManager.getVolume()
            
def set_music_volume(value):
    base.musicManager.setVolume(value)
    
def get_fullscreen_value():
    wp = WindowProperties(base.win.getProperties())  
    return wp.get_fullscreen()
    
def set_fullscreen_value(fullscreen):
    wp = WindowProperties(base.win.getProperties())  
    is_currently_in_fullscreen = wp.get_fullscreen()
    if fullscreen and not is_currently_in_fullscreen:
        wp.set_fullscreen(True)
        wp.set_size(1920, 1080)
        wp.clearCursorHidden()
        base.win.requestProperties(wp)
    elif not fullscreen and is_currently_in_fullscreen:
       setup_windowed() 
