import unittest
from datetime import datetime
from DTO.reservationDTO import ReservationDTO
from modele.chambre import Chambre,TypeChambre
from modele.usager import Usager
from modele.reservation import Reservation
from metier.reservationMetier import creerReservation


class test_reservation(unittest.TestCase):
    def test_creerReservation(self):
        usager = Usager(id_usager ='07586C6A-FB2B-4B31-8D10-01AD8D9D7489',
                            prenom= 'Houssam',
                            nom='Broumi',
                            adresse='Gaspé',
                            mobile='581-887-7912',
                            mot_de_passe= '12345678'
                            )
        chambre = Chambre(
                        numero_chambre = 101,
                        disponible_reservation = True,
                        type_chambre = 
                                TypeChambre(
                                    nom_type= 'king',
                                    prix_plancher= 229.0
                                )
            )
        reservation = Reservation(
            date_debut_reservation=datetime.strptime("2025-09-25 16:00", "%Y-%m-%d %H:%M"),
            date_fin_reservation=datetime.strptime("2025-09-26 11:00", "%Y-%m-%d %H:%M"),
            prix_jour=179.99,
            chambre=chambre,
            usager=usager
        )

        nouvelleReservationDTO = ReservationDTO(reservation)
        nouvelleReservation = creerReservation(nouvelleReservationDTO)
        self.assertIsNotNone(nouvelleReservation.id_reservation)
       
    

""" import unittest
from datetime import datetime
from DTO.reservationDTO import ReservationDTO
from modele.chambre import Chambre, TypeChambre
from modele.usager import Usager
from modele.reservation import Reservation
 
 
class test_reservation(unittest.TestCase):
    def test_creerReservation(self):
        usager = Usager(
            id_usager="07586C6A-FB2B-4B31-8D10-01AD8D9D7489",
            prenom="Houssam",
            nom="Broumi",
            adresse="Gaspé",
            mobile="581-887-7912",
            mot_de_passe="12345678",
        )
 
        type_chambre = TypeChambre(
            nom_type="king",
            prix_plancher=229.0,
        )
 
        chambre = Chambre(
            numero_chambre=101,
            disponible_reservation=True,
            type_chambre=type_chambre,
        )
 
        reservation = Reservation(
            date_debut_reservation=datetime.strptime("2025-09-25 16:00", "%Y-%m-%d %H:%M"),
            date_fin_reservation=datetime.strptime("2025-09-26 11:00", "%Y-%m-%d %H:%M"),
            prix_jour=179.99,
            info_reservation="",
            chambre=chambre,
            usager=usager,
        )
 
        nouvelleReservationDTO = ReservationDTO(reservation)
        self.assertEqual(
            nouvelleReservationDTO.dateDebut,
            datetime.strptime("2025-09-25 16:00", "%Y-%m-%d %H:%M"),
        )
        self.assertEqual(
            nouvelleReservationDTO.dateFin,
            datetime.strptime("2025-09-26 11:00", "%Y-%m-%d %H:%M"),
        )
        self.assertAlmostEqual(nouvelleReservationDTO.prixParJour, 179.99, places=2)
        self.assertEqual(nouvelleReservationDTO.chambre.numero_chambre, 101)
        self.assertTrue(nouvelleReservationDTO.chambre.disponible_reservation)
        self.assertEqual(nouvelleReservationDTO.chambre.type_chambre.nom_type, "king")
        self.assertEqual(nouvelleReservationDTO.usager.nom, "Broumi")
        self.assertEqual(nouvelleReservationDTO.usager.prenom, "Houssam")
  """