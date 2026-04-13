'''
    Elaborato Programmazione di Reti
            a.a. 2020/2021
           Sansone Lorenzo
           Matricola: 887714
              Traccia 2
'''

#!/bin/env python
import sys, signal
import http.server
import socketserver
#new imports
import threading 


#manage the wait witout busy waiting
waiting_refresh = threading.Event()

users_data = { 'user123' : 'standardpass'}
# Legge il numero della porta dalla riga di comando oppure setto di default 8080
if sys.argv[1:]:
  port = int(sys.argv[1])
else:
  port = 8080

# classe che mantiene le funzioni di SimpleHTTPRequestHandler e implementa
# il metodo get nel caso in cui si voglia fare un refresh
class ServerHandler(http.server.SimpleHTTPRequestHandler):        
    def do_GET(self):
        # Scrivo sul file AllRequestsGET le richieste dei client     
        with open("AllRequestsGET.txt", "a") as out:
          info = "GET request,\nPath: " + str(self.path) + "\nHeaders:\n" + str(self.headers) + "\n"
          out.write(str(info))
        if self.path == '/refresh':
            refresh_contents()
            self.path = '/'
        http.server.SimpleHTTPRequestHandler.do_GET(self)
        
        
# ThreadingTCPServer per gestire più richieste
server = socketserver.ThreadingTCPServer(('127.0.0.1',port), ServerHandler)

# la parte iniziale è identica per tutti le pagine
header_html = """
<html>
    <head>
        <style>
            h1 {
                text-align: center;
                margin: 0;
            }
            table {width:70%;}
            img {
                max-width:300;
                max-height:200px;
                width:auto;
            }
            td {width: 33%;}
            p {text-align:justify;}
            td {
                padding: 20px;
                text-align: center;
            }
            .topnav {
  		        overflow: hidden;
  		        background-color: #333;
  		    }
            .topnav a {
  		        float: left;
  		        color: #f2f2f2;
  		        text-align: center;
  		        padding: 14px 16px;
  		        text-decoration: none;
  		        font-size: 17px;
  		    }        
  		    .topnav a:hover {
  		        background-color: #ddd;
  		        color: black;
  		    }        
  		    .topnav a.active {
  		        background-color: #4CAF50;
  		        color: white;
  		    }
        </style>
    </head>
    <body>
        <title>Policlinico S.Orsola Malpighi</title>
"""

# la barra di navigazione è identica per tutte le pagine
navigation_bar = """
        <div class="topnav">
            <a class="active" href="http://127.0.0.1:{port}">Home</a>
  		    <a href="http://127.0.0.1:{port}/reparti.html">Reparti</a>
            <a href="http://127.0.0.1:{port}/cerca_un_medico.html">Cerca un medico</a>
            <a href="http://127.0.0.1:{port}/privacy_cittadini.html">Privacy cittadini</a>
            <a href="http://127.0.0.1:{port}/numeri_utili.html">Numeri utili</a>
            <a href="http://127.0.0.1:{port}/libera_professione.html">Libera professione</a>
  		    <a href="http://127.0.0.1:{port}/refresh" style="float: right">Aggiorna contenuti</a>
            <a href="http://127.0.0.1:{port}/info.pdf" download="info.pdf" style="float: right">Download info pdf</a>
  		</div>
        <table align="center">
""".format(port=port)

# la parte finale è identica per tutte le pagine
footer_html= """
        </table>
    </body>
</html>
"""

