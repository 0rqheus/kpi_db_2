import redis
import datetime
import logging
from dotenv import dotenv_values

config = dotenv_values(".env")
logging.basicConfig(filename='lab2.log', level=logging.INFO, encoding='utf-8', format='[%(asctime)s] — %(message)s', datefmt='%d-%m-%YT%H:%M:%S')

# auth

def register(connection, username):
    if (connection.hget('users', username)):
        print('User already exist!')
        return

    user_id = connection.incr('user:id')

    pipeline = connection.pipeline(True)
    pipeline.hset('users', username, user_id)
    pipeline.hset('user:%s' % user_id, 'login', username)
    pipeline.hset('user:%s' % user_id, 'queue', 0)
    pipeline.hset('user:%s' % user_id, 'checking', 0)
    pipeline.hset('user:%s' % user_id, 'blocked', 0)
    pipeline.hset('user:%s' % user_id, 'sent', 0)
    pipeline.hset('user:%s' % user_id, 'delivered', 0)
    pipeline.execute()

    logging.info('User: %s\tAction: register\n' % username)


def login(connection, username) -> int:    
    try:
        user_id = int(connection.hget('users', username))
    except TypeError:
        print('User not found!')
        return None
    else:
        connection.sadd('online', username)
        connection.publish('users', '%s logged in' % username)
        logging.info('User: %s;\tAction: login' % username)

        return user_id


def logout(connection, user_id):
    username = connection.hget('user:%s' % user_id, 'login')

    connection.srem('online', username)
    connection.publish('users', 'User %s signed out' % username)
    logging.info('User: %s;\tAction: logout' % username)



# features

def create_message(connection, user_id, receiver, text):
    try:
        receiver_id = int(connection.hget('users', receiver))
    except TypeError:
        print('Receiver not found!')
        return

    message_id = int(connection.incr('message:id'))
    current_user = connection.hget('user:%s' % user_id, 'login')

    pipeline = connection.pipeline(True)

    msg_key = 'message:%s' % message_id

    pipeline.hset(msg_key, 'id', message_id)
    pipeline.hset(msg_key, 'sender_id', user_id)
    pipeline.hset(msg_key, 'receiver_id', receiver_id)
    pipeline.hset(msg_key, 'text', text)
    pipeline.hset(msg_key, 'status', 'created')

    pipeline.lpush('queue', message_id)

    pipeline.hset(msg_key, 'status', 'queue')

    pipeline.zincrby('sent', 1, '%s:%s' % (user_id, current_user))
    pipeline.hincrby('user:%s' % user_id, 'queue', 1)

    pipeline.execute()


def show_inbox(connection, user_id):
    messages = connection.smembers('sent-to:%s' % user_id)
    print()

    for message_id in messages:
        
        sender_id, text, status = connection.hmget('message:%s' % message_id, ['sender_id', 'text', 'status'])
        sender_username = connection.hmget('user:%s' % sender_id, ['login'])[0]

        print('From: %s\nText: %s\n\n' % (sender_username, text))

        if status != 'delivered':
            pipeline = connection.pipeline(True)
            pipeline.hset('message:%s' % message_id, 'status', 'delivered')
            pipeline.hincrby('user:%s' % sender_id, 'sent', -1)
            pipeline.hincrby('user:%s' % sender_id, 'delivered', 1)
            pipeline.execute()


def show_stats(connection, user_id):
    user_stats = connection.hmget('user:%s' % user_id,['queue', 'checking', 'blocked', 'sent', 'delivered'])
    print('\nIn queue: %s\nChecking: %s\nBlocked: %s\nSent: %s\nDelivered: %s' % tuple(user_stats))



# menus

def user_menu(connection, user_id):
    
    while True:
        print('\n\n1. Create new message')
        print('2. Show inbox messages')
        print('3. Show message statistics')
        print('4. Logout')

        choice = int(input())

        if choice == 1:
            receiver = input('\nEnter receiver: ')
            text = input('Enter text: ')
            create_message(connection, user_id, receiver, text)
        elif choice == 2:
            show_inbox(connection, user_id)
        elif choice == 3:
            show_stats(connection, user_id)
        elif choice == 4:
            logout(connection, user_id)
            break
        else:
            print('Incorrect option!')


def main():

    connection = redis.StrictRedis(host=config["REDIS_HOST"], port=config["REDIS_PORT"], password=config["REDIS_PASSWORD"], charset='utf-8',decode_responses=True)

    while True:
        print('\n\n1. Login')
        print('2. Register')
        print('3. Exit')

        choice = int(input())

        if choice == 1:
            user_id = login(connection, input('\nEnter login: '))
            if(user_id != None):
                user_menu(connection, user_id)
        elif choice == 2:
            register(connection, input('\nEnter username: '))
        elif choice == 3:
            break
        else:
            print('Incorrect option!')


if __name__ == '__main__':
    main()