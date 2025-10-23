import unittest
from modele.chambre import Chambre, TypeChambre
from metier.chambreMetier import creerChambre, ChambreDTO
class TestCreerChambre(unittest.TestCase):
    def test_creerChambre(self):
        chambreDTO = ChambreDTO(
            Chambre(
                numero_chambre=504,
                disponible_reservation=True,
                type_chambre=TypeChambre(
                    nom_type='king',
                    prix_plancher=229.0
                )
            )
        )
        chambreDTOCree = creerChambre(chambreDTO)
        self.assertEqual(chambreDTOCree.numero_chambre, 504)
