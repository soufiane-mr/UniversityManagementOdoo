# -*- coding: utf-8 -*-

from odoo import models, fields, api

class InscriptionPedagogique(models.Model):
    _name = "estk.inscriptionpedag"
    _description = "Inscription Pedagogique Rescord"

    etudiant_id = fields.Many2one(comodel_name="estk.etudiant", string="Etudiant")
    nom = fields.Char(related="etudiant_id.nom", string='Nom')
    prenom = fields.Char(related="etudiant_id.prenom", string='Prénom')
    cne = fields.Char(related="etudiant_id.cne", string='CNE')
    numappogee = fields.Char(related="etudiant_id.numero_appogee", string='N° APPOGEE')
    anneeuniversitaire_id = fields.Many2one(comodel_name="estk.anneeuniversitaire", string="Année Universitaire")
    semestre_id = fields.Many2one(comodel_name="estk.semestre", string="Semestre")
    formation_id = fields.Many2one(comodel_name="estk.formation", string="Formation")
    module_ids = fields.Many2many(comodel_name="estk.module", string = "Modules")
    elementmodule_ids = fields.Many2many(comodel_name="estk.elementmodule", string="Elements de Modules")
    affecte_groupe = fields.Boolean(string="Affecté a un groupe", Default=False)
    groupe_id = fields.Many2one(comodel_name="estk.groupe", string="groupe")



    def name_get(self):
        result = []
        for rec in self:
            name = 'Inscription Pédagogique pour l\'étudiant '+self.etudiant_id.nom+' '+self.etudiant_id.prenom+' | '+self.cne
            result.append((rec.id, name))
        return result

    _sql_constraints = [('etudiant_id_semestre_id_unique', 'UNIQUE(etudiant_id, semestre_id)',
                         'l\'Etudiant ne peut pas avoir deux inscriptions pédagogiques ou plus dans un meme semestre')]



