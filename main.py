from typing import Annotated
from pydantic import BaseModel
 
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from metier.chambreMetier import creerChambre, creerTypeChambre, getChambreParNumero, ChambreDTO, TypeChambreDTO
from metier.reservationMetier import rechercherReservation
from DTO.reservationDTO import CriteresRechercheDTO
import uvicorn
 
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret"
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2"
    },
}
 
app = FastAPI()
 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
   
@app.get("/chambres/{no_chambre}")
def read_item(no_chambre: int):
    return getChambreParNumero(no_chambre)
   
@app.post("/creerTypeChambre")
def read_item(type: TypeChambreDTO):
    return creerTypeChambre(type)
   
@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
 
    return {"access_token": user.username, "token_type": "bearer"}
 
def fake_hash_password(password: str):
    return "fakehashed" + password
 
def fake_decode_token(token):
    # TODO : Implémenter un vrai token
    user = get_user(fake_users_db, token)
    return user
 
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
 
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
 
class UserInDB(User):
    hashed_password: str
 
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
 
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