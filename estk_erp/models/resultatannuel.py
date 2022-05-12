# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class ResultatAnnuel(models.Model):
    _name = 'estk.resultatannuel'
    _description = 'resultat annuel pour un etudiant'


    etudiant_id = fields.Many2one(comodel_name="estk.etudiant", string="Etudiant")
    nom = fields.Char(related="etudiant_id.nom", string="Nom")
    prenom = fields.Char(related="etudiant_id.prenom", string="Prenom")
    cne = fields.Char(related="etudiant_id.cne", string="CNE")
    cni = fields.Char(related="etudiant_id.cni", string="CNI")
    appogee = fields.Char(related="etudiant_id.numero_appogee", string="N° Appogée")
    anneeuniversitaire = fields.Many2one(comodel_name="estk.anneeuniversitaire", string="Année Universitaire")
    semestre = fields.Many2one(comodel_name="estk.semestre", string="Semestre")
    note_semestre = fields.Float(digits=(2, 2), string="note", default=0)
    observation = fields.Selection([('Validé', 'Validé'), ('Non Validé', 'Non Validé')],string="Observation")




    def name_get(self):
        result = []
        for rec in self:
            name = 'Resultat Annuel pour l\'étudiant '+rec.nom+' '+rec.prenom
            result.append((rec.id, name))
        return result
