# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

from datetime import datetime
from dateutil.relativedelta import relativedelta

class Examen(models.Model):
    _name = 'estk.examen'
    _description = 'examens records'

    session_id = fields.Many2one(comodel_name="estk.sessionexamen", string="Session")
    periode = fields.Selection(related="session_id.periode")
    type_session = fields.Selection(related="session_id.type_session")
    anneeuniversitaire = fields.Many2one(related="session_id.anneeuniversitaire_id")
    formation = fields.Many2one(related="session_id.formation_id")
    semestre = fields.Many2one(related="session_id.semestre_id")
    elementmodule_id = fields.Many2one(comodel_name="estk.elementmodule", string="Element de Module")
    date = fields.Datetime(string="Date et Heure")
    duree = fields.Selection([('1h00', '1h00'), ('1h30', '1h30'), ('2h00', '2h00'),
                              ('2h30', '2h30'), ('3h00', '3h00'), ('3h30', '3h30'), ('4h00', '4h00')], string="Durée")
    salle_ids = fields.Many2many(comodel_name="estk.salle", string="Salles")
    effecter_etudiants_aux_examens = fields.Boolean(Default=False, string="Etudiants affectés ?")

    # Record Name
    def name_get(self):
        result = []
        for rec in self:
            name = 'examen ' + rec.elementmodule_id.element + ' / session ' + rec.type_session +' | A.U : ' + rec.anneeuniversitaire.anneeuniversitaire
            result.append((rec.id, name))
        return result

    _sql_constraints = [('examen_unique',
                         'UNIQUE(session_id, elementmodule_id, anneeuniversitaire)',
                         'Un examen ne peut pas etre dupliquée dans une session')]

    def inscriptions_examens(self):
        if not self.salle_ids:
            raise exceptions.ValidationError("ajouter les locaux pour cet examen pour effectuer l'inscription des etudiants")
        else:
            if self.type_session=="Normale":
                salles = [] #liste des salles reserverées pour l'examen
                for salle in self.salle_ids:
                    salles.append(salle)
                nbr_places=0 # le nombre des places pour l'examen
                for salle in self.salle_ids:
                    nbr_places = nbr_places + salle.capacite_examens

                elements_tab = []
                elements_tab.append(self.elementmodule_id.element)

                etudiants = self.env["estk.inscriptionpedag"].search(
                        [("anneeuniversitaire_id", "=", self.anneeuniversitaire.anneeuniversitaire),
                         ("formation_id", "=", self.formation.formation),
                         ("semestre_id", "=", self.semestre.semestre), ("elementmodule_ids.element", "in", elements_tab)]).etudiant_id
                etuds = []
                for etudiant in etudiants:
                    etuds.append(etudiant)
                i=0
                j=0
                nbr=1
                while nbr <= nbr_places and i < len(salles) and j < len(etuds):
                     #inscrire un etudiant a l'examen
                     self.env["estk.examenetudiant"].create({
                            'etudiant_id': etuds[j].id,
                            'examen_id': self.id,
                            'salle_id': salles[i].id,
                            'numéro_examen':nbr
                     })
                     if nbr > salles[i].capacite_examens:
                         i=i+1
                         nbr=0
                     nbr=nbr+1
                     j=j+1
                self.effecter_etudiants_aux_examens = True
            if self.type_session == "Rattrapage":
                salles = []  # liste des salles reserverées pour l'examen
                for salle in self.salle_ids:
                    salles.append(salle)
                nbr_places = 0  # le nombre des places pour l'examen
                for salle in self.salle_ids:
                    nbr_places = nbr_places + salle.capacite_examens
                elements_tab = []
                elements_tab.append(self.elementmodule_id.element)

                etudiants = self.env["estk.resultatexamen"].search(
                    [("anneeuniversitaire_id", "=", self.anneeuniversitaire.anneeuniversitaire),
                     ("formation", "=", self.formation.formation),
                     ("semestre_id", "=", self.semestre.semestre),
                     ("elementmodule.element", "=", self.elementmodule_id.element),
                     ("observation", "=", "Ratt")]).etudiant_id
                etuds = []
                for etudiant in etudiants:
                    etuds.append(etudiant)
                i = 0
                j = 0
                nbr = 1
                while nbr <= nbr_places and i < len(salles) and j < len(etuds):
                    # inscrire un etudiant a l'examen
                    self.env["estk.examenetudiant"].create({
                        'etudiant_id': etuds[j].id,
                        'examen_id': self.id,
                        'salle_id': salles[i].id,
                        'numéro_examen': nbr
                    })
                    if nbr > salles[i].capacite_examens:
                        i = i + 1
                        nbr = 0
                    nbr = nbr + 1
                    j = j + 1
                self.effecter_etudiants_aux_examens = True


    def calculer_notes_modules(self):
        print("hello, i can calculate all modules marks")
        # pour calculer le notes d'un module dans une session  il faut avoir:
        #         - les notes de ses elements de module du meme session {
        module = self.elementmodule_id.module_id
        print(module.nom)
        elements = self.env["estk.elementmodule"].search([("module_id", "=", module.id)])
        for e in elements:
            print(e.element)
        #chercher les etudiants qui ont passer cet examen
        etudiants = self.env["estk.examenetudiant"].search([("periode", "=", self.periode),
                                                            ("type_session", "=", self.type_session),
                                                            ("anneeuniversitaire_id", "=", self.anneeuniversitaire.id),
                                                            ("formation", "=", self.formation.id),
                                                            ("semestre_id", "=", self.semestre.id),
                                                            ("elementmodule", "=", self.elementmodule_id.id)]).etudiant_id
        eles =[]
        for element in elements:
            print(element.element)
            eles.append(element.element)
        for etud in etudiants:
            resultat_elements= self.env["estk.resultatexamen"].search([("elementmodule", "in", eles),("etudiant_id", "=", etud.id),("type_session", "=", self.type_session)])

            note = 0
            for res in resultat_elements:
                note = note + res.note_elementmodule
            print(note / len(eles))
            self.env["estk.resultatsemestre"].search([("module", "=", module.id),
                                                          ("etudiant_id", "=", etud.id)]) \
                    .update({
                    'note_module': note / len(eles)
            })
        #note des element pour cet examen

        #               * chercher le module de self
        #               * chercher les resultats des element de modules dans resulat_examen
        #               * calculer note du module
        #               * update la note du module dans resultat_semestre
        #               * update la note du semestre dans resultat_annuel  }

        # pour promotionner un etudiant:
        #               * on_change  sur les notes des modules dans les resultats_semestre
        #               * delete and create enrigistrement d'un inscription administrative relative a année_correspondante
        #               * delete and create enrigistrement d'un inscription pédagogique relative a année_correspondante


    def créer_resultats_examens(self):
        if self.effecter_etudiants_aux_examens == False:
            raise exceptions.ValidationError("il faut d'abord effectuer l'inscription des étudiant(e)s aux examens")
        else:
            examensetudiants = self.env["estk.examenetudiant"].search([("examen_id", "=", self.id)])

            #créer resultats examen des etudiants
            for exametudiant in examensetudiants:
                self.env["estk.resultatexamen"].create({
                'examenetudiant_id': exametudiant.id,
                'note_elementmodule': 0
                })
            # créer resultats semestres des etudiants
            for exametudiant in examensetudiants:
                 if not self.env["estk.resultatsemestre"].search([("semestre", "=", self.semestre.semestre),
                                                                  ("etudiant_id", "=", exametudiant.etudiant_id.id),
                                                                  ("anneeuniversitaire", "=", self.anneeuniversitaire.anneeuniversitaire),
                                                                  ("session", "=", self.session_id.periode),
                                                                  ("module", "=", self.elementmodule_id.module_id.nom)]).module:
                    self.env["estk.resultatsemestre"].create({
                    'etudiant_id': exametudiant.etudiant_id.id,
                    'anneeuniversitaire': self.anneeuniversitaire.id,
                    'semestre': self.semestre.id,
                    'session': self.session_id.periode,
                    'type_session': self.type_session,
                    'module': self.elementmodule_id.module_id.id,
                    'note_module': 0,
                    'observation': "Non Validé"
                    })


            #créer resultats annuels des etudiants
            # resultat_semestre = self.env["estk.resultatannuel"].search([("semestre", "=", self.semestre), ("etudiant_id", "in")])
            # if not resultat_semestre:
            for exametudiant in examensetudiants:
                 if not self.env["estk.resultatannuel"].search([("semestre", "=", self.semestre.semestre), ("etudiant_id", "=", exametudiant.etudiant_id.id)]):
                    self.env["estk.resultatannuel"].create({
                    'etudiant_id': exametudiant.etudiant_id.id,
                    'anneeuniversitaire': self.anneeuniversitaire.id,
                    'semestre': self.semestre.id,
                    'note_semestre': 0,
                    'observation': "Non Validé"
                    })





