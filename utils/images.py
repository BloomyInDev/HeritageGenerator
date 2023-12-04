import os
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from utils.person import Person, Family


class Font:
    small = ImageFont.truetype("./assets/DejaVuSans.ttf", 40)
    medium = ImageFont.truetype("./assets/DejaVuSans.ttf", 50)
    big = ImageFont.truetype("./assets/DejaVuSans.ttf", 60)
    really_big = ImageFont.truetype("./assets/DejaVuSans.ttf", 70)


class PersonCard:
    def __init__(self, person: Person, image: str = "./assets/person.png", prepare_image: bool = False) -> None:
        assert isinstance(person, Person)
        assert isinstance(image, str)
        assert os.path.isfile(image)
        self.__img = Image.new("RGBA", (800, 500), (255, 255, 255, 0))
        self.__img_person = image
        self.__person = person
        if prepare_image:
            self.draw_image()
        pass

    def draw_image(self):
        if self.__img_person == "./assets/person.png":
            img_default = Image.open(self.__img_person)
            self.__img.paste(img_default, (796 - img_default.size[0], 4))
        else:
            pass
        draw_zone = ImageDraw.Draw(self.__img)
        color_outline = (30, 170, 255)
        draw_zone.rounded_rectangle((4, 4, 796, 496), 45, None, color_outline, 6)
        draw_zone.text((24, 12), self.__person.first_name, (0, 0, 0), Font.big)  # type: ignore
        draw_zone.text((24, 72), self.__person.name, (0, 0, 0), Font.big)  # type: ignore
        if self.__person.old_name != None:
            draw_zone.text((24, 132), f"({self.__person.old_name})", (0, 0, 0), Font.medium)  # type: ignore
        if self.__person.job != None:
            draw_zone.text((24, 342), self.__person.job, (0, 0, 0), Font.small)  # type: ignore
        draw_zone.text((24, 392), self.__person.get_birth_str(), (0, 0, 0), Font.small)  # type: ignore
        draw_zone.text((24, 442), self.__person.get_death_str(), (0, 0, 0), Font.small)  # type: ignore

    def save(self):
        if not os.path.exists("./data"):
            os.mkdir("./data")
        if not os.path.exists("./data/cards"):
            os.mkdir("./data/cards")
        self.__img.save(f"./data/cards/p{self.__person.id}{self.__person.first_name.lower()}.png", "PNG")


class ProfilePicture:
    def __init__(self, img: str, person: Person, prepare_image: bool = False) -> None:
        assert isinstance(person, Person)
        assert os.path.isfile(img)
        self.__img_obj = Image.open(img)
        self.__person = person
        if prepare_image:
            self.draw_image()
        pass

    def draw_image(self):
        self.__img_obj.thumbnail((150, 194), Image.Resampling.LANCZOS)
        mask = Image.new("L", self.__img_obj.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle(((2, 2), (self.__img_obj.size[0] - 2, self.__img_obj.size[1] - 2)), radius=15, outline=255, fill=255, width=3)
        new_img_obj = Image.new("RGBA", self.__img_obj.size, (0, 0, 0, 0))
        new_img_obj.paste(self.__img_obj, (0, 0), mask.filter(ImageFilter.GaussianBlur(2)))
        self.__img_obj = new_img_obj

    def save(self):
        if not os.path.exists("./data"):
            os.mkdir("./data")
        if not os.path.exists("./data/pp"):
            os.mkdir("./data/pp")
        self.__img_obj.save(f"./data/pp/{self.__person.id}{self.__person.first_name.lower()}.png", "PNG")


class FamilyCard:
    def __init__(self, family: Family, prepare_image: bool = False) -> None:
        assert isinstance(family, Family)
        self.__family = family
        self.__img: Image.Image
        if prepare_image:
            self.draw_image()
        pass

    def draw_image(self):
        img: Image.Image
        if self.__family.get_divorce_date() == None:
            # Still together (except one dead)
            img = Image.open("./assets/love.png")
        else:
            img = Image.open("./assets/deadlove.png")
        wedding_width = get_text_width(self.__family.get_wedding_str(), Font.medium)
        divorce_width = get_text_width(self.__family.get_divorce_str(), Font.medium)
        width_needed = [wedding_width, divorce_width]
        width_needed.sort()
        self.__img = Image.new(
            "RGBA",
            (width_needed[1] + 64 if width_needed[1] <= 64 else width_needed[1], 68 + (106 if (self.__family.get_wedding_str() != "") or (self.__family.get_divorce_str() != "") else 0)),
            (255, 255, 255, 0),
        )
        self.__img.paste(img, ((self.__img.width // 2) - (img.width // 2), 0))
        draw_zone = ImageDraw.Draw(self.__img)
        draw_zone.text(((self.__img.width // 2) - (wedding_width // 2), 66), self.__family.get_wedding_str(), (0, 0, 0), Font.medium)  # type: ignore
        draw_zone.text(((self.__img.width // 2) - (wedding_width // 2), 118), self.__family.get_divorce_str(), (0, 0, 0), Font.medium)  # type: ignore

    def save(self):
        if not os.path.exists("./data"):
            os.mkdir("./data")
        if not os.path.exists("./data/cards"):
            os.mkdir("./data/cards")
        self.__img.save(f"./data/cards/f{self.__family.id}.png", "PNG")


def get_text_width(text: str, font: ImageFont.FreeTypeFont) -> int:
    if text == "":
        return 0
    width = len(text) * 100
    height = 150
    back_ground_color = (0, 0, 0)
    font_color = (255, 255, 255)

    im: Image.Image = Image.new("RGB", (width, height), back_ground_color)
    draw = ImageDraw.Draw(im)
    draw.text((0, 0), text, font=font, fill=font_color)  # type: ignore
    im.save("./data/temp.png")
    box: tuple[int, int, int, int] = Image.open("./data/temp.png").getbbox()  # type: ignore
    return box[2] - box[0]
