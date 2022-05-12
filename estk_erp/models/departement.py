# -*- coding: utf-8 -*-

from odoo import models,fields, api

class departement(models.Model):
    _name = 'estk.departement'
    _description = 'departements records'
    _rec_name = "departement"


    departement = fields.Char(string='Nom du département', required=True)
    formation_ids = fields.One2many('estk.formation', inverse_name='departement_id', string='Formations du Département')
    prefesseur_ids = fields.One2many('estk.professeur', inverse_name='departement_id', string='Profresseurs du département')
    professeur_id = fields.Many2one('estk.professeur', 'Chef du Département')
