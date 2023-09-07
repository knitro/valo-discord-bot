import asyncio
import os
import requests

from classes.lineup import Lineup

save_directory = r"./lineup-images/"
do_download = True
authorised_users = ["knitr0"]


def setup_downloader():
    print("test")
    # opener = urllib.request.build_opener()
    # opener.addheaders = [("User-Agent", "Chrome")]
    # urllib.request.install_opener(opener)


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
    file_path = save_directory + file_name + file_extension

    isExist = os.path.exists(file_path)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(file_path)
        print("The new directory is created!")

    data = requests.get(image_url).content
    f = open(file_path, "wb")
    f.write(data)
    f.close()

    print("File '" + file_name + "' is saved at: " + file_path)


async def test_main():
    setup_downloader()
    await download_image(
        r"https://cdn.discordapp.com/attachments/1149320716106346496/1149320796217561158/image.png",
        "knitr0",
        "BRIMSTONE",
        "HAVEN",
        "C",
        "Long Post Plant",
        "location",
    )


if __name__ == "__main__":
    asyncio.run(test_main())
    # main(sys.argv[1])
