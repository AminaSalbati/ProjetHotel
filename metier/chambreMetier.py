from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select, func
from DTO.chambreDTO import ChambreDTO, TypeChambreDTO
from modele.chambre import Chambre, TypeChambre
from modele.reservation import Reservation

engine = create_engine('mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+17+for+SQL+Server', use_setinputsizes=False)

def creerChambre(chambre: ChambreDTO):
    with Session(engine) as session:
            stmt = select(TypeChambre).where(TypeChambre.nom_type == chambre.type_chambre.nom_type)
            result = session.execute(stmt)

            for typeChambre in result.scalars():
                
                nouvelleChambre = Chambre (
                    numero_chambre = chambre.numero_chambre,
                    disponible_reservation = chambre.disponible_reservation,
                    autre_informations = chambre.autre_informations,
                    type_chambre = typeChambre
                )

            session.add(nouvelleChambre)
            session.commit()
        
            return chambre
            
def creerTypeChambre(typeChambre: TypeChambreDTO):
     with Session(engine) as session:
       
        nouveauTypeChambre = TypeChambre(
            nom_type=typeChambre.nom_type,
            description_chambre=typeChambre.description_chambre ,
            prix_plancher=typeChambre.prix_plancher,
            prix_plafond=typeChambre.prix_plafond

        )


        session.add(nouveauTypeChambre)
        session.commit()
        
        return typeChambre
     
def supprimerTypeChambre(nom_type):
    with Session(engine) as session:
        type_chambre = session.query(TypeChambre).filter_by(nom_type=nom_type).first()
        if type_chambre:
            session.delete(type_chambre)
            session.commit()   

#supprimer chambre; modifier type chambre; rechercher type chambre
            
def getChambreParNumero(no_chambre: int):
     with Session(engine) as session:
        stmt = select(Chambre).where(Chambre.numero_chambre == no_chambre)
        result = session.execute(stmt)
        
        for chambre in result.scalars():
            return ChambreDTO (chambre)
        
def modifierChambre(chambre:ChambreDTO):
    with Session(engine) as session:
        stmt = select(Chambre).where(Chambre.id_chambre == chambre.idChambre)
        chambreAModifier = session.execute(stmt).scalars().one_or_none()
        if chambreAModifier is None:
            raise ValueError(f"La chambre avec l'ID {chambre.idChambre} n'existe pas.")

        chambreAModifier.disponible_reservation = chambre.disponible_reservation
        chambreAModifier.autre_informations = chambre.autre_informations
        chambreAModifier.numero_chambre = chambre.numero_chambre

        if chambre.type_chambre is not None:
            stmt_type = select(TypeChambre).where(TypeChambre.nom_type == chambre.type_chambre.nom_type)
            type_chambre_existant = session.execute(stmt_type).scalars().first()
            if not type_chambre_existant:
                raise ValueError(f"Le type de chambre '{chambre.type_chambre.nom_type}' n'existe pas dans la base.")
            chambreAModifier.type_chambre = type_chambre_existant

        session.commit()
        return ChambreDTO(chambreAModifier)
    


def supprimerChambre(numero_chambre: int) -> bool:
    
    with Session(engine) as session:
        chambre = session.scalars(
            select(Chambre).where(Chambre.numero_chambre == numero_chambre)
        ).first()
 
        if not chambre:
            raise ValueError(f"Aucune chambre trouvée avec le numéro {numero_chambre}.")
 
        
        nb_res = session.scalar(
            select(func.count(Reservation.id_reservation)).where(
                Reservation.fk_id_chambre == chambre.id_chambre
            )
        )
        if nb_res and nb_res > 0:
            raise ValueError(
                "Impossible de supprimer cette chambre : elle est associée à une ou plusieurs réservations."
            )
 
        session.delete(chambre)
        session.commit()
        return True
        

def modifierTypeChambre(typeChambre: TypeChambreDTO) -> TypeChambreDTO:
    
    with Session(engine) as session:
        existing = session.scalars(
            select(TypeChambre).where(TypeChambre.nom_type == typeChambre.nom_type)
        ).first()
 
        if not existing:
            raise ValueError(f"Le type de chambre '{typeChambre.nom_type}' n'existe pas.")
 
        if typeChambre.prix_plancher is not None and typeChambre.prix_plafond is not None:
            if typeChambre.prix_plancher > typeChambre.prix_plafond:
                raise ValueError("Le prix plancher doit être inférieur ou égal au prix plafond.")
 
        existing.description_chambre = typeChambre.description_chambre
        existing.prix_plancher = typeChambre.prix_plancher
        existing.prix_plafond = typeChambre.prix_plafond
 
        session.commit()
        session.refresh(existing)
 
        return TypeChambreDTO(existing)

    


def rechercherTypeChambreParNom(nom_type: str) -> TypeChambreDTO | None:
    with Session(engine) as session:
        result = session.scalars(
            select(TypeChambre).where(TypeChambre.nom_type == nom_type)
        ).first()
 
        if not result:
            return None

        return TypeChambreDTO(result)



