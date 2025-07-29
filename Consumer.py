# consumer.py
from kafka import KafkaConsumer
import json
import sqlite3
from sqlite3 import Error

consumer = KafkaConsumer(
    'order_topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)


# def update_product_quantity(product_id, quantity):
#     db = SessionLocal()
#     product = db.query(Product).filter(Product.id == product_id).first()
#     if product:
#         product.quantity -= quantity
#         db.commit()
#         db.refresh(product)
#     db.close()
#     connection = get_db_connection()
#     if connection is None:
#         raise HTTPException(status_code=500, detail="Could not connect to the database")
#     cursor = connection.cursor()
#     cursor.execute("UPDATE Product SET name = ?, description = ?, price = ?, quantity = ? WHERE id = ?", (product.name, product.description, product.price, product.quantity, product_id))
#     connection.commit()
#     cursor.close()
#     connection.close()


# for message in consumer:
#     order_data = message.value
#     update_product_quantity(order_data['product_id'], order_data['quantity'])


# Fonction pour mettre à jour la quantité de produit
def update_product_quantity(product_id, quantity):
    # Connexion à la base de données SQLite
    conn = sqlite3.connect('MSPR.db')
    cursor = conn.cursor()
    
    # Récupérer les informations actuelles du produit
    cursor.execute("SELECT * FROM Product WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    print(f"Product { product[4]} ")
    if product:
        # Calculer la nouvelle quantité
        new_quantity = product[4] - quantity
        
        # Mise à jour de la quantité dans la base de données
        cursor.execute("UPDATE Product SET quantity = ? WHERE id = ?", (new_quantity, product_id))
        conn.commit()
    
    # Fermeture de la connexion à la base de données
    conn.close()

# Consommer les messages du topic
for message in consumer:
    order_data = message.value
    update_product_quantity(order_data['product_id'], order_data['quantite'])
    print(f"Updated product {order_data['product_id']} with new quantity after order: {order_data['quantite']}")