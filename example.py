
from http.server import HTTPServer as BaseHTTPServer, SimpleHTTPRequestHandler
import threading
import sys
import time


class HTTPHandler(SimpleHTTPRequestHandler):
    """This handler uses server.base_path instead of always using os.getcwd()"""


class HTTPServer(BaseHTTPServer):
    """The main server, you pass in base_path which is the path you want to serve requests from"""

    def __init__(self, base_path, server_address, RequestHandlerClass=HTTPHandler):
        self.base_path = base_path
        self.host, self.port = server_address
        BaseHTTPServer.__init__(self, server_address, RequestHandlerClass)
        # self.keep_going = True

    def run(self):
        print(f'serving {self.base_path} on {self.host}:{self.port}...')
        print(
            f'(russ: not actually serving {self.base_path}. just using the default cwd bc laziness...)')

        try:
            sys.stdout.flush()
            self.serve_forever()
        except (KeyboardInterrupt, OSError):
            print('>>closing HTTPServer...')
            # self.keep_going = False
            pass
        finally:
            print('>>server_close')
            self.server_close()

        print('>>leaving run')


class TopThread(threading.Thread):
    def __init__(self, *args, server='blah', **kwargs):
        super().__init__(*args, **kwargs)
        self.keep_going = True
        self.server = server

    def run(self):
        print(self.server)
        self.server.run()
        while self.keep_going:
            try:
                time.sleep(.21)
            except KeyboardInterrupt:
                print('caught keyboard interrupt at top level thread')
                self.server.close()
                print('>>server close')
                self.keep_going = False
            finally:
                print('>top level thread close')
                return
        print('>top level thread closed.')


def serve_httpserver(directory_to_serve='data', server_name='localhost', port=9001):
    httpd = HTTPServer(directory_to_serve, (server_name, port))
    httpd.run()
    print('>>leaving serve')
    # thread = threading.Thread(None, target=httpd.run)
    # thread.start()
    # print('.shutdown')

    # thread.join()
    # print('joined.')


def serve_thread_over_httpserver(directory_to_serve='data', server_name='localhost', port=9001):
    with HTTPServer(directory_to_serve, (server_name, port)) as server:
        server_thread = TopThread(server=server, target=server.run)
        server_thread.start()
        while server_thread.keep_going:
            time.sleep(.2)
        server.shutdown()
        server_thread.join()


if __name__ == "__main__":
    # serve_httpserver() # <- this works
    serve_thread_over_httpserver()  # <- this works
