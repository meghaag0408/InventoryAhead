# -*- coding: utf-8 -*-
# try something like
POSTS_PER_PAGE = 10
import datetime
import decimal
import math
@auth.requires_membership('Manager')
def index(): 
    return dict()

@auth.requires_membership('Manager')
def item_show():
    rows = db(db.item_details).select()
    return locals()

@auth.requires_membership('Manager')
def edit_item():
    rows2 = db(db.item_details).select()
    return locals()

@auth.requires_membership('Manager')
def delete_item():
    rows = db(db.item_details).select()
    return locals()

@auth.requires_membership('Manager')
def delete_item2():
    item = request.vars.item_no
    db(db.item_details.item_no == item).delete()
    return locals()


@auth.requires_membership('Manager')
def edit_item2():
    L1= request.vars.item_no
    L2 = request.vars.item_name
    rows = db(db.item_details).select()
    i=0
    for row in rows:
        db(db.item_details.id==row.id).update(item_no=L1[i])
        db(db.item_details.id==row.id).update(item_name=L2[i])
        i+=1  
    rows = db(db.item_details).select()
    return locals()


@auth.requires_membership('Manager')
def stock_details():
    rows = db(db.stock).select()
    return locals()

@auth.requires_membership('Manager')
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
    flag=0
    for i in range(len(L1)):
        if not L1[i]:
            L1[i]=0
        else:
            flag=1
    if flag==0:
        session.flash="Enter valid quantity"
        redirect(URL('manager','sale_form'))
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

@auth.requires_membership('Manager')
def create_stock():
    rows=db(db.purchase).select()
    rowstock=db(db.stock).select()
    stockl = []
    for row in rowstock:
        stockl.append(row.purchase_no)
    for row in rows:
        if row.delivered_on<=datetime.datetime.now():
            if row.purchase_no not in stockl:
                p=db.stock.insert(item_item_no=row.item_item_no,purchase_no=row.purchase_no,
                  quantity=row.quantity, cost_price=row.cost_price,selling_price=row.selling_price,
                  stocked_on=datetime.datetime.now()) 
                db(db.stock.id==p).update(stock_no=p+1000)
                stockl.append(row.purchase_no)
    return locals()
@auth.requires_membership('Manager')
def purchase_form():
    db.purchase.ordered_on.default=datetime.datetime.now()
    db.purchase.delivered_on.default=datetime.datetime.now()+datetime.timedelta(minutes=10)
    rows = SQLFORM(db.purchase).process()
    if rows.accepted:
        session.flash = 'form accepted'
        redirect(URL('manager','index'))
    elif rows.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return locals()

@auth.requires_membership('Manager')
def sale_form2():
    form = SQLFORM(db.sale).process()
    return locals()

@auth.requires_membership('Manager')
def purchase_report():
    day = request.vars.date
    rows = db(db.purchase).select()
    L = []
    for row in rows:
        if str(row.delivered_on.date())==day:
            L.append(row)
    return locals()

@auth.requires_membership('Manager')
def sale_report():
    day = request.vars.date
    rows = db(db.sale).select()
    L = []
    for row in rows:
        if str(row.date_of_bill.date())==day:
            L.append(row)
    return locals()

@auth.requires_membership('Manager')
def purchase_insert():
    rows = db(db.purchase).select()
    L = []
    for row in rows:
        if row.delivered_on.date() not in L:
            L.append(row.delivered_on.date())
    return locals()

@auth.requires_membership('Manager')
def sale_insert():
    rows = db(db.sale).select()
    L = []
    for row in rows:
        if row.date_of_bill.date() not in L:
            L.append(row.date_of_bill.date())
    return locals()

@auth.requires_membership('Manager')
def sale_form():
    rows2 = db().select(db.stock.item_item_no, db.stock.item_item_no.count(),db.stock.quantity.sum(),groupby=db.stock.item_item_no)
    rows1 = db(db.item_details).select()
    return locals()
