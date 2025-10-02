import unittest
from modele.chambre import TypeChambre
from metier.chambreMetier import creerTypeChambre, TypeChambreDTO,supprimerTypeChambre

class TestCreerTypeChambre(unittest.TestCase):
    def test_creerTypeChambre(self):
        typeDTO = TypeChambreDTO(
           TypeChambre(
               nom_type = 'king',
               prix_plancher = 229.0,
               prix_plafond=300.0,
               description_chambre='Lit king size'
           )
        )
        
        typeChambreCree = creerTypeChambre(typeDTO)
        self.assertEqual(typeChambreCree.nom_type, 'king')
        self.assertEqual(typeChambreCree.prix_plancher, 229.0)
        self.assertEqual(typeChambreCree.prix_plafond, 300.0)
        self.assertEqual(typeChambreCree.description_chambre,'Lit king size' )

        supprimerTypeChambre('king')

     
      