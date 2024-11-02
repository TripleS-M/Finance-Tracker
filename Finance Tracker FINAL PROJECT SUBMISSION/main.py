from customtkinter import *
from PIL import Image
from tkinter import ttk, messagebox
import database

#Functions(integrate functions from database file into here)

def delete_all():
    result=messagebox.askyesno('Delete all records', 'Are you sure you want to delete all records?')
    if result:
        database.deleteall_rec()
        clear()
def show_all():
    treeview_data()
    searchEntry.delete(0, END)
    searchBox.set('Search By')
    orderBox.set('Order By')
    sortBox.set('Sort By')
def search_item():
    if searchEntry.get()=='':
        messagebox.showerror('Error','Enter value to search')
    elif searchBox.get()=='Search By':
        messagebox.showerror('Error','Select an option to search by')
    else:
        searched_data=database.search(searchBox.get(),searchEntry.get())
        tree.delete(*tree.get_children())
        for i in searched_data:
            tree.insert('', END, values=i)

def sort_by():
    if sortBox.get()=='Sort By':
        if orderBox.get()=='Order By' and sortBox.get()=='Sort By':
            messagebox.showerror('Error','Select options to order and sort')
        else:
            messagebox.showerror('Error','Select option to sort by')
    elif orderBox.get()=='Order By':
        if orderBox.get()=='Order By' and sortBox.get()=='Sort By':
            messagebox.showerror('Error','Select options to order and sort')
        else:
            messagebox.showerror('Error','Select option to order by')
    else:
        sorted_data=database.sort(sortBox.get(),orderBox.get())
        tree.delete(*tree.get_children())
        for i in sorted_data:
            tree.insert('',END,values=i)

def treeview_data():
    items=database.fetch_items()
    tree.delete(*tree.get_children())
    for i in items:
        tree.insert('',END, values=i)
def add_item():
    if idEntry.get()=='' or nameEntry.get()=='' or categEntry.get()=='' or priceEntry.get()=='':
        messagebox.showerror('Error','Please fill all the fields')
    elif database.id_exists(list(idEntry.get())):
        messagebox.showerror('Error','This ID already exists')
    elif (priceEntry.get().isnumeric()==False and idEntry.get().isnumeric()==False) or idEntry.get().isnumeric()==False or priceEntry.get().isnumeric()==False:
        if priceEntry.get().isnumeric()==False and idEntry.get().isnumeric()==False:
            messagebox.showerror('Error', 'Please enter a VALID PRICE and VALID ID')
        elif priceEntry.get().isnumeric()==False:
            messagebox.showerror('Error', 'Please enter a VALID PRICE')
        elif idEntry.get().isnumeric()==False:
            messagebox.showerror('Error', 'Please enter a VALID ID')
    else:
        database.insert(idEntry.get(),nameEntry.get(),categEntry.get(),priceEntry.get())
        treeview_data()
        clear()

def update_item():
    selected_item=tree.selection()
    if not selected_item:
        messagebox.showerror('Error','Select an item')
    else:
        database.update(idEntry.get(),nameEntry.get(),categEntry.get(),priceEntry.get())
        treeview_data()
        clear()
        messagebox.showinfo('Success','Item updated')
def clear(val=False):
    if val:
        tree.selection_remove(tree.focus())
    idEntry.delete(0,END)
    nameEntry.delete(0,END)
    categEntry.delete(0,END)
    priceEntry.delete(0,END)

def delete_item():
    selected_item=tree.selection()
    if not selected_item:
        messagebox.showerror('Error','Select an item')
    else:
        database.delete(idEntry.get())
        treeview_data()
        clear()
        messagebox.showerror('Error',"Item deleted")

def selection(event):
    selected_item=tree.selection()
    if selected_item:
        row=tree.item(selected_item)['values']
        clear()
        idEntry.insert(0,row[0])
        nameEntry.insert(0,row[1])
        categEntry.insert(0,row[2])
        priceEntry.insert(0,row[3])


#GUI Part
window=CTk()
window.geometry('1230x600+100+100')
window.resizable(False, False)
window.title("Finance Tracker")
window.configure(fg_color = '#dad7cd')
logo=CTkImage(Image.open('bg.png'),size=(1230,208))
logoLabel=CTkLabel(window,image=logo,text='')
logoLabel.grid(row=0,column=0,columnspan=2)

leftFrame=CTkFrame(window,fg_color='#588157')
leftFrame.grid(row=1,column=0,padx=20)

idLabel=CTkLabel(leftFrame,text='ID',font=('arial',18,'bold'),text_color='#fefae0')
idLabel.grid(row=0,column=0,padx=20,pady=15)

idEntry=CTkEntry(leftFrame,font=('arial',18,'bold'),width=180)
idEntry.grid(row=0,column=1,padx=5)

nameLabel=CTkLabel(leftFrame,text='Name',font=('arial',18,'bold'),text_color='#fefae0')
nameLabel.grid(row=1,column=0,padx=20,pady=20)

