import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from uuid import UUID, uuid4

from .base import Base
from .usager import Usager



from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .chambre import Chambre
   


class Reservation(Base):
    __tablename__ = "reservation"

    date_debut_reservation : Mapped[datetime.datetime]
    date_fin_reservation : Mapped[datetime.datetime]
    prix_jour : Mapped[float]
    info_reservation : Mapped[str]
    id_reservation: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)

    fk_id_usager : Mapped[UUID] = mapped_column(ForeignKey("usager.id_usager"))
    fk_id_chambre: Mapped[UUID] = mapped_column(ForeignKey("chambre.id_chambre"))

    usager: Mapped['Usager'] = relationship()
    chambre: Mapped['Chambre'] = relationship('Chambre',back_populates='reservations')


   