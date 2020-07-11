from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch
from kivy.core.window import Window

window_width = Window.size[0]
key_combo_column_width = window_width*0.12
intro_column_width = window_width*0.12
active_column_width = window_width*0.12
text_column_width = window_width*0.64


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


class MainPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 4
        self.add_widget(Label(text='TRIGGER', size_hint_x=None, width=key_combo_column_width))
        self.add_widget(Label(text='TEXT', size_hint_x=None, width=text_column_width))
        self.add_widget(Label(text='INTRO', size_hint_x=None, width=intro_column_width))
        self.add_widget(Label(text='ACTIVE', size_hint_x=None, width=active_column_width))

        for kc in key_combos:
            self.add_widget(Label(text=kc.name, size_hint_x=None, width=key_combo_column_width))
            self.add_widget(kc.text_input)
            self.add_widget(kc.intro)
            self.add_widget(kc.switch)

class HobbaToolApp(App):
    def open_settings(self, *largs):
        pass
    def build(self):
        return MainPage()


# Listen for key presses
from pynput.keyboard import Controller, Listener, Key

keyboard = Controller()
triggers = [x.trigger for x in key_combos]

def on_press(key):
    try:
        k = key.char
    except:
        k = key.name
    print(f':: {k} pressed')
    if k in triggers:
        kc = key_combos[triggers.index(k)]
        if kc.switch.active:
            keyboard.type(kc.text())
            if kc.intro.active:
                keyboard.press(Key.enter)

listener = Listener(on_press=on_press)
listener.start()


if __name__ == "__main__":
    HobbaToolApp().run()












