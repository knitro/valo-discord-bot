import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import lineup

global app
global db


def setup_firebase():
    cred = credentials.Certificate("secrets/serviceAccountKey.json")
    app = firebase_admin.initialize_app(cred)
    db = firestore.client()


def add_lineup_firestore(lineup):
    global db
    update_time, city_ref = db.collection("lineups").add(lineup)
