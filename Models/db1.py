# -*- coding: utf-8 -*-

db.define_table('item_details',
                Field('item_no', 'string', requires=IS_NOT_EMPTY()), 
                Field('item_name', 'string', requires=IS_NOT_EMPTY()))

db.define_table('purchase',
                Field('purchase_no', 'string', requires=IS_NOT_EMPTY()),
                Field('item_item_no', requires=IS_IN_DB(db, db.item_details.item_no,'%(item_no)s')),
                Field('vendor_name', 'string', requires=IS_NOT_EMPTY()), 
                Field('vendor_details', 'text', requires=IS_NOT_EMPTY()),
                Field('quantity', 'integer'),
                 Field('cost_price', 'decimal(10,2)'),
                 Field('selling_price', 'decimal(10,2)'),
                   Field('ordered_on', 'datetime'),
                   Field('delivered_on', 'datetime'))

db.define_table('stock',
                 Field('stock_no'),
                 Field('purchase_no'),
                Field('item_item_no'),
                 Field('cost_price', 'decimal(10,2)'),
                 Field('selling_price', 'decimal(10,2)'),
                Field('quantity', 'integer'),
                  Field('stocked_on', 'datetime'))

db.define_table('sale',
                Field('bill_no'),
                 Field('stock_no'),
                Field('item_item_no'),
                 Field('quantity', 'integer'),                
                 Field('cost_price', 'decimal(10,2)'),
                 Field('selling_price', 'decimal(10,2)'),
                 Field('discount', 'decimal(10,2)'),
                Field('profit', 'decimal(10,2)'),
                Field('loss', 'decimal(10,2)'),
                 Field('final_price', 'decimal(10,2)'),
                Field('date_of_bill', 'datetime'))
