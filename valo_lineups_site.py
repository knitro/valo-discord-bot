"""Checks if an site is valid on a Valorant map

Usage:
    py valo_lineups_site.py site
"""
import sys
def check_site(input, map):
    """Checks if a site input is valid or not based on the valorant map

    Args:
        input: the site string name to check against
        map: the map string name to check against

    Returns:
        A tuple (bool, str) where bool is if the map name is valid,
        and the str being the converted valid site name.
    """
    # Conforming to Uppercase Standard
    input_upper = input.upper()
    map_upper = map.upper()

    # Check against actual names
    maps_2_sites = [
        "BIND", "SPLIT", "ASCENT", "ICEBOX", "BREEZE", "FRACTURE", "PEARL"
    ]
    maps_3_sites = [
        "HAVEN", "LOTUS"
    ]
    for name in maps_2_sites:
        if name == map_upper: 
            if input_upper == "A" or input_upper == "B":
                return (True, input_upper)
        
    for name in maps_3_sites: 
        if name == map_upper: 
            if input_upper == "A" or input_upper == "B" or input_upper == "C":
                return (True, input_upper)

    # No matches at this point
    return (False, "")


def main(site_to_check, map_name_to_check_against):
    """Prints the outcome of a check_map call

    Args:
        site_to_check: the site to check
        map_name_to_check_against: the map name to check against
    """
    valid, updated_name = check_site(site_to_check, map_name_to_check_against)
    print_string = str(valid) + ": " + site_to_check + " -> " + updated_name + " on " + map_name_to_check_against
    print(print_string)

if __name__ == '__main__':
    main(sys.argv[1])
    

        