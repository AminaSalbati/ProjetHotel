import unittest
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from modele.chambre import Chambre , TypeChambre
from DTO.chambreDTO import ChambreDTO
from metier.chambreMetier import modifierChambre
import logging

logging.basicConfig()
logging.getLogger("sqlachemy.engine").setLevel(logging.INFO)

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