#la parte finale per la pagine principale
index_end_page = """
        <br><br>
		<form action="http://127.0.0.1:{port}" method="post" style="text-align: center;">		  
          <p>L'Azienda Ospedaliero-Universitaria di Bologna Policlinico S. Orsola - Malpighi e' un ospedale molto antico (il primo nucleo risale al 1592) ed e' sede della Facolta' di Medicina e Chirurgia dell'Universita' Alma Mater Studiorum di Bologna.
          Si colloca nel cuore della citta' di Bologna con un'estensione di circa 1,8 Km e un'organizzazione logistica che si struttura in 27 Padiglioni che ospitano le Unita' Operative del Policlinico.
          Ogni giorno circa 20.000 persone accedono al Policlinico (personale dipendente, studenti e docenti universitari, pazienti, visitatori e fornitori). Il Policlinico e' centro di riferimento nazionale ed internazionale per diverse patologie; 
          ogni anno sono organizzati, nelle sue sedi interne, eventi didattico-formativi ai quali partecipano professionisti di fama nazionale e internazionale.
          L'organizzazione interna e' strutturata in 9 Dipartimenti ad attività integrata (ospedaliera e universitaria), una tipologia di organizzazione che consente di assicurare l'esercizio delle attività assistenziali, didattiche e di ricerca, cui afferiscono le 87 Unita' Operative.
          E' dotato di 1.515 posti letto con un organico di 6807 dipendenti, compresi i ricercatori e i medici universitari; vi si effettuano circa 49.000 ricoveri all'anno e oltre 3.300.000 prestazioni specialistiche per esterni.
          </p>
          <p>I servizi si possono scegliere dalla barra di navigazione o dalla seguente lista</p>     
		    <a href="http://127.0.0.1:{port}/reparti.html">Reparti</a><br>
            <a href="http://127.0.0.1:{port}/cerca_un_medico.html">Cerca un medico</a><br>
            <a href="http://127.0.0.1:{port}/privacy_cittadini.html">Privacy cittadini</a><br>
            <a href="http://127.0.0.1:{port}/numeri_utili.html">Numeri utili</a><br>
            <a href="http://127.0.0.1:{port}/libera_professione.html">Libera professione</a><br>
		</form>
		<br>
    </body>
</html>
""".format(port=port)

#parte finale della pagina dei reparti e servizi
reparti_end_page = """
	<form action="http://127.0.0.1:{port}/reparti.html" method="post" style="text-align: center;">
    <p>In questa sezione e' pubblicato l'elenco completo delle Unita' Operative del Policlinico S. Orsola-Malpighi.
    Le Unita' Operative sono a loro volta raggruppate in nove Dipartimenti.</p>
    <ul>
    <li><a href="https://www.aosp.bo.it/content/anestesiologia-e-rianimazione-frascaroli">Anestesia e Rianimazione CTV (Cardio-toraco-vascolare)</a></li>
    <li><a href="https://www.aosp.bo.it/content/angiologia-e-malattie-della-coagulazione-marino-golinelli">Angiologia e malattie della coagulazione</a></li>
    <li><a href="https://www.aosp.bo.it/content/chirurgia-orale-e-maxillo-facciale-marchetti">Chirurgia orale e maxillo facciale</a></li>
    <li><a href="https://www.aosp.bo.it/content/anatomia-e-istologia-patologica">Anatomia patologica</a></li>
    <li><a href="https://www.aosp.bo.it/content/andrologia-colombo">Andrologia</a></li>
    <li><a href="https://www.aosp.bo.it/content/anestesia-terapia-intensiva-polivalente">Anestesia e TI polivalente</a></li>
    <li><a href="https://www.aosp.bo.it/content/anestesiologia-e-rianimazione">Anestesiologia e rianimazione generale e pediatrica</a></li>
    <li><a href="https://www.aosp.bo.it/content/anestesiologia-e-rianimazione-melotti">Anestesiologia e terapia del dolore</a></li>     
    <li><a href="https://www.aosp.bo.it/content/cardiochirurgia">Cardiochirurgia</a></li>
    <li><a href="https://www.aosp.bo.it/content/cardiochirurgia-pediatrica-e-dellet-evolutiva-gargiulo">Cardiochirurgia pediatrica e dell'eta' evolutiva</a></li>
    <li><a href="https://www.aosp.bo.it/content/UOcardiologia">Cardiologia</a></li>
    <li><a href="https://www.aosp.bo.it/content/cardiologia-pediatrica-e-dellet-evolutiva">Cardiologia pediatrica e dell'eta' evolutiva</a></li>
    <li><a href="https://www.aosp.bo.it/content/centro-di-chirurgia-metabolica-e-obesit">Centro di chirurgia metabolica e dell'obesita'</a></li>
    <li><a href="https://www.aosp.bo.it/content/centro-marfan-0">Centro MARFAN - Centro Hub presidio della rete per le malattie rare (DGR 1966/06)</a></li>
    <li><a href="https://www.aosp.bo.it/content/centro-riferimento-trapianti">Centro Riferimento Trapianti</a></li>
    <li><a href="https://www.aosp.bo.it/content/crba-centro-unificato-di-ricerca-biomedica-applicata-chieco-0">Centro Unificato di Ricerca Biomedica Applicata CRBA</a></li>
    <li><a href="https://www.aosp.bo.it/content/chirurgia-pancreas-endocrina">Chirurgia del pancreas ed endocrina</a></li>
    </ul>
""".format(port=port)