nameEntry=CTkEntry(leftFrame,font=('arial',18,'bold'),width=180)
nameEntry.grid(row=1,column=1,padx=5)

categLabel=CTkLabel(leftFrame,text='Category',font=('arial',18,'bold'),text_color='#fefae0')
categLabel.grid(row=2,column=0,padx=20,pady=20)

categEntry=CTkEntry(leftFrame,font=('arial',18,'bold'),width=180)
categEntry.grid(row=2,column=1,padx=5)

priceLabel=CTkLabel(leftFrame,text='Price',font=('arial',18,'bold'),text_color='#fefae0')
priceLabel.grid(row=3,column=0,padx=20,pady=15)

priceEntry=CTkEntry(leftFrame,font=('arial',18,'bold'),width=180)
priceEntry.grid(row=3,column=1,padx=5)

rightFrame=CTkFrame(window)
rightFrame.grid(row=1,column=1,pady=15,padx=10)

#searchby code
search_options=['SNo','Name','Category','Price']
searchBox=CTkComboBox(rightFrame,values=search_options,state='readonly',width=98)
searchBox.grid(row=0,column=0,sticky=E)
searchBox.set('Search By')
searchEntry=CTkEntry(rightFrame,width=95)
searchEntry.grid(row=0,column=1)
searchButton=CTkButton(rightFrame,text='Search',width=80,command=search_item,fg_color='#386641',hover_color='#3a5a40')
searchButton.grid(row=0,column=2,sticky=W)

#sortby code
sortBox=CTkComboBox(rightFrame,values=search_options,state='readonly',width=98)
sortBox.grid(row=0,column=3)
sortBox.set('Sort By')
order_options = ['Ascending','Descending']
orderBox=CTkComboBox(rightFrame,values=order_options,state='readonly',width=105)
orderBox.grid(row=0,column=4)
orderBox.set('Order By')
sortButton=CTkButton(rightFrame,text='Sort',width=70,command=sort_by,fg_color='#386641',hover_color='#3a5a40')
sortButton.grid(row=0,column=5,sticky=W)

tree=ttk.Treeview(rightFrame,height=13)
tree.grid(row=1,column=0,columnspan=6)

tree['columns']=('ID','Name','Category','Price')

tree.heading('ID',text='ID',anchor=CENTER)
tree.heading('Name',text='Name',anchor=CENTER)
tree.heading('Category',text='Category',anchor=CENTER)
tree.heading('Price',text='Price',anchor=CENTER)

tree.config(show='headings')

tree.column('ID',width=110)
tree.column('Name',width=240)
tree.column('Category',width=200)
tree.column('Price',width=160)

style=ttk.Style()

style.configure('Treeview.Heading',font=('arial',25,'bold'))
style.configure('Treeview',font=('arial',20,'bold'),rowheight=25,background='#386641',foreground='#fefae0')

scrollbar=ttk.Scrollbar(rightFrame,orient=VERTICAL,command=tree.yview)
scrollbar.grid(row=1,column=6,sticky='ns')
tree.configure(yscrollcommand=scrollbar.set)

buttonFrame=CTkFrame(window,fg_color='#dad7cd')
buttonFrame.grid(row=2,column=0,columnspan=2)#pady here to give gap

newButton=CTkButton(buttonFrame,text='New Item',font=('arial',15,'bold'),width=130,corner_radius=15,fg_color='#386641',hover_color='#3a5a40',command=lambda: clear(True))#idk what lambda does
newButton.grid(row=0,column=0,pady=5)

addButton=CTkButton(buttonFrame,text='Add Item',font=('arial',15,'bold'),width=130,corner_radius=15,fg_color='#386641',hover_color='#3a5a40',command=add_item)
addButton.grid(row=0,column=1,pady=5,padx=5)

updateButton=CTkButton(buttonFrame,text='Update Item',font=('arial',15,'bold'),width=130,corner_radius=15,fg_color='#386641',hover_color='#3a5a40',command=update_item)
updateButton.grid(row=0,column=2,pady=5,padx=5)

deleteButton=CTkButton(buttonFrame,text='Delete Item',font=('arial',15,'bold'),width=130,corner_radius=15,fg_color='#386641',hover_color='#3a5a40',command=delete_item)
deleteButton.grid(row=0,column=3,pady=5,padx=5)

deleteallButton=CTkButton(buttonFrame,text='Delete All',font=('arial',15,'bold'),width=130,corner_radius=15,fg_color='#386641',hover_color='#3a5a40',command=delete_all)
deleteallButton.grid(row=0,column=4,pady=5,padx=5)

showallButton=CTkButton(buttonFrame,text='Show All',font=('arial',15,'bold'),width=130,corner_radius=15,fg_color='#386641',hover_color='#3a5a40',command=show_all)
showallButton.grid(row=0,column=5,pady=5)

treeview_data()

window.bind('<ButtonRelease>',selection)

window.mainloop()