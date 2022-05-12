# -*- coding: utf-8 -*-

from odoo import models, fields, api
from  datetime import datetime
from dateutil.relativedelta import relativedelta

class Employee(models.Model):
    _name = 'estk.employee'
    _description = 'Employées records'



    #info de l'employée
    nom = fields.Char(string='Nom', required=True)
    prenom = fields.Char(string='Prénom', required=True)
    date_naissance = fields.Date(string='Date de Naissance')
    age = fields.Char(compute="_calculer_age", string="Age")
    fontionalite = fields.Char(string='Fonctionnalité', required=True)
    image = fields.Binary(string="Photo")

    def _calculer_age(self):
        for rec in self:
            age = relativedelta(datetime.now().date(), fields.Datetime.from_string(rec.date_naissance)).years
            rec.age = str(age) + " Ans"


    def name_get(self):
        result = []
        for rec in self:
            name = rec.nom+' '+rec.prenom
            result.append((rec.id, name))
        return result