#parte finale della pagine della privacy cittadini
privacy_cittadini_end_page = """
<form action="http://127.0.0.1:{port}/privacy_cittadini.html" method="post" style="text-align: center;">
<p>
L'Azienda Ospedaliero-Universitaria di Bologna Policlinico Sant'Orsola-Malpighi, nel perseguimento dei propri obbiettivi istituzionali, e' costantemente impegnata a garantire il diritto alla riservatezza di ogni paziente adeguando la propria attivita' alla normativa vigente in tema di protezione dei dati personali. Lo scopo e' quello di fornire alle strutture sanitarie del Policlinico gli strumenti necessari per garantire che la relazione “medico-paziente” sia sempre improntata al rispetto della dignita' della persona e della sua riservatezza.
A tale fine, l'Azienda promuove al suo interno la sensibilizzazione di tutti gli operatori sulle tematiche connesse alla protezione dei dati attraverso corsi di formazione, strumenti/procedure finalizzati a supportare gli stessi nella gestione consapevole del paziente sotto il profilo della riservatezza
offre al cittadino la garanzia del rispetto dei principi contenuti nella normativa, adottando una serie di strumenti finalizzati a fornirgli un'adeguata informazione sul trattamento dei dati effettuato all'interno dell'Azienda al fine di permettergli di esprimere, rispetto allo stesso, un consenso informato, libero, esplicito, specifico ed inequivocabile
In Azienda è presente un Ufficio Privacy che si occupa delle varie problematiche inerenti il rispetto della riservatezza e si pone come punto di riferimento non soltanto per gli operatori interni, ma anche per gli utenti che desiderino maggiori informazioni sulle politiche adottate dall'Azienda a tutela della privacy o abbiano la necessita' di chiarimenti o approfondimenti rispetto a  quanto scritto in questo sezione dedicata.
</p>
""".format(port=port)

#parte finale della pagina per cercare un medico
cerca_un_medico_end_page = """
<form action="http://127.0.0.1:{port}/cerca_un_medico.html" method="post" style="text-align: center;">
<p>Cerca un medico tra quelli presenti:</p>
<ul>
<li> Sabatino matteo: Cardiologia </li>
<li> Anna Fracchi: Ortopedia </li>
<li> Manuela Angelotti: Anestesia </li>
<li> Giovanni Manotti: Cardiochirurgia </li>
<li> Antonio DePascoli: Pediatria </li>
<li> Marco Matteotti: Chirurgia del pancreas </li>
<li> Luca Basotti: Centro di chirurgia</li>
<li> Angeletto Belotti: Angiologia </li>
</ul>
""".format(port=port)

#parte finale della pagina dei numeri utili
numeri_utili_end_page = """
<form action="http://127.0.0.1:{port}/numeri_utili.html" method="post" style="text-align: center;">
<p><b>Call Center - Tel. 051 214 1111</b><br>
Per informazioni e richieste di numeri telefonici.<br>
dal lunedì al venerdì dalle 7.00 alle 19.00 e sabato dalle 7.00 alle 13.00<br>

<b>URP - Ufficio relazioni con il pubblico - Tel. 051 214 1259</b><br>

Per orientarsi all'interno del Policlinico e per avere informazioni sui servizi erogati.<br>
dal lunedì al venerdì, dalle 8.00 alle 17.00<br>

<b>Numero verde regionale -Tel. 800-033033</b><br>
Per informazioni su: prestazioni sanitarie e servizi erogati nelle Aziende Sanitarie della Regione.<br>

<b>Posto di Polizia - Tel. 051 2144723</b><br>
Padiglione 5 - Nuovo Pronto Soccorso <br>

<b>Vigilanza Coopservice - Tel. 051 2143078</b><br>
Il servizio è attivo 24h<br>
</p>

""".format(port=port)

