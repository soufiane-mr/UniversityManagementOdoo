# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Salle(models.Model):
    _name = 'estk.salle'
    _description = 'salle records'
    _rec_name = "nom_salle"

    nom_salle = fields.Char(string="Nom de la salle")
    capacite_cours = fields.Integer(string="Capacité pour les cours")
    capacite_examens = fields.Integer(string="Capacité poue les examens")