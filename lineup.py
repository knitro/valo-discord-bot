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
