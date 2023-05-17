from collections import defaultdict


class ModelMeta(defaultdict):
    pass


class ApiMetaModel(type):
    def __new__(cls, name, bases, dct):
        print(name)
        print(bases)
        x = super().__new__(cls, name, bases, dct)
        print(x)
        return x


class ApiModel(metaclass=ApiMetaModel):
    pass


class TextField:
    def __init__(self, read_field=None, write_field=None):
        self.read_field = read_field
        self.write_field = write_field

    def __set__(self, instance, value):
        print("Worked set method")
        setattr(instance, self.private_field_name, str(value).capitalize())

    def __set_name__(self, owner, name):
        self.private_field_name = f"_{name}"
        print(self.private_field_name)

    def __get__(self, obj, objtype=None):
        print("Worked get")
        value = getattr(obj, self.private_field_name)
        return value

    def validate(self):
        pass


class PrimaryIntegerField:
    pass


class EmailField:
    pass


class PasswordField:
    pass


class DateTimeField:
    pass


class User(ApiModel):
    id = PrimaryIntegerField(read_field=True)
    name = TextField(write_field=True)
    email = EmailField(write_field=True)
    password = PasswordField(write_field=True)
    created_date = DateTimeField(read_field=True)
    last_login = DateTimeField(read_field=True)

    def __init__(self, name=None):
        self.name = name if name else None

    def save(self):
        pass

    class Meta:
        service_url = "https://user-servie.main.com"
        endpoint = "users"
        version = "v1"


user = User("Vasya")
print(user.name)
