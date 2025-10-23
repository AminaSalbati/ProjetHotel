from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from DTO.reservationDTO import CriteresRechercheDTO, ReservationDTO
from modele.reservation import Reservation
from modele.usager import Usager
from modele.chambre import Chambre
from DTO.usagerDTO import UsagerDTO
from datetime import date


engine = create_engine('mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+17+for+SQL+Server', use_setinputsizes=False)

def rechercherReservation(criteres: CriteresRechercheDTO):
        stmt = None
        stmt = select(Reservation)

        if(criteres.idReservation):
            stmt = stmt.where(Reservation.id_reservation == criteres.idReservation)
        
        if(criteres.idChambre):
            stmt = stmt.where(Reservation.fk_id_chambre == criteres.idChambre)

        if(criteres.idUsager):
            stmt = stmt.where(Reservation.fk_id_usager == criteres.idUsager)

        if(criteres.nom):
            stmt = stmt.join(Usager).where(Usager.nom == criteres.nom)
            if(criteres.prenom):
                 stmt.where(Usager.prenom == criteres.prenom) 

        if criteres.dateDebut and criteres.dateFin:
            stmt = stmt.where(Reservation.date_debut_reservation < criteres.dateFin)
            stmt = stmt.where(Reservation.date_fin_reservation > criteres.dateDebut)
                              
        if stmt is None:
            raise ValueError("Aucun critère de recherche fourni")
        
        reservations = []
        with Session(engine) as session:
           for reservation in session.execute(stmt).scalars():
                reservations.append(ReservationDTO(reservation))

        return reservations


def creerReservation(reservationDTO: ReservationDTO):
    with Session(engine) as session:

        usager = session.scalars(
            select(Usager).filter_by(id_usager=reservationDTO.usager.id_usager)
        ).first()

        if not usager:
            raise ValueError("Usager introuvable")

        chambre = session.scalars(
            select(Chambre).filter_by(numero_chambre=reservationDTO.chambre.numero_chambre)
        ).first()

        if not chambre:
            raise ValueError("Chambre introuvable")

        reservation = Reservation(
            date_debut_reservation=reservationDTO.dateDebut,
            date_fin_reservation=reservationDTO.dateFin,
            prix_jour=reservationDTO.prixParJour,
            info_reservation=reservationDTO.infoReservation,
            usager=usager,
            chambre=chambre
        )

        session.add(reservation)
        session.commit()
        session.refresh(reservation)
        return reservation  

def supprimerReservation(id_reservation: int):
    with Session(engine) as session:
        reservation = session.query(Reservation).filter_by(id_reservation=id_reservation).first()
        
        if reservation:
            if reservation.date_fin_reservation < date.today():
                raise ValueError("Impossible de supprimer une réservation déjà terminée.")

            session.delete(reservation)
            session.commit()


def modifierReservation(id_reservation: int, reservationDTO: ReservationDTO):
    if reservationDTO.dateFin <= reservationDTO.dateDebut:
        raise ValueError("La date de fin doit être supérieure à la date de début.")
 
    with Session(engine) as session:
        reservation = session.query(Reservation).filter_by(id_reservation=id_reservation).first()
        if not reservation:
            raise ValueError("Réservation introuvable.")

        if reservation.date_fin_reservation < date.today():

            raise ValueError("Impossible de modifier une réservation déjà terminée.")
        
        usager = session.scalars(
            select(Usager).filter_by(id_usager=reservationDTO.usager.id_usager)).first()

        if not usager:
            raise ValueError("Usager introuvable.")

        chambre = session.scalars(
            select(Chambre).filter_by(numero_chambre=reservationDTO.chambre.numero_chambre)).first()

        if not chambre:
            raise ValueError("Chambre introuvable.")

        reservation.date_debut_reservation = reservationDTO.dateDebut
        reservation.date_fin_reservation   = reservationDTO.dateFin
        reservation.prix_jour              = reservationDTO.prixParJour
        reservation.info_reservation       = reservationDTO.infoReservation or ""
        reservation.usager                 = usager
        reservation.chambre                = chambre

        session.commit()
 






















