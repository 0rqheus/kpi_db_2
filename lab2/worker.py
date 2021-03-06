import redis
import random
import time
import logging
from threading import Thread
from dotenv import dotenv_values

config = dotenv_values(".env")
logging.basicConfig(filename='lab2.log', level=logging.INFO, encoding='utf-8', format='[%(asctime)s] — %(message)s', datefmt='%d-%m-%YT%H:%M:%S')

class EventListener(Thread):
    def __init__(self, connection):
        Thread.__init__(self)
        self.connection = connection

    def run(self):
        pubsub = self.connection.pubsub()
        pubsub.subscribe(['users', 'spam'])
        for item in pubsub.listen():
            if item['type'] == 'message':
                message = 'Event: %s' % item['data']
                logging.info(message)


class MesssageQueueWorker(Thread):
    def __init__(self, connect):
        Thread.__init__(self)
        self.connection = connect

    def run(self):

        while True:
            message = self.connection.brpop('queue')
            print(message)

            if message:
                message_id = int(message[1])

                self.connection.hset('message:%s' % message_id, 'status', 'checking')
                
                sender_id = int(self.connection.hget('message:%s' % message_id, 'sender_id'))
                receiver_id = int(self.connection.hget('message:%s' % message_id, 'receiver_id'))
                message_text = self.connection.hget('message:%s' % message_id, 'text')

                self.connection.hincrby('user:%s' % sender_id, 'queue', -1)
                self.connection.hincrby('user:%s' % sender_id, 'checking', 1)

                time.sleep(random.randint(0, 0.2))
                is_spam = random.choice([True, False])

                pipeline = self.connection.pipeline(True)
                pipeline.hincrby('user:%s' % sender_id, 'checking', -1)

                if is_spam:
                    sender_username = self.connection.hget('user:%s' % sender_id, 'login')
                    pipeline.zincrby('spam', 1, '%s:%s' % (sender_id, sender_username))
                    pipeline.hset('message:%s' % message_id, 'status', 'blocked')
                    pipeline.hincrby('user:%s' % sender_id, 'blocked', 1)
                    pipeline.publish('spam', 'User %s sent spam message: \'%s\'' % (sender_username, message_text))
                else:
                    pipeline.hset('message:%s' % message_id, 'status', 'sent')
                    pipeline.hincrby('user:%s' % sender_id, 'sent', 1)
                    pipeline.sadd('sent-to:%s' % receiver_id, message_id)

                pipeline.execute()


def main():
    connection = redis.StrictRedis(host=config["REDIS_HOST"], port=config["REDIS_PORT"], password=config["REDIS_PASSWORD"], charset='utf-8',decode_responses=True)
    listener = EventListener(connection)
    listener.setDaemon(True)
    listener.start()

    for i in range(1):
        connection = redis.StrictRedis(host=config["REDIS_HOST"], port=config["REDIS_PORT"], password=config["REDIS_PASSWORD"], charset='utf-8',decode_responses=True)
        worker = MesssageQueueWorker(connection)
        worker.daemon = True
        worker.start()

    while True:
        pass

if __name__ == '__main__':
    main()