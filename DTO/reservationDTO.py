""" TODO : Compléter les DTOs, ajouter des validations au besoin et ajuster les imports. """

import datetime
from pydantic import BaseModel, Field, ValidationError, model_validator
from DTO.chambreDTO import ChambreDTO
from modele.reservation import Reservation
from DTO.usagerDTO import UsagerDTO
from uuid import UUID

# Data Transfer Object : pydantic BaseModel pour intégration facile avec FastAPI
class CriteresRechercheDTO(BaseModel):
    idReservation: str = Field(min_length=36, max_length=36, custom_error='idReservation doit contenir 36 caractères')
    idUsager: str = Field(min_length=36, max_length=36, custom_error='idUsager doit contenir 36 caractères')
    idChambre: str = Field(min_length=36, max_length=36, custom_error='idChambre doit contenir 36 caractères')
    nom: str = Field(max_length=60, custom_error = 'Le nom est trop long')
    prenom: str = Field(max_length=60, custom_error = 'Le prenom est trop long')
    motdePasse: str = Field(min_length=8,max_length=60, custom_error = 'Le mot de passe doit contenir au moins 8 caractères')
    

    
    @model_validator(mode='after')
    def check_fields_together(self):
        if (self.nom is not None and self.prenom is None) or \
           (self.prenom is None and self.nom is not None):
            raise ValueError("Le nom et prenom doivent être touss les deux présents ou absents")
        return self
    
    @model_validator(mode='after')
    def validate_dates(self):
        if self.dateFin <= self.dateDebut:
            raise ValueError("La date de fin doit être superieure à la date de début")

class ReservationDTO(BaseModel):
    idReservation: UUID
    dateDebut : datetime.datetime
    dateFin : datetime.datetime
    prixParJour : float
    infoReservation : str
    chambre : ChambreDTO
    usager : UsagerDTO


    def __init__(self, reservation: Reservation):
        super().__init__(idReservation=reservation.id_reservation, 
            dateDebut=reservation.date_debut_reservation, 
            dateFin=reservation.date_fin_reservation, 
            prixParJour=reservation.prix_jour, 
            infoReservation = reservation.info_reservation,
            chambre = ChambreDTO(reservation.chambre),
            usager = UsagerDTO(reservation.usager)) 
        
    
 


#modifier reservations


    """ TODO : usager = UsagerDTO() """

  


   