import urllib.request

save_directory = "/lineup-images/"
do_download = False
authorised_users = ["knitr0"]


async def download_lineup(lineup, message):
    lineup_actions = ["location", "aim", "landing"]
    for action in lineup_actions:
        image_url = ""
        match action:
            case "location":
                image_url = lineup.positioning_image_url
            case "aim":
                image_url = lineup.aim_image_url
            case "landing":
                image_url = lineup.landing_image_url

        user = message.author

        await download_image(
            image_url, user, lineup.agent, lineup.map, lineup.site, lineup.name, action
        )


async def download_image(image_url, user, agent, map, site, name, lineup_action):
    if not do_download:
        return

    if user not in authorised_users:
        return

    file_name = agent + "-" + map + "-" + site + "-" + name + "-" + lineup_action
    file_extension = ".png"
    file_save = save_directory + file_name + file_extension

    urllib.request.urlretrieve(image_url, file_save)

    print("File '" + file_name + "' is saved at: " + file_save)
