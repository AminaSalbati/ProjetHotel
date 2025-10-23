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
            self.usager_dto.id_usager = resultats[0].id_usager

    def tearDown(self):
        
        if self.usager_dto.id_usager:
            supprimerUsager(self.usager_dto.id_usager)

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

        
        updated = rechercherUsager(id_usager=self.usager_dto.id_usager)[0]
        self.assertEqual(updated.mobile.strip(), "9999999999")

    def test_supprimerUsager(self):
        supprimerUsager(self.usager_dto.id_usager)

        
        results = rechercherUsager(id_usager=self.usager_dto.id_usager)
        self.assertEqual(len(results), 0)













       