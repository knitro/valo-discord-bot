import discord
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import constants
from valo_lineups_agent import check_agent
from valo_lineups_map import check_map
from valo_lineups_site import check_site

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

cred = credentials.Certificate("secrets/serviceAccountKey.json")
default_app = firebase_admin.initialize_app(cred)

# States
  # 0 = Awaiting Request
  # 1 = Awaiting Name
  # 2 = Image Position
  # 3 = Image Aim
  # 4 = Image Lineup Landing
  # 5 = Awaiting Cancel Operation
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
    print('We have logged in as {0.user}'.format(client))
 
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
        command_items = message.content.split(" ") # Index 0: !agent, 1: agent
        agent_input = command_items[1]
        
        is_valid, agent_output = check_agent(agent_input)
        if (is_valid):
            selected_agent = agent_output
            message_to_send = "Agent set to '" + agent_output + "'"
            await message.channel.send(message_to_send)
        else:
            message_to_send = "Agent '" + agent_input + "' is not a valid agent name"
            await message.channel.send(message_to_send)

    elif message.content.startswith("!map "):
        command_items = message.content.split(" ") # Index 0: !map, 1: map
        map_input = command_items[1]

        is_valid, map_output = check_map(map_input)
        if (is_valid):
            selected_map = map_output
            selected_site = ""
            message_to_send = "Map set to '" + map_output + "'. Please select a site." 
            await message.channel.send(message_to_send)
        else:
            message_to_send = "Map '" + map_output + "' is not a valid map name"
            await message.channel.send(message_to_send)

    elif message.content.startswith("!site "):
        command_items = message.content.split(" ") # Index 0: !site, 1: site
        site_input = command_items[1]

        is_valid, site_output = check_site(site_input, selected_map)
        if (is_valid):
            selected_site = site_output
            message_to_send = "Site set to '" + site_output + "'"
            await message.channel.send(message_to_send)
        else:
            message_to_send = "Site '" + map_input + "' is not a valid site on " + selected_map
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
            output_message = "Starting Lineup for '" + selected_agent + "' on '" + selected_map + "'\nInput a name for the Lineup:"
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
            output_message = "Are you sure you want to cancel your lineup creation for '" + selected_agent + "' on Site '" + selected_site + " for " + selected_map + "'"
            print(output_message)
            await message.channel.send(output_message)
        else:
            output_message = "You cannot cancel a lineup creation when there is no lineup currently being created."
            print(output_message)
            await message.channel.send(output_message)            

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
        output_message = "Selected Lineup Name: " + lineup_name + ".\nAdd Image for Lineup Position" 
        print(output_message)
        await message.channel.send(output_message)   

    print("State = " + str(state))

async def send_complete_lineup_info(message):
    global lineups_file_store
    global selected_agent
    global selected_map
    global selected_site
    global lineup_name
    global image_position_url
    global image_aim_url
    global image_landing_url

    # Add to File
    file = open(lineups_file_store, 'a')
    data_to_write = selected_agent + ", " + selected_map + ", " + selected_site + ", " + lineup_name + ", " + image_position_url + ", " + image_aim_url + ", " + image_landing_url
    file.write(data_to_write)
    file.write("\n") 
    file.close()

    # Send back copy paste information
    await message.channel.send(data_to_write)

    # Send to Firebase
    ref = firestore.reference("/")
    obj_to_send = {
        "map": selected_map,
        "site": selected_site,
        "agent": selected_agent,
        "name": lineup_name,
        "locationImage": image_position_url,
        "lineupImage": image_aim_url,
        "resultImage": image_landing_url,
    }
    ref.push().set(obj_to_send)

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


    

        