"""Adds lineups to the valups firebase

Usage:
    py valups_firebase.py map, site, agent, name, location_image_url, lineup_image_url, result_image_url
"""

import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore_async
import classes.lineup as lineup

global app
global db


def setup_firebase():
    global app
    global db

    cred = credentials.Certificate("secrets/serviceAccountKey.json")
    app = firebase_admin.initialize_app(cred)
    db = firestore_async.client()
    print("Firebase Setup Complete")


async def add_lineup_firestore(lineup):
    global db

    obj_to_send = lineup.to_dict()

    await db.collection("lineups").add(obj_to_send)
    print("Lineup '" + lineup.name + "' has been added to Firestore")


def main(
    map, site, agent, name, location_image_url, lineup_image_url, result_image_url
):
    """Adds a lineup to the associated firebase connection

    Args:
        map: the map the lineup is for
        site: the site the lineup is for
        agent: the agent the lineup is for
        name: the name of the lineup
        location_image_url: the image url of the position where you shoot your lineup
        lineup_image_url: the image url of the position where you aim to shoot your lineup
        result_image_url: the image url of the location where the lineup lands
    """
    setup_firebase()
    lineup_instance = lineup.Lineup(
        map, site, agent, name, location_image_url, lineup_image_url, result_image_url
    )
    add_lineup_firestore(lineup_instance)


if __name__ == "__main__":
    main(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3],
        sys.argv[4],
        sys.argv[5],
        sys.argv[6],
        sys.argv[7],
    )
