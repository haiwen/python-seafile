from seafileapi.utils import utf8lize

class Account(object):
    """
    A seafile account
    """
    def __init__(self, client, id, email, create_time, is_active, is_staff, usage, total):
        self.client = client
        self.id = id
        self.email = email
        self.create_time = create_time
        self.is_active = is_active
        self.is_staff = is_staff
        self.usage = usage
        self.total = total

    def __str__(self):
        return 'SeafileAccount<id={}, email={}, usage={}Mo, total={}Mo, is_active={}>'.format(
            self.id, self.email, self.usage/1000000, self.total/1000000, self.is_active)

    @classmethod
    def from_json(cls, client, account_json):
        account_json = utf8lize(account_json)
        account_id = account_json['id']
        email = account_json['email']
        create_time = account_json['create_time']
        is_active = account_json['is_active']
        is_staff = account_json['is_staff']
        usage = account_json['usage']
        total = account_json['total']

        return cls(client, account_id, email, create_time, is_active, is_staff, usage, total)