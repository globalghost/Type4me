### Type4Me ###
#Author: Simon Whitbread
#Date: 01-02-2022

#NOTES:
'''
Special ascii characters
■
⬤

'''

#UI NOTES:
'''
UI Layout:

---- MAIN APP ----

<main_window>
    <toolbar>
        <File>
            <Configuration>Opens configuration window</Configuration>
            <Exit>Exits application</Exit>
        </File>

        <Help>
            <About>Open about window</About>
        </Help>
    </toolbar>

    <main_canvas>
        <main_input>Text field for users to input what they want to type</main_input>
        <type_button>Button to manually initiate typing after select delay period in the configration window</type_button>
        <previous_input>Selectable list of previous inputs that you can select from</previous_input>
    </main_canvas>
</main_window>

---- Configuation Window ----

<config_window>
    <delay_time>User defined time in seconds that program should wait before typing selected string</delay_time>
    <key_binding>User defined keybinding for the program to listen for to initiate typing</key_binding>
    <save_button>Button to save config to config file</save_button>
    <close_button>Button to close config_window</close_button>
</config_window>

---- About Window ----

<about_window>
    <info_label>Show app info </info_label>
    <support_label>Show suppot info</support_label>
    <donate_button>Open donation web page</donate_button>
    <close_button>Close about_window</close_button>
</About_window>
'''

#CONFIG FILE NOTES
'''
File Format: json
File Name: t4m_config.json
Info to save to file:
- App Version
- Preferred delay time
- Preferred key binding
- Preffered always on top
- Preffered Auto clipboard input
- List of previous inputs hashed

JSON layout:
'{
    'version':'',
    'delay_time':'',
    'key_binding':'',
    'always_ontop':'',
    'auto_clipboard':'',
    'previous_inputs':list[]
}'
'''

#CHANGE LOG:
'''
V0.2a Features
- Add MacOS Support - Done ✅ 29-01-2022
- Added GUI - Done ✅ 02-02-2022
- Added Configuration window - Done ✅ 02-02-2022
- Add save button for config window. - Done ✅ 02-02-2022
- Add main_input enter key listener - Done ✅ 03-02-2022
- Add enter key listener to main_input - Done ✅ 03-02-2022
- Add key bind to trigger "Virtual Keyboard" output. - Done ✅ 05-02-2022
- Stop App from freezing when it is waiting to type - Done ✅ 05-02-2022
- Copy clipboard into main_input when control + c is pressed - Done ✅ 05-02-2022
- previous_input clear button - Done ✅ 05-02-2022
- Add up and down arrows listeners to main_input - Done ✅ 01-03-2022
- Always ontop option in configuration menu - Done ✅ 02-03-2022
- Make About window - Done ✅ 02-03-2022
- Create Donation page for dono button - Done ✅ 02-03-2022
- Add user select key binding for virtual keyboard to config window - Done ✅ 04-03-2022
- Toggle clipboard listener - Done ✅ 04-03-2022
- Add json config file to save settings - Done ✅ 07-03-2022

Future Features:
- Dark mode, pretty self explanitary
- Log file, hashed entries and log file purge button in config window
- VMWare mode, specialised for entering into Virtual machines opened in browser window.
- Character delay, user defined time delay between each character
- Visible delay countdown, show countdown in seconds so user can see if it is activated
- Redesign UI, redesign all UI using grid method
- Install and uninstall?
- Windows App Certification?
- Refactor Entire project
- Error handling
'''

#TO DO
'''
#### BUG FIXES ####
- Index selection in listbox needs to be limited to range of listbox. - Done ✅ 07-03-2022
- Icon is not part of exe after build - Done ✅ 12-03-2022
- Cant save config if about window isnt open - Done ✅ 12-03-2022

#### QOL FIXES ####
- Clean up toolbar on windows version, showing lines as first item - Done ✅ 07-03-2022
- Always ontop toggle doesnt refresh all active windows - Done ✅ 07-03-2022
- Up and down key doesnt scroll previous input list - Done ✅ 07-03-2022
- Make previous enties smarter by looking to see if main_input is already in list box. - Done ✅ 07-03-2022
- App icon - Done ✅ 07-03-2022
- App meta information - Done ✅ 10-03-2022

#### FEATURES ####
- Wide mode - Done ✅ 12-03-2022
'''

