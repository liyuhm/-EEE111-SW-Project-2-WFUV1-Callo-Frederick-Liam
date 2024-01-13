import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import db_if

app = customtkinter.CTk()
app.title('Employee Management System')
app.geometry('1500x500')
app.config(bg='#161C25')
app.resizable(False, False)

font1 = ('Arial', 20, 'bold')
font2 = ('Arial', 12, 'bold')

def newCtkLabel(text = 'CTK Label'):
    widget_Font=font1
    widget_TextColor='#FFF'
    widget_BgColor='#161C25'

    widget = customtkinter.CTkLabel(app, 
                                  text=text,
                                  font=widget_Font, 
                                  text_color=widget_TextColor,
                                  bg_color=widget_BgColor)
    return widget

def newCtkEntry(text = 'CTK Label'):
    widget_Font=font1
    widget_TextColor='#000'
    widget_FgColor='#FFF'
    widget_BorderColor='#0C9295'
    widget_BorderWidth=2
    widget_Width=250

    widget = customtkinter.CTkEntry(app,
                                  font=widget_Font,
                                  text_color=widget_TextColor,
                                  fg_color=widget_FgColor,
                                  border_color=widget_BorderColor,
                                  border_width=widget_BorderWidth,
                                  width=widget_Width)
    return widget

def newCtkComboBox(options=['DEFAULT', 'OTHER'], entryVariable=None):
    widget_Font=font1
    widget_TextColor='#000'
    widget_FgColor='#FFF'
    widget_DropdownHoverColor='#0C9295'
    widget_ButtonColor='#0C9295'
    widget_ButtonHoverColor='#0C9295'
    widget_BorderColor='#0C9295'
    widget_BorderWidth=2
    widget_Width=250
    widget_Options=options

    widget = customtkinter.CTkComboBox(app,
                                    font=widget_Font,
                                    text_color=widget_TextColor,
                                    fg_color=widget_FgColor,
                                    border_color=widget_BorderColor,
                                    width=widget_Width,
                                    variable=entryVariable,
                                    values=options,
                                    state='readonly')
    
    # set default value to 1st option
    widget.set(options[0])

    return widget

def newCtkButton(text = 'CTK Button', onClickHandler=None, fgColor='#161C25', hoverColor='#FF5002', bgColor='#161C25', borderColor='#F15704'):
    widget_Font=font1
    widget_TextColor='#FFF'
    widget_FgColor=fgColor
    widget_HoverColor=hoverColor
    widget_BackgroundColor=bgColor
    widget_BorderColor=borderColor
    widget_BorderWidth=2
    widget_Cursor='hand2'
    widget_CornerRadius=15
    widget_Width=260
    widget_Function=onClickHandler

    widget = customtkinter.CTkButton(app,
                                    text=text,
                                    command=widget_Function,
                                    font=widget_Font,
                                    text_color=widget_TextColor,
                                    fg_color=widget_FgColor,
                                    hover_color=widget_HoverColor,
                                    bg_color=widget_BackgroundColor,
                                    border_color=widget_BorderColor,
                                    border_width=widget_BorderWidth,
                                    cursor=widget_Cursor,
                                    corner_radius=widget_CornerRadius,
                                    width=widget_Width)
    

    return widget


def add_to_treeview():
    employees = db_if.fetch_employees()
    tree.delete(*tree.get_children())
    for employee in employees:
        tree.insert('', END, values=employee)

def clear_form(*clicked):
    if clicked:
        tree.selection_remove(tree.focus())
        tree.focus('')
    id_entry.delete(0, END)
    name_entry.delete(0, END)
    role_cboxVar.set('SW-Engineer')
    gender_cboxVar.set('Male')
    status_cboxVar.set('On-Site')

def read_display_data(event):
    selected_item = tree.focus()
    if selected_item:
        row = tree.item(selected_item)['values']
        clear_form()
        id_entry.insert(0, row[0])
        name_entry.insert(0, row[1])
        role_cboxVar.set(row[2])
        gender_cboxVar.set(row[3])
        status_cboxVar.set(row[4])
    else:
        pass

def add_entry():
    id=id_entry.get()
    name=name_entry.get()
    role=role_cboxVar.get()
    gender=gender_cboxVar.get()
    status=status_cboxVar.get()

    if not (id and name and role and gender and status):
        messagebox.showerror('Error', 'Enter all fields.')
    elif db_if.id_exists(id):
        messagebox.showerror('Error', 'ID already exists')
    else:
        db_if.insert_employee(id, name, role, gender, status)
        add_to_treeview()
        clear_form()
        messagebox.showinfo('Success', 'Data has been inserted')

