import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import lineup

global app
global db


def setup_firebase():
    global app
    global db

    cred = credentials.Certificate("secrets/serviceAccountKey.json")
    app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firebase Setup Complete")


def add_lineup_firestore(lineup):
    global db

    obj_to_send = {
        "map": lineup.map,
        "site": lineup.site,
        "agent": lineup.agent,
        "name": lineup.name,
        "locationImage": lineup.positioning_image_url,
        "lineupImage": lineup.aim_image_url,
        "resultImage": lineup.landing_image_url,
    }

    update_time, city_ref = db.collection("lineups").add(obj_to_send)
