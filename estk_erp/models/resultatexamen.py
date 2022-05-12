# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class ResultatExamen(models.Model):
    _name = 'estk.resultatexamen'
    _description = 'resultat d\'un examen pour un etudiant'

    examenetudiant_id = fields.Many2one(comodel_name="estk.examenetudiant")
    etudiant_id = fields.Many2one(related="examenetudiant_id.etudiant_id")
    nom = fields.Char(related="etudiant_id.nom", string="Nom")
    prenom = fields.Char(related="etudiant_id.prenom", string="Prenom")
    cne = fields.Char(related="etudiant_id.cne", string="CNE")
    cni = fields.Char(related="etudiant_id.cni", string="CNI")
    appogee = fields.Char(related="etudiant_id.numero_appogee", string="N° Appogée")
    examen_id = fields.Many2one(related="examenetudiant_id.examen_id", string="Element de Module")
    periode = fields.Selection(related="examen_id.session_id.periode", string="Période")
    type_session = fields.Selection(related="examen_id.type_session", string="Session")
    anneeuniversitaire_id = fields.Many2one(related="examen_id.anneeuniversitaire")
    formation = fields.Many2one(related="examen_id.formation")
    semestre_id = fields.Many2one(related="examen_id.semestre")
    numéro_examen = fields.Integer(related="examenetudiant_id.numéro_examen",string="N° de la table")
    elementmodule = fields.Many2one(related="examen_id.elementmodule_id", string="Element de Module")
    note_elementmodule = fields.Float(digits=(2, 2), string="note", default=0)
    observation = fields.Selection([('Validé', 'Validé'), ('Ratt', 'Ratt'), ('Non Validé', 'Non Validé'), ('Validé Ratt', 'Validé Ratt')], string="Observation")
    absent = fields.Boolean(string="Absent(e)", default=False)
    absence_justifié = fields.Boolean(string="Abcence justifié ?", default=False)
    resultatsemestre_id = fields.Many2one(comodel_name="estk.resultatsemestre")

    _sql_constraints = [('note_elementmodule_check', 'CHECK(note_elementmodule>=0 and note_elementmodule<=20)',
                         'La note de l\'élément de module est entre 0 et 20')]
    _sql_constraints = [('resultat_unique', 'UNIQUE(examenetudiant_id, type_session, anneeuniversitaire_id, elementmodule)',
                         'l\'Etudiant ne peut pas avoir deux résultats ou plus pour le meme élément de module dans une session d\'examens')]



    def calculer_note_module(self):
        module = self.elementmodule.module_id.nom
        print(module)
        #max des resultats de element de module du meme année universitaire
        resultats_elements = self.env["estk.resultatexamen"].search([("anneeuniversitaire_id","=", self.anneeuniversitaire_id.id),
                                                               ("elementmodule","=", self.elementmodule.id)])
        res_list = []
        for res in resultats_elements:
            res_list.append(res.note_elementmodule)
        max_res = max(res_list)
        print(max_res)
        other_element = self.env["estk.elementmodule"].search([("module_id", "=", module),
                                                                ("element","!=", self.elementmodule.element)])
        print(other_element.element)

        #max resultat des autres elements du meme module du self (same année universitaire)
        resultats_other_element = self.env["estk.resultatexamen"].search(
            [("anneeuniversitaire_id", "=", self.anneeuniversitaire_id.id),
             ("elementmodule", "=", other_element.id)])
        print(resultats_other_element.note_elementmodule)
        res_list2 = []
        for res2 in resultats_other_element:
            res_list2.append(res2.note_elementmodule)
        max_res2 = max(res_list2)
        print(max_res2)

        elements = self.env["estk.elementmodule"].search([("module_id", "=", module)])

        note = (max_res+max_res2)/len(elements)
        print(note)
        self.env["estk.resultatsemestre"].search([("module", "=", module),
                                                  ("etudiant_id", "=", self.etudiant_id.id)])\
            .update({
            'note_module': note
        })



    @api.onchange('note_elementmodule')
    def on_change_note_element(self):
        if self.type_session == "Normale":
            if self.note_elementmodule<12:
                self.calculer_note_module()
                self.observation="Ratt"

            else:
                self.calculer_note_module()
                self.observation="Validé"

        if self.type_session == "Rattrapage":
            if self.note_elementmodule<12:
                self.calculer_note_module()
                self.observation="Non Validé"

            else:
                self.calculer_note_module()
                self.observation ="Validé Ratt"






    def name_get(self):
        result = []
        for rec in self:
            name = 'Resultat d\'examen pour l\'étudiant '+rec.nom+' '+rec.prenom
            result.append((rec.id, name))
        return result

    # def valider_resultat(self):


