from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.properties import NumericProperty, ListProperty, BooleanProperty, ObjectProperty
from kivy.uix.textinput import TextInput
import sqlite3
import re
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.clock import Clock
from collections import OrderedDict
from kivy.uix.gridlayout import GridLayout

Builder.load_file('Operatorwindow/operator.kv')

class CustomDropDown(DropDown):
    force_below = BooleanProperty(False)  # if True, DropDown will be positioned below attached to Widget
    def __init__(self, **kwargs):
        super(CustomDropDown, self).__init__(**kwargs)
        self.do_not_reposition = False  # flag used to avoid repositioning recursion

    def _reposition(self, *largs):
        if self.do_not_reposition:
            return
        super(CustomDropDown, self)._reposition(*largs)
        if self.force_below:
            self.make_drop_below()

    def make_drop_below(self):
        self.do_not_reposition = True  # avoids recursion triggered by the changes below
        if self.attach_to is not None:
            wx, wy = self.to_window(*self.attach_to.pos)
            self.height = wy  # height of DropDown will fill window below attached to Widget
            self.top = wy  # top of DropDown will be at bottom of attached to Widget
        self.do_not_reposition = False  # now turn auto repositioning back on

class OperatorWindow(BoxLayout):
    code_inp = ObjectProperty()
    flt_list = ObjectProperty()
    word_list = ListProperty()



    def __init__(self, **kwargs):
        super(OperatorWindow, self).__init__(**kwargs)
        self.cart = []
        self.qty = []
        self.idx = 0
        self.total = 0.00
        self.pname = self.ids.disc_inp.text
        self.rows = ListProperty()
        self._stocks = OrderedDict()
        self.pcode = self.ids.code_inp.text
        self.product_code = []
        self.product_name = []
        self.product_weight = []
        self.price = []


    def update_price(self):
        pcode = self.ids.code_inp.text
        pqty = self.ids.qty_inp.text
        pname = self.ids.disc_inp.text
        pprice = self.ids.price_inp.text
        products_container = self.ids.products
        conn = sqlite3.connect('jdbc:sqlite:sqlite.db')
        c = conn.cursor()
        takser = '''SELECT * FROM products WHERE productcode = ?'''
        input_list = []
        if c.execute(takser, (pcode,)) is not None:
            self.rows = c.fetchall()
            for j in self.rows:
                self.product_code.append(j[1])
                self.product_name.append(j[2])
                self.product_weight.append(pqty)
                self.price.append(str(int(j[4])* int(pqty)))
            products_length = len(self.product_code)

            self.ids.price_inp.text=""
            mlen = len(self.price)
            self.ids.price_inp.text = str(self.price[mlen-1])


            '''
            self.total += float(self._stocks['price'][0])
            purchase_total = '`\n\nTotal\t\t\t\t\t\t\t\t' + str(self.total)
            preview = self.ids.receipt_preview
            prev_text = preview.text
            pqty = str(1)
            _prev = prev_text.find('`')
            if _prev > 0:
                prev_text = prev_text[:_prev]
            ptarget = -1
            for i, c in enumerate(self.cart):
                if c == pcode:
                    ptarget = i
            if ptarget >= 0:
                pqty = self.qty[ptarget] + 1
                self.qty[ptarget] = pqty
                expr = '%s\t\tx\d\t' % (pname)
                rexpr = pname + '\t\tx' + str(pqty) + '\t'
                nu_text = re.sub(expr, rexpr, prev_text)
                preview.text = nu_text + purchase_total
            else:
                self.cart.append(pcode)
                self.qty.append(1)
                pqty = 1
                nu_preview = '\n'.join(
                    [prev_text, pname + '\t\tx' + str(pqty) + '\t\t' + str(pprice), str(purchase_total)])
                preview.text = nu_preview
            '''

    def printer(self):
        total = 0
        pqty = self.ids.qty_inp.text
        for ij in self.price:

            total += float(ij)

        purchase_total = '`\n\nTotal\t\t\t\t\t\t\t\t' + str(total)
        preview = self.ids.receipt_preview
        preview.text = ""
        texter = "\t\t\t\tThe Collector\n\t\t\t\t123 Main St\n\t\t\t\tKnowhere, Space\n\n\t\t\t\tTel:(555)-123-456\n\t\t\t\tReceipt No:\n\t\t\t\t Gate:\n\n"
        preview.text = texter
        prev_text = preview.text
        js = 0
        for pcod in self.product_name:

            preview.text = preview.text + ('\n'+ pcod + '\t\tx' + self.product_weight[js] + '\t\t' + self.price[js])
            js += 1
        preview.text = preview.text+str(purchase_total)