import tkinter, tkinter.ttk, webbrowser, json, base64, os.path
from pynput import keyboard as pk
from PIL import ImageTk, Image

tk = tkinter
ttk = tkinter.ttk
appName = 'Type4Me'
appVersion = 'Alpha 0.2'
list_selection = -1
delay_time = 2
user_defined_keybind = ''
default_keybind = '<ctrl>+q'
bind_counter = 0
combo = ''
end = False
about_open = False
config_open = False
k = pk.Controller()

icon_file = "icon.ico" 
if not hasattr(os.sys, "frozen"):
    icon_file = os.path.join(os.path.dirname(__file__), icon_file) 
else:  
    icon_file = os.path.join(os.sys.prefix, icon_file)
    
wide_file = "wide.jpg" 
if not hasattr(os.sys, "frozen"):
    wide_file = os.path.join(os.path.dirname(__file__), wide_file) 
else:  
    wide_file = os.path.join(os.sys.prefix, wide_file)

def encrpyt():
    data = []
    for i in range(0, previous_input.size()):
        input = str(previous_input.get(i))
        revD = input[::-1]
        input = list(input)
        revD = list(revD)
        count = 0
        key = ''

        while count < len(input):
            key = key + input[count] + revD[count]
            count = count + 1

        key = key[:int((len(key)/2))]
        key.join('')
        key = key.encode('ascii')
        key = base64.b64encode(key)
        key = base64.b64encode(key)
        data.append(key.decode('ascii'))
    
    return data
    
def decrpyt(key):
    key = base64.b64decode(key)
    key = base64.b64decode(key)
    key = key.decode('ascii')
    revK = key [::-1]
    key = key + revK
    key = list(key)
    data = ''
    count = 0
    
    while count < len(key):
        data = data + key[count]
        count = count + 2
    
    return data

def readConfigFile():
    global delay_time, user_defined_keybind, clip_toggle_value,  previous_input
    config_file = (os.path.dirname(os.path.abspath(__file__))) + '\\t4m_config.json'
    if os.path.isfile(config_file) == False:
        all_settings = {
            'version': appName + ' - ' + appVersion,
            'delay_time': delay_time,
            'key_binding': trigger(),
            'always_ontop': onTop_value.get(),
            'auto_clipboard':clip_toggle_value.get(),
            'previous_inputs':''
        }
        with open('t4m_config.json', 'w') as outfile:
            json.dump(all_settings, outfile)

    with open('t4m_config.json') as read_file:
        json_data = json.load(read_file)
    delay_time = json_data['delay_time']
    user_defined_keybind = json_data['key_binding']
    clip_toggle_value.set(json_data['auto_clipboard'])
    onTop_value.set(json_data['always_ontop'])
    for data in json_data['previous_inputs']:
        previous_input.insert(json_data['previous_inputs'].index(data), decrpyt(data))

def writeToConfigFile():
    all_settings = {
        'version': appName + ' - ' + appVersion,
        'delay_time': delay_time,
        'key_binding': trigger(),
        'always_ontop': onTop_value.get(),
        'auto_clipboard':clip_toggle_value.get()
    }
    all_settings['previous_inputs'] = encrpyt()
    with open('t4m_config.json', 'w') as outfile:
        json.dump(all_settings, outfile)
    
def typeIt():
    global k, list_selection
    my_string = main_input.get()
    tmp = []
    for i in range(0, previous_input.size()):
        tmp.append(str(previous_input.get(i)))
    if my_string not in tmp:
        previous_input.insert(0, my_string)
    previous_input.select_clear(0, tk.END)
    list_selection = 0
    previous_input.see(list_selection)
    previous_input.selection_set(list_selection)
    k.type(str(my_string))
    k.tap(pk.Key.enter)
    writeToConfigFile()

def delayIt():
    main_window.after((delay_time * 1000), typeIt)

def changeMainInput(event):
    global list_selection
    list_selection = previous_input.curselection()[0]
    data = previous_input.get(list_selection)
    main_input.delete(0, tk.END)
    main_input.insert(0, data)

