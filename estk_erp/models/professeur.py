# -*- coding: utf-8 -*-

from odoo import models, fields, api
from  datetime import datetime
from dateutil.relativedelta import relativedelta

class Professeur(models.Model):
    _name = 'estk.professeur'
    _description = 'Professeurs records'



    #info du professeur
    nom = fields.Char(string='Nom', required=True)
    prenom = fields.Char(string='Prénom', required=True)
    image = fields.Binary(string="Photo")
    date_naissance = fields.Date(string='Date de Naissance')

    def _calculer_age(self):
        for rec in self:
            age = relativedelta(datetime.now().date(), fields.Datetime.from_string(rec.date_naissance)).years
            rec.age = str(age) + " Ans"
    age = fields.Char(string='Age', compute='_calculer_age')
    departement_id = fields.Many2one(comodel_name='estk.departement', string='Département')
    elementmodule_ids = fields.Many2many(comodel_name='estk.elementmodule', string='Matières')

    def name_get(self):
        result = []
        for rec in self:
            name = rec.nom+' '+rec.prenom
            result.append((rec.id, name))
        return result
