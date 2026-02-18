from tkinter import *
from tkinter import messagebox
import json
import os

fileName = 'contacts.json'


def loadcontacts():
    if os.path.exists(fileName):
        with open(fileName, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def savecontact():
    with open(fileName, 'w', encoding='utf-8') as f:
        json.dump(contacts, f, ensure_ascii=False, indent=4)


def updatecontact():
    contactList.delete(0, END)
    for c in contacts:
        contactList.insert(END, f"{c['name']} - {c['phone']}")


def addcontact():
    name = inputName.get().strip()
    phone = inputPhone.get().strip()

    if not name or not phone:
        messagebox.showwarning('خطا', 'نام و شماره تلفن الزامی است')
        return

    for c in contacts:
        if c['name'] == name:
            answer = messagebox.askyesno(
                'هشدار',
                'نام مخاطب تکراری است، جایگزین شود؟'
            )
            if answer:
                c['phone'] = phone
                savecontact()
                updatecontact()
            return

    contacts.append({'name': name, 'phone': phone})
    savecontact()
    updatecontact()

    inputName.delete(0, END)
    inputPhone.delete(0, END)


def delcontact():
    selected = contactList.curselection()
    if not selected:
        messagebox.showwarning('خطا', 'یک مخاطب انتخاب کنید')
        return

    for i in reversed(selected):
        name = contactList.get(i).split(' - ')[0]
        contacts[:] = [c for c in contacts if c['name'] != name]
        contactList.delete(i)

    savecontact()


# ---------------- GUI ----------------

contacts = loadcontacts()

root = Tk()
root.title("دفترچه تلفن")
root.geometry("420x320")

font_fa = ("Tahoma", 10)

frameTop = Frame(root)
frameTop.pack(pady=10)

inputName = Entry(frameTop, font=font_fa, justify='right')
inputName.grid(row=0, column=0)
Label(frameTop, text='نام', font=font_fa).grid(row=0, column=1)

inputPhone = Entry(frameTop, font=font_fa, justify='right')
inputPhone.grid(row=1, column=0)
Label(frameTop, text="تلفن", font=font_fa).grid(row=1, column=1)

addBut = Button(frameTop, text='افزودن مخاطب', font=font_fa, command=addcontact)
addBut.grid(row=2, column=0, columnspan=2, pady=5)

contactList = Listbox(
    root,
    selectmode=MULTIPLE,
    width=50,
    height=10,
    font=font_fa,
    justify='right'
)
contactList.pack()

delBut = Button(root, text='حذف مخاطب', font=font_fa, command=delcontact)
delBut.pack(pady=5)

updatecontact()
root.mainloop()