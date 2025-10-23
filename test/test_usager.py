import unittest
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from uuid import uuid4

from modele.usager import Usager
from modele.reservation import Reservation
from metier.usagerMetier import creerUsager, rechercherUsager, modifierUsager, supprimerUsager
from DTO.usagerDTO import UsagerDTO

engine = create_engine(
    'mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+17+for+SQL+Server',
    use_setinputsizes=False
)

User_Prenom = "Houssam"

class test_usager(unittest.TestCase):

    def setUp(self):
        # Créer un Usager SQLAlchemy pour les tests
        self.usager_obj = Usager(
            nom="TestNom",
            prenom="TestPrenom",
            adresse="123 rue Test",
            mobile="8888888888",
            mot_de_passe="motdepasse"
        )
        self.usager_dto = UsagerDTO(self.usager_obj)
        creerUsager(self.usager_dto)

        # recupere l ID
        resultats = rechercherUsager(nom="TestNom", prenom="TestPrenom")
        if resultats:
            self.usager_dto.idUsager = resultats[0].idUsager

    def tearDown(self):
        
        if self.usager_dto.idUsager:
            supprimerUsager(self.usager_dto.idUsager)

    def test_utilisateur(self):
        with Session(engine) as session:
            stmt = select(Usager).where(Usager.prenom == User_Prenom)
            usager = session.execute(stmt).scalars().first()
            self.assertIsNotNone(usager, f"Usager avec le prénom '{User_Prenom}' introuvable")
            nb_res = len(usager.reservations)

            self.assertGreaterEqual(
                nb_res, 2,
                f"L'usager {User_Prenom} devrait avoir au moins 2 réservations, trouvé: {nb_res}"
            )

    def test_rechercherUsager(self):
        resultats = rechercherUsager(nom="TestNom", prenom="TestPrenom")
        self.assertGreaterEqual(len(resultats), 1)
        self.assertEqual(resultats[0].adresse, "123 rue Test")

    def test_modifierUsager(self):
       
        self.usager_dto.mobile = "9999999999"
        modifierUsager(self.usager_dto)

        
        updated = rechercherUsager(id_usager=self.usager_dto.idUsager)[0]
        self.assertEqual(updated.mobile.strip(), "9999999999")

    def test_supprimerUsager(self):
        supprimerUsager(self.usager_dto.idUsager)

        
        results = rechercherUsager(id_usager=self.usager_dto.idUsager)
        self.assertEqual(len(results), 0)













       #version eronnée# import unittest from sqlalchemy.orm import Session from sqlalchemy import create_engine, select from modele.usager import Usager from modele.reservation import Reservation import unittest from uuid import UUID from metier.usagerMetier import creerUsager, rechercherUsager, modifierUsager, supprimerUsager from DTO.usagerDTO import UsagerDTO from modele.usager import Usager from sqlalchemy.orm import Session from sqlalchemy import create_engine, select engine = create_engine('mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+17+for+SQL+Server', use_setinputsizes=False) User_Prenom = "Houssam" class test_usager(unittest.TestCase): def test_utilisateur(self): with Session(engine) as session: stmt = select(Usager).where(Usager.prenom == User_Prenom) usager = session.execute(stmt).scalars().first() self.assertIsNotNone(usager, f"Usager avec le prénom '{User_Prenom}' introuvable") nb_res = len(usager.reservations) self.assertGreaterEqual( nb_res, 2, f"L'usager {User_Prenom} devrait avoir au moins 2 réservation, trouvé: {nb_res}" ) #test rechercher usager def test_rechercherUsager(self): resultats = rechercherUsager(nom="TestNom", prenom="TestPrenom") self.assertGreaterEqual(len(resultats), 1) self.assertEqual(resultats[0].adresse, "123 rue Test") #modifier usager res chambre def test_modifierUsager(self): # Modification du mobile self.usager_test.mobile = "9999999999" modifierUsager(self.usager_test) # Vérification updated = rechercherUsager(id_usager=self.usager_test.idUsager)[0] self.assertEqual(updated.mobile, "9999999999") def test_supprimerUsager(self): supprimerUsager(self.usager_test.idUsager) # Vérifier qu’il n’est plus dans la DB results = rechercherUsager(id_usager=self.usager_test.idUsager) self.assertEqual(len(results), 0)
