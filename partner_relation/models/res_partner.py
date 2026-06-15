# Copyright 2014-2023 Artisanat Monastique de Provence (www.barroux.org)
# Copyright 2015-2023 Akretion France (www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    relation_ids = fields.One2many(
        'res.partner.relation', 'src_partner_id', string='Partner Relations')
