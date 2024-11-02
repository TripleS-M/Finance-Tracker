from customtkinter import *
from PIL import Image
from tkinter import ttk, messagebox
import mysql.connector as mc

con = mc.connect(host="localhost", user="root", password='bpsdoha',database='Suhaas12B')
cur = con.cursor()
cur.execute("create table if not exists ftable(SNo int,Name varchar(200),Category varchar(100),Price decimal(10,2))")
def insert(id,name,categ,price):
    cur.execute("insert into ftable values(%s,%s,%s,%s)",(id,name,categ,price))
    con.commit()

def id_exists(id):
    l=['']
    for i in range(0,len(id)):
        l[0]+=id[i]
    cur.execute("select count(*) from ftable where SNo =%s;",l)
    result = cur.fetchone()
    print(result)
    return result[0]>0

def fetch_items():
    cur.execute("select * from ftable")
    result=cur.fetchall()
    return result

def update(id,name,categ,price):
    cur.execute('update ftable set name=%s,category=%s,price=%s where SNo=%s',(name,categ,price,id))
    con.commit()

def delete(id):
    cur.execute('delete from ftable where SNo=%s',(id,))
    con.commit()

def search(option,value):
    global result
    if option=='SNo':
        cur.execute("select * from ftable where SNo=%s", (value,))
        result = cur.fetchall()
    elif option=='Name':
        cur.execute("select * from ftable where Name=%s", (value,))
        result = cur.fetchall()
    elif option=='Category':
        cur.execute("select * from ftable where Category=%s", (value,))
        result = cur.fetchall()
    elif option=='Price':
        cur.execute("select * from ftable where Price=%s",(value,))
        result=cur.fetchall()
    return result

def sort(option,order):
    global result
    if option=='SNo' and order=="Ascending":
        cur.execute("select * from ftable order by SNo")
        result = cur.fetchall()
    elif option=='SNo' and order=="Descending":
        cur.execute("select * from ftable order by SNo desc")
        result = cur.fetchall()
    elif option=='Name' and order=="Ascending":
        cur.execute("select * from ftable order by Name")
        result = cur.fetchall()
    elif option=='Category' and order=="Ascending":
        cur.execute("select * from ftable order by Category")
        result = cur.fetchall()
    elif option=='Price' and order=="Ascending":
        cur.execute("select * from ftable order by Price;")
        result=cur.fetchall()
    elif option=='Name' and order=="Descending":
        cur.execute("select * from ftable order by Name desc")
        result = cur.fetchall()
    elif option=='Category' and order=="Descending":
        cur.execute("select * from ftable order by Category desc")
        result = cur.fetchall()
    elif option=='Price' and order=="Descending":
        cur.execute("select * from ftable order by Price desc;")
        result=cur.fetchall()
    return result

def deleteall_rec():
    cur.execute("drop table ftable;")
    con.commit()