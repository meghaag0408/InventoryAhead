# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('INVENTORY AHEAD'),
                  _class="navbar-brand",
                  _id="web2py-logo")
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Megha Agarwal <megha.agarwal@students.iiit.ac.in>'
response.meta.description = 'Inventory Management System of a store'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################


if auth.has_membership('Manager'):
    response.menu = [
          (T('Home'),False,URL('manager','index'),[]), 
         [T('ITEMS').capitalize(),
             False,
             '', 
             [
             [T('Show Items').capitalize(),
                 False,
                 URL(request.application,
                 'manager',
                 'item_show'),
                 [
                     [T('Purchase Reports').capitalize(),
                     False,
                     URL(request.application,
                     'manager',
                     'purchase_insert'),
                     []],
                 ]],
             [T('Edit Items').capitalize(),
                 False,
                 URL(request.application,
                 'manager',
                 'edit_item'),
                 []],
             [T('Delete Items').capitalize(),
                 False,
                 URL(request.application,
                 'manager',
                 'delete_item'),
                 []],
             
         ]],
         (T('Stock'),False,URL('manager', 'stock_details'),[]),
      (T('Purchase'),False,URL('manager', 'purchase_form'),[]), 
     (T('Sale'),False,URL('manager', 'sale_form'),[]),
         [T('reports').capitalize(),
             False,
             '',
             [
                 [T('Purchase Report').capitalize(),
                     False,
                     URL(request.application,
                     'manager',
                     'purchase_insert'),
                     []],
                 [T('Sale Report').capitalize(),
                     False,
                     URL(request.application,
                     'manager',
                     'sale_insert'),
                     []],
         ]],
     
        ]
    
if auth.has_membership('Cashier'):
    response.menu = [
          (T('Home'),False,URL('cashier','index'),[]), 
           (T('Items'),False,URL('cashier','item_show'),[]), 
         (T('Sale'),False,URL('cashier', 'sale_form'),[]),   
           (T('Generate Bill'),False,URL('cashier','bill'),[]), 
        ]

if auth.has_membership('Admin'):
    response.menu = [
          (T('Home'),False,URL('admin','index'),[]), 
         [T('ITEMS').capitalize(),
             False,
             '', 
             [
             [T('Show Items').capitalize(),
                 False,
                 URL(request.application,
                 'admin',
                 'item_show'),
                 [
                     [T('Purchase Reports').capitalize(),
                     False,
                     URL(request.application,
                     'admin',
                     'purchase_insert'),
                     []],
                 ]],
             [T('Edit Items').capitalize(),
                 False,
                 URL(request.application,
                 'admin',
                 'edit_item'),
                 []],
             [T('Delete Items').capitalize(),
                 False,
                 URL(request.application,
                 'admin',
                 'delete_item'),
                 []],
             
         ]],
         (T('Stock'),False,URL('admin', 'stock_details'),[]),
        
      (T('Purchase'),False,URL('admin', 'purchase_form'),[]), 
     (T('Sale'),False,URL('admin', 'sale_form'),[]),
         [T('reports').capitalize(),
             False,
             '',
             [
                 [T('Purchase Report').capitalize(),
                     False,
                     URL(request.application,
                     'admin',
                     'purchase_insert'),
                     []],
                 [T('Sale Report').capitalize(),
                     False,
                     URL(request.application,
                     'admin',
                     'sale_insert'),
                     []],
         ]],
         (T('Add User'),False,URL('admin', 'add_user'),[]),  
           (T('Manage User'),False,URL('admin', 'manage_user'),[]), 
        ]
    

if "auth" in locals(): auth.wikimenu()
