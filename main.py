from typing import Annotated
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException,Depends,status
from metier.chambreMetier import creerChambre, creerTypeChambre, getChambreParNumero, ChambreDTO, TypeChambreDTO
from metier.reservationMetier import rechercherReservation
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from DTO.reservationDTO import CriteresRechercheDTO
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


fake_users_db = {
    "houssam": {
        "username": "houssam",
        "full_name": "Houssam Broumi",
        "email": "houssam@broumi.com",
        "hashed_pasword": "secret1"
    },
    "amina": {
        "username": "amina",
        "full_name": "Amina Salbati",
        "email": "amina@salbati.com",
        "hashed_pasword": "secret2" 
    },
}


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    
@app.get("/chambres/{no_chambre}")
def read_item(no_chambre: int):
    return getChambreParNumero(no_chambre)

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username,"token_type": "bearer"}

def fake_hash_password(password: str):
    return "fakehashed" + password

def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None

class User(BaseModel):
    username : str
    email: str | None = None
    full_name: str | None = None

class UserInDB(User):
    hashed_password : str

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentification credntials",
            headers={"WWW-Aurhentificate": "Bearer"},
        )   
    return user


@app.post("/creerTypeChambre")
def read_item(type: TypeChambreDTO, current_user: Annotated[User,Depends(get_current_user)]):
    return creerTypeChambre(type)

@app.post("/rechercherReservation")
def read_item(critere: CriteresRechercheDTO, current_user: Annotated[User, Depends(get_current_user)]):
    try:
        return rechercherReservation(critere)
    except ValueError as e:
        return HTTPException(status_code=404, detail=str(e))
    
@app.post("/creerChambre")
def read_item(chambre: ChambreDTO, current_user: Annotated[User, Depends(get_current_user)]):
    return creerChambre(chambre)

uvicorn.run(app, host="127.0.0.1", port=8000)  