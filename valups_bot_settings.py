import discord
from classes.lineup import Lineup
from data.valups_agent import check_agent
from data.valups_map import check_map
from data.valups_site import check_site

dict = {}


def get_dict_entry(key):
    isKeyPresent = key in dict
    if not isKeyPresent:
        lineup = Lineup("", "", "", "", "", "", "", "")
        dict[key] = lineup
    return dict[key]


async def set_agent(agent_input, message):
    is_valid, agent_output = check_agent(agent_input)
    if is_valid:
        user = message.author
        user_data = get_dict_entry(user)
        user_data.agent = agent_output
        dict[user] = user_data

        message_to_send = "Agent set to '" + agent_output + "'"
        await message.reply.send(message_to_send)
    else:
        message_to_send = "Agent '" + agent_input + "' is not a valid agent name"
        await message.reply.send(message_to_send)


async def set_map(map_input, message):
    is_valid, map_output = check_map(map_input)
    if is_valid:
        user = message.author
        user_data = get_dict_entry(user)
        user_data.map = map_output
        user_data.site = ""
        dict[user] = user_data

        message_to_send = "Map set to '" + map_output + "'. Please select a site."
        await message.reply.send(message_to_send)
    else:
        message_to_send = "Map '" + map_output + "' is not a valid map name"
        await message.reply.send(message_to_send)


async def set_site(site_input, message):
    # Retrieve Stored "map" entry if it exists
    user = message.author
    user_data = get_dict_entry(user)
    user_map = user_data.map
    if user_map == "":
        message_to_send = "You have not set up the 'map' yet. Please use !site [map] to set the map first before setting the site."
        await message.reply.send(message_to_send)

    is_valid, site_output = check_site(site_input, user_map)
    if is_valid:
        user = message.author
        user_data = get_dict_entry(user)
        user_data.site = site_output
        dict[user] = user_data

        message_to_send = "Site set to '" + site_output + "'"
        await message.reply.send(message_to_send)
    else:
        message_to_send = "Site '" + user_map + "' is not a valid site on " + site_input
        await message.reply.send(message_to_send)


async def set_setup(agent_input, map_input, site_input, message):
    await set_agent(agent_input, message)
    await set_map(map_input, message)
    await set_site(site_input, message)


def check_user_can_start_lineup_creation(user):
    isKeyPresent = user in dict
    if not isKeyPresent:
        return (False, "The following variables are missing values { Agent Map Site }")

    user_lineup = dict[user]

    missing_values = ""

    if user_lineup.agent != "":
        missing_values += " Agent "
    if user_lineup.map != "":
        missing_values += " Map "
    if user_lineup.site != "":
        missing_values += " Site "

    if missing_values == "":
        # Reset any previous values that may have lingered
        user_lineup.positioning_image_url = ""
        user_lineup.aim_image_url = ""
        user_lineup.landing_image_url = ""

        # Check that user isn't already creating lineup. If so, remove that previous information
        if user_lineup.name != "":
            previous_name = user_lineup.name
            user_lineup.name = ""
            return (True, "Removing previous lineup creation data for " + previous_name)

        return (True, "")
    else:
        output_message = (
            "The following variables are missing values: {" + missing_values + "}"
        )
        return (False, output_message)


async def set_name(name_input, message):
    user = message.author
    user_data = get_dict_entry(user)
    user_data.name = name_input

    output_message = (
        "Selected Lineup Name: "
        + name_input
        + ".\nAdd Image for Lineup Position (where you shoot the lineup from)"
    )
    await message.reply.send(output_message)


async def set_positioning_image_url(positioning_url_input, message):
    user = message.author
    user_data = get_dict_entry(user)
    user_data.positioning_image_url = positioning_url_input

    output_message = "Add Image for Lineup Aim (where you aim to shoot your lineup from the position)"
    await message.reply.send(output_message)


async def set_aim_image_url(aim_url_input, message):
    user = message.author
    user_data = get_dict_entry(user)
    user_data.aim_image_url = aim_url_input

    output_message = "Add Image for Lineup Landing (where the lineup ends up)"
    await message.reply.send(output_message)


async def set_landing_image_url(landing_url_input, message):
    user = message.author
    user_data = get_dict_entry(user)
    user_data.landing_image_url = landing_url_input
    # No need to reply as this is the last image
