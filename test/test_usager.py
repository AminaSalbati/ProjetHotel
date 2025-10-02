import unittest
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from modele.usager import Usager
from modele.reservation import Reservation



engine = create_engine('mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+17+for+SQL+Server', use_setinputsizes=False)
User_Prenom = "Houssam"


class test_usager(unittest.TestCase):
    def test_utilisateur(self):
        with Session(engine) as session:
          stmt = select(Usager).where(Usager.prenom == User_Prenom)
          usager= session.execute(stmt).scalar_one()

          
          self.assertIsNotNone(usager, f"Usager avec le prénom '{User_Prenom}' introuvable")
          nb_res = len(usager.reservations)

          self.assertGreaterEqual(
            nb_res, 2,
            f"L'usager {User_Prenom} devrait avoir au moins 2 réservation, trouvé: {nb_res}"
            )

          
         
#test rechercher usager
#modifier usager res chambre
