# сервер

import sys
import json
import socket
from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from common.utils import get_message, send_message

def process_client_message(message):
    # обработка сообщенийот клиента, принимает словарь, проверяет корректность, возвращает словарь

    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return{
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    # проверка параметров командной строки, если нет параметров, то задаем значение по умолчанию.
    # сначала обрабатывает порт: server.py -p 8888 -a 127.0.0.1

    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        print('После параметра -\'p\' необходимо указать номер порта')
        sys.exit(1)
    except ValueError:
        print('номер порта от 1024 lj 65535')
        sys.exit(1)

    # загружаем какой адрес слушать

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a')+1]
        else:
            listen_address = ''

    except IndexError:
        print('После параметра \'a\'- необходимо указать адрес, который будет слушать сервер')
        sys.exit(1)

    # готовим сокет

    transport =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    transport.bind((listen_address, listen_port))

    # слушаем порт. колличество вызовов
    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        try:
            message_from_client = get_message(client)
            print(message_from_client)
            response = process_client_message(message_from_client)
            send_message(client, response)
            client.close()
        except (ValueError, Json.JSONDecodeError):
            print ('некорректное сообщение')
            client.close()


if __name__ == '__main__':
    main()