{
    'name': "Cars Management",
    'version': "17.0.1.0.0",
    'depends': ['base',
                'mail'],
    'author'    : "Fraz Ahmad",
    'license': "GPL-3",
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