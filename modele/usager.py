from typing import List
 
from sqlalchemy.orm import Mapped, relationship, mapped_column
from uuid import UUID, uuid4
 
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .reservation import Reservation
 
from .base import Base    
 
 
class Usager(Base):
    __tablename__ = "usager"
 

 
    prenom : Mapped[str]
    nom : Mapped[str]
    adresse : Mapped[str]
    mobile : Mapped[str]
    mot_de_passe : Mapped[str]
    id_usager : Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
 
    reservations : Mapped[List["Reservation"]] = relationship('Reservation',back_populates="usager")


    
