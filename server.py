__author__ = 'MiKelloggs'

from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
import json
from http import cookies, cookiejar
import os
from urllib.parse import parse_qs
import urllib.request
import urllib
import random


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class httpServerRequestHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, HEAD, OPTIONS, DELETE")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        return

    def do_GET(self):
            if self.path == "/tickets":
                db = TicketDB()
                rows = db.getTickets()
                json_string = json.dumps(rows)
                print("JSON:", json_string)
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, HEAD, OPTIONS")
                self.send_header("Access-Control-Allow_Headers", "X-Requested-With")
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(bytes(json_string, "utf-8"))
            else:
                self.handle404()
                print("Sorry, something went wrong, please try again.")

    def send_cookie(self):
        self.send_header("Set-Cookie", "oompa=loompa")

    def load_cookie(self):
        if "Cookie" in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            self.cookie = cookies.SimpleCookie()

    def do_POST(self):
        self.load_cookie()
        if "Cookie" in self.headers:
            self.handle403();
        else:
            if self.path == "/tickets":
                length = self.headers["Content-Length"]
                length = int(length)
                body = self.rfile.read(length).decode("utf-8")
                data = parse_qs(body)
                print(data)
                fName = data["fName"]
                print(fName[0])
                firstN = fName[0]

                age = data["age"]
                print(age[0])
                userAge = age[0]

                gName = data["gName"]
                print(gName[0])
                guestN = gName[0]

                rand_token = random.randrange(0,6)
                db = TicketDB()
                db.createTicket(firstN, userAge, guestN, rand_token)

                self.cookie["oompa"] = "loompa"
                print(self.cookie)
                self.send_response(200)
                self.send_cookie()
                self.end_headers()

                self.send_response(201)
                self.send_header("Access-Control-Allow_Headers", "X-Requested-With")
                self.send_header("Content-type", "application/x-www-form-urlencoded")
                self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
                self.send_header("Access-Control-Allow-Credentials", "true")
                self.send_cookie()
                self.end_headers()
            else:
                self.handle404()

    def handle404(self):
        self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes("<strong>Error 404! Not Found</strong>", "utf-8"))

    def handle403(self):
        self.send_response(403)
        self.end_headers()
        self.wfile.write(bytes("<strong>The Oompa Loompas have already received your ticket. Please try again tomorrow.</strong>", "utf-8"))


class TicketDB:

    def __init__(self):
        self.connection = sqlite3.connect("wonka.db")
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()
        return

    def __del__(self):
        self.connection.close()
        return

    def getTickets(self):
        self.cursor.execute("SELECT * FROM tickets")
        return self.cursor.fetchall()

    def createTicket(self, firstN, userAge, guestN, rand_token):
        self.cursor.execute("INSERT INTO tickets (entrant_name, entrant_age, guest_name, random_token) VALUES(?, ?, ?, ?)", (firstN, userAge, guestN, rand_token))
        self.connection.commit()

def run():
        db = TicketDB()

        listen = ("127.0.0.1", 8080)
        server = HTTPServer(listen, httpServerRequestHandler)

        print("Listening on port 8080")
        server.serve_forever()

run()
