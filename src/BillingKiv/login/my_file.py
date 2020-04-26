from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder
Builder.load_file('login/pong.kv')
class PongGame(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def validate_user(self):
        user = self.ids.username_field
        pwd = self.ids.pwd_field
        info = self.ids.info
        uname = user.text
        passw = pwd.text
        if uname == "" or passw == "":
            info.text = "[color=#FF0000]username and/ or password required[/color]"
        else:

            if uname == "nadeem" and passw == "rawther":
                info.text = "[color=#00ff00]Logged in successfully[/color]"
                self.parent.parent.current = 'scrn_admin'

            elif uname == "nads" and passw == "rawt":
                info.text = "[color=#ff0000]invalid username and/or password error[/color]"
                self.parent.parent.current = 'scrn_op'


class PongApp(App):
    def build(self):
        return PongGame()


if __name__ == '__main__':
    PongApp().run()
