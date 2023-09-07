class Lineup:
    def __init__(
        self,
        agent,
        map,
        site,
        name,
        positioning_image_url,
        aim_image_url,
        landing_image_url,
    ):
        self.agent = agent
        self.map = map
        self.site = site
        self.name = name
        self.positioning_image_url = positioning_image_url
        self.aim_image_url = aim_image_url
        self.landing_image_url = landing_image_url

    def clearNameAndImages(self):
        self.name = ""
        self.positioning_image_url = ""
        self.aim_image_url = ""
        self.landing_image_url = ""

    def to_dict(self):
        return {
            "map": self.map,
            "site": self.site,
            "agent": self.agent,
            "name": self.name,
            "locationImage": self.positioning_image_url,
            "lineupImage": self.aim_image_url,
            "resultImage": self.landing_image_url,
        }

    def __str__(self):
        return (
            f"Agent: {self.agent}\n"
            f"Map: {self.map}\n"
            f"Site: {self.site}\n"
            f"Positioning Url: {self.positioning_image_url}\n"
            f"Aim Url: {self.aim_image_url}\n"
            f"Landing Url: {self.landing_image_url}"
        )
