from cassandra.cluster import Cluster
from Utils import config_section_map
from DataBaseMetaClass import DataBaseMetaClass


class CassandraConnector(DataBaseMetaClass):
    def __init__(self):
        cassandra_ips = config_section_map("cassandra")['ip']
        port = config_section_map("cassandra")['port']
        cluster = Cluster(cassandra_ips.split(','), port=port)
        self.session = cluster.connect()
        self.session.set_keyspace("shareit")
        self.__user_authentication_statement = self.session.prepare("SELECT value FROM authentication WHERE key=?")

    def connect_to_db(self):
        pass

    def add_user(self):
        pass

    def update_user(self):
        pass

    def fetch_user_detail(self):
        pass

    def validate_login(self, user_id, password):
        provided_hashed_password = self.__get_hashed_password(password)
        actual_hashed_password = self.session.execute(self.__user_authentication_statement, [user_id])[0]
        if provided_hashed_password == actual_hashed_password:
            self.direct_to_user_home_page(user_id)
        else:
            return

    def get_session(self):
        return self.session

    def get_all_users(self):
        try:
            rows = self.session.execute('SELECT name, age, contact from users')
        except:
            session.execute('')
        return rows

    @staticmethod
    def __get_hashed_password(password):
        return hash(password)

    @staticmethod
    def direct_to_user_home_page(user_id):
        return 'write_function_direct_user_to_home_page'

    def add_new_user(self, name, mobile, user_id):
        self.session.execute(
            """
            INSERT INTO users (name, mobile, user_id)
            VALUES (%s, %s, %s)
            """,
            (name, mobile, user_id)
        )

