{
    'name': 'Estate',
    'version': '17.0.1.0.0',
    'license': "GPL-3",
    'depends': [
        'base',
    ],
    'installable': True,
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menus.xml'
    ]
}