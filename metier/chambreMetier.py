from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from DTO.chambreDTO import ChambreDTO, TypeChambreDTO
from modele.chambre import Chambre, TypeChambre

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