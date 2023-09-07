async def send_help_message(message):
    output_message = (
        ""
        + "How the Valups Bot works\n"
        + "1. Set up agent, map and site that you want your lineups to be for. Note that these are not reset after each lineup creation.\n"
        + "2. Call the !lineup command and set your name of the lineup.\n"
        + "3. Paste your images for each prompt that provided inside the created thread.\n"
        + "Note that your agent, map and site settings are only set for you, and are not affected by other people creating lineups.\n"
        + "\n"
        + "Commands for the Valups Bot\n"
        + "!agent [agent]: Sets the Agent that you want to make linesup for.\n"
        + "!map [map]: Sets the map that you want to make linesup for.\n"
        + "!site {A, B, C}: Sets the site that you want to make linesup for. Note that it must be a site that is valid on the map.\n"
        + "!setup [agent] [map] [site]: Sets all agent, map and site. All valid values will be set, even if one parameter provided is invalid.\n"
        + "!lineup: Starts the lineup creation process. Requires agent, map and site to be set."
    )
    await message.reply(output_message)
