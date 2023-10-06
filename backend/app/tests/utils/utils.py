from faker import Faker


class FakeData:
    """產生隨機測試資料"""

    def __init__(self, locale: str = "en_US"):
        self.fake = Faker(locale=locale)

    def random_string(self, string_lenght: int = 32) -> str:
        return self.fake.text(max_nb_chars=string_lenght)

    def random_email(self) -> str:
        return self.fake.ascii_email()

    def random_url(self) -> str:
        return self.fake.url()

    def random_lorem(self, nb_sentences: int = 3) -> str:
        return self.fake.paragraph(nb_sentences=nb_sentences)

    def random_int(self, min: int = 0, max: int = 10) -> int:
        return self.fake.random_int(min=min, max=max)

    def random_username(self) -> str:
        return self.fake.name()

    def random_city(self) -> str:
        return self.fake.city()
