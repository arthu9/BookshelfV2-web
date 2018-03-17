import psycopg2
from flask_sqlalchemy import SQLAlchemy
from configparser import ConfigParser


class Entry(object):
    def __init__(self, payor, nature1, nature1amt, nature2, nature2amt, nature3, nature3amt, insurance,  total, amtwords, paymentmethod, draweebank, draweenum, draweedate, receiptno, officer, collectiondate):

        self.payor = payor
        self.nature1 = nature1
        self.nature1amt = nature1amt
        self.nature2 = nature2
        self.nature2amt = nature2amt
        self.nature3 = nature3
        self.nature3amt = nature3amt
        self.insurance = insurance
        self.total = total
        self.amtwords = amtwords
        self.paymentmethod = paymentmethod
        self.draweebank = draweebank
        self.draweenum = draweenum
        self.draweedate = draweedate
        self.receiptno = receiptno
        self.officer = officer
        self.collectiondate = collectiondate


 
if __name__ == '__main__':
    connect()
