import sqlite3

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from collections import OrderedDict
from src.BillingKiv.utils.datatable import DataTable
Builder.load_file('admin/admin.kv')
class AdminWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        content = self.ids.scrn_product_contents
        product = self.get_products()
        producttable = DataTable(table=product)
        content.add_widget(producttable)
    def add_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()
        crud_code = TextInput(hint_text = 'Product Code')
        crud_name = TextInput(hint_text='Product Name')
        crud_weight = TextInput(hint_text='Quantity')
        crud_price = TextInput(hint_text='Price')
        crud_submit = Button(text= 'Add',size_hint_x=None,width=100,on_release=lambda  x:self.add_product(crud_code.text,crud_name.text,crud_weight.text,crud_price.text))
        target.add_widget(crud_code)
        target.add_widget(crud_name)
        target.add_widget(crud_weight)
        target.add_widget(crud_price)
        target.add_widget(crud_submit)
    def update_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()
        crud_code = TextInput(hint_text='Product Code')
        crud_name = TextInput(hint_text='Product Name')
        crud_quantity = TextInput(hint_text='Quantity')
        crud_price = TextInput(hint_text='Price')
        crud_submit = Button(text='Update', size_hint_x=None,width=100,on_release=lambda  x:self.update_product(crud_code.text,crud_name.text,crud_quantity.text,crud_price.text))
        target.add_widget(crud_code)
        target.add_widget(crud_name)
        target.add_widget(crud_quantity)
        target.add_widget(crud_price)
        target.add_widget(crud_submit)
    def add_product(self,crud_code,crud_name,crud_weight,crud_price):
        task = (crud_code,crud_name,crud_weight,crud_price)
        sql = ''' INSERT INTO products(productcode,productname,instock,price)
                      VALUES(?,?,?,?) '''
        conn = sqlite3.connect('jdbc:sqlite:sqlite.db')
        c = conn.cursor()
        c.execute(sql,task)
        conn.commit()
        content = self.ids.scrn_product_contents
        content.clear_widgets()
        product = self.get_products()
        producttable = DataTable(table=product)
        content.add_widget(producttable)
        conn.close()
    def update_product(self,crud_code,crud_name,crud_quantity,crud_price):
        sql = ''' Update products set productname = ?, instock = ?, price = ? where productcode = ?'''
        columnValues = (crud_name,crud_quantity,crud_price,crud_code)
        conn = sqlite3.connect('jdbc:sqlite:sqlite.db')
        c = conn.cursor()
        c.execute(sql, columnValues)
        conn.commit()
        content = self.ids.scrn_product_contents
        content.clear_widgets()
        product = self.get_products()
        producttable = DataTable(table=product)
        content.add_widget(producttable)
        conn.close()

    def remove_product_fields(self):
        target = self.ids.ops_fields_p
        target.clear_widgets()
        crud_code = TextInput(hint_text='Product Code')
        crud_submit = Button(text='Remove',size_hint_x=None,width=100,on_release=lambda  x:self.remove_product(crud_code.text))
        target.add_widget(crud_code)
        target.add_widget(crud_submit)
    def remove_product(self,crud_code):
        sql = '''DELETE FROM products
                 WHERE productcode = ?'''
        columnValues = (crud_code)
        conn = sqlite3.connect('jdbc:sqlite:sqlite.db')
        c = conn.cursor()
        c.execute(sql,(columnValues,))
        conn.commit()
        content = self.ids.scrn_product_contents
        content.clear_widgets()
        product = self.get_products()
        producttable = DataTable(table=product)
        content.add_widget(producttable)
        conn.close()
    def get_products(self):
        sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS products (
                                                id integer PRIMARY KEY,
                                                productcode text NOT NULL,
                                                productname text NOT NULL,
                                                instock text ,
                                                price text
                                                
                                            ); """
        conn = sqlite3.connect('jdbc:sqlite:sqlite.db')
        c = conn.cursor()
        c.execute(sql_create_projects_table)
        takser = '''SELECT * FROM products'''
        c.execute(takser)
        _stocks = OrderedDict()
        _stocks['product code'] = {}
        _stocks['product name'] = {}
        _stocks['product weight'] = {}
        _stocks['price'] = {}
        product_code = []
        product_name = []
        product_weight = []
        price = []
        rows = c.fetchall()
        '''if (len(name) > 10):
            name = name[:10] + '...' 
        '''
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
        return _stocks

    def change_screen(self,instance):
        if instance.text == 'Manage Users':
            self.ids.scrn_mngr.current = 'scrn_content'
        elif instance.text == 'Manage Products':
            self.ids.scrn_mngr.current = 'scrn_product_content'
        else:
            self.ids.scrn_mngr.current = 'scrn_analysis'
class AdminApp(App):
    def build(self):
        return AdminWindow()
if __name__ == '__main__':
    AdminApp().run()
