from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder






Builder.load_string('''
<DataTable>:
    id : main_win
    RecycleView:
        viewclass:'CustLabel'
        id:table_floor
        RecycleGridLayout:
            id:table_floor_layout
            cols:5
            default_size:(None,250)
            default_size_hint:(1,None)
            size_hint_y:None
            height:self.minimum_height
            spacing: 5
<CustLabel@Label>:
    bcolor:(1,1,1,1)
    canvas.before:
        Color:
            rgba:root.bcolor
        Rectangle:
            size:self.size
            pos:self.pos                
''')

class DataTable(BoxLayout):
    def __init__(self,table = '', **kwargs):
        super().__init__(**kwargs)
        '''product_code = []
        product_name = []
        product_weight = []
        in_stock = []
        sold = []
        order = []
        last_purchase = []
        product_code.append('code to appen producode')
        product_name.append('onnu')
        product_weight.append('rnadu')
        in_stock.append('munnu')
        sold.append('naalu')
        order.append('anchu')
        last_purchase.append('aaru')
        product_code.append('code to appen producode2')
        product_name.append('onnu2')
        product_weight.append('rnadu2')
        in_stock.append('munnu2')
        sold.append('naalu2')
        order.append('anchu2')
        last_purchase.append('aaru2')
        _stocks = OrderedDict()
        _stocks['product_code']= product_code[0]
        _stocks['product_name'] = product_name[0]
        _stocks['product_weight'] = product_weight[0]
        _stocks['in_stock'] = in_stock[0]
        _stocks['sold'] = sold[0]
        _stocks['order'] = order[0]
        _stocks['last_purchase'] = last_purchase[0]'''
        products =  table #self.get_products()
        col_titles= [k for k in products.keys()]
        rows_len = len(products[col_titles[0]])
        print(col_titles)
        self.columns = len(col_titles)
        print(rows_len)
        table_data =[]
        for t in col_titles:
            table_data.append({'text':str(t),'size_hint_y':None,'height':50,'bcolor':(.06,.45,.45,1)})
        for r in range(rows_len):
            for t in col_titles:
                print(str(products[t][r]))
                table_data.append({'text':str(products[t][r]),'size_hint_y':None,'height':30,'bcolor':(.06,.45,.45,1)})
        self.ids.table_floor_layout.cols = self.columns
        self.ids.table_floor.data = table_data


