import os
import socket
import network
import websocket_helper
import uselect
from time import sleep, sleep_ms
from websocket import websocket

########## ws_connection
class ClientClosedError(Exception):
    pass


class WebSocketConnection:
    def __init__(self, addr, s, close_callback):
        self.client_close = False
        self._need_check = False

        self.address = addr
        self.socket = s
        self.ws = websocket(s, True)
        self.poll = uselect.poll()
        self.close_callback = close_callback

        self.socket.setblocking(False)
        self.poll.register(self.socket, uselect.POLLIN)

    def read(self):
        poll_events = self.poll.poll(0)

        if not poll_events:
            return

        # Check the flag for connection hung up
        if poll_events[0][1] & uselect.POLLHUP:
            self.client_close = True

        msg_bytes = None
        try:
            msg_bytes = self.ws.read()
        except OSError:
            self.client_close = True

        # If no bytes => connection closed. See the link below.
        # http://stefan.buettcher.org/cs/conn_closed.html
        if not msg_bytes or self.client_close:
            raise ClientClosedError()

        return msg_bytes

    def write(self, msg):
        try:
            self.ws.write(msg)
        except OSError:
            self.client_close = True

    def is_closed(self):
        return self.socket is None

    def close(self):
        print("Closing connection.")
        self.poll.unregister(self.socket)
        self.socket.close()
        self.socket = None
        self.ws = None
        if self.close_callback:
            self.close_callback(self)

########### ws_server base
class WebSocketClient:
    def __init__(self, conn):
        self.connection = conn

    def process(self):
        pass


class WebSocketServer:
    def __init__(self, page, connectionCallback,disconnectionCallback, max_connections=1):
        self._listen_s = None
        self._listen_poll = None
        self._clients = []
        self._max_connections = max_connections
        self._page = page
        self.disconnected = disconnectionCallback
        self.connected = connectionCallback
        self.isConnected = False

    def _setup_conn(self, port):
        self._listen_s = socket.socket()
        self._listen_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._listen_poll = uselect.poll()

        ai = socket.getaddrinfo("0.0.0.0", port)
        addr = ai[0][4]

        self._listen_s.bind(addr)
        self._listen_s.listen(1)
        self._listen_poll.register(self._listen_s)
        for i in (network.AP_IF, network.STA_IF):
            iface = network.WLAN(i)
            if iface.active():
                print("WebSocket started on ws://%s:%d" % (iface.ifconfig()[0], port))

    def _check_new_connections(self, accept_handler):
        poll_events = self._listen_poll.poll(0)
        if not poll_events:
            return

        if poll_events[0][1] & uselect.POLLIN:
            accept_handler()

    def _accept_conn(self):
        cl, remote_addr = self._listen_s.accept()
        print("Client connection from:", remote_addr)
        self.connected()
        if len(self._clients) >= self._max_connections:
            # Maximum connections limit reached
            cl.setblocking(True)
            cl.sendall("HTTP/1.1 503 Too many connections\n\n")
            cl.sendall("\n")
            #TODO: Make sure the data is sent before closing
            sleep(0.1)
            cl.close()
            return

        try:
            websocket_helper.server_handshake(cl)
        except OSError:
            # Not a websocket connection, serve webpage
            self._serve_page(cl)
            return

        self._clients.append(self._make_client(WebSocketConnection(remote_addr, cl, self.remove_connection)))

    def _make_client(self, conn):
        self.isConnected = True
        return WebSocketClient(conn)

    def _serve_page(self, sock):
        try:
            sock.sendall('HTTP/1.1 200 OK\nConnection: close\nServer: WebSocket Server\nContent-Type: text/html\n')
            length = os.stat(self._page)[6]
            sock.sendall('Content-Length: {}\n\n'.format(length))
            # Process page by lines to avoid large strings
            with open(self._page, 'r') as f:
                for line in f:
                    sock.sendall(line)
        except OSError:
            # Error while serving webpage
            pass
        sock.close()

    def stop(self):
        if self._listen_poll:
            self._listen_poll.unregister(self._listen_s)
        self._listen_poll = None
        if self._listen_s:
            self._listen_s.close()
        self._listen_s = None

        for client in self._clients:
            client.connection.close()
        print("Stopped WebSocket server.")

    def start(self, port=80):
        if self._listen_s:
            self.stop()
        self._setup_conn(port)
        print("Started WebSocket server.")

    def process_all(self):
        self._check_new_connections(self._accept_conn)

        for client in self._clients:
            client.process()

    def remove_connection(self, conn):
        
        for client in self._clients:
            if client.connection is conn:
                self._clients.remove(client)
                self.isConnected = False
                self.disconnected()
                return
            
############ from main
class WSClient(WebSocketClient):
    def __init__(self, conn,receivedCallback):
        super().__init__(conn)
        self.receivedCallback = receivedCallback

    def process(self):
        try:
            msg = self.connection.read()
            if not msg:
                return
            msg = msg.decode("utf-8")
            self.receivedCallback(msg)
        except ClientClosedError:
            self.connection.close()
            
    def sendData(self,dataToSend):
        self.connection.write(dataToSend)


class WSServer(WebSocketServer):
    def __init__(self,connectionCallback,disconnectionCallback,receivedCallback):
        super().__init__("test.html",connectionCallback,disconnectionCallback,2)
        self.isConnected = False
        self.receivedCallback = receivedCallback

    def _make_client(self, conn):
        self.cli = WSClient(conn,self.receivedCallback)
        self.isConnected = True
        return self.cli
    
    def sendData(self,dataToSend):
        self.cli.sendData(dataToSend)