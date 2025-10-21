import unittest
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from modele.chambre import Chambre

engine = create_engine('mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+17+for+SQL+Server', use_setinputsizes=False)
class test_chambre(unittest.TestCase):
    def test_getChambreParNumero(self):
        with Session(engine) as session:
            stmt = select(Chambre).where(Chambre.numero_chambre == 243)
            chambre = session.execute(stmt).scalar_one()
            self.assertEqual(chambre.numero_chambre,243)
            self.assertEqual(chambre.type_chambre.nom_type,'king')