def upOrDown(direction):
    global list_selection
    previous_input.select_clear(0, tk.END)
    if (direction == 'up' or direction == 'down') and list_selection == -1:
        list_selection = 0
    elif direction == 'up' and list_selection > 0:
        list_selection = list_selection - 1
    elif direction == 'down' and list_selection < (previous_input.size() - 1):
        list_selection = list_selection + 1
    elif direction == 'up' and list_selection == 0:
        list_selection = 0
    else:
        list_selection = previous_input.size() - 1
    previous_input.see(list_selection)
    previous_input.selection_set(list_selection)
    data = previous_input.get(list_selection)
    main_input.delete(0, tk.END)
    main_input.insert(0, data)

def mainInputKeyPress(event):
    if event.keysym == 'Return':
        delayIt()
    elif event.keysym == 'Up':
        upOrDown('up')
    elif event.keysym == 'Down':
        upOrDown('down')

def stayOnTop():
    global onTop_value
    if onTop_value.get() == 1:
        condition = True
    else:
        condition = False
    return condition

def trigger():
    global default_keybind, user_defined_keybind
    if user_defined_keybind == '':
        binding = default_keybind
    else:
        binding = user_defined_keybind
    return binding

def getClipboard():
    clip = main_window.clipboard_get()
    main_input.delete(0, tk.END)
    main_input.insert(0, clip)

def onBindingPress():
    global k
    a = trigger()
    ctl = False
    alt = False
    shift = False
    startKeyListener.hotkey.stop()
    if a.find('ctrl') >= 1:
        k.release(pk.Key.ctrl)
        ctl = True
    
    if a.find('alt') >= 1:
        k.release(pk.Key.alt)
        alt = True
    
    if a.find('shift')>= 1:
        k.release(pk.Key.shift)
        shift = True
    
    typeIt()
    
    startKeyListener()
    
    if ctl == True:
        k.tap(pk.Key.ctrl)
        k.press(pk.Key.ctrl)
    
    if alt == True:
        k.tap(pk.Key.alt)
        k.press(pk.Key.alt)
    
    if shift == True:
        k.tap(pk.Key.shift)
        k.press(pk.Key.shift)

def onClipPress():
    global clip_toggle_value
    if clip_toggle_value.get() == 1:
        startKeyListener.hotkey.stop()
        main_window.after(10, getClipboard)
        startKeyListener()

def startKeyListener():
    global k
    a = trigger()
    hotkey = pk.GlobalHotKeys({a: onBindingPress ,'<ctrl>+c': onClipPress})
    startKeyListener.hotkey = hotkey
    hotkey.start()

def closeWindow(window):
    global about_open, config_open
    if window == 'config':
        config_open = False
        openConfigWindow.main.destroy()
    
    elif window == 'about':
        about_open = False
        openAboutWindow.main.destroy()
        
def saveConfig():
    global delay_time, about_open
    startKeyListener.hotkey.stop()
    delay_time = int(openConfigWindow.seconds.get())
    if about_open == True:
        openAboutWindow.main.attributes('-topmost', stayOnTop())
    main_window.attributes('-topmost', stayOnTop())
    openConfigWindow.main.attributes('-topmost', stayOnTop())
    writeToConfigFile()
    startKeyListener()
    closeWindow('config')
    
def clearListBox():
    previous_input.delete(0, tk.END)
    writeToConfigFile()

def parseKeybindCombo(bs):
    if bs[0] == 'K':
        bs = bs[4:].split('_')
        bs = '<' + str(bs[0]) + '>'
    else:
        bs = str(bs[1])
    return bs

def getKeyPressed(key):
    global combo, k, end
    if end == True:
        return False
    combo = combo + '+' + parseKeybindCombo(str(key))
    k.release(key)

def startListener():
    listener = pk.Listener(on_press=getKeyPressed).start()
    startListener.l = listener

def getUserKeyBind():
    global bind_counter, user_defined_keybind, combo, end, k
   
    if bind_counter == 0:
        openConfigWindow.edit_bind.config(text='■', fg='black')
        bind_counter = 1
        end = False
        startListener()

    else:
        openConfigWindow.edit_bind.config(text='⬤', fg='red')
        bind_counter = 0
        end = True
        k.tap(pk.Key.ctrl)
        user_defined_keybind = str(combo[1:])
        combo = ''
        openConfigWindow.bind_field.delete(0, tk.END)
        openConfigWindow.bind_field.insert(0, trigger())

def openBugreport(e):
    recipient = 'bugs@bloq.me'
    subject = 'Type4Me - Bug Report'
    subject = subject.replace(' ', '%20')
    body = '''Name:
Version:
Issue in detail:
    '''
    body = body.replace(' ', '%20')
    body = body.replace('\n', '%0A%0A')
    webbrowser.open('mailto:' + recipient + '&subject=' + subject + '&body=' + body, new=1)

def escapeTheGoblin(e):
    wideMode.main.destroy()

#WIDE MODE
def wideMode():
    wide_window = tk.Toplevel(main_window)
    wideMode.main = wide_window
    wide_window.wm_attributes('-fullscreen', 'True')
    wide_window.bind('<Escape>', escapeTheGoblin)
    widemon = Image.open(wide_file)
    widemon = widemon.resize((wide_window.winfo_screenwidth(), wide_window.winfo_screenheight()), Image.ANTIALIAS)
    widemon = ImageTk.PhotoImage(widemon)
    bigboi = tk.Label(wide_window, image=widemon)
    bigboi.image = widemon
    bigboi.pack()
    wide_window.focus_set()

#DONO PAGE
def openDonationPage():
    webbrowser.open('https://www.paypal.com/donate/?business=5YX7ZYMNDJDZJ&no_recurring=1&item_name=%0A----------+Starving+gamer+needs+a+RTX+3070+Ti+----------&currency_code=AUD', new=1)

#ABOUT WINDOW
def openAboutWindow():
    global about_open
    about_open = True
    about_window = tk.Toplevel(main_window)
    about_window.title('Help')
    about_window.geometry('250x150')
    about_window.attributes('-topmost', stayOnTop())
    about_window.iconbitmap(default=icon_file)
    openAboutWindow.main = about_window
    about_window.protocol("WM_DELETE_WINDOW", lambda:closeWindow('about'))
    app_info_text = tk.Label(about_window, text=(appName + ' - ' + appVersion))
    app_info_text.pack(fill=tk.BOTH)
    about_text = tk.Label(about_window, text='Please report bugs to ')
    about_text.pack(fill=tk.BOTH)
    email_text = tk.Label(about_window, text='bugs@bloq.me', fg='blue')
    email_text.bind('<Button-1>', openBugreport)
    email_text.pack(fill=tk.BOTH)
    about_window_close = ttk.Button(about_window, text='Close', command=lambda:closeWindow('about'))
    about_window_close.pack(side=tk.BOTTOM, fill=tk.BOTH)
    dono_button = ttk.Button(about_window, text='$ Donate $', command=openDonationPage)
    dono_button.pack(side=tk.BOTTOM, fill=tk.BOTH)
    
