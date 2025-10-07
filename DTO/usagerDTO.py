from typing import Optional
from pydantic import BaseModel, Field, model_validator
from uuid import UUID
from datetime import datetime
from modele.usager import Usager
import re
 
 
class UsagerDTO(BaseModel):
    idUsager: Optional[UUID]
    prenom: str 
    nom: str 
    adresse: str
    mobile: str 
    motdePasse: str
 
    @model_validator(mode='after')
    def check_nom_prenom(self):
        if (self.nom and not self.prenom) or (self.prenom and not self.nom):#pas obligatoire
            raise ValueError("Le prénom et le nom doivent être tous les deux présents.")
        return self
    @model_validator(mode='after')
    def validate_mobile_format(self):
        if self.mobile is not None:
            if not re.fullmatch(r"[\d\s\+\-]+", self.mobile):
                raise ValueError("Le numéro de mobile contient des caractères invalides")
        return self
 
    def __init__(self, usager: Usager):
        super().__init__(
            idUsager=usager.id_usager,
            prenom=usager.prenom,
            nom=usager.nom,
            adresse=usager.adresse,
            mobile=usager.mobile,
            motdePasse=usager.mot_de_passe
        )
 
 
class CriteresRechercheDTO(BaseModel):
    nom: Optional[str] = Field(None, max_length=60)
    prenom: Optional[str] = Field(None, max_length=60)
    motdePasse: Optional[str] = Field(None, min_length=8, max_length=60)
    adresse: Optional[str] = Field(None, min_length=5, max_length=255)
    mobile: Optional[str] = Field(None, min_length=10, max_length=20)
 
    @model_validator(mode='after')
    def check_nom_prenom_presence(self):
        if (self.nom is not None and self.prenom is None) or \
           (self.prenom is not None and self.nom is None):
            raise ValueError("Le nom et le prénom doivent être tous les deux présents ou absents")
        return self
    
    