import unittest
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from modele.chambre import Chambre , TypeChambre
from DTO.chambreDTO import ChambreDTO, TypeChambreDTO
from metier.chambreMetier import modifierChambre, supprimerChambre, rechercherTypeChambreParNom, modifierTypeChambre




engine = create_engine('mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+17+for+SQL+Server', use_setinputsizes=False)
class test_chambre(unittest.TestCase):
    def test_getChambreParNumero(self):
        with Session(engine) as session:
            stmt = select(Chambre).where(Chambre.numero_chambre == 243)
            chambre = session.execute(stmt).scalar_one()
            self.assertEqual(chambre.numero_chambre,243)
            self.assertEqual(chambre.type_chambre.nom_type,'king')

   


    def test_modifierChambre(self):
        with Session(engine) as session:
            chambreDTO = ChambreDTO(
                Chambre(
                    id_chambre="47CD0198-1C8C-4C77-AE92-A8F250C5E6C3",
                    numero_chambre=101,
                    disponible_reservation=True,
                    autre_informations="Nouvelle info",
                    type_chambre=TypeChambre(nom_type="king", prix_plancher=229.00),
                )
            )
        modifierChambre(chambreDTO)

        with Session(engine) as session:
            stmt = select(Chambre).where(Chambre.id_chambre == chambreDTO.idChambre)
            chambreDB = session.execute(stmt).scalars().one()
            self.assertEqual(chambreDB.autre_informations, "Nouvelle info")

            chambreDB.autre_informations = "ancienne info"
            chambreDB.disponible_reservation = False
            session.commit()
    def test_supprimerChambre(self):
        with Session(engine) as session:
            type_test = TypeChambre(nom_type="TypeTestSuppr", prix_plancher=100.0)
            chambre = Chambre(
                numero_chambre=501,
                disponible_reservation=True,
                autre_informations="Chambre pour test suppression",
                type_chambre=type_test
            )
            session.add_all([type_test, chambre])
            session.commit()
            session.refresh(chambre)
            id_chambre = chambre.id_chambre

        resultat = supprimerChambre(501)
        self.assertTrue(resultat)

        with Session(engine) as session:
            chambre_supprimee = session.get(Chambre, id_chambre)
            self.assertIsNone(chambre_supprimee)


    def test_rechercherTypeChambreParNom(self):
        with Session(engine) as session:
            type_chambre = TypeChambre(
                nom_type="TypeRecherche",
                prix_plancher=120.0,
                prix_plafond=200.0,
                description_chambre="Type de chambre pour test recherche"
            )
            session.add(type_chambre)
            session.commit()

        dto = rechercherTypeChambreParNom("TypeRecherche")
        self.assertIsNotNone(dto)
        self.assertEqual(dto.nom_type, "TypeRecherche")
        self.assertEqual(dto.description_chambre, "Type de chambre pour test recherche")

        with Session(engine) as session:
            t = session.scalars(select(TypeChambre).where(TypeChambre.nom_type == "TypeRecherche")).first()
            if t:
                session.delete(t)
                session.commit() 

    def test_modifierTypeChambre(self):
        with Session(engine) as session:
            type_chambre = TypeChambre(
                nom_type="TypeModif",
                prix_plancher=100.0,
                prix_plafond=150.0,
                description_chambre="Avant modification"
            )
            session.add(type_chambre)
            session.commit()

        dto = TypeChambreDTO(
            TypeChambre(
                nom_type="TypeModif",
                description_chambre="Après modification",
                prix_plancher=110.0,
                prix_plafond=160.0
            )
        )

        resultat = modifierTypeChambre(dto)

        self.assertEqual(resultat.nom_type, "TypeModif")
        self.assertEqual(resultat.description_chambre, "Après modification")

        with Session(engine) as session:
            type_verifie = session.scalars(select(TypeChambre).where(TypeChambre.nom_type == "TypeModif")).first()
            self.assertEqual(type_verifie.description_chambre, "Après modification")

            session.delete(type_verifie)
            session.commit()
    
    
