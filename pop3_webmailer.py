# -*- coding: UTF-8 -*-
import socket

def recvline(conn):
    data = ''
    while 1:
        d = conn.recv(1)
        if d == '\n':
            break
        if d != '\r':
            data = data + d
    return data

    # 1. Adress Familie -> IPv4; AF_INET6 ist IPv6
    # 2. Welches Protokoll? TCP; SOCK_DGRAM wäre UDP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # An den Port binden; IP nicht notwending
s.bind( ("", 8080) )

while 1:
    # nur eine Verbindung parallel verarbeiten
    s.listen(1)
    # Verbindung mit Client erstellen
    conn, addr = s.accept()
    #Buffergröße
    data = conn.recv(1024)

    ####
    # POP3 Anfrage als Client:
    ####
    # a) Verbindung aufnehmen
    pop3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pop3.connect(("dem.informatik.tu-chemnitz.de", 110))
    a = pop3.recv(1024)

        # Entertaste definieren
    CRLF = "\r\n" ## Entertaste

    # b) User senden
    pop3.send("USER rot" + CRLF)
    b = pop3.recv(1024)

    # c) Passwort senden
    pop3.send("PASS rot" + CRLF)
    c = pop3.recv(1024)

    # d) E-Mail Liste abrufen
    pop3.send("LIST" + CRLF)
    d = pop3.recv(1024)

    # e) Aus der Liste die Anzahl filtern und als integer ablegen
    anzahl = d.split(" ")
    mail_anzahl = int(anzahl[1])

    # f) Mails abrufen und drucken
    Mails = []

    i = 0
    while i <= mail_anzahl:
        pop3.send("RETR "+ str(i + 1) + CRLF) # Hier wird ab 1 gezählt
        ########################
        ### Was nocht fehlt:
        ### 1. Ich will nur die Nachricht haben, nicht den ganzen Header
        ### 2. StatusNachricht -> URL nicht gefunde statt Daten Fehlerbeschreibung
        ##############################
        f = pop3.recv(2056)

        Mails.append( f )
        i = i + 1

    pop3.close()



    ###
    # Antwort an Seite geben
    nachrichten = ""

    for x in Mails:
        nachrichten += "<a>{}</a><br><br><br>".format(x)



    website = """HTTP/1.1 200 OK
                Conten-Type: text/html

                <html>
                    <head>
                        <p><b><H1>Liste der E-Mails</H1></b></p>
                    </head>
                    <body>
                        <p>Der Server hat {} Nachrichten.</p><br><br>
                        {}
                    </body>
                </html>\n""".format(mail_anzahl, nachrichten)

    conn.send(website)
    conn.close()
s.close()
