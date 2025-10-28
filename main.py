from fastapi import FastAPI, HTTPException
from metier.chambreMetier import creerChambre, creerTypeChambre, getChambreParNumero, ChambreDTO, TypeChambreDTO
from metier.reservationMetier import rechercherReservation
from DTO.reservationDTO import CriteresRechercheDTO
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
@app.get("/chambres/{no_chambre}")
def read_item(no_chambre: int):
    return getChambreParNumero(no_chambre)
    
@app.post("/creerTypeChambre")
def read_item(type: TypeChambreDTO):
    return creerTypeChambre(type)

@app.post("/rechercherReservation")
def read_item(critere: CriteresRechercheDTO):
    try:
        return rechercherReservation(critere)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))
    
@app.post("/creerChambre")
def read_item(chambre: ChambreDTO):
    return creerChambre(chambre)

uvicorn.run(app, host="127.0.0.1", port=8000)  