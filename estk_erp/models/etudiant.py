# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Professeur(models.Model):
    _name = 'estk.etudiant'
    _description = 'etudiant records'
    _inherit = 'mail.thread'




    #info de l'etudiant
    nom = fields.Char(string='Nom', required=True, track_visibility=True)
    prenom = fields.Char(string='Prénom', required=True, track_visibility=True)
    cni = fields.Char(string='CNI', required=True, track_visibility=True)
    cne = fields.Char(string='CNE', required=True, track_visibility=True)
    numero_appogee = fields.Char(string="N° Appogée", required=True, track_visibility=True)
    genre = fields.Selection([('feminin', 'feminin'), ('masculin', 'masculin')], track_visibility=True)
    date_naissance = fields.Date(string='Date de Naissance', track_visibility=True)
    ville_naissance = fields.Char(string='Ville de Naissance', track_visibility=True)
    nationalite = fields.Many2one('res.country', string='Nationalité', track_visibility=True)
    inscriptionadmin_ids = fields.One2many(comodel_name="estk.inscriptionadmin", inverse_name="etudiant_id", string='Inscriptions Administratives')
    inscriptionpeda_ids = fields.One2many(comodel_name="estk.inscriptionpedag", inverse_name="etudiant_id", string='Inscriptions Pédagogiques')
    examenetudiant_ids = fields.One2many(comodel_name="estk.examenetudiant", inverse_name="etudiant_id", string='Inscriptions Aux Examens')
    resultatexamens_ids = fields.One2many(comodel_name="estk.resultatexamen", inverse_name="etudiant_id", string='Résultats des Examens')
    resultatsemestres_ids = fields.One2many(comodel_name="estk.resultatsemestre", inverse_name="etudiant_id", string='Résultats de Semestres')
    resultatannuels_ids = fields.One2many(comodel_name="estk.resultatannuel", inverse_name="etudiant_id", string='Résultats Annuels')


    #inscriptions administratifs (inclu actuelle)
    #inscriptions pedagogiques (inclu actuelle)
    #groupes (inclu actuel)


     #definition de la fonction name_get
    def name_get(self):
        result = []
        for rec in self:
            name = rec.nom+' '+rec.prenom
            result.append((rec.id, name))
        return result

    # fonction pour calculer l'age de l'etudiant
    def _calculer_age(self):
        for rec in self:
            age = relativedelta(datetime.now().date(), fields.Datetime.from_string(rec.date_naissance)).years
            rec.age = str(age) + " Ans"
    age = fields.Char(string='Age', compute='_calculer_age')


    #contraints SQL
    _sql_constraints = [('cni_unique', 'UNIQUE(cni)', 'Le Code d\'Identité Nationale de l\'étudiant ne peut pas etre dupliqué'),
                        ('cne_unique', 'UNIQUE(cne)', 'Le Code Nationale de l\'étudiant ne peut pas etre dupliqué'),
                        ('numero_appogee_unique', 'UNIQUE(numero_appogee)', 'Le Numéro d\'appogée de l\'étudiant ne peut pas etre dupliqué')]

    def imprimer_attestation(self):
        return {'type': 'ir.actions.act_window',
                'res_model': 'estk.imprimer.attestation.inscription.wizard',
                'view_mode': 'form',
                'target': 'new'}