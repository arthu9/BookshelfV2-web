import psycopg2
from flask import Flask, render_template, request
from configparser import ConfigParser
from models import Entry


app = Flask(__name__)







print "Program Start"
 
def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db


print "Table created successfully"

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print "Connecting to the PostgreSQL database..."
        conn = psycopg2.connect(**params)
 
        # create a cursor
        cur = conn.cursor()
        
 # execute a statement
        print 'PostgreSQL database version:'
        cur.execute('SELECT version()')
 
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print db_version
       
     # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print error
    finally:
        if conn is not None:
            conn.close()
            print "Database connection closed."


print "Program End"



def add_entry(ent):
   conn = psycopg2.connect(database = "AF51", user = "postgres", password = "carrotcake092814", host = "127.0.0.1", port = "5432")
   print "Opened database successfully"
   cur = conn.cursor()

   cur.execute('''INSERT INTO form (payor, nature1, nature1amt, nature2, nature2amt, nature3, nature3amt, insurance, total, amtwords, paymentmethod, draweebank, draweenum, draweedate, receiptno, officer, collectiondate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', (ent.payor, ent.nature1, ent.nature1amt, ent.nature2, ent.nature2amt, ent.nature3, ent.nature3amt, ent.insurance, ent.total, ent.amtwords, ent.paymentmethod, ent.draweebank, ent.draweenum, ent.draweedate, ent.receiptno, ent.officer, ent.collectiondate))            
               
   print "Good"
   conn.commit()
   conn.close()
 





@app.route('/form')
def register():
   return render_template('form.html')


@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():

   empty = []
   if request.method == 'POST':
    
         collectiondate = request.form['CollectionDate']
         payor = request.form['payor']
         nature1 = request.form['nature1']
         nature1amt = request.form['nature1amt']
         nature2 = request.form['nature2']
         nature2amt = request.form['nature2amt']
         nature3 = request.form['nature3']
         nature3amt = request.form['nature3amt']
         insurance = request.form['insurance']
         total = request.form['total']
         amtwords = request.form['amtwords']
         paymentmethod = request.form['paymentmethod']
         draweebank = request.form['draweebank']
         draweenum = request.form['draweenum']
         draweedate = request.form['draweedate']
         receiptno = request.form['receiptno']
         officer = request.form['officer']

         if nature1 is empty:
            nature1 = "None"
            nature1amt = 0
         if nature2 is empty:
            nature2 = "None"
            nature2amt = 0
         if nature3 is empty:
            nature3 = "None"
            nature3amt = 0

         
         ent = Entry(payor, nature1, nature1amt, nature2, nature2amt, nature3, nature3amt, insurance, total, amtwords, paymentmethod, draweebank, draweenum, draweedate, receiptno, officer,collectiondate)
         add_entry(ent)
         msg = "Record successfully added"

         return render_template("result.html", msg=msg)





