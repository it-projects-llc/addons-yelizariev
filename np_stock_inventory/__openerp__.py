{
    'name' : 'Update fill inventory behavior',
    'version' : '1.0.0',
    'author' : 'IT-Projects LLC, Ivan Yelizariev',
    'category' : 'Stock',
    'website' : 'https://twitter.com/OdooFree',
    'description': """
* In Physical Inventories "Fill inventory" button add only not listed products (by default line for same product is created if quantity are different from stock value)
* add checkbox "inventoried" in stock.inventory.line
    """,
    'depends' : ['stock'],
    'data':[
        'views.xml'
        ],
    'installable': True
}
