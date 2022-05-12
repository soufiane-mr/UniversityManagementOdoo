#-*- coding: utf-8 -*-
{
    'name': "ESTK Erp Core",

    'summary': " Un Module de base qui permet la gestion de l'EST de Kénitra",

    'description': """
        Long description of module's purpose
    """,

    'author': "SOUFIANE MTER",
    'website': "http://www.est.uit.ac.ma",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Educational',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/menus.xml',
        'views/departement_view.xml',
        'views/formation_view.xml',
        'views/professeur_view.xml',
        'views/module_view.xml',
        'views/elementmodule_view.xml',
        'views/etape_view.xml',
        'views/semestre_view.xml',
        'views/anneeuniversitaire_view.xml',
        'views/etudiant_view.xml',
        'views/inscriptionadministrative_view.xml',
        'views/inscriptionpedagogique_view.xml',
        'views/sessionexamen_view.xml',
        'views/groupe_view.xml',
        'views/examen_view.xml',
        'views/examenetudiant_view.xml',
        'views/salle_view.xml',
        'views/resultatexamen_view.xml',
        'views/employee_view.xml',
        'views/equipement_view.xml',
        'views/resultatsemestre_view.xml',
        'views/resultatannuel_view.xml'
        #'views/templates.xml',
        #'views/openacademyviews.xml',
        #'views/menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'application': True,
}