#CONFIGUATION WINDOW
def openConfigWindow():
    global delay_time, onTop_value, clip_toggle_value, config_open
    config_open = True
    config_window = tk.Toplevel(main_window)
    config_window.title('Configuration')
    config_window.attributes('-topmost', stayOnTop())
    config_window.geometry('250x150')
    config_window.iconbitmap(default=icon_file)
    openConfigWindow.main = config_window
    config_window.protocol("WM_DELETE_WINDOW", lambda:closeWindow('config'))
    config_frame1 = tk.Frame(config_window)
    countdown_text = tk.Label(config_frame1, text='Seconds to wait:')
    countdown_text.pack(side=tk.LEFT, fill=tk.BOTH)
    input_seconds = tk.Entry(config_frame1)
    input_seconds.insert(0, delay_time)
    input_seconds.pack(side=tk.RIGHT, fill=tk.BOTH)
    openConfigWindow.seconds = input_seconds
    config_frame1.pack(fill=tk.BOTH)
    config_frame3 = tk.Frame(config_window)
    user_bind_label = tk.Label(config_frame3, text='Type text key binding:')
    user_bind_label.pack(fill=tk.BOTH, side=tk.LEFT)
    edit_bind = tk.Button(config_frame3, text='⬤', fg='red', command=getUserKeyBind)
    edit_bind.pack(side=tk.RIGHT)
    openConfigWindow.edit_bind = edit_bind
    user_bind_field = tk.Entry(config_frame3)
    user_bind_field.insert(0, trigger())
    openConfigWindow.bind_field = user_bind_field
    user_bind_field.pack(side=tk.RIGHT)
    config_frame3.pack(fill=tk.BOTH)
    config_frame2 = tk.Frame(config_window)
    on_top_label = tk.Label(config_frame2, text='Window always on top:')
    on_top_label.pack(side=tk.LEFT, fill=tk.BOTH)
    on_top_checkbox = tk.Checkbutton(config_frame2, variable=onTop_value)
    on_top_checkbox.pack(side=tk.RIGHT, fill=tk.BOTH)
    config_frame2.pack(fill=tk.BOTH)
    config_frame4 = tk.Frame(config_window)
    clip_toggle_label = tk.Label(config_frame4, text='Input clipboard automatically:')
    clip_toggle_label.pack(side=tk.LEFT, fill=tk.BOTH)
    clip_toggle_checkbox = tk.Checkbutton(config_frame4, variable=clip_toggle_value)
    clip_toggle_checkbox.pack(side=tk.RIGHT, fill=tk.BOTH)
    config_frame4.pack(fill=tk.BOTH)
    wide_button = ttk.Button(config_window, text='Wide Mode', command=wideMode)
    wide_button.pack(fill=tk.BOTH)
    save_button = ttk.Button(config_window, text='Save & Close', command=saveConfig)
    save_button.pack(fill=tk.BOTH)
    
#MAIN WINDOW
main_window = tk.Tk(screenName=appName,baseName=appName)
main_window.title(appName)
main_window.geometry('250x275')
main_window.iconbitmap(default=icon_file)
onTop_value = tk.IntVar()
clip_toggle_value = tk.IntVar()
clip_toggle_value.set(1)

toolbar = tk.Menu(main_window)
file_menu = tk.Menu(toolbar, tearoff=False)
file_menu.add_command(label='Configuration', command=openConfigWindow)
file_menu.add_command(label='Exit', command=main_window.destroy)
toolbar.add_cascade(label='File', menu=file_menu)
help_menu = tk.Menu(toolbar, tearoff=False)
help_menu.add_command(label='About', command=openAboutWindow)
toolbar.add_cascade(label='Help', menu=help_menu)
main_window.config(menu=toolbar)
input_frame = ttk.LabelFrame(main_window, text='Text to Type:')
main_input = tk.Entry(input_frame)
main_input.bind('<KeyPress>', mainInputKeyPress)
main_input.pack(side=tk.TOP, fill=tk.BOTH)
run_code = ttk.Button(input_frame, text='Type Text', command=delayIt)
run_code.pack(side=tk.BOTTOM, fill=tk.BOTH)
input_frame.pack(fill=tk.BOTH)
previous_input_top_frame = ttk.LabelFrame(main_window, text='Previous Inputs:')
previous_input = tk.Listbox(previous_input_top_frame, selectmode='SINGLE', width=37)
previous_input.pack(side=tk.LEFT, fill=tk.BOTH)
previous_input_scroll = ttk.Scrollbar(previous_input_top_frame)
previous_input_scroll.pack(side=tk.RIGHT, fill=tk.BOTH)
previous_input.config(yscrollcommand=previous_input_scroll.set)
previous_input_scroll.config(command=previous_input.yview)
previous_input.bind("<<ListboxSelect>>", changeMainInput)
previous_input_top_frame.pack(fill=tk.BOTH)
previous_input_clear = ttk.Button(main_window, text='Clear List', command=lambda:clearListBox())
previous_input_clear.pack(fill=tk.BOTH)

#Works on windows, not on mac.
main_window.after(0, startKeyListener)
readConfigFile()
main_window.attributes('-topmost', stayOnTop())
main_window.mainloop()