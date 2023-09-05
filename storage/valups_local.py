"""Adds lineups to a local file

Usage:
    py valups_local.py map, site, agent, name, location_image_url, lineup_image_url, result_image_url
"""

import sys
import lineup

lineups_file_store = "lineup_data.csv"


def setup_local():
    # Ensure local file exists
    file = open(lineups_file_store, "a")
    file.close()
    print("Local Storage Setup Complete")


def add_lineup_csv(lineup):
    data_to_write = (
        lineup.map,
        lineup.site,
        lineup.agent,
        lineup.name,
        lineup.positioning_image_url,
        lineup.aim_image_url,
        lineup.landing_image_url,
    )
    file = open(lineups_file_store, "a")
    file.write(data_to_write)
    file.write("\n")
    file.close()
    print("Lineup '" + lineup.map + "' has been added")


def main(
    map, site, agent, name, location_image_url, lineup_image_url, result_image_url
):
    """Adds a lineup to the local csv file

    Args:
        map: the map the lineup is for
        site: the site the lineup is for
        agent: the agent the lineup is for
        name: the name of the lineup
        location_image_url: the image url of the position where you shoot your lineup
        lineup_image_url: the image url of the position where you aim to shoot your lineup
        result_image_url: the image url of the location where the lineup lands
    """
    lineups_file_store()
    lineup_instance = lineup.Lineup(
        map, site, agent, name, location_image_url, lineup_image_url, result_image_url
    )
    add_lineup_csv(lineup_instance)


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
