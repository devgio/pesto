__version__ = '1.0'

# Supress the stdout
import sys, io
std_out = io.StringIO()
sys.stdout = std_out
sys.stderr = std_out

import pkg_resources.py2_warn # this is for pyinstaller
import atexit
import os
from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch
from kivy.core.window import Window
from pynput.keyboard import Controller, Listener, Key

dir_path = os.path.dirname(os.path.realpath(__file__))
home_dir = os.path.expanduser("~")

# Sizes for GUI
window_width, window_height = Window.size
text_size = int(window_height/30)
small_text_size = int(text_size/2)
key_combo_column_width = int(window_width*0.12)
intro_column_width = int(window_width*0.12)
active_column_width = int(window_width*0.12)
text_column_width = int(window_width*0.64)


# Key combinations to trigger the typing
class KeyCombo:
    def __init__(self, name, trigger):
        self.name = name
        self.trigger = trigger
        self.switch = Switch(active=True, size_hint_x=None, width=active_column_width)
        self.text_input = TextInput(size_hint_x=None, width=text_column_width)
        self.intro = Switch(size_hint_x=None, width=intro_column_width)

    def text(self):
        return self.text_input.text

key_combos = [
    KeyCombo('F1', 'f1'),
    KeyCombo('F2', 'f2'),
    KeyCombo('F3', 'f3'),
    KeyCombo('F4', 'f4'),
    KeyCombo('F5', 'f5'),
    KeyCombo('F6', 'f6'),
    KeyCombo('F7', 'f7'),
    KeyCombo('F8', 'f8'),
    KeyCombo('F9', 'f9'),
    KeyCombo('F10', 'f10'),
    KeyCombo('F11', 'f11'),
    KeyCombo('F12', 'f12'),
]


# Load texts from last time
text_save_separator = '¶¶'
text_save_file = 'cache.temp'
text_save_file = os.path.join(home_dir, text_save_file)
if os.path.isfile(text_save_file):
    try:
        with open(text_save_file, 'r') as f:
            texts = f.read().split(text_save_separator)
            for kc in key_combos:
                state = texts[key_combos.index(kc)]
                if state[0] == '1': kc.intro.active = True
                if state[1] == '0': kc.switch.active = False
                kc.text_input.text = state[2:]
    except:
        os.remove(text_save_file)


# Create GUI
class MainPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 4
        self.add_widget(Label(text=f'[size={text_size}][b]TRIGGER[/b][/size]', markup=True, size_hint_x=None, width=key_combo_column_width))
        self.add_widget(Label(text=f'[size={text_size}][b]TEXT[/b][/size]', markup=True, size_hint_x=None, width=text_column_width))
        self.add_widget(Label(text=f'[size={text_size}][b]ENTER[/b][/size]', markup=True, size_hint_x=None, width=intro_column_width))
        self.add_widget(Label(text=f'[size={text_size}][b]ACTIVE[/b][/size]', markup=True, size_hint_x=None, width=active_column_width))
        for kc in key_combos:
            self.add_widget(Label(text=f'[i][size={text_size}]'+kc.name+'[/size][/i]', markup=True, size_hint_x=None, width=key_combo_column_width))
            self.add_widget(kc.text_input)
            self.add_widget(kc.intro)
            self.add_widget(kc.switch)
        self.add_widget(Label(text=f'[size={small_text_size}]Version: {__version__}[/size]', markup=True))

class PestoApp(App):
    def open_settings(self, *largs):
        pass

    def build(self):
        self.icon = os.path.join(dir_path, 'duck.ico')
        return MainPage()


# Listen for key presses
keyboard = Controller()
triggers = [x.trigger for x in key_combos]

def on_press(key):
    try:
        k = key.char
    except:
        k = key.name
    if k in triggers:
        kc = key_combos[triggers.index(k)]
        if kc.switch.active:
            keyboard.type(kc.text())
            if kc.intro.active:
                keyboard.press(Key.enter)

listener = Listener(on_press=on_press)
listener.start()


# Save the texts for next time
def save_texts():
    with open(text_save_file, 'w') as f:
        for kc in key_combos:
            intro, switch = 0, 0
            if kc.switch.active: switch = 1
            if kc.intro.active: intro = 1
            f.write(f'{intro}{switch}{kc.text()}{text_save_separator}')
atexit.register(save_texts)



if __name__ == "__main__":
    PestoApp().run()