def delete_entry():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Choose an employee to delete')
    else:
        id = id_entry.get()
        db_if.delete_employee(id)
        add_to_treeview()
        clear_form()
        messagebox.showinfo('Success', 'Data has been deleted')


def update_entry():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Choose an employee to update')
    else:
        id=id_entry.get()
        name=name_entry.get()
        role=role_cboxVar.get()
        gender=gender_cboxVar.get()
        status=status_cboxVar.get()
        db_if.update_employee(name, role, gender, status, id)
        add_to_treeview()
        clear_form()
        messagebox.showinfo('Success', 'Data has been updated')

id_label = newCtkLabel('ID')
id_label.place(x=20, y=40)
id_entry = newCtkEntry()
id_entry.place(x=100, y=40)

name_label = newCtkLabel('Name')
name_label.place(x=20, y=100)
name_entry = newCtkEntry()
name_entry.place(x=100, y=100)

role_label = newCtkLabel('Role')
role_label.place(x=20, y=160)
# role_entry = newCtkEntry()
# role_entry.place(x=100, y=160)
role_cboxVar = StringVar()
role_cboxOptions = ['SW-Engineer', 'HW-Engineer', 'FW-Engineer', 'Layout-Engineer', 'Project-Manager', 'System-Architect']
role_cbox = newCtkComboBox(options=role_cboxOptions, 
                             entryVariable=role_cboxVar)
role_cbox.place(x=100, y=160)


gender_label = newCtkLabel('Gender')
gender_label.place(x=20, y=220)
gender_cboxVar = StringVar()
gender_cboxOptions = ['Male', 'Female']
gender_cbox = newCtkComboBox(options=gender_cboxOptions, 
                             entryVariable=gender_cboxVar)
gender_cbox.place(x=100, y=220)

status_label = newCtkLabel('Status')
status_label.place(x=20, y=280)
# status_entry = newCtkEntry()
# status_entry.place(x=100, y=280)
status_cboxVar = StringVar()
status_cboxOptions = ['On-Site', 'Remote', 'Sick-Leave', 'On-Leave', 'On-Trip', 'On-Training']
status_cbox = newCtkComboBox(options=status_cboxOptions, 
                             entryVariable=status_cboxVar)
status_cbox.place(x=100, y=280)

add_button = newCtkButton(text='Add Employee',
                          onClickHandler=add_entry,
                          fgColor='#05A312',
                          hoverColor='#00850B',
                          borderColor='#05A312')
add_button.place(x=50,y=350)

new_button = newCtkButton(text='New Employee',
                          onClickHandler=lambda:clear_form(True))
new_button.place(x=50,y=400)

update_button = newCtkButton(text='Update Employee',
                             onClickHandler=update_entry)
update_button.place(x=360,y=400)

delete_button = newCtkButton(text='Delete Employee',
                            onClickHandler=delete_entry,
                            fgColor='#E40404',
                            hoverColor='#AE0000',
                            borderColor='#E40404')
delete_button.place(x=670,y=400)

style = ttk.Style(app)
style.theme_use('clam')
style.configure('Treeview', 
                font=font2, 
                foreground='#fff',
                background='#000',
                fieldlbackground='#313837')

style.map('Treeview', background=[('selected', '#1A8F2D')])

tree = ttk.Treeview(app, height=15)
tree['columns'] = ('ID', 'Name', 'Role', 'Gender', 'Status')
tree.column('#0', width=0, stretch=tk.NO)
tree.column('ID', anchor=tk.CENTER, width=10)
tree.column('Name', anchor=tk.CENTER, width=150)
tree.column('Role', anchor=tk.CENTER, width=150)
tree.column('Gender', anchor=tk.CENTER, width=10)
tree.column('Status', anchor=tk.CENTER, width=150)

tree.heading('ID', text='ID')
tree.heading('Name', text='Name')
tree.heading('Role', text='Role')
tree.heading('Gender', text='Gender')
tree.heading('Status', text='Status')

tree.place(x=360, y=20, width=1000, height=350)

tree.bind('<ButtonRelease>', read_display_data)




add_to_treeview()

app.mainloop()