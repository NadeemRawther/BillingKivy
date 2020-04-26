from kivy.app import  App
from kivy.uix.boxlayout import BoxLayout
from src.BillingKiv.admin.admin import AdminWindow
from src.BillingKiv.login.my_file import PongGame
from src.BillingKiv.Operatorwindow.operatorwindow import OperatorWindow





class MainWindow(BoxLayout):
    admin_widget = AdminWindow()
    signin_widget = PongGame()
    operator_widget = OperatorWindow()

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.ids.scrn_si.add_widget(self.signin_widget)
        self.ids.scrn_admin.add_widget(self.admin_widget)
        self.ids.scrn_op.add_widget(self.operator_widget)


class MainApp(App):
    def build(self):
        return MainWindow()

if __name__=='__main__':
    MainApp().run()