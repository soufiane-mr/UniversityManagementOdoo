# -*- coding: utf-8 -*-

from odoo import models, fields


class module(models.Model):
    _name = "estk.module"
    _description = 'Modules records'
    _rec_name = "nom"

    nom = fields.Char(string="Intitulé du module", required=True)
    formation_id = fields.Many2one(comodel_name="estk.formation", string='Formation du Module')
    semestre_id = fields.Many2one(comodel_name="estk.semestre", string='Semestre du Module')
    elementmodule_ids = fields.One2many(comodel_name="estk.elementmodule", inverse_name="module_id", string="Les éléments du module")
    note = fields.Float(digits=(2, 2), compute="calculer_note_module")
    correspondant = fields.Many2one(comodel_name="estk.module", string='correspoondant')
    #professeurs_ids = fields.Many2many('estk.professeur', string='Professeurs du module')



    #calculer la note d'un module a partir des notes de ses elements de module
    def calculer_note_module(self):
        total1 = len(self.elementmodule_ids)
        total2 = 0
        for element in self.elementmodule_ids:
            total2 = total2+element.note
        return total2/total1

