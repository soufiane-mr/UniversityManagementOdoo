# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AnneeUniversitaire(models.Model):

    _name = "estk.anneeuniversitaire"
    _description = "Année Universitaire Records"
    _rec_name = "anneeuniversitaire"

    anneeuniversitaire = fields.Char(string='Année Universitaire', required=True)
    debut = fields.Date(string='date de début')
    fin = fields.Date(string='date de fin')
    année_prochaine = fields.Many2one(comodel_name="estk.anneeuniversitaire", string="Année Universitaire suivante")
    # est_courante = fields.Boolean()