import time
import socket

from typing import Union


class ClientError(Exception):
    pass


class Client:
    def __init__(self, host: str, port: int, timeout: Union[int, float] = None):
        try:
            self.sock = None
            self.host = host
            self.port = port
            self.timeout = timeout

        # connect

            self.sock = socket.socket()
            self.sock.settimeout(self.timeout)
            self.sock.connect((self.host, self.port))
        except:
            raise ClientError("no connection")

    def put(self, name: str, value: Union[int,float], timestamp: Union[int,float] = None):
        # set timestamp default as int(time.time())

        timestamp = timestamp or int(time.time())

        # send data
        try:
            self.sock.send(("put"+" " + name +" "+ str(value)+" " + str(timestamp) + "\n").encode("utf-8"))

        # get response

            response = self.sock.recv(1024).decode("utf-8")
            assert response.startswith("ok\n")
            assert response.endswith("\n\n")

        except:
            raise ClientError()

    def to_dict(self,line):

        dict = {}
        try:
            for i in line.split("\n")[1:-2]:
                # print(i)
                key = i.split()[0]

                values = i.split()[1:3]
                # assert type(values)
                values.reverse()

                values = (int(values[0]), float(values[1]))
                assert type(values[0]) == int
                assert type(values[1]) == float
                values = tuple(values)

                # print('key=',key,"values=",values)
                if key in dict:
                    dict[key].append(values)
                else:
                    dict[key] = [values]

                for key in dict:
                    dict[key].sort(key=lambda x: x[0])
            # print(dict)
            return dict
        except:
            raise ClientError()

    def get(self, metric:str):
         # send data
        try:
            self.sock.send(("get "+metric+"\n").encode("utf-8"))

        # get response

            response = self.sock.recv(1024).decode("utf-8")
            print('response',response)
            assert response.startswith("ok\n")
            assert response.endswith("\n\n")

        except:
            raise ClientError

        try:
            # create dictionary
            dict= self.to_dict(response)

            # return result
            return dict

        except:
            raise ClientError


client = Client("127.0.0.1", 8889, timeout=150)

client.put("palm.cpu", 0.5, timestamp=115)
# #
client.put("palm.cpu", 0.7, timestamp=115)
client.put("palm.cpu", 2.0, timestamp=1150864248)
# #
client.put("eardrum.memo", 0.11, timestamp=1700005)
#
# print(client.get("palm.cpu"))
print(client.get("*"))
import time
time.sleep(100)