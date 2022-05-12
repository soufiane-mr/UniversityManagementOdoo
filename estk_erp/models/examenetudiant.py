# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class ExamenEtudiant(models.Model):
    _name = 'estk.examenetudiant'
    _description = 'examens de l\'etudiant records'

    etudiant_id = fields.Many2one(comodel_name="estk.etudiant", string="Inscription Pedagogique de")
    nom = fields.Char(related="etudiant_id.nom", string="Nom")
    prenom = fields.Char(related="etudiant_id.prenom", string="Prenom")
    cne = fields.Char(related="etudiant_id.cne", string="CNE")
    cni = fields.Char(related="etudiant_id.cni", string="CNI")
    appogee = fields.Char(related="etudiant_id.numero_appogee", string="N° Appogée")
    examen_id = fields.Many2one(comodel_name="estk.examen", string="Element de Module")
    periode = fields.Selection(related="examen_id.session_id.periode", string="Période")
    type_session = fields.Selection(related="examen_id.type_session", string="Session")
    anneeuniversitaire_id = fields.Many2one(related="examen_id.anneeuniversitaire")
    formation = fields.Many2one(related="examen_id.formation")
    semestre_id = fields.Many2one(related="examen_id.semestre")
    elementmodule = fields.Many2one(related="examen_id.elementmodule_id", string="Element de Module")
    salle_id = fields.Many2one(comodel_name="estk.salle", string="Local",)
    numéro_examen = fields.Integer(string="N° de la table")

    _sql_constraints = [('examen_etudiant_unique', 'UNIQUE(etudiant_id, examen_id)',
                          'un etudiant ne peut pas etre inscrit deux fois ou plus dans le meme examen dans une session d\'examens')]




    def name_get(self):
        result = []
        for rec in self:
            name = 'session '+rec.periode+' / '+rec.type_session+' | '+rec.semestre_id.semestre+' | A.U : '+rec.anneeuniversitaire_id.anneeuniversitaire
            result.append((rec.id, name))
        return result


