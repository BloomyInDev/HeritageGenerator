import os
from PIL import Image, ImageFont, ImageDraw
from utils.person import Person


class Font:
    small = ImageFont.truetype("./assets/DejaVuSans.ttf", 20)
    big = ImageFont.truetype("./assets/DejaVuSans.ttf", 30)


class PersonImage:
    def __init__(self, person: Person, prepare_image: bool = False) -> None:
        assert isinstance(person, Person)
        self.__img = Image.new("RGBA", (400, 250), (255, 255, 255, 0))
        self.__person = person
        if prepare_image:
            self.draw_image()
        pass

    def draw_image(self):
        draw_zone = ImageDraw.Draw(self.__img)
        color_outline = (30, 170, 255)
        draw_zone.rounded_rectangle((2, 2, 398, 248), 15, None, color_outline, 3)
        draw_zone.text((12, 6), self.__person.first_name, (0, 0, 0), Font.big)  # type: ignore
        draw_zone.text((12, 36), self.__person.name, (0, 0, 0), Font.big)  # type: ignore
        draw_zone.text((12, 196), self.__person.get_birth_str(), (0, 0, 0), Font.small)  # type: ignore
        draw_zone.text((12, 221), self.__person.get_death_str(), (0, 0, 0), Font.small)  # type: ignore

    def save(self):
        if not os.path.exists("./data"):
            os.mkdir("./data")
        if not os.path.exists("./data/cards"):
            os.mkdir("./data/cards")
        self.__img.save(f"./data/cards/{self.__person.id}{self.__person.first_name.lower()}.png", "PNG")
