# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Groupe(models.Model):
    _name = 'estk.groupe'
    _description = 'groupes records'
    _rec_name = 'nom_groupe'

    nom_groupe = fields.Selection([('Groupe 1', 'Groupe 1'),
                                   ('Groupe 2', 'Groupe 2'),
                                   ('Groupe 3', 'Groupe 3'),
                                   ('Groupe 4', 'Groupe 4'),
                                   ('Groupe 5', 'Groupe 5'),
                                   ('Groupe 6', 'Groupe 6'),
                                   ('Groupe 7', 'Groupe 7'),
                                   ('Groupe 8', 'Groupe 8'),
                                   ('Groupe 9', 'Groupe 9'),
                                   ('Groupe 10', 'Groupe 10')], string="Nom du groupe", required=True)
    formation_id = fields.Many2one(comodel_name='estk.formation', string='Filière', required=True)
    semestre_id = fields.Many2one(comodel_name='estk.semestre', string='Semestre', required=True)
    anneeuniversitaire_id = fields.Many2one(comodel_name="estk.anneeuniversitaire", string="Année universitaire", required=True)
    etudiant_ids = fields.Many2many(comodel_name='estk.etudiant', string='Etudiants')
    effectif = fields.Integer(string='Effectif du Groupe', required=True)
    inscriptionpedag_ids = fields.One2many(comodel_name="estk.inscriptionpedag", inverse_name="groupe_id", string="Inscriptions Pédagogiques")
    groupe_complet = fields.Boolean(Default=False, string="Groupe Complet ?")

    # SQL constraints
    _sql_constraints = [('groupe_unique',
                         'UNIQUE(nom_groupe, formation_id, semestre_id, anneeuniversitaire_id)',
                         'ce groupe est déja creé pour cette filière !')]


    # def name_get(self):
    #     result = []
    #     for rec in self:
    #         name = self.nom_groupe+' | '+self.semestre_id.semestre+' | '\
    #                +self.formation_id.formation+' | '\
    #                +self.anneeuniversitaire_id.anneeuniversitaire
    #         result.append((rec.id, name))
    #     return result


    def affectation_etudiants(self):
        if self.groupe_complet == False:
            inscriptionpedags = self.env["estk.inscriptionpedag"].search(
                [("semestre_id.semestre", "=", self.semestre_id.semestre),
                 ("anneeuniversitaire_id.anneeuniversitaire", "=", self.anneeuniversitaire_id.anneeuniversitaire),
                 ("formation_id.formation", "=", self.formation_id.formation), ("affecte_groupe", "=", False)], order="nom asc", limit=self.effectif)
            for i in inscriptionpedags:
                i.update({'affecte_groupe': True,
                          'groupe_id': self})
            self.inscriptionpedag_ids = inscriptionpedags
            for i in inscriptionpedags:
                self.etudiant_ids = self.etudiant_ids | i.etudiant_id
            self.groupe_complet= True

