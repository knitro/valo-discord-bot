import discord
import constants
from classes.lineup import Lineup
import storage.valups_local as valups_local
import storage.valups_firebase as valups_firebase
from valups_bot_settings import (
    check_user_can_start_lineup_creation,
    get_dict_entry,
    set_agent,
    set_aim_image_url,
    set_landing_image_url,
    set_map,
    set_name,
    set_positioning_image_url,
    set_setup,
    set_site,
)

intents = discord.Intents.all()
client = discord.Client(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    valups_firebase.setup_firebase()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print("Message Received from: " + message.author)

    if message.content.startswith("!agent "):
        command_items = message.content.split(" ")  # Index 0: !agent, 1: agent
        agent_input = command_items[1]
        set_agent(agent_input, message)
        return

    elif message.content.startswith("!map "):
        command_items = message.content.split(" ")  # Index 0: !map, 1: map
        map_input = command_items[1]
        set_map(map_input, message)
        return

    elif message.content.startswith("!site "):
        command_items = message.content.split(" ")  # Index 0: !site, 1: site
        site_input = command_items[1]
        set_site(site_input, message)
        return

    elif message.content.startswith("!setup"):
        command_items = message.content.split(" ")
        # Index 0: !setup, 2: agent, 3: map, 4: site
        agent_input = command_items[1]
        map_input = command_items[2]
        site_input = command_items[3]
        set_setup(agent_input, map_input, site_input, message)
        return

    elif message.content.startswith("!lineup"):
        can_start_lineup_creation, error_message = check_user_can_start_lineup_creation(
            message.author
        )
        if error_message != "":
            await message.reply.send(error_message)
        if not can_start_lineup_creation:
            return

        user_data = get_dict_entry(message.author)
        thread_name = message.author + "'s Lineup @ " + message.created_at
        thread = await message.create_thread(thread_name)
        output_message = (
            "Starting Lineup for '"
            + user_data.agent
            + "' on Site '"
            + user_data.site
            + "' of '"
            + user_data.map
            + "'\nInput a name for the Lineup:"
        )
        await thread.message.send(content=output_message)

    elif message.content.startswith("!lineupcsv "):
        message_prefix_removed = message.content.removeprefix("!lineupcsv ")
        lineup = process_csv_message_singular(message_prefix_removed)
        await send_lineup(lineup)


@client.event
async def on_thread(before, after):
    last_message = after.last_message
    if last_message == None:
        return
    if last_message.author == client.user:
        return

    if last_message.attachments:
        user = last_message.author
        current_lineup_entry = get_dict_entry(user)
        image_url = last_message.attachments[0].url

        if current_lineup_entry.positioning_image_url == "":
            await set_positioning_image_url(image_url, last_message)
        elif current_lineup_entry.aim_image_url == "":
            await set_aim_image_url(image_url, last_message)
        elif set_landing_image_url.landing_image_url == "":
            await set_positioning_image_url(image_url, last_message)
            # At this stage, all data should have been filled in
            await get_and_send_lineup(last_message)
    else:
        can_start_lineup_creation, error_message = check_user_can_start_lineup_creation(
            last_message.author
        )

        if can_start_lineup_creation:
            # At this point, must be name reply
            message_contents = after.last_message.content
            await set_name(message_contents)


def process_csv_message_singular(message):
    lineup_info = message.content.split(",")

    agent = lineup_info[0].strip(" ")
    map = lineup_info[1].strip(" ")
    site = lineup_info[2].strip(" ")
    name = lineup_info[3].strip(" ")
    image_position_url = lineup_info[4].strip(" ")
    image_aim_url = lineup_info[5].strip(" ")
    image_landing_url = lineup_info[6].strip(" ")

    lineup = Lineup(
        agent, map, site, name, image_position_url, image_aim_url, image_landing_url
    )
    return lineup


async def get_and_send_lineup(message):
    user = message.author
    lineup = await get_dict_entry(user)

    # Send to Storage
    valups_local.add_lineup_csv(lineup)
    valups_firebase.add_lineup_firestore(lineup)


async def send_lineup(lineup):
    valups_local.add_lineup_csv(lineup)
    valups_firebase.add_lineup_firestore(lineup)


client.run(constants.DISCORD_API_KEY)
