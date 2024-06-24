from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
from sqlite3 import Error
from datetime import datetime


app = FastAPI()

DATABASE = "MSPR3.db"

# Configuration de la connexion à la base de données
def get_db_connection():
    try:
        connection = sqlite3.connect(DATABASE)
        connection.row_factory = sqlite3.Row
        return connection
    except Error as e:
        print(f"Error connecting to SQLite: {e}")
        return None

# Initialisation de la base de données pour les commandes
def init_db():
    connection = get_db_connection()
    if connection is None:
        print("Failed to connect to the database.")
        return
    try:
        cursor = connection.cursor()
        # Création de la table Commande
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Commande (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_produit INTEGER NOT NULL,
            id_client INTEGER NOT NULL,
            date DATETIME NOT NULL,
            quantite INTEGER NOT NULL,
            numero_commande TEXT NOT NULL,
            statut TEXT NOT NULL,
            FOREIGN KEY (id_produit) REFERENCES Product(id),
            FOREIGN KEY (id_client) REFERENCES Client(id)
        );
        """)
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        connection.close()

# Modèle de données pour la commande
class Commande(BaseModel):
    id: int
    id_produit: int
    id_client: int
    date: datetime
    quantite: int
    numero_commande: str
    statut: str

class CommandeCreate(BaseModel):
    id_produit: int
    id_client: int
    date: datetime
    quantite: int
    numero_commande: str
    statut: str

# Routes pour les commandes
@app.get("/commandes", response_model=List[Commande])
async def read_commandes():
    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Could not connect to the database")
    cursor = connection.cursor()
    cursor.execute("SELECT id, id_produit, id_client, date, quantite, numero_commande, statut FROM Commande")
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    commandes = [Commande(**dict(row)) for row in result]
    return commandes

@app.get("/commandes/{commande_id}", response_model=Commande)
async def read_commande(commande_id: int):
    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Could not connect to the database")
    cursor = connection.cursor()
    cursor.execute("SELECT id, id_produit, id_client, date, quantite, numero_commande, statut FROM Commande WHERE id = ?", (commande_id,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    if result:
        return Commande(**dict(result))
    else:
        raise HTTPException(status_code=404, detail="Commande not found")

@app.post("/commandes", response_model=Commande)
async def create_commande(commande: CommandeCreate):
    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Could not connect to the database")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO Commande (id_produit, id_client, date, quantite, numero_commande, statut) VALUES (?, ?, ?, ?, ?, ?)",
        (commande.id_produit, commande.id_client, commande.date, commande.quantite, commande.numero_commande, commande.statut)
    )
    connection.commit()
    commande_id = cursor.lastrowid
    cursor.close()
    connection.close()
    return Commande(id=commande_id, **commande.dict())

@app.put("/commandes/{commande_id}", response_model=Commande)
async def update_commande(commande_id: int, commande: CommandeCreate):
    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Could not connect to the database")
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE Commande SET id_produit = ?, id_client = ?, date = ?, quantite = ?, numero_commande = ?, statut = ? WHERE id = ?",
        (commande.id_produit, commande.id_client, commande.date, commande.quantite, commande.numero_commande, commande.statut, commande_id)
    )
    connection.commit()
    cursor.close()
    connection.close()
    return Commande(id=commande_id, **commande.dict())

@app.delete("/commandes/{commande_id}", response_model=dict)
async def delete_commande(commande_id: int):
    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Could not connect to the database")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Commande WHERE id = ?", (commande_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return {"message": "Commande deleted successfully"}

# Initialiser la base de données au démarrage
init_db()
