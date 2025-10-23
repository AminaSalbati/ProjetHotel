import unittest
from datetime import datetime,timedelta
from sqlalchemy.orm import Session 
from sqlalchemy import create_engine, select, func
from modele.chambre import Chambre, TypeChambre
from modele.reservation import Reservation
from DTO.reservationDTO import ReservationDTO
from metier.reservationMetier import modifierReservation,supprimerReservation
from modele.usager import Usager





engine = create_engine('mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+17+for+SQL+Server', use_setinputsizes=False)
Room_Num = 101


class test_reservation(unittest.TestCase):
    def test_chambre(self):
        with Session(engine) as session:
            stmt = select(Chambre).where(Chambre.numero_chambre == Room_Num)
            chambre = session.execute(stmt).scalars().first()
    
            self.assertIsNotNone(chambre, f"Chambre {Room_Num} doit exister sans la base de données.")
            self.assertEqual(chambre.numero_chambre, Room_Num)

    def test_reservation_chambre(self):
        with Session(engine) as session:
            req= select(func.count(Reservation.id_reservation)).join(Chambre, Reservation.fk_id_chambre == Chambre.id_chambre).where(Chambre.numero_chambre == Room_Num)  
            nb_reservations = session.execute(req).scalar_one()

            self.assertGreaterEqual(
                nb_reservations, 2,
                f"La chambre {Room_Num} doit avoir au moins deux réservations, trouvé: {nb_reservations}"
            )  

class TestModifierReservation(unittest.TestCase):
    def test_modifierReservation(self):
        debut_init = datetime.now().replace(microsecond=0) + timedelta(days=5)
        fin_init   = debut_init + timedelta(days=1)
        debut_new  = debut_init + timedelta(days=2)
        fin_new    = debut_new + timedelta(days=1)

        with Session(engine) as session:
            usager1 = Usager(prenom="Houssam", nom="Broumi",
                             adresse="Gaspé", mobile="581-000-0000", mot_de_passe="12345678")
            usager2 = Usager(prenom="Amina", nom="Salbati",
                             adresse="Québec", mobile="581-111-1111", mot_de_passe="87654321")
            type_king = TypeChambre(nom_type="king", prix_plancher=229.0)
            chambre101 = Chambre(numero_chambre=101, disponible_reservation=True, type_chambre=type_king)
            chambre102 = Chambre(numero_chambre=102, disponible_reservation=True, type_chambre=type_king)

            reservation = Reservation(
                date_debut_reservation=debut_init,
                date_fin_reservation=fin_init,
                prix_jour=179.99,
                info_reservation="init",
                usager=usager1,
                chambre=chambre101,
            )

            session.add_all([usager1, usager2, type_king, chambre101, chambre102, reservation])
            session.commit()
            session.refresh(reservation)

            id_res = reservation.id_reservation
            id_usager2 = usager2.id_usager
            num_chambre2 = 102

        with Session(engine) as session:
            usager2_db = session.get(Usager, id_usager2)
            chambre102_db = session.scalars(
                select(Chambre).where(Chambre.numero_chambre == num_chambre2)
            ).first()

            reservation_maj = Reservation(
                date_debut_reservation=debut_new,
                date_fin_reservation=fin_new,
                prix_jour=199.99,
                info_reservation="mise à jour",
                usager=usager2_db,
                chambre=chambre102_db,
            )

            majDTO = ReservationDTO(reservation_maj)

        modifierReservation(id_res, majDTO)

        with Session(engine) as session:
            r = session.get(Reservation, id_res)
            self.assertIsNotNone(r)
            self.assertEqual(r.date_debut_reservation.replace(microsecond=0), debut_new)
            self.assertEqual(r.date_fin_reservation.replace(microsecond=0),   fin_new)
            self.assertAlmostEqual(r.prix_jour, 199.99, places=2)
            self.assertEqual(r.info_reservation, "mise à jour")
            self.assertEqual(r.chambre.numero_chambre, 102)
            self.assertEqual(r.usager.nom, "Salbati")

class TestSupprimerReservation(unittest.TestCase):
    def test_supprimerReservation(self):
        debut = datetime.now() + timedelta(days=5)
        fin = debut + timedelta(days=1)

        with Session(engine) as session:
            usager = Usager(
                prenom="Houssam",
                nom="Broumi",
                adresse="Gaspé",
                mobile="581-000-0000",
                mot_de_passe="12345678",
            )
            type_king = TypeChambre(nom_type="king", prix_plancher=229.0)
            chambre = Chambre(numero_chambre=303, disponible_reservation=True, type_chambre=type_king)
            reservation = Reservation(
                date_debut_reservation=debut,
                date_fin_reservation=fin,
                prix_jour=179.99,
                info_reservation="à supprimer",
                usager=usager,
                chambre=chambre,
            )

            session.add_all([usager, type_king, chambre, reservation])
            session.commit()
            session.refresh(reservation)
            id_res = reservation.id_reservation

        supprimerReservation(id_res)

        # --- Vérification ---
        with Session(engine) as session:
            res = session.get(Reservation, id_res)
            self.assertIsNone(res, "La réservation devrait avoir été supprimée.")