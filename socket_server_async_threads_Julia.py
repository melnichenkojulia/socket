import time
import socket
import threading
import asyncio


class ServerError(Exception):
    pass


dict = {}


def run_server(host: str, port: int):  # '127.0.0.1', 8888
    try:
        sock = socket.socket()
        sock.bind((host, port))
        sock.listen()
        while True:
            print('wait for connection')
            conn, addr = sock.accept()
            th = threading.Thread(target=process_request,
                                  args=(conn, addr))
            th.start()
    except:
        raise ServerError("Server Error")


def process_request(conn, addr):
    try:
        print("connected client:", addr)
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                request = data.decode('utf-8')
                print(f'Получен запрос: {ascii(request)}')
                response = recycle(request)
                print("response=", response)
                conn.send((response.encode("utf-8")))

    except:
        raise ServerError("Process Error")


def recycle(line: str):
    try:
        word = line.split(" ")[0]
        if word == 'put':

            key = line.split()[1]

            values = line.split()[2:]

            values = (float(values[0]), int(values[1]))
            if key in dict:
                [dict[key].remove(x) for x in list(dict[key]) if x[1] == values[1]]
                dict[key].append(values)
            else:
                dict[key] = [values]

            for key in dict:
                dict[key].sort(key=lambda x: x[0])
                print(key)

            return "ok\n\n"

        if word == 'get':
            assert len(line.split(' ')) == 2
            template = line.split(" ")[1].strip("\n")

            if template == "*":
                print(dict)
                row = ""
                for key in dict:
                    for i in dict[key]:
                        row += key + " " + str(i).strip("()").replace(",", "") + "\n"

                response = "ok\n" + row + "\n"
                
                return response
            elif template not in dict:
                return 'ok\n\n'
            else:
                row = ""
                for i in dict[template]:
                    row += template + " " + str(i).strip("()").replace(",", "") + "\n"

                response = "ok\n" + row + "\n"

                return response

    except:
        return 'error\n'


# class ClientServerProtocol(asyncio.Protocol):
#     def connection_made(self, transport):
#         self.transport = transport
#
#     def data_received(self, data):
#         resp = process_data(data.decode())
#         self.transport.write(resp.encode())
#
#
# loop = asyncio.get_event_loop()
# coro = loop.create_server(
#     ClientServerProtocol,
#     '127.0.0.1', 8181
# )
#
# server = loop.run_until_complete(coro)
#
# try:
#     loop.run_forever()
# except KeyboardInterrupt:
#     pass
#
# server.close()
# loop.run_until_complete(server.wait_closed())
# loop.close()

# run_server("127.0.0.1", 8888)

# recycle("put palm.cpu 0.5 115\n")
# recycle("put palm.cpu 2.0 1150864248\n")
# recycle("put vasia.cpu 2.0 1150864248\n")
# print(recycle("get *\n"))
# print(recycle("get palm.cpu\n"))
