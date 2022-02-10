from infi.systray import SysTrayIcon
import threading, mouse, keyboard, time

# Icons Config
defaultPath = "icons/"
trayIconNormal = defaultPath + "cursor.ico"
trayIconPlaying = defaultPath + "cursorPlaying.ico"
trayIconRecording = defaultPath + "cursorRecording.ico"

# General Config
mouse_events = []
keyboard_events = []
recording_started = False

sysTrayIcon = None

# Record the mouse and keyboard
def record():
    global mouse_events
    global keyboard_events
    global recording_started
    
    if (recording_started):
        mouse.unhook(mouse_events.append)
        keyboard_events = keyboard.stop_recording()[4:]
        print(mouse_events)
        print(keyboard_events)
        
        sysTrayIcon.update(icon=trayIconNormal)
        
    else:
        mouse_events = []
        keyboard_events = []
        mouse.hook(mouse_events.append)
        keyboard.start_recording()
        
        sysTrayIcon.update(icon=trayIconRecording)
        
    recording_started = not recording_started

# Playback
def playback():
    global mouse_events
    global keyboard_events
    global recording_started
    global playbackKeyboard
    global playbackMouse
    
    if (recording_started):
        return
    
    
    sysTrayIcon.update(icon=trayIconPlaying)
    
    #Keyboard thread
    k_thread = threading.Thread(target = lambda :keyboard.play(keyboard_events))
    k_thread.start()

    #Mouse thread
    m_thread = threading.Thread(target = lambda :mouse.play(mouse_events))
    m_thread.start()

    #Wait for both threads to complete
    k_thread.join() 
    m_thread.join()
    
    # Because of how the recording is done, the ctrl and alt buttons will still be pressed from the shortcut. Release them
    keyboard.release("ctrl")
    keyboard.release("alt")
    
    sysTrayIcon.update(icon=trayIconNormal)
    
# Add the hotkeys for recording and playing back the keyboard + mouse inputs
keyboard.add_hotkey("ctrl+alt+1", lambda: record())
keyboard.add_hotkey("ctrl+alt+2", lambda: playback())


# Setup the tray icon1
options = (("Start/Stop Recording", None, lambda x: record()), ("Playback Recording", None, lambda x: playback()),)
sysTrayIcon = SysTrayIcon(trayIconNormal, "InputReplay", options, default_menu_index=1)
sysTrayIcon.start()