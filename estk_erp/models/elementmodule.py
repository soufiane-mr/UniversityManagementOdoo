# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ElementModule(models.Model):
    _name = "estk.elementmodule"
    _description = "element de module"
    _rec_name = "element"

    element = fields.Char('Intitulé de l\'élément', required=True)
    note = fields.Float(digits=(2, 2))
    module_id = fields.Many2one(comodel_name="estk.module", string="Module")
    # element_formation = fields.Char(related="module_id.formation_id")
    # element_semestre = fields.Char(related="module_id.semestre_id")