class MyTextInput(TextInput):
    code_inp = ObjectProperty()
    flt_list = ObjectProperty()
    word_list = ListProperty()
    starting_no = NumericProperty(1)
    def __init__(self, **kwargs):
        super(MyTextInput, self).__init__(**kwargs)
        #Clock.schedule_once(self.on_text)
        conn = sqlite3.connect('jdbc:sqlite:sqlite.db')
        self.c = conn.cursor()
        self.takser = '''SELECT * FROM products WHERE productcode LIKE ? '''
        self.word_list = []
        self.bind()
        self.dropdown = CustomDropDown(force_below=True)
        self.display_data = []
    def mymethod(self,instance,x):

        takser = '''SELECT * FROM products WHERE productcode = ? '''
        input_list = []
        if self.c.execute(takser,(x,)) is not None:
            rows = self.c.fetchall()
            _stocks = OrderedDict()
            _stocks['product code'] = {}
            _stocks['product name'] = {}
            _stocks['product weight'] = {}
            _stocks['price'] = {}
            product_code = []
            product_name = []
            product_weight = []
            price = []
            for j in rows:
                product_code.append(j[1])
                product_name.append(j[2])
                product_weight.append(j[3])
                price.append(j[4])
            products_length = len(product_code)

            for j in product_name:
                App.get_running_app().root.operator_widget.ids.disc_inp.text=j
                App.get_running_app().root.operator_widget.ids.code_inp.text = x
                print(j)

    def on_text(self, instance, value):
        self.dropdown.clear_widgets()
        self.word_list.clear()
        self.display_data.clear()
        if self.c.execute(self.takser,(value+"%",)) is not None:
            rows = self.c.fetchall()
            _stocks = OrderedDict()
            _stocks['product code'] = {}
            _stocks['product name'] = {}
            _stocks['product weight'] = {}
            _stocks['price'] = {}
            product_code = []
            product_name = []
            product_weight = []
            price = []
            for j in rows:
                product_code.append(j[1])
                product_name.append(j[2])
                product_weight.append(j[3])
                price.append(j[4])
            products_length = len(product_code)
            for j in product_code:
                self.word_list.append(j)
        for i in self.word_list:
            self.display_data.append(i)
        print(self.display_data)
        for note in self.display_data:
            btn = Button(text='%r' % int(note), size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)

        self.dropdown.bind(on_select= self.mymethod)#lambda instance, x: setattr(self, 'text', x))

        if self.dropdown.parent is None and self.get_parent_window() is not None:
            self.dropdown.open(self)
            self.dropdown.clear_widgets()
            self.word_list.clear()
            self.display_data.clear()


    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if self.suggestion_text and keycode[1] == 'tab':
            self.insert_text(self.suggestion_text + ' ')
            return True
        return super(MyTextInput, self).keyboard_on_key_down(window, keycode, text, modifiers)
class MyTextInput2(TextInput):
    code_inp = ObjectProperty()
    flt_list = ObjectProperty()
    word_list = ListProperty()
    # this is the variable storing the number to which the look-up will start
    starting_no = NumericProperty(1)
    suggestion_text = ''


    def __init__(self, **kwargs):
        super(MyTextInput2, self).__init__(**kwargs)
        self.word_list = []
        # display the data in the recycleview
        self.dropdown = CustomDropDown(force_below=True)
        conn = sqlite3.connect('jdbc:sqlite:sqlite.db')
        self.c = conn.cursor()
        self.takser = '''SELECT * FROM products WHERE productname LIKE ? '''
        self.word_list = []

        # display the data in the recycleview
        self.dropdown = CustomDropDown(force_below=True)
        self.display_data = []

    def mymethod2(self,instance,x):

        takser = '''SELECT * FROM products WHERE productname = ? '''
        input_list = []
        if self.c.execute(takser,(x,)) is not None:
            rows = self.c.fetchall()
            _stocks = OrderedDict()
            _stocks['product code'] = {}
            _stocks['product name'] = {}
            _stocks['product weight'] = {}
            _stocks['price'] = {}
            product_code = []
            product_name = []
            product_weight = []
            price = []
            for j in rows:
                product_code.append(j[1])
                product_name.append(j[2])
                product_weight.append(j[3])
                price.append(j[4])
            products_length = len(product_code)

            for j in product_code:
                App.get_running_app().root.operator_widget.ids.code_inp.text=j
                App.get_running_app().root.operator_widget.ids.disc_inp.text = x
                print(j)

    def on_text(self, instance, value):
        self.dropdown.clear_widgets()
        self.word_list.clear()

        self.display_data.clear()
        if self.c.execute(self.takser, (value + "%",)) is not None:
            rows = self.c.fetchall()
            _stocks = OrderedDict()
            _stocks['product code'] = {}
            _stocks['product name'] = {}
            _stocks['product weight'] = {}
            _stocks['price'] = {}
            product_code = []
            product_name = []
            product_weight = []
            price = []
            for j in rows:
                product_code.append(j[1])
                product_name.append(j[2])
                product_weight.append(j[3])
                price.append(j[4])
            products_length = len(product_code)
            for j in product_name:
                print(j)
                self.word_list.append(j)
        for i in self.word_list:
            self.display_data.append(i.strip("'"))
        print(self.display_data)
        for note in self.display_data:
            btn = Button(text=note.strip("'"), size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
        self.dropdown.bind(on_select= self.mymethod2) #lambda instance, x: setattr(self, 'text', x))
        if self.dropdown.parent is None and self.get_parent_window() is not None:
            self.dropdown.open(self)
            self.dropdown.clear_widgets()
            self.word_list.clear()
            self.display_data.clear()
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        print('The key', keycode, 'have been pressed')

        if self.suggestion_text and keycode[1] == 'tab':
            self.insert_text(self.suggestion_text + ' ')
            return True
        return super(MyTextInput2, self).keyboard_on_key_down(window, keycode, text, modifiers)


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''

class SelectableLabel(RecycleDataViewBehavior, GridLayout):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    cols = 5


    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        self.label1_text = data['label1']['text']
        self.label2_text = data['label2']['text']
        self.label4_text = data['label4']['text']
        self.label3_text = data['label3']['text']

        #self.ids['id_label3'].text = data['label3']['text']  # As an alternate method of assignment
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)
    def callme(self,index):
        print(index)
        App.get_running_app().root.operator_widget.ids.rv.data.pop(index)
        App.get_running_app().root.operator_widget.product_code.pop(index)
        App.get_running_app().root.operator_widget.product_name.pop(index)
        App.get_running_app().root.operator_widget.product_weight.pop(index)
        App.get_running_app().root.operator_widget.price.pop(index)
        for m in App.get_running_app().root.operator_widget.price:
            print(m+"nadeem got")


    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []

class OperatorApp(App):
    def build(self):
        return OperatorWindow()

if __name__ == '__main__':
    OperatorApp().run()