#parte finale della pagina della libera professione
libera_professione_end_page = """
<form action="http://127.0.0.1:{port}/libera_professione.html" method="post" style="text-align: center;">
<p>I cittadini italiani e stranieri possono accedere alle prestazioni sanitarie erogate all'interno del Policlinico di S. Orsola anche a pagamento.

L'erogazione di prestazioni in libera professione e' un'opportunita' per il cittadino di richiedere visite specialistiche, indagini strumentali o di laboratorio e ricoveri ospedalieri, con la garanzia di essere seguiti dal proprio specialista di fiducia.

L'erogazione di prestazioni in libera professione si affianca a quella del Servizio Sanitario Regionale garantendo cosi' una piena e reale libera scelta del cittadino che puo' usufruire dei servizi offerti dall'Ospedale in un contesto altamente qualificato dal punto di vista clinico assistenziale garantendo (per le prestazioni erogate in regime di ricovero) servizi alberghieri di livello superiore.

Utilizzando il motore di ricerca Cerca un medico delle pagine internet del portale dell'ospedale e' possibile cercare il medico che si desidera contattare per una prestazione libero professionale. Saranno così visualizzati i dati del medico (cliccando sul nome si accede al curriculum) e il link alla pagina dell'Unita' Operativa di riferimento.
</p>
""".format(port=port)


#permette di creare una pagina passando il titolo, l'end page creato precedentemente e il nome del file
def create_page(title,end_page,file):
    f = open(file,'w', encoding="utf-8")
    message = header_html + title + navigation_bar + end_page + footer_html
    f.write(message)
    f.close()

header_title = """ <h1><strong>Policlinico S. Orsola - Malpighini</strong></h1><br> """


def create_page_index():
    create_page("<title>index</title>" + header_title,index_end_page,'index.html')

def create_page_reparti():
    create_page("<title>reparti</title>" + header_title,reparti_end_page,'reparti.html')
    
def create_page_cerca_un_medico():
    create_page("<title>cerca un medico</title>" + header_title,cerca_un_medico_end_page,'cerca_un_medico.html')
    
def create_page_privacy_cittadino():
    create_page("<title>privacy cittadino</title>" + header_title,privacy_cittadini_end_page,'privacy_cittadini.html')
    
def create_page_numeri_utili():
    create_page("<title>numeri utili</title>" + header_title,numeri_utili_end_page,'numeri_utili.html')
    
def create_page_libera_professione():
    create_page("<title>libera professione</title>" + header_title,libera_professione_end_page,'libera_professione.html')
    

# creo tutti i file utili per navigare.
def refresh_contents():
    print("updating all contents")
    create_page_index()
    create_page_reparti()
    create_page_cerca_un_medico()
    create_page_privacy_cittadino()
    create_page_numeri_utili()
    create_page_libera_professione()
    print("finished update")


#lancio un thread che aggiorna i contenuti delle pagine nel caso si verificiassero aggiornamenti relativi
# ai contenuti delle pagine     
def launch_thread_resfresh():
    t_refresh = threading.Thread(target=refresh_contents())
    t_refresh.daemon = True
    t_refresh.start()
    
# definiamo una funzione per permetterci di uscire dal processo tramite Ctrl-C
def signal_handler(signal, frame):
    print( 'Exiting http server (Ctrl+C pressed)')
    try:
      if(server):
        server.server_close()
    finally:
      # fermo il thread del refresh senza busy waiting
      waiting_refresh.set()
      sys.exit(0)
     
#variabile per l'accesso
logged = False    
while logged == False:
    user = input('Inserire username:')
    password = input('Inserire password:')
    if user in users_data and password == users_data[user]:
        logged = True
        print('\nLogged with account:')
        print('Username:',user)
        print('Password:',password)
    else:
        print('Dati non corretti')

print('Porta collegata:',port)
# lancio un thread che carica e aggiorna ricorrentemente i contenuti
launch_thread_resfresh()
    #Assicura che da tastiera usando la combinazione
    #di tasti Ctrl-C termini in modo pulito tutti i thread generati
server.daemon_threads = True 
    #il Server acconsente al riutilizzo del socket anche se ancora non è stato
    #rilasciato quello precedente, andandolo a sovrascrivere
server.allow_reuse_address = True  
    #interrompe l'esecuzione se da tastiera arriva la sequenza (CTRL + C) 
signal.signal(signal.SIGINT, signal_handler)

    # cancella i dati get ogni volta che il server viene attivato
f = open('AllRequestsGET.txt','w', encoding="utf-8")
f.close()
    # entra nel loop infinito
try:
    while True:
        server.serve_forever()
except KeyboardInterrupt:
    pass
server.server_close()

