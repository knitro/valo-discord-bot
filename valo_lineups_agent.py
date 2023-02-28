"""Checks if an agent supplied is a valid Valorant Agent

Usage:
    py valo_lineups_agent.py agent
"""
import sys
def check_agent(input):
    """Checks if an agent input is valid or not

    Args:
        input: the agent string name to check against

    Returns:
        A tuple (bool, str) where bool is if the agent name is valid,
        and the str being the converted valid agent name.
    """
    # Conforming to Uppercase Standard
    input_upper = input.upper()

    # Check against actual names
    agents = [
        "BRIMSTONE", "VIPER", "OMEN", "KILLJOY", "CYPHER",
        "SOVA", "SAGE", "PHOENIX", "JETT", "REYNA", "RAZE",
        "BREACH", "SKYE", "YORU", "ASTRA", "KAYO", "CHAMBER",
        "NEON", "FADE", "HARBOR"
    ]
    for name in agents:
        if input_upper == name:
            return (True, input_upper)
    
    # Check against "misspellings" of agents
    brimstone_misspells = ["BRIM"]
    for name in brimstone_misspells:
        if input_upper == name:
            return (True, "BRIMSTONE")

    kayo_misspells = ["KAY0", "KAY/O", "KAY/0"]
    for name in kayo_misspells:
        if input_upper == name:
            return (True, "KAYO")

    killjoy_misspells = ["KJ"]
    for name in killjoy_misspells:
        if input_upper == name:
            return (True, "KILLJOY")

    # No matches at this point
    return (False, "")


def main(agent_name_to_check):
    """Prints the outcome of a check_agent call

    Args:
        agent_name_to_check: the agent name to check
    """
    valid, updated_name = check_agent(agent_name_to_check)
    print_string = str(valid) + ": " + agent_name_to_check + " -> " + updated_name
    print(print_string)

if __name__ == '__main__':
    main(sys.argv[1])
    

        