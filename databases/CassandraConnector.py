from cassandra.cluster import Cluster
from Utils import config_section_map


cassandra_ips = config_section_map("cassandra")['ip']
port = config_section_map("cassandra")['port']
cluster = Cluster(cassandra_ips.split(','), port=port)
session = cluster.connect()
__user_authentication_statement = session.prepare("SELECT value FROM authentication_table WHERE key=?")


def get_session():
    return session


def get_all_users():
    rows = session.execute('SELECT name, age, contact from users')
    return rows


def authenticate(user_id, password):
    provided_hashed_password = __get_hashed_password(password)
    actual_hashed_password = session.execute(__user_authentication_statement, [user_id])[0]
    if provided_hashed_password == actual_hashed_password:
        direct_to_user_home_page(user_id)
    else:
        return


def __get_hashed_password(password):
    return hash(password)


def direct_to_user_home_page(user_id):
    return 'write_function_direct_user_to_home_page'


def add_new_user(name, mobile, user_id):
    session.execute(
        """
        INSERT INTO users (name, mobile, user_id)
        VALUES (%s, %s, %s)
        """,
        (name, mobile, user_id)
    )


