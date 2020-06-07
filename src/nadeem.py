def update_purchases(self):
    pcode = self.ids.code_inp.text
    pqty = self.ids.qty_inp.text
    pname = self.ids.disc_inp.text
    pprice = self.ids.price_inp.text
    products_container = self.ids.products
    conn = sqlite3.connect('jdbc:sqlite:sqlite.db')
    c = conn.cursor()

    if c.execute(takser, (pcode,)) is not None:
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
        code = Label(text=_stocks['product code'][0], size_hint_x=.2, color=(.06, .45, .45, 1))
        name = Label(text=_stocks['product name'][0], size_hint_x=.3, color=(.06, .45, .45, 1))
        qty = Label(text=_stocks['price'][0], size_hint_x=.1, color=(.06, .45, .45, 1))
        price = Label(text=str(float(_stocks['price'][0]) * float(_stocks['price'][0])), size_hint_x=.1,
                      color=(.06, .45, .45, 1))
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
        _stocks.clear()
        # paired_iter = zip(items_1, items_2,items_3,items_4)
        self.data = []

        # for i1, i2,i3,i4 in paired_iter:
        #    d = {'label1':{'text':i4},'label2': {'text': i1}, 'label3': {'text': i2},'label4': {'text': i3}}
        #    self.data.append(d)
        # can also be performed in a complicated one liner for those who like it tricky
        # self.data = [{'label2': {'text': i1}, 'label3': {'text': i2}} for i1, i2 in zip(items_1, items_2)]
