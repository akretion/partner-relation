# Copyright 2014-2023 Artisanat Monastique de Provence (www.barroux.org)
# Copyright 2015-2023 Akretion France (www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models
from odoo.exceptions import UserError


class ResPartnerRelationType(models.Model):
    _name = "res.partner.relation.type"
    _description = "Partner Relation Type"
    _order = "name"

    name = fields.Char(string="Relation Name", required=True)
    reverse_id = fields.Many2one(
        "res.partner.relation.type",
        string="Reverse Relation Type",
        copy=False,
        help="If the relation type is asymetric, select the corresponding "
        "reverse relation type. For exemple, 'A recommends B' is an "
        "asymetric relation ; it's reverse relation is 'B is recommended "
        "by A'. If the relation type is symetric, leave the field empty. "
        "For example, 'A is a competitor of B' is a symetric relation "
        "because we also have 'B is the competitor of A'.",
    )
    active = fields.Boolean(default=True)

    def _get_reverse_relation_type_id(self):
        self.ensure_one()
        if self.reverse_id:
            return self.reverse_id
        else:
            return self

    @api.model_create_multi
    def create(self, vals_list):
        new = super().create(vals_list)
        for vals in vals_list:
            if vals.get("reverse_id"):
                reverse = self.browse(vals["reverse_id"])
                reverse.with_context(allow_write_reverse_id=True).write(
                    {"reverse_id": new.id}
                )
        return new

    def write(self, vals):
        if "reverse_id" in vals and not self.env.context.get("allow_write_reverse_id"):
            if vals["reverse_id"] != self.reverse_id.id:
                raise UserError(
                    self.env._(
                        "It is not possible to modify the reverse of a relation "
                        "type. You should desactivate or delete this relation "
                        "type and create a new one."
                    )
                )
        return super().write(vals)
