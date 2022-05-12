# -*- coding: utf-8 -*-

from odoo import models, fields


class etape(models.Model):
    _name = "estk.etape"
    _description = "etapes records"
    _rec_name = "etape"

    etape = fields.Selection([('1ère Année', '1ère Année'), ('2ème Année', '2ème Année')], string="Etape", required=True)
    semstre_ids = fields.One2many('estk.semestre', inverse_name='etape_id', string='Les Semestres de L\'étape')
    # anneeuniversitaire_ids = fields.Many2many('estk.anneeuniversitaire', string="Années Universitaires")