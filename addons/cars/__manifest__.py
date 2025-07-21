{
    'name': "Cars Management",
    'version': "1.0",
    'depends': ['base',
                'mail'],
    'author'    : "Fraz Ahmad",
    'category': "Sales",
    'description': "A module to manage car inventory, sales, and profit tracking.",
    'data': [
        'security/ir.model.access.csv',
        'views/car_views.xml',
        'views/car_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}