# © 2015-2023 Akretion France (www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase


class TestPartnerRelation(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.rprt = cls.env['res.partner.relation.type']
        cls.rpr = cls.env['res.partner.relation']
        # Create a symetric relation type
        cls.friend_of = cls.rprt.create({'name': 'Friend of'})
        # Create an asymetric relation type
        cls.parent_of = cls.rprt.create({'name': 'Parent of'})
        # Create the reverse of the asymetric relation type
        cls.child_of = cls.rprt.create({
            'name': 'Child of',
            'reverse_id': cls.parent_of.id,
            })

        # Create a symetric relation
        cls.friend1 = cls.rpr.create({
            'src_partner_id': cls.env.ref('base.res_partner_address_1').id,
            'relation_type_id': cls.friend_of.id,
            'dest_partner_id': cls.env.ref('base.res_partner_address_10').id,
            })
        # Create asymetric relation
        cls.parent1 = cls.rpr.create({
            'src_partner_id': cls.env.ref('base.res_partner_address_11').id,
            'relation_type_id': cls.parent_of.id,
            'dest_partner_id': cls.env.ref('base.res_partner_address_13').id,
            })

    def test_relation(self):
        # Check the creation of the asymetric relation
        self.assertEqual(self.parent_of.reverse_id, self.child_of)
        # Check symetric and asymetric relations
        friend_rels = self.rpr.search(
            [('relation_type_id', '=', self.friend_of.id)])
        self.assertEqual(len(friend_rels), 2)
        self.assertEqual(
            friend_rels[0].src_partner_id.id,
            friend_rels[1].dest_partner_id.id)
        self.assertEqual(
            friend_rels[1].src_partner_id.id,
            friend_rels[0].dest_partner_id.id)
        parent_rels = self.rpr.search(
            [('relation_type_id', '=', self.parent_of.id)])
        self.assertEqual(len(parent_rels), 1)
        child_rels = self.rpr.search(
            [('relation_type_id', '=', self.child_of.id)])
        self.assertEqual(len(child_rels), 1)
        self.assertEqual(
            child_rels[0].src_partner_id,
            self.env.ref('base.res_partner_address_13'))
        self.assertEqual(
            child_rels[0].dest_partner_id,
            self.env.ref('base.res_partner_address_11'))

    def test_write(self):
        friend_rels = self.rpr.search(
            [('relation_type_id', '=', self.friend_of.id)], order='id')
        # Reverse rel should be created before relation
        self.assertEqual(friend_rels[1], self.friend1)
        self.friend1.write({
            'relation_type_id': self.env.ref('partner_relation.recommends').id,
            'dest_partner_id': self.env.ref('base.res_partner_address_15').id,
            })
        friend1_rel = friend_rels[1]
        friend1_inv_rel = friend_rels[0]
        self.assertEqual(
            friend1_rel.relation_type_id,
            self.env.ref('partner_relation.recommends'))
        self.assertEqual(
            friend1_rel.src_partner_id,
            self.env.ref('base.res_partner_address_1'))
        self.assertEqual(
            friend1_rel.dest_partner_id,
            self.env.ref('base.res_partner_address_15'))
        self.assertEqual(
            friend1_inv_rel.relation_type_id,
            self.env.ref('partner_relation.is_recommended_by'))
        self.assertEqual(
            friend1_inv_rel.src_partner_id,
            self.env.ref('base.res_partner_address_15'))
        self.assertEqual(
            friend1_inv_rel.dest_partner_id,
            self.env.ref('base.res_partner_address_1'))

    def test_delete(self):
        self.parent1.unlink()
        child_rels = self.rpr.search(
            [('relation_type_id', '=', self.child_of.id)])
        self.assertEqual(len(child_rels), 0)
