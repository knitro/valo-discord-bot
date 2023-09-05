import discord
import constants
from lineup import Lineup
from valo_lineups_agent import check_agent
from valo_lineups_map import check_map
from valo_lineups_site import check_site
import storage.valups_local as valups_local
import storage.valups_firebase as valups_firebase

intents = discord.Intents.all()
client = discord.Client(command_prefix="!", intents=intents)

# States
# 0 = Awaiting Request
# 1 = Awaiting Name
# 2 = Image Position
# 3 = Image Aim
# 4 = Image Lineup Landing
# 5 = Awaiting Cancel Operation
# 6 = Awaiting Full Lineup String
state = 0
selected_agent = "BRIMSTONE"
selected_map = "HAVEN"
selected_site = "C"
lineup_name = ""
image_position_url = ""
image_aim_url = ""
image_landing_url = ""
previous_state = 0
lineups_file_store = "lineup_data.csv"


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    valups_firebase.setup_firebase()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    global state
    global selected_agent
    global selected_map
    global selected_site

    print("Message Received")

    if message.content.startswith("!agent "):
        command_items = message.content.split(" ")  # Index 0: !agent, 1: agent
        agent_input = command_items[1]

        is_valid, agent_output = check_agent(agent_input)
        if is_valid:
            selected_agent = agent_output
            message_to_send = "Agent set to '" + agent_output + "'"
            await message.channel.send(message_to_send)
        else:
            message_to_send = "Agent '" + agent_input + "' is not a valid agent name"
            await message.channel.send(message_to_send)

    elif message.content.startswith("!map "):
        command_items = message.content.split(" ")  # Index 0: !map, 1: map
        map_input = command_items[1]

        is_valid, map_output = check_map(map_input)
        if is_valid:
            selected_map = map_output
            selected_site = ""
            message_to_send = "Map set to '" + map_output + "'. Please select a site."
            await message.channel.send(message_to_send)
        else:
            message_to_send = "Map '" + map_output + "' is not a valid map name"
            await message.channel.send(message_to_send)

    elif message.content.startswith("!site "):
        command_items = message.content.split(" ")  # Index 0: !site, 1: site
        site_input = command_items[1]

        is_valid, site_output = check_site(site_input, selected_map)
        if is_valid:
            selected_site = site_output
            message_to_send = "Site set to '" + site_output + "'"
            await message.channel.send(message_to_send)
        else:
            message_to_send = (
                "Site '" + map_input + "' is not a valid site on " + selected_map
            )
            await message.channel.send(message_to_send)

    elif message.content.startswith("!lineup"):
        if selected_agent == "" or selected_map == "" or selected_site == "":
            output_message = "The following variables are missing values: {"
            if selected_agent == "":
                output_message += " Agent "
            if selected_map == "":
                output_message += " Map "
            if selected_site == "":
                output_message += " Site "
            output_message += "}"
            print(output_message)
        if state == 0:
            output_message = (
                "Starting Lineup for '"
                + selected_agent
                + "' on '"
                + selected_map
                + "'\nInput a name for the Lineup:"
            )
            state = 1
            print(output_message)
            await message.channel.send(output_message)
        else:
            output_message = "You are still in a lineup creation process. Type '!cancel' if you want to stop creation of a lineup."
            await message.channel.send(output_message)

    elif message.content.startswith("!cancel"):
        if state != 0:
            global previous_state
            previous_state = state
            state = 5
            output_message = (
                "Are you sure you want to cancel your lineup creation for '"
                + selected_agent
                + "' on Site '"
                + selected_site
                + " for "
                + selected_map
                + "'"
            )
            print(output_message)
            await message.channel.send(output_message)
        else:
            output_message = "You cannot cancel a lineup creation when there is no lineup currently being created."
            print(output_message)
            await message.channel.send(output_message)

    elif message.content.startswith("!fulllineup"):
        state = 6
        output_message = "Add your singular lineup in csv form:"
        print(output_message)
        await message.channel.send(output_message)

    elif state == 6:
        print("Parsing CSV Lineup Info")
        await process_csv_message_singular(message)
        await send_complete_lineup_info(message)

    elif message.attachments:
        attachment_url = message.attachments[0].url
        if state == 2:
            # 2 = Image Location
            global image_position_url
            image_position_url = attachment_url
            state = 3
            output_message = "Add Image for Lineup Aim"
            print(output_message)
            await message.channel.send(output_message)
        elif state == 3:
            # 3 = Image Aim
            global image_aim_url
            image_aim_url = attachment_url
            state = 4
            output_message = "Add Image for Lineup Landing"
            print(output_message)
            await message.channel.send(output_message)
        elif state == 4:
            # 4 = Image Lineup Landing
            global image_landing_url
            image_landing_url = attachment_url
            state = 0
            await send_complete_lineup_info(message)

    elif state == 1:
        global lineup_name
        lineup_name = message.content
        state = 2
        output_message = (
            "Selected Lineup Name: " + lineup_name + ".\nAdd Image for Lineup Position"
        )
        print(output_message)
        await message.channel.send(output_message)

    print("State = " + str(state))


async def process_csv_message_singular(message):
    global selected_agent
    global selected_map
    global selected_site
    global lineup_name
    global image_position_url
    global image_aim_url
    global image_landing_url

    lineup_info = message.content.split(",")
    print(lineup_info)
    selected_agent = lineup_info[0].strip(" ")
    selected_map = lineup_info[1].strip(" ")
    selected_site = lineup_info[2].strip(" ")
    lineup_name = lineup_info[3].strip(" ")
    image_position_url = lineup_info[4].strip(" ")
    image_aim_url = lineup_info[5].strip(" ")
    image_landing_url = lineup_info[6].strip(" ")


async def send_complete_lineup_info(message):
    global lineups_file_store
    global selected_agent
    global selected_map
    global selected_site
    global lineup_name
    global image_position_url
    global image_aim_url
    global image_landing_url

    lineup = Lineup(
        selected_agent,
        selected_map,
        selected_site,
        lineup_name,
        image_position_url,
        image_aim_url,
        image_landing_url,
    )

    # Send to Storage
    valups_local.add_lineup_csv(lineup)
    valups_firebase.add_lineup_firestore(lineup)

    # Cleanup
    reset_lineup_variables()


def reset_lineup_variables():
    global lineup_name
    global image_position_url
    global image_aim_url
    global image_landing_url

    lineup_name = ""
    image_position_url = ""
    image_aim_url = ""
    image_landing_url = ""


def reset_all_variables():
    global selected_agent
    global selected_map
    global selected_site
    global lineup_name
    global image_position_url
    global image_aim_url
    global image_landing_url

    selected_agent = ""
    selected_map = ""
    selected_site = ""
    lineup_name = ""
    image_position_url = ""
    image_aim_url = ""
    image_landing_url = ""


client.run(constants.DISCORD_API_KEY)
