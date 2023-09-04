# Copyright 2014-2023 Artisanat Monastique de Provence (www.barroux.org)
# Copyright 2015-2023 Akretion France (www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Partner Relation',
    'version': '16.0.1.0.0',
    'category': 'Partner',
    'license': 'AGPL-3',
    'summary': 'Manage relations between partners',
    'author': 'Barroux Abbey, Akretion',
    'website': 'https://github.com/akretion/partner-relation',
    'depends': ['contacts'],
    'data': [
        'partner_relation_view.xml',
        'security/ir.model.access.csv',
        ],
    'demo': [
        'partner_relation_demo.xml',
        ],
    'installable': True,
}
