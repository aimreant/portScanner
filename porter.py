# -------------------------------------------------------------------------------
# Name:        PortScan
# Purpose:     scan which ports are open
# Author:      Aimreant JerryLu
# Python3.5
# -------------------------------------------------------------------------------
# Destination of this file is implementing functions of portScanner
# -------------------------------------------------------------------------------
import socket
import concurrent.futures
import queue
import sqlite3


class porter():

    def __init__(self):
        self.open_ports = []
        self.db = sqlite3.connect("/Users/aimreant/PycharmProjects/portScanner/portServer.db")
        self.common_port = \
            [port[0] for port in self.db.execute("select port from portServer").fetchall()]


    def get_input(self):

        ip = input('Input IP:(default 127.0.0.1)')
        if ip == '':
            ip = '127.0.0.1'

        s = input('Input the beginning port you wanna scan:(default is common ports)')
        if s == '':
            port_list = self.common_port
        else:
            start_port = int(s)
            s = input('Input the ending port you wanna scan:(default is beginning port)')
            if s == '':
                end_port = start_port
            else:
                end_port = int(s)
            port_list = [i for i in range(start_port, end_port + 1)]

        return (ip, port_list)



    def scan(self, ip, port):
        try:
            sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sk.settimeout(1)
            sk.connect((ip, port))
            # print('Server %s port %d OK!' % (ip, port))

            self.open_ports.append([ip, port])
            sk.close()

        except Exception:
            pass

    def worker(self, scan_queue):
        while not scan_queue.empty():
            ip, port = scan_queue.get()
            try:
                self.scan(ip, port)
            finally:
                scan_queue.task_done()

    def start(self, ip_list, port_list):
        q = queue.Queue()
        if port_list == '':
            port_list = self.common_port

        for ip in ip_list:
            for port in port_list:
                q.put([ip, port])

        size = q.qsize()
        if size <= 50:
            size = 50

        print("Scanning begins.")
        with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
            for i in range(int(size/20)):
                if q.empty():
                    break
                else:
                    future = executor.submit(self.worker, q)

                if future.result() == None:
                    print("Scanning ends.")
                    break
                else:
                    print(future.result())

        open_ports_msg = []

        for port in self.open_ports:
            server = self.db.execute("select `server`,`description` from portServer where `port`=" + str(port[1])).fetchone()
            if server:
                open_ports_msg.append("<th>%s</th><th>%s</th><th>%s</th><th>%s</th>" %(str(port[0]),str(port[1]), server[0], server[1]))
            else:
                open_ports_msg.append("<th>%s</th><th>%s</th><th>%s</th><th>%s</th>" %(str(port[0]),str(port[1]), "UNKNOWN", "未知服务"))

        return open_ports_msg


if __name__ == '__main__':
    # for test
    p = porter()
    print(p.start(['127.0.0.1', '127.0.0.2'], [1080, 3306]))

