import requests
import random
import json
import sqlite3
import time
import os
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
with open('cfg.fil','r') as rd_cfg:
    fl_data=rd_cfg.read()
fl_data=json.loads(fl_data)
api_key=fl_data['api_key']
conn=sqlite3.connect('test.db')

rd_link=r"https://api.random.org/json-rpc/2/invoke"
nr_link = r"https://api.chucknorris.io/jokes/random"
dt_link = r"https://api.tronalddump.io/random/quote"


def db_create():
    conn.execute('''CREATE TABLE norris
             (ID Text PRIMARY KEY     NOT NULL,
             Response_code INT NOT NULL,
             Response          TEXT,
             time_taken INT,
             fdata text);''')
    conn.execute('''CREATE TABLE dtrump
             (ID Text PRIMARY KEY     NOT NULL,
             Response_code INT NOT NULL,
             Response          TEXT,
             time_taken INT,
             fdata text);''')

    conn.execute('''CREATE TABLE rnd_org
             (ID Text PRIMARY KEY     NOT NULL,
             Response_code INT NOT NULL,
             Response          TEXT,
             time_taken INT,
             fdata text);''')
    conn.commit()
import datetime
def do_requests(r1=0,r2=1000):
    conn2 = sqlite3.connect('test.db')
    id=str(time.time())+"_"+str(random.randint(r1,r2))
    print(id)
    st=time.time()
    s1=time.time()
    nr=requests.get(nr_link)
    e1=time.time()
    s2=time.time()
    dt=requests.get(dt_link)
    e2=time.time()
    s3=time.time()
    rd=requests.post(rd_link,json={"jsonrpc": "2.0","method": "generatesignedintegers","params": {"apiKey": api_key,"n": 1,"min": 1,"max": 10000,"base": 10},"id": 18197})
    e3=time.time()
    et=time.time()
    print(rd.text)
    nr_c=json.loads(nr.text)['value'] if nr.status_code==200 else "Error"
    dt_c=json.loads(dt.text)['value'] if dt.status_code==200 else "Error"
    rd_c=json.loads(rd.text)['result']['random']['data'][0] if rd.status_code==200 else "Error"
    os.system('cls')
    dt_c=str(dt_c.encode('utf-16'))
    print(nr_c)
    print(dt_c)
    print(rd_c)
    conn2.execute("INSERT INTO {table} (ID,Response_code,Response,time_taken,fdata) VALUES {data1}".format(table="norris",data1=(id,nr.status_code,nr.text,e1-s1,nr_c)))
    conn2.execute("INSERT INTO {table} (ID,Response_code,Response,time_taken,fdata) VALUES {data1}".format(table="dtrump",data1=(id,dt.status_code,dt.text,e2-s2,dt_c)))
    conn2.execute("INSERT INTO {table} (ID,Response_code,Response,time_taken,fdata) VALUES {data1}".format(table="rnd_org",data1=(id,rd.status_code,dt.text,e3-s3,rd_c)))
    conn2.commit()
    conn2.close()


    if json.loads(rd.text)['result']['random']['data'][0]%2 is  0:
        return "<h1>"+json.loads(dt.text)['value']+"</h1>\n total time taken : "+str(et-st)+"\n<p>time for reach request:</p><p>\nnorris:"+str(e1-s1)+"</p><p>\ntrump:"+str(e2-s2)+"</p><p>\nrnd_org:"+str(e3-s3)+"</p>"
    else :
        return "<h1>"+json.loads(nr.text)['value']+"</h1>\n total time taken : "+str(et-st)+"\n<p>time for reach request:</p><p>\nnorris:"+str(e1-s1)+"</p><p>\ntrump:"+str(e2-s2)+"</p><p>\nrnd_org:"+str(e3-s3)+"</p>"


do_db=False
test_stres=False
import _thread
if not test_stres:
    pass
else :
    for i in range(0,5):
        _thread.start_new(do_requests,(0,100000))
    time.sleep(500)



if not do_db:
    class Serv(BaseHTTPRequestHandler):

        def do_GET(self):
            if self.path == '/':
                self.path = '/index.html'
                file_to_open = open(self.path[1:]).read()
                self.send_response(200)
                self.end_headers()
                s=do_requests()
                self.wfile.write(bytearray(s,'utf-8'))
                # self.wfile.write(bytes(file_to_open, 'utf-8'))



    httpd = HTTPServer(('localhost', 8000), Serv)
    httpd.serve_forever()
else:
    rd_s=0
    ch_s=0
    dt_s=0
    a=conn.execute("select avg(time_taken) from norris")
    b=conn.execute("select avg(time_taken) from dtrump")
    c=conn.execute("select avg(time_taken) from rnd_org")
    for i in a: print ("For norris api : {} s".format(i[0]))
    for i in b: print("For donaltrump api : {} s".format(i[0]))
    for i in c: print("For random_org api : {} s".format(i[0]))