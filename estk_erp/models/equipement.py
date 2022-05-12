# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Equipement(models.Model):
    _name = 'estk.equipement'
    _description = 'equipements records'
    _rec_name = "libelle"

    libelle = fields.Char(string="Libelle")
    etat = fields.Selection([("Bonne Etat","Bonne Etat"),("Mauvaise Etat","Mauvaise Etat"),("Etat Neuve","Etat Neuve")], string="Etat")
    nombre = fields.Integer(string="Nombre")
    image = fields.Binary(string="Photo")