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
from kivy.uix.button import Button
from collections import OrderedDict
Builder.load_file('listcreation.kv')
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):

            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

class ListcreationWindow(BoxLayout):

    code_inp = ObjectProperty()
    flt_list = ObjectProperty()
    word_list = ListProperty()
    def __init__(self, **kwargs):
        super(ListcreationWindow, self).__init__(**kwargs)
        self.cart = []
        self.qty = []
        self.total = 0.00


    # this is the variable storing the number to which the look-up will start
    starting_no = NumericProperty(3)

    def update_purchases(self):
        pcode = self.ids.code_inp.text
        pqty = self.ids.qty_inp.text
        pname = self.ids.disc_inp.text
        pprice = self.ids.price_inp.text
        products_container = self.ids.products
        conn = sqlite3.connect('jdbc:sqlite:sqlite.db')
        c = conn.cursor()
        takser = '''SELECT * FROM products WHERE productcode = ?'''
        if c.execute(takser,(pcode,)) is not None:
            rows = c.fetchall()
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
            idx = 0
            while idx < products_length:
                _stocks['product code'][idx] = product_code[idx]
                _stocks['product name'][idx] = product_name[idx]
                _stocks['product weight'][idx] = product_weight[idx]
                _stocks['price'][idx] = price[idx]
                idx += 1
            self.ids.code_inp.text = _stocks['product code'][0]
            self.ids.disc_inp.text = _stocks['product name'][0]
            self.ids.price_inp.text = _stocks['price'][0]
            details = BoxLayout(size_hint_y=None, height=30, pos_hint={'top': 1})
            products_container.add_widget(details)
            code = Label(text= _stocks['product code'][0], size_hint_x=.2, color=(.06, .45, .45, 1))
            name = Label(text=_stocks['product name'][0], size_hint_x=.3, color=(.06, .45, .45, 1))
            qty = Label(text=_stocks['price'][0], size_hint_x=.1, color=(.06, .45, .45, 1))
            price = Label(text=str(float(_stocks['price'][0]) * float(_stocks['price'][0])), size_hint_x=.1,color=(.06, .45, .45, 1))
            details.add_widget(code)
            details.add_widget(name)
            details.add_widget(qty)
            details.add_widget(price)
            self.total += float(_stocks['price'][0])
            purchase_total = '`\n\nTotal\t\t\t\t\t\t\t\t' + str(self.total)
            self.ids.cur_product.text = _stocks['product name'][0]
            self.ids.cur_price.text = _stocks['price'][0]
            pname = _stocks['product name'][0]
            pprice = _stocks['price'][0]
            pcode = _stocks['product code'][0]
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
                expr = '%s\t\tx\d\t' %(pname)
                rexpr = pname + '\t\tx' + str(pqty) + '\t'
                nu_text = re.sub(expr, rexpr, prev_text)
                preview.text = nu_text + purchase_total
            else:
                self.cart.append(pcode)
                self.qty.append(1)
                pqty = 1
                nu_preview = '\n'.join([prev_text,pname+'\t\tx'+ str(pqty) +'\t\t'+str(pprice),str(purchase_total)])
                preview.text = nu_preview
            _stocks.clear()
    def dopdown(self):
        pass
class MyLayout(BoxLayout):
    code_inp = ObjectProperty()
    rv = ObjectProperty()
    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)

class MyTextInput(TextInput):
    code_inp = ObjectProperty()
    flt_list = ObjectProperty()
    word_list = ListProperty()
    # this is the variable storing the number to which the look-up will start
    starting_no = NumericProperty(3)
    suggestion_text = ''


    def __init__(self, **kwargs):
        super(MyTextInput, self).__init__(**kwargs)
    def on_text(self, instance, value):
        # find all the occurrence of the word
        #self.parent.ids.rv.data = []
        matches = [self.word_list[i] for i in range(len(self.word_list)) if
                   self.word_list[i][:self.starting_no] == value[:self.starting_no]]
        # display the data in the recycleview
        display_data = []
        for i in matches:
            display_data.append({'text': i})
        #self.parent.ids.rv.data = display_data
        #ensure the size is okay
        if len(matches) <= 10:
            self.parent.height = (50 + (len(matches) * 20))
        else:
            self.parent.height = 240
        
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if self.suggestion_text and keycode[1] == 'tab':
            self.insert_text(self.suggestion_text + ' ')
            return True
        return super(MyTextInput, self).keyboard_on_key_down(window, keycode, text, modifiers)

class RV(RecycleView,DropDown):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': str(x)} for x in range(100)]
        self.data.insert(0, {'text': 'frank'})
        self.data.append({'text': 'man'})





class ListcreationApp(App):
    def build(self):
        return ListcreationWindow()

if __name__=='__main__':
    ListcreationApp().run()