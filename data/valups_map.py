"""Checks if an map supplied is a valid Valorant map

Usage:
    py valo_lineups_map.py map
"""
import sys


def check_map(input):
    """Checks if an map input is valid or not

    Args:
        input: the map string name to check against

    Returns:
        A tuple (bool, str) where bool is if the map name is valid,
        and the str being the converted valid map name.
    """
    # Conforming to Uppercase Standard
    input_upper = input.upper()

    # Check against actual names
    maps = [
        "BIND",
        "HAVEN",
        "SPLIT",
        "ASCENT",
        "ICEBOX",
        "BREEZE",
        "FRACTURE",
        "PEARL",
        "LOTUS",
        "SUNSET",
    ]
    for name in maps:
        if input_upper == name:
            return (True, input_upper)

    # No matches at this point
    return (False, "")


def main(map_name_to_check):
    """Prints the outcome of a check_map call

    Args:
        map_name_to_check: the map name to check
    """
    valid, updated_name = check_map(map_name_to_check)
    print_string = str(valid) + ": " + map_name_to_check + " -> " + updated_name
    print(print_string)


if __name__ == "__main__":
    main(sys.argv[1])
