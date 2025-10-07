from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from modele.usager import Usager
from DTO.usagerDTO import UsagerDTO
 
engine = create_engine('mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+17+for+SQL+Server', use_setinputsizes=False)
 
def creerUsager(usagerDTO: UsagerDTO):
    with Session(engine) as session:
        nouvel_usager = Usager(
            nom=usagerDTO.nom,
            prenom=usagerDTO.prenom,
            adresse=usagerDTO.adresse,
            mobile=usagerDTO.mobile,
            mot_de_passe=usagerDTO.motdePasse
        )

        session.add(nouvel_usager)
        session.commit()
        return nouvel_usager.id_usager  
 
def rechercherUsager(id_usager=None, nom=None, prenom=None):
    stmt = select(Usager)

    if id_usager:
        stmt = stmt.where(Usager.id_usager == id_usager)

    if nom:
        stmt = stmt.where(Usager.nom == nom)

    if prenom:
        stmt = stmt.where(Usager.prenom == prenom)

    usagers = []
    with Session(engine) as session:
        for usager in session.execute(stmt).scalars():
            usagers.append(UsagerDTO(usager))

    return usagers

def supprimerUsager(id_usager: int):
    with Session(engine) as session:
        usager = session.query(Usager).filter_by(id_usager=id_usager).first()
 
        if usager:
            if usager.reservations and len(usager.reservations) > 0:
                raise ValueError("Impossible de supprimer un usager ayant des réservations actives.")
 
            session.delete(usager)
            session.commit()
 
def modifierUsager(usagerDTO: UsagerDTO):
    with Session(engine) as session:
        usager = session.query(Usager).filter_by(id_usager=usagerDTO.idUsager).first()
 
        if not usager:
            raise ValueError("Usager introuvable")
 
        
        usager.nom = usagerDTO.nom
        usager.prenom = usagerDTO.prenom
        usager.adresse = usagerDTO.adresse
        usager.mobile = usagerDTO.mobile
        usager.adresse = usagerDTO.adresse
        usager.mot_de_passe=usagerDTO.motdePasse
 
        session.commit()

        