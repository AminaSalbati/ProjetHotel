import unittest
from sqlalchemy.orm import Session 
from sqlalchemy import create_engine, select, func
from modele.chambre import Chambre
from modele.reservation import Reservation


engine = create_engine('mssql+pyodbc://localhost\\SQLEXPRESS/Hotel?driver=ODBC+Driver+17+for+SQL+Server', use_setinputsizes=False)
Room_Num = 101


class test_reservation(unittest.TestCase):
    def test_chambre(self):
        with Session(engine) as session:
            stmt = select(Chambre).where(Chambre.numero_chambre == Room_Num)
            chambre = session.execute(stmt).scalars().first()
            
        
           
            self.assertIsNotNone(chambre, f"Chambre {Room_Num} doit exister sans la base de données.")
 
            
            self.assertEqual(chambre.numero_chambre, Room_Num)

    def test_reservation_chambre(self):
        with Session(engine) as session:
            req= select(func.count(Reservation.id_reservation)).join(Chambre, Reservation.fk_id_chambre == Chambre.id_chambre).where(Chambre.numero_chambre == 101)  
            nb_reservations = session.execute(req).scalar_one()

            self.assertGreaterEqual(
                nb_reservations, 2,
                f"La chambre {Room_Num} doit avoir au moins deux réservations, trouvé: {nb_reservations}"
            )  
            
                   
         

            
            
           
   
