from typing import Optional
from pydantic import BaseModel
from modele.chambre import TypeChambre, Chambre
from uuid import UUID
 
# Data Transfer Object : pydantic BaseModel pour intégration facile avec FastAPI
class TypeChambreDTO(BaseModel):
    nom_type: str
    prix_plafond: Optional[float] = None
    prix_plancher: float
    description_chambre : Optional[str] = None
 
    def __init__(self, typeChambre: TypeChambre):
        super().__init__(
                         nom_type = typeChambre.nom_type,
                         prix_plafond = typeChambre.prix_plafond,
                         prix_plancher = typeChambre.prix_plancher,
                         description_chambre = typeChambre.description_chambre
                         )
 
class ChambreDTO(BaseModel):
    idChambre : Optional[UUID]
    numero_chambre: int
    disponible_reservation : bool
    autre_informations: Optional[str] = None
    type_chambre: TypeChambreDTO
 
    def __init__(self, chambre: Chambre):
        super().__init__(idChambre = chambre.id_chambre,
                         numero_chambre = chambre.numero_chambre,
                         disponible_reservation = chambre.disponible_reservation,
                         autre_informations = chambre.autre_informations,
                         type_chambre = TypeChambreDTO(chambre.type_chambre))
 