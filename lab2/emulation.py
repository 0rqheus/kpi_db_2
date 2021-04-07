import random
from threading import Thread
import user
from faker import Faker
import redis
import atexit
from dotenv import dotenv_values

config = dotenv_values(".env")

fake = Faker()

class User(Thread):
    def __init__(self, connection, username, users_list, users_amount):
        Thread.__init__(self)
        self.connection = connection
        self.users_list = users_list
        self.users_amount = users_amount
        user.register(connection, username)
        self.user_id = user.login(connection, username)

    def run(self):
        for i in range(5):
            message_text = fake.sentence(nb_words=15, variable_nb_words=True, ext_word_list=None)
            receiver = self.users_list[random.randint(0, self.users_amount - 1)]
            user.create_message(self.connection, self.user_id, receiver, message_text)


def exit_handler():
    connection = redis.StrictRedis(host=config["REDIS_HOST"], port=config["REDIS_PORT"], password=config["REDIS_PASSWORD"], charset='utf-8',decode_responses=True)
    online = connection.smembers('online')
    for i in online:
        connection.srem('online', i)


def main():
    atexit.register(exit_handler)

    users_amount = 10
    threads = []
    users = [fake.profile(fields=['username'], sex=None)['username'] for u in range(users_amount)]

    for i in range(users_amount):
        connection = redis.StrictRedis(host=config["REDIS_HOST"], port=config["REDIS_PORT"], password=config["REDIS_PASSWORD"], charset='utf-8',decode_responses=True)
        threads.append(User(connection, users[i], users, users_amount))

    for t in threads:
        t.start()

if __name__ == '__main__':
    main()