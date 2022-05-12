# -*- coding: utf-8 -*-

from odoo import models, fields, api

class InscriptionAdministrative(models.Model):
    _name = "estk.inscriptionadmin"
    _description = "Inscription Administrative Rescord"


    etudiant_id = fields.Many2one(comodel_name="estk.etudiant", string="Etudiant")
    nom = fields.Char(related="etudiant_id.nom", string='Nom')
    prenom = fields.Char(related="etudiant_id.prenom", string='Prénom')
    cne = fields.Char(related="etudiant_id.cne", string='CNE')
    numappogee = fields.Char(related="etudiant_id.numero_appogee",string='N° APPOGEE')
    anneeuniversitaire_id = fields.Many2one(comodel_name="estk.anneeuniversitaire", string="Année Universitaire")
    formation_id = fields.Many2one(comodel_name="estk.formation", string="Formation")
    typeformation = fields.Selection(related='formation_id.type_formation', string='type de formation')
    etape_id = fields.Many2one(comodel_name="estk.etape", string="Etape")
    inscriptionpedag_effectuee = fields.Boolean(Default=False, string="Inscriptions Pedagogiques Effectuées ?")


    # contraints SQL
    _sql_constraints = [
        ('inscription_admin_unique', 'UNIQUE(etudiant_id, etape_id)', 'Un etudiant ne peut pas avoir deux ou plus une inscription administrative dans une meme etape')]





    def créer_inscription_pedag(self):
        if self.inscriptionpedag_effectuee== False:
            semestre1 = self.env["estk.semestre"].search([("semestre", "=", "s1")]).id
            semestre2 = self.env["estk.semestre"].search([("semestre", "=", "s2")]).id
            semestre3 = self.env["estk.semestre"].search([("semestre", "=", "s3")]).id
            semestre4 = self.env["estk.semestre"].search([("semestre", "=", "s4")]).id

            modules_s1 = self.env["estk.module"].search([("semestre_id.semestre", "=", "s1"), ("formation_id.formation", "=", self.formation_id.formation)])
            modules_s2 = self.env["estk.module"].search([("semestre_id.semestre", "=", "s2"), ("formation_id.formation", "=", self.formation_id.formation)])
            modules_s3 = self.env["estk.module"].search([("semestre_id.semestre", "=", "s3"), ("formation_id.formation", "=", self.formation_id.formation)])
            modules_s4 = self.env["estk.module"].search([("semestre_id.semestre", "=", "s4"), ("formation_id.formation", "=", self.formation_id.formation)])

            etudiant = self.env["estk.etudiant"].search([("cne", "=", self.etudiant_id.cne)])

            annee = self.env["estk.anneeuniversitaire"].search([("anneeuniversitaire", "=", self.anneeuniversitaire_id.anneeuniversitaire)])

            if self.etape_id.etape == "1ère Année":
                 self.env["estk.inscriptionpedag"].create({
                    'etudiant_id': etudiant.id,
                    'nom': etudiant.nom,
                    'cne': etudiant.cne,
                    'numappogee': etudiant.numero_appogee,
                    'anneeuniversitaire_id': annee.id,
                    'semestre_id': semestre1,
                    'formation_id': self.formation_id.id,
                    'module_ids': modules_s1,
                    'elementmodule_ids': modules_s1.elementmodule_ids
                 })
                 self.env["estk.inscriptionpedag"].create({
                    'etudiant_id': etudiant.id,
                    'nom': etudiant.nom,
                    'cne': etudiant.cne,
                    'numappogee': etudiant.numero_appogee,
                    'anneeuniversitaire_id': annee.id,
                     'semestre_id': semestre2,
                     'formation_id': self.formation_id.id,
                    'module_ids': modules_s2,
                    'elementmodule_ids': modules_s2.elementmodule_ids
                 })
                 self.inscriptionpedag_effectuee=True
            if self.etape_id.etape == '2ème Année':
                self.env["estk.inscriptionpedag"].create({
                    'etudiant_id': etudiant.id,
                    'nom': etudiant.nom,
                    'cne': etudiant.cne,
                    'numappogee': etudiant.numero_appogee,
                    'anneeuniversitaire_id': annee.id,
                    'semestre_id': semestre3,
                    'formation_id': self.formation_id.id,
                    'module_ids': modules_s3,
                    'elementmodule_ids': modules_s3.elementmodule_ids
                })
                self.env["estk.inscriptionpedag"].create({
                    'etudiant_id': etudiant.id,
                    'nom': etudiant.nom,
                    'cne': etudiant.cne,
                    'numappogee': etudiant.numero_appogee,
                    'anneeuniversitaire_id': annee.id,
                    'semestre_id': semestre4,
                    'formation_id': self.formation_id.id,
                    'module_ids': modules_s4,
                    'elementmodule_ids': modules_s4.elementmodule_ids
                })
                self.inscriptionpedag_effectuee = True







    def name_get(self):
        result = []
        for rec in self:
            name = 'Inscription Administrative pour l\'étudiant '+self.etudiant_id.nom+' '+self.etudiant_id.prenom+' | A.U :'+self.anneeuniversitaire_id.anneeuniversitaire
            result.append((rec.id, name))
        return result