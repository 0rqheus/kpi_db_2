import redis

connection = redis.StrictRedis(
    host='redis-13699.c1.us-east1-2.gce.cloud.redislabs.com',
    port=13699,
    password='GzUEBiCvKdrm3gBAaQvNrGOE4WpMQDMa',
    charset='utf-8',
    decode_responses=True
)

def main():

    while True:
        print('\n\n1. Online users')
        print('2. Top senders')
        print('3. Top spamers')
        print('4. Exit')
        
        choice = int(input())

        if choice == 1:
            online_users = connection.smembers('online')
            print('\nOnline users:')
            for user in online_users:
                print(user)
        elif choice == 2:
            senders = connection.zrange('sent', 0, 10, desc=True, withscores=True)
            print('\nTop senders:')
            for index, sender in enumerate(senders):
                print('%d. %s - %d messages' % (index + 1, sender[0], sender[1]))
        elif choice == 3:
            spamers = connection.zrange('spam', 0, 10, desc=True, withscores=True)
            print('\nTop spamers:')
            for index, spamer in enumerate(spamers):
                print('%d. %s - %d spams' % (index + 1, spamer[0], spamer[1]))
        elif choice == 4:
            break
        else:
            print('\nIncorrect option!')


if __name__ == '__main__':
    main()