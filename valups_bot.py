import sys
import discord
import constants
from classes.lineup import Lineup
import storage.valups_local as valups_local
import storage.valups_firebase as valups_firebase
from valups_bot_settings import (
    check_user_can_start_lineup_creation,
    clear_image_cache,
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
from valups_help import send_help_message
import valups_downloader

intents = discord.Intents.all()
client = discord.Client(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    valups_url = "http://valups.web.app/"
    activity = discord.Activity(
        type=discord.ActivityType.streaming, name="!help", url=valups_url
    )
    await client.change_presence(status=discord.Status.online, activity=activity)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print("Message Received from: " + message.author.display_name)

    if type(message.channel) == discord.Thread:
        print("Update on Thread: " + message.channel.name)
        await thread_update(message)

    elif message.content.startswith("!agent "):
        command_items = message.content.split(" ")  # Index 0: !agent, 1: agent
        agent_input = command_items[1]
        await set_agent(agent_input, message)
        return

    elif message.content.startswith("!map "):
        command_items = message.content.split(" ")  # Index 0: !map, 1: map
        map_input = command_items[1]
        await set_map(map_input, message)
        return

    elif message.content.startswith("!site "):
        command_items = message.content.split(" ")  # Index 0: !site, 1: site
        site_input = command_items[1]
        await set_site(site_input, message)
        return

    elif message.content.startswith("!setup"):
        command_items = message.content.split(" ")
        # Index 0: !setup, 2: agent, 3: map, 4: site
        agent_input = command_items[1]
        map_input = command_items[2]
        site_input = command_items[3]
        await set_setup(agent_input, map_input, site_input, message)
        return

    elif message.content.startswith("!lineup"):
        can_start_lineup_creation, error_message = check_user_can_start_lineup_creation(
            message.author
        )
        if error_message != "":
            await message.reply(error_message)
        if not can_start_lineup_creation:
            return

        user_data = get_dict_entry(message.author)
        thread_name = (
            message.author.display_name
            + "'s Lineup @ "
            + message.created_at.strftime("%m/%d/%Y, %H:%M:%S")
        )
        thread = await message.create_thread(name=thread_name, auto_archive_duration=60)
        output_message = (
            "Starting Lineup for '"
            + user_data.agent
            + "' on Site '"
            + user_data.site
            + "' of '"
            + user_data.map
            + "'\nInput a name for the Lineup:"
        )
        await thread.send(content=output_message)

    elif message.content.startswith("!lineupcsv "):
        message_prefix_removed = message.content.removeprefix("!lineupcsv ")
        lineup = process_csv_message_singular(message_prefix_removed)
        await send_lineup(lineup)

    elif message.content.startswith("!help"):
        await send_help_message(message)


async def thread_update(message):
    if message == None:
        return
    if message.author == client.user:
        return

    if message.attachments:
        user = message.author
        current_lineup_entry = get_dict_entry(user)
        image_url = message.attachments[0].url

        if current_lineup_entry.positioning_image_url == "":
            await set_positioning_image_url(image_url, message)
        elif current_lineup_entry.aim_image_url == "":
            await set_aim_image_url(image_url, message)
        elif current_lineup_entry.landing_image_url == "":
            await set_landing_image_url(image_url, message)
            # At this stage, all data should have been filled in
            await get_and_send_lineup(message)
    else:
        can_start_lineup_creation, error_message = check_user_can_start_lineup_creation(
            message.author
        )

        if can_start_lineup_creation:
            # At this point, must be name reply
            message_contents = message.content
            await set_name(message_contents, message)


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
    lineup = get_dict_entry(user)

    # Send to Storage
    await send_lineup(lineup)

    # Send Success Message
    await message.reply("Success! Your lineup has been added")

    # Download Images
    await valups_downloader.download_lineup(lineup, message)

    # Remove saved images
    clear_image_cache(user)


async def send_lineup(lineup):
    valups_local.add_lineup_csv(lineup)
    await valups_firebase.add_lineup_firestore(lineup)


def main():
    print("Started: Valups Bot Main")
    valups_firebase.setup_firebase()

    client.run(constants.DISCORD_API_KEY)
    print("Finished: Valups Bot Main")


if __name__ == "__main__":
    main()
