# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class ResultatSemestre(models.Model):
    _name = 'estk.resultatsemestre'
    _description = 'resultat semestre pour un etudiant'

    etudiant_id = fields.Many2one(comodel_name="estk.etudiant", string="etudiant")
    nom = fields.Char(related="etudiant_id.nom", string="Nom")
    prenom = fields.Char(related="etudiant_id.prenom", string="Prenom")
    cne = fields.Char(related="etudiant_id.cne", string="CNE")
    cni = fields.Char(related="etudiant_id.cni", string="CNI")
    anneeuniversitaire = fields.Many2one(comodel_name="estk.anneeuniversitaire", string="Année Universitaire")
    semestre = fields.Many2one(comodel_name="estk.semestre", string="Semestre")
    session = fields.Char(string="Session")
    type_session = fields.Char(string="Type de session")
    module = fields.Many2one(comodel_name="estk.module", string="Module")
    note_module = fields.Float(digits=(2, 2), string="note", default=0)
    observation = fields.Selection(
        [('Validé', 'Validé'), ('Non Validé', 'Non Validé')],
        string="Observation")




    def name_get(self):
        result = []
        for rec in self:
            name = 'Resultat du Semestre pour l\'étudiant '+rec.nom+' '+rec.prenom
            result.append((rec.id, name))
        return result



    def calculer_note_semestre(self):
        #notes des module de cet etudiant dans le meme semestre et la meme année universitaire
        notes_modules = self.env["estk.resultatsemestre"].search([("etudiant_id","=", self.etudiant_id.id),
                                                                  ("semestre","=", self.semestre.id),
                                                                  ("anneeuniversitaire","=", self.anneeuniversitaire.id)])
        nbr_modules = self.env["estk.inscriptionpedag"].search([("etudiant_id","=", self.etudiant_id.id),
                                                                  ("semestre_id","=", self.semestre.id),
                                                                  ("anneeuniversitaire_id","=", self.anneeuniversitaire.id)]).module_ids
        somme=0
        for note in notes_modules:
            somme=somme+note.note_module
        note_sem=somme/len(nbr_modules)

        print(note_sem)
        self.env["estk.resultatannuel"].search([("etudiant_id", "=", self.etudiant_id.id),
                                                  ("anneeuniversitaire", "=", self.anneeuniversitaire.id),
                                                ("semestre", "=", self.semestre.semestre)]) \
            .update({
            'note_semestre': note_sem
        })



    @api.onchange('note_module')
    def on_change_note_module(self):
         if self.note_module < 12:
            self.observation = "Non Validé"
         else:
            self.observation = "Validé"

