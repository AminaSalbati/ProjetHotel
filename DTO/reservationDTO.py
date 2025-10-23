import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, model_validator
from DTO.chambreDTO import ChambreDTO
from DTO.usagerDTO import UsagerDTO
from modele.reservation import Reservation


class CriteresRechercheDTO(BaseModel):
    idReservation: Optional[str] = Field(default=None, min_length=36, max_length=36)
    idUsager: Optional[str] = Field(default=None, min_length=36, max_length=36)
    idChambre: Optional[str] = Field(default=None, min_length=36, max_length=36)
    nom: Optional[str] = Field(default=None, max_length=60)
    prenom: Optional[str] = Field(default=None, max_length=60)
    motdePasse: Optional[str] = Field(default=None, min_length=8, max_length=60)
    dateDebut: Optional[datetime.datetime] = None
    dateFin: Optional[datetime.datetime] = None

    @model_validator(mode='after')
    def check_fields_together(self):
        if (self.nom is not None and self.prenom is None) or \
           (self.prenom is None and self.nom is not None):
            raise ValueError("Le nom et prenom doivent être tous les deux présents ou absents")
        return self
    
    @model_validator(mode='after')
    def validate_dates(self):
        if self.dateFin <= self.dateDebut:
            raise ValueError("La date de fin doit être superieure à la date de début")


class ReservationDTO(BaseModel):
    idReservation: Optional[UUID] = None
    dateDebut: datetime.datetime
    dateFin: datetime.datetime
    prixParJour: float
    infoReservation: Optional[str] = ""
    chambre: ChambreDTO
    usager: UsagerDTO

    def __init__(self, reservation: Reservation):
        super().__init__(
            idReservation=reservation.id_reservation,
            dateDebut=reservation.date_debut_reservation, 
            dateFin=reservation.date_fin_reservation, 
            prixParJour=reservation.prix_jour, 
            infoReservation = reservation.info_reservation,
            chambre = ChambreDTO(reservation.chambre),
            usager = UsagerDTO(reservation.usager))   

    

    






  


   