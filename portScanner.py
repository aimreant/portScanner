# -------------------------------------------------------------------------------
# Name:        PortScan
# Purpose:     scan which ports are open
# Author:      Aimreant JerryLu
# Python3.5
# -------------------------------------------------------------------------------
# Destination of this file is implementing access to Flask API
# -------------------------------------------------------------------------------
from flask import Flask, request, jsonify, render_template
from porter import porter

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scanner')
def scanner():
    return render_template('scanner.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/ip_port/', methods = ['POST'])
def scan_port():
    ip = request.form['ip']
    method = request.form['method']
    p = porter()

    if method == 'sequential':
        start_port = int(request.form['start_port'])
        end_port = int(request.form['end_port'])
        port_list = [i for i in range(start_port, end_port + 1)]
        open_ports_msg = p.start([ip], port_list)

    elif method == 'selected':
        port = int(request.form['port'])
        open_ports_msg = p.start([ip], [port])

    elif method == 'multi_ip':
        start_ip = request.form['start_ip']
        end_ip = request.form['end_ip']
        start_port = int(request.form['multi_ip_start_port'])
        end_port = int(request.form['multi_ip_end_port'])

        x1=start_ip.rfind('.')
        x2=end_ip.rfind('.')
        if int(start_ip[x1+1:]) > int(end_ip[x2+1:]):
            return jsonify(
                open_ports_msg=["<th>%s</th><th>%s</th><th>%s</th><th>%s</th>" %("ERROR", "ERROR", "UNKNOWN", "IP错误输入")]
            )
        else:
            ip_list = [ start_ip[:x1+1]+str(i) for i in range(int(start_ip[x1+1:]), int(end_ip[x2+1:]) + 1)]

        port_list = [i for i in range(start_port, end_port + 1)]
        open_ports_msg = p.start(ip_list, port_list)

    else:
        open_ports_msg = p.start([ip], '')

    return jsonify(open_ports_msg=open_ports_msg)


if __name__ == '__main__':
    app.run()
