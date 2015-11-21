# -*- coding: utf-8 -*-
# try something like
POSTS_PER_PAGE = 10
import datetime
import decimal
import math
@auth.requires_membership('Cashier')
def index(): 
    return dict(message="CASHIER HOME PAGE!! WELCOME!!")

@auth.requires_membership('Cashier')
def item_show():
    rows = db(db.item_details).select()
    return locals()

@auth.requires_membership('Cashier')
def bill():
    rows = db().select(db.sale.bill_no, groupby=db.sale.bill_no)
    return locals()

@auth.requires_membership('Cashier')
def generate_bill():
    bil = request.vars.bill_no
    rows = db(db.sale.bill_no==bil).select()
    return locals()

@auth.requires_membership('Cashier')
def insert_sale():
    rows = db(db.stock).select(groupby=db.stock.item_item_no)
    rowcount=db(db.sale).count()
    billdate = datetime.datetime.now()
    billcount=str(2001+rowcount)
    L1= request.vars.quantity
    L2 = request.vars.discount
    L3 = []
    stock_del = []
    dis_list=[]
    quantitylist=[]
    count = 0
    for row in rows:
        count+=1
        L3.append(row.item_item_no)
    for i in range(len(L1)):
        if not L1[i]:
            L1[i]=0
    for i in range(len(L2)):
        if not L2[i]:
            L2[i]=0 
    rows = db(db.stock).select(orderby=db.stock.stocked_on) 
    for i in range(len(L3)):        
            for row in rows:
                if float(L1[i])>0.0:
                    if row.item_item_no == L3[i]:
                        if row.quantity<float(L1[i]): 
                            db(db.stock.id == row.id).delete()
                            L1[i] = float(L1[i])-float(row.quantity)
                            quantitylist.append(float(row.quantity))
                            continue
                        else:
                            db(db.stock.id == row.id).update(quantity=row.quantity-float(L1[i]))
                            quantitylist.append(float(L1[i]))
                            L1[i] = 0
                            
                        stock_del.append(row.stock_no)
                        dis_list.append(L2[i])
    rows = db(db.stock).select()
    
    for i in range(len(stock_del)):
        for row in rows:
            if row.stock_no == stock_del[i]:
                
                q=db.sale.insert(bill_no=str(billcount), date_of_bill=billdate, item_item_no=row.item_item_no, quantity= quantitylist[i],
                                 stock_no=stock_del[i], discount = dis_list[i], cost_price=decimal.Decimal(row.cost_price),
                                 selling_price=decimal.Decimal(row.selling_price))
                db(db.sale.id==q).update(cost_price=((decimal.Decimal(db.sale[q].quantity)) *
                                                  (decimal.Decimal(db.sale[q].cost_price))))
                db(db.sale.id==q).update(selling_price=((decimal.Decimal(db.sale[q].quantity)) *
                                                  (decimal.Decimal(db.sale[q].selling_price))))
                                             
                db(db.sale.id==q).update(final_price=
                                         (
                                         (decimal.Decimal(db.sale[q].selling_price))-
                                         ((decimal.Decimal(db.sale[q].discount))*(decimal.Decimal(db.sale[q].selling_price))
                                          *(decimal.Decimal(0.01)))
                                         )
                                        )
                db(db.sale.id==q).update(profit=
                                         (
                                         (((decimal.Decimal(db.sale[q].final_price)) - 
                                                  (decimal.Decimal(db.sale[q].cost_price)))/
                                                 ((decimal.Decimal(db.sale[q].cost_price)))) *
                                                   ((decimal.Decimal(100)))
                                         )
                                         )
                db(db.sale.id==q).update(loss=
                                         (
                                         (((decimal.Decimal(db.sale[q].cost_price)) - 
                                                  (decimal.Decimal(db.sale[q].final_price)))/
                                                 ((decimal.Decimal(db.sale[q].cost_price)))) *
                                                   ((decimal.Decimal(100)))
                                         )
                                         )
                for row in db(db.sale.id==q).select():
                    if row.loss<0:
                        db(db.sale.id==q).update(loss=0)
                for row in db(db.sale.id==q).select():
                    if row.profit<0:
                        db(db.sale.id==q).update(profit=0)
    return dict()         

@auth.requires_membership('Cashier')
def sale_form():
    rows2 = db().select(db.stock.item_item_no, db.stock.item_item_no.count(),db.stock.quantity.sum(),groupby=db.stock.item_item_no)
    rows1 = db(db.item_details).select()
    return locals()

