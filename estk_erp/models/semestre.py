# -*- coding: utf-8 -*-

from odoo import models, fields

class semestre(models.Model):
    _name = "estk.semestre"
    _description = "semestres records"
    _rec_name = "semestre"

    semestre = fields.Selection([('s1', 'Semestre 1 - S1'), ('s2', 'Semestre 2 - S2'), ('s3', 'Semestre 3 - S3'),
                                 ('s4', 'Semestre 4 - S4'), ('s5', 'Semestre 5 - S5'), ('s6', 'Semestre 6 - S6')],
                                string="Semestre", required=True)
    etape_id = fields.Many2one('estk.etape', string='L\'étape du Semestre')
    module_ids = fields.One2many('estk.module', inverse_name='semestre_id', string='Les Modules du Semestre')