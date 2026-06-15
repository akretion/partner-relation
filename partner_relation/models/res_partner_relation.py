# Copyright 2014-2023 Artisanat Monastique de Provence (www.barroux.org)
# Copyright 2015-2023 Akretion France (www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models
from odoo.exceptions import UserError


class ResPartnerRelation(models.Model):
    _name = 'res.partner.relation'
    _description = 'Partner Relation'

    src_partner_id = fields.Many2one(
        'res.partner', string='Source Partner', required=True)
    relation_type_id = fields.Many2one(
        'res.partner.relation.type', string='Relation Type', required=True)
    dest_partner_id = fields.Many2one(
        'res.partner', string='Destination Partner', required=True)

    _sql_constraints = [(
        'src_dest_partner_relation_uniq',
        'unique(src_partner_id, dest_partner_id, relation_type_id)',
        'This relation already exists!'
        )]

    @api.model_create_multi
    def create(self, vals_list):
        '''When a user creates a relation, Odoo creates the reverse
        relation automatically'''
        reverse_vals_list = []
        for vals in vals_list:
            assert vals.get('relation_type_id'), 'relation_type_id is required'
            rel_type = self.env['res.partner.relation.type'].browse(
                vals['relation_type_id'])
            reverse_rel_type = rel_type._get_reverse_relation_type_id()
            reverse_vals_list.append({
                'relation_type_id': reverse_rel_type.id,
                'src_partner_id': vals['dest_partner_id'],
                'dest_partner_id': vals['src_partner_id'],
                })

        # Create reverse relation
        super().create(reverse_vals_list)
        return super().create(vals_list)

    def _get_reverse_relation(self):
        self.ensure_one()
        reverse_rel_type = self.relation_type_id.\
            _get_reverse_relation_type_id()
        reverse_rels = self.search([
            ('src_partner_id', '=', self.dest_partner_id.id),
            ('dest_partner_id', '=', self.src_partner_id.id),
            ('relation_type_id', '=', reverse_rel_type.id)
            ])
        assert len(reverse_rels) == 1, \
            'A relation always has one reverse relation'
        return reverse_rels

    def unlink(self):
        '''When a user deletes a relation, Odoo deletes the reverse
        relation automatically'''
        relations = self
        for relation in self:
            reverse_rel = relation._get_reverse_relation()
            if reverse_rel not in self:
                relations |= reverse_rel
        return super(ResPartnerRelation, relations).unlink()

    def write(self, vals):
        '''When a user writes on a relation, we also have to update
        the reverse relation'''
        reverse_relations = self.browse(False)
        for relation in self:
            reverse_rel = relation._get_reverse_relation()
            if reverse_rel in self:
                raise UserError(self.env._(
                    "You cannot write the same values on the relation "
                    "and it's reverse relation."))
            assert reverse_rel not in reverse_relations, \
                "Impossible: it's relation has it's own reverse relation."
            reverse_relations |= reverse_rel
        reverse_vals = {}
        if 'src_partner_id' in vals:
            reverse_vals['dest_partner_id'] = vals['src_partner_id']
        if 'dest_partner_id' in vals:
            reverse_vals['src_partner_id'] = vals['dest_partner_id']
        if 'relation_type_id' in vals:
            rel_type = self.env['res.partner.relation.type'].browse(
                vals['relation_type_id'])
            reverse_vals['relation_type_id'] = \
                rel_type._get_reverse_relation_type_id().id
        super(ResPartnerRelation, reverse_relations).write(
            reverse_vals)
        return super().write(vals)

    def go_to_dest_partner(self):
        self.ensure_one()
        action = {
            'name': self.env['res.partner']._description,
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_mode': 'form,list,kanban',
            'target': 'current',
            'res_id': self.dest_partner_id.id,
            }
        return action
