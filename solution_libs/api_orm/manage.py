from enum import Enum


class RequestMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    PUT = "PUT"
    PATCH = "PATH"


class EmailField:
    pass


class StatusField:
    pass


class DateTimeField:
    pass


class User:
    email = EmailField()
    status = StatusField()
    created_date = DateTimeField()
    last_login = DateTimeField()

    # def register(self, password1, password2):
    #     data = self.get_write_data()
    #     self.request_manager.register()
    #
    # def get_write_data(self):
    #     write_field_names = self._meta.write_fields

    class Meta:
        service_endpoint = "https://user.service.com"
        resource_endpoint = "user"

        create_endpoint = {"method": "POST", "url": None}

        update_endpoint = {"method": "POST", "url": None}

        delete_endpoint = {"method": "POST", "url": None}

        register_endpoint = {"method": "POST", "url": "register"}


class RequestQueryBuilder:
    def __init__(self, client):
        self.client = client

    def filter(self, **kwargs):
        return self

    def limit(self, limit: int):
        return self

    def params(self, **kwargs):
        return self


class RequestOperation:
    def __init__(self, method, data, endpoint, client, model_cls=None, plain_data=False):
        self.model_cls = model_cls
        self.endpoint = endpoint
        self.method = method
        self.data = data
        self.client = client
        self.plain_data = plain_data

    def run(self):
        if not self.plain_data and not self.model_cls:
            raise Exception(
                "Making a operation call for to Api without model class or not set plain_data to True can't be done"
            )

        result = self.client.call(self.method, self.data)

        if self.plain_data:
            return result

        return self.model_cls(**result)


class RequestManager:
    def __init__(self, model=None, client=None):
        self._client = client
        self._model = model

    def get_request_query(self):
        return RequestQueryBuilder(self._client)

    def get(self, **kwargs):
        return self.get_request_query().filter(**kwargs).limit(1).params(single_response=True)

    def create(self, **kwargs):
        return RequestOperation(
            model_cls=self._model,
            endpoint=self._model.meta.get_create_url(),
            method=RequestMethod.POST,
            data=kwargs,
            client=self._client,
        )

    def update(self, **kwargs):
        return RequestOperation(
            model_cls=self._model,
            endpoint=self._model.meta.get_update_url(),
            method=RequestMethod.PATCH,
            data=kwargs,
            client=self._client,
        )

    def delete(self, **kwargs):
        return RequestOperation(
            model_cls=self._model,
            endpoint=self._model.meta.get_update_url(),
            method=RequestMethod.PATCH,
            data=kwargs,
            client=self._client,
        )


# email = 'test@gmail.com'
#
# products_id = [1, 2, 3, 4]
# user_request = User.request_manager.get_user(email=email)
#
# UserOrder.request_manager.filter(user=user_request).limit(100)
# products.request_manager.filter(pk__in=products_id)
#
#
#
# UserOrder.request_manager.create(
#     user=user_request,
#     products=products_id,
#     address=address,
#     payment_method=UserOrder.PAYMENTS_METHOD.CREDIT_CARD,
#     status=UserOrder.STATUSES.CREATED
# )
#
# User.request_manager.create(
#     email='test@gamil.com',
#     password1='123123',
#     password2='123123'
# )
