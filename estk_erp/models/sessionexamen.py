# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class SessionExamen(models.Model):
    _name = 'estk.sessionexamen'
    _description = 'sessionexamens records'

    #fields
    periode = fields.Selection([('Automne', 'Automne'), ('Printemps', 'Printemps')], string="Période")
    type_session = fields.Selection([('Normale', 'Normale'), ('Rattrapage', 'Rattrapage')], string="Type de la session")
    anneeuniversitaire_id = fields.Many2one(comodel_name='estk.anneeuniversitaire', string="Année Universitaire")
    formation_id = fields.Many2one(comodel_name="estk.formation", string="Formation")
    semestre_id = fields.Many2one(comodel_name="estk.semestre", string="Semestre")
    examen_ids = fields.One2many(comodel_name="estk.examen", inverse_name="session_id", string="Examens")
    session_effectue = fields.Boolean(Default=False, string="Examen ajouté ?")


    #Record Name
    def name_get(self):
        result = []
        for rec in self:
            name = 'session '+rec.periode+' / '+rec.type_session+' | '+rec.semestre_id.semestre+' | A.U : '+rec.anneeuniversitaire_id.anneeuniversitaire
            result.append((rec.id, name))
        return result

    #SQL constraints
    _sql_constraints = [('session_unique',
                         'UNIQUE(type_session, formation_id, semestre_id, anneeuniversitaire_id)',
                         'Une session ne peut pas etre dupliquée pour une filière dans la meme periode d\'examen')]

    def creation_examens(self):
        if self.session_effectue == False:
            modules = self.env["estk.module"].search([("formation_id", "=", self.formation_id.formation), ("semestre_id", "=", self.semestre_id.semestre)])
            elements = modules.elementmodule_ids
            for element in elements:
                self.env["estk.examen"].create({
                    'session_id': self.id,
                    'elementmodule_id': element.id

                })
            self.session_effectue= True

