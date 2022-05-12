# -*- coding: utf-8 -*-

from odoo import models,fields, api

class formation(models.Model):

    _name = "estk.formation"
    _description = "formations records"
    _rec_name = "formation"

    formation = fields.Char(string='Nom de la formation', required=True)
    type_formation = fields.Selection([('dut', 'DIPLÔME UNIVERSITAIRE DE TECHNOLOGIE - DUT'),
                                  ('lp', 'LICENCE PROFESSIONNELLE - LP'), ('fc', 'Formation Continue')],
                                  string='Type de la formation', required=True)
    departement_id = fields.Many2one(comodel_name='estk.departement', string='Département de la Formation')
    # filiere_ids = fields.One2many(comodel_name='estk.filiere', inverse_name='formation_id', string='Liste des Filières de la Formation')
    module_ids = fields.One2many(comodel_name='estk.module', inverse_name='formation_id', string='Liste des Modules')


