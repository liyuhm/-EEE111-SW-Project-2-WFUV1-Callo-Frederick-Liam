import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from PlayListDbSqlite import PlaylistDbSqlite
from datetime import date

class PlayListGuiCtk(customtkinter.CTk):

    def __init__(self, dataBase=PlaylistDbSqlite('PlayList.db')):
        super().__init__()
        self.db = dataBase

        self.title('PlayLister')
        self.geometry('1500x500')
        self.config(bg='#191414')
        self.resizable(False, False)

        self.font1 = ('Calibri', 15, 'bold')
        self.font2 = ('Calibri', 12, 'bold')
        self.font3 = ('Calibri', 12, 'bold')

        # Data Entry Form
        # 'ID' Label and Entry Widgets
        self.id_label = self.newCtkLabel('Song ID')
        self.id_label.place(x=20, y=30)
        self.id_entry = self.newCtkID()
        self.id_entry.place(x=110, y=30)

        # 'Title' Label and Entry Widgets
        self.title_label = self.newCtkLabel('Song Title')
        self.title_label.place(x=20, y=70)
        self.title_entry = self.newCtkEntry()
        self.title_entry.place(x=110, y=70)

        # 'Artist' Label and Entry Widgets
        self.artist_label = self.newCtkLabel('Artist')
        self.artist_label.place(x=20, y=110)
        self.artist_entry = self.newCtkEntry()
        self.artist_entry.place(x=110, y=110)

        # 'Genre' Label and Combo Box Widgets
        self.genre_label = self.newCtkLabel('Genre')
        self.genre_label.place(x=20, y=150)
        self.genre_cboxVar = StringVar()
        self.genre_cboxOptions = ['Pop', 'K-Pop', 'Rock', 'Hip-Hop', 'RnB', 'Jazz']
        self.genre_cbox = self.newCtkComboBox(options=self.genre_cboxOptions, 
                                    entryVariable=self.genre_cboxVar)
        self.genre_cbox.place(x=110, y=150)

       # 'Date_Added' Label and Entry Widgets
        self.added_label = self.newCtkLabel('Date Added')
        self.added_label.place(x=20, y=190)
        self.added_entry = self.newCtkEntry()
        self.added_entry.place(x=110, y=190)

        # 'Spotify Link' Label and Entry Widgets
        self.spot_label = self.newCtkLabel('Spotify Link')
        self.spot_label.place(x=20, y=230)
        self.spot_entry = self.newCtkEntry()
        self.spot_entry.place(x=110, y=230)

        #Buttons
        self.add_button = self.newCtkButton(text='Add Song',
                                onClickHandler=self.add_entry,
                                fgColor='#1db954',
                                hoverColor='#1ed760',
                                borderColor='#1db954')
        self.add_button.place(x=50,y=350)

        self.new_button = self.newCtkButton(text='New Song',
                                onClickHandler=lambda:self.clear_form(True))
        self.new_button.place(x=50,y=400)

        self.update_button = self.newCtkButton(text='Update Song',
                                    onClickHandler=self.update_entry)
        self.update_button.place(x=360,y=400)

        self.delete_button = self.newCtkButton(text='Remove from Playlist',
                                    onClickHandler=self.delete_entry,
                                    fgColor='#8D021F',
                                    hoverColor='#420D09',
                                    borderColor='#8D021F')
        self.delete_button.place(x=670,y=400)

        self.export_button = self.newCtkButton(text='Export to CSV',
                                    onClickHandler=self.export_to_csv)
        self.export_button.place(x=980,y=400)

        self.add_button = self.newCtkButton(text = 'Import CSV',
                                            onClickHandler=self.import_from_csv)
        self.add_button.place(x=1290,y=400)


        # Tree View for Database Entries
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Treeview', 
                        font=self.font2, 
                        foreground='#FFFFFF',
                        background='#191414',
                        fieldlbackground='#191414')

        self.style.map('Treeview', background=[('selected', '#1A8F2D')])

        self.songtree = ttk.Treeview(self, height=15)
        self.songtree['columns'] = ('Song ID', 'Song Title', 'Artist', 'Genre', 'Spotify Link', 'Date Added')
        self.songtree.column('#0', width=0, stretch=tk.NO)
        self.songtree.column('Song ID', anchor=tk.CENTER, width=100)
        self.songtree.column('Song Title', anchor=tk.CENTER, width=100)
        self.songtree.column('Artist', anchor=tk.CENTER, width=100)
        self.songtree.column('Genre', anchor=tk.CENTER, width=20)
        self.songtree.column('Spotify Link', anchor=tk.CENTER, width=150)
        self.songtree.column('Date Added', anchor=tk.CENTER, width=50)

        self.songtree.heading('Song ID', text='Song ID')
        self.songtree.heading('Song Title', text='Song Title')
        self.songtree.heading('Artist', text='Artist')
        self.songtree.heading('Genre', text='Genre')
        self.songtree.heading('Spotify Link', text='Spotify Link')
        self.songtree.heading('Date Added', text='Date Added')

        self.songtree.place(x=400, y=20, width=1000, height=340)
        self.songtree.bind('<ButtonRelease>', self.read_display_data)

        self.add_to_treeview()

    # new Label Widget
    def newCtkLabel(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_BgColor='#161C25'

        widget = customtkinter.CTkLabel(self, 
                                    text=text,
                                    font=widget_Font, 
                                    text_color=widget_TextColor,
                                    bg_color=widget_BgColor)
        return widget

    # new Entry Widget
    def newCtkEntry(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=250

        widget = customtkinter.CTkEntry(self,
                                    font=widget_Font,
                                    text_color=widget_TextColor,
                                    fg_color=widget_FgColor,
                                    border_color=widget_BorderColor,
                                    border_width=widget_BorderWidth,
                                    width=widget_Width)
        return widget

    def newCtkID(self, text = 'CTK Label'):
        widget_Font=self.font3
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=1
        widget_Width=80

        widget = customtkinter.CTkEntry(self,
                                    font=widget_Font,
                                    text_color=widget_TextColor,
                                    fg_color=widget_FgColor,
                                    border_color=widget_BorderColor,
                                    border_width=widget_BorderWidth,
                                    width=widget_Width)
        return widget

    # new Combo Box Widget
    def newCtkComboBox(self, options=['DEFAULT', 'OTHER'], entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_DropdownHoverColor='#0C9295'
        widget_ButtonColor='#0C9295'
        widget_ButtonHoverColor='#0C9295'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=250
        widget_Options=options

        widget = customtkinter.CTkComboBox(self,
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

    # new Button Widget
    def newCtkButton(self, text = 'CTK Button', onClickHandler=None, fgColor='#1db954', hoverColor='#1ed760', bgColor='#191414', borderColor='#1db954'):
        widget_Font=self.font1
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

        widget = customtkinter.CTkButton(self,
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
                                        width=200)
       
        return widget

    # Handles
    def add_to_treeview(self):
        songs = self.db.fetch_songs()
        self.songtree.delete(*self.songtree.get_children())
        for song in songs:
            print(song)
            self.songtree.insert('', END, values=song)

    def get_genre(self):
        rows = self.db.fetch_genres()
        if (rows.count == 0):
             rows = ['Pop', 'K-Pop', 'Rock', 'Hip-Hop', 'RnB', 'Jazz']
        
        return rows

    def clear_form(self, *clicked):
        if clicked:
            self.songtree.selection_remove(self.songtree.focus())
            self.songtree.focus('')
        self.id_entry.delete(0, END)
        self.title_entry.delete(0, END)
        self.genre_cboxVar.set('Pop')
        self.artist_entry.delete(0, END)
        self.spot_entry.delete(0, END)
        self.added_entry.delete(0,END)

    def read_display_data(self, event):
        selected_item = self.songtree.focus()
        if selected_item:
            row = self.songtree.item(selected_item)['values']
            self.clear_form()
            self.id_entry.insert(0, row[0])
            self.title_entry.insert(0, row[1])
            self.artist_entry.insert(0,row[2])
            self.genre_cboxVar.set(row[3])
            self.spot_entry.insert(0,row[4])
            self.added_entry.insert(0,row[5])
        else:
            pass

    def add_entry(self):
        id = self.id_entry.get()
        title = self.title_entry.get()
        artist = self.artist_entry.get()
        genre=self.genre_cboxVar.get()
        spot = self.spot_entry.get()

        if not (id and title and artist and genre and spot):
            messagebox.showerror('Error', 'Enter all fields.')
        elif self.db.songID_exists(id):
            messagebox.showinfo('Error', 'Song ID already exists')
        else:
            self.db.insert_song(id, title, artist, genre, spot, date.today())
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been inserted')

    def delete_entry(self):
        selected_item = self.songtree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose the Song ID to delete')
        else:
            id = self.id_entry.get()
            self.db.delete_song(id)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been deleted')

    def update_entry(self):
        selected_item = self.songtree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose the song to update')
        else:
            songID=self.id_entry.get()
            title=self.title_entry.get()
            artist = self.artist_entry.get()
            genre=self.genre_cboxVar.get()
            added=self.added_entry.get()
            spot=self.spot_entry.get()
            #self.db.update_song(title, artist, genre, added, spot, id)
            self.db.update_playlist(title, artist, genre, added, spot, songID)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been updated')

    def export_to_csv(self):
        self.db.export_csv()
        messagebox.showinfo('Success', f'Data exported to {self.db.dbName}.csv')

    def import_from_csv(self):
        self.db.import_csv()
        self.add_to_treeview()
        messagebox.showinfo('Success', f'Data Imported from {self.db.dbName}.csv')