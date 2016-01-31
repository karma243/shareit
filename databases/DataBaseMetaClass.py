from abc import ABCMeta, abstractmethod
from CassandraConnector import CassandraConnector


class DataBaseMetaClass:
    def __init__(self):
        pass

    __metaclass__ = ABCMeta

    @abstractmethod
    def connect_to_db(self):
        pass

    @abstractmethod
    def fetch_user_detail(self):
        pass

    @abstractmethod
    def validate_login(self, user_id, password):
        pass

    @abstractmethod
    def add_user(self):
        pass

    @abstractmethod
    def update_user(self):
        pass

DataBaseMetaClass.register(CassandraConnector)
