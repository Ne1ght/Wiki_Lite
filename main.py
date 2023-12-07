import  os
import sys
import subprocess
from pathlib import Path
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import PIL.Image
from PIL import Image, ImageTk
import zipfile
import webbrowser
import requests
import sqlite3


def create_virtualenv(venv_path):
    subprocess.run([sys.executable, "-m", "venv", str(venv_path)])

def install_dependencies(venv_path):
    subprocess.run([str(venv_path / "bin" / "pip"), "install", "-r", "requirements.txt"])

def setup_environment(venv_path):
    if not venv_path.is_dir():
        create_virtualenv(venv_path)
        install_dependencies(venv_path)

    # Create a marker file to indicate that setup is completed
    Path("setup_completed.marker").touch()

def check_previous_setup():
    # Check for the marker file
    return Path("setup_completed.marker").is_file()

def main():
    # Determine the virtual environment path
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        # If in a virtual environment, use sys.prefix
        venv_path = Path(sys.prefix)
    else:
        # If not in a virtual environment, use the current working directory
        venv_path = Path.cwd()

    if not check_previous_setup():
        setup_environment(venv_path)

def is_update_needed(current_version):
    # Replace 'username' and 'repo' with your GitHub username and repository name
    latest_release_url = 'https://github.com/Ne1ght/Wiki_Lite/releases/latest'

    response = requests.get(latest_release_url)
    latest_version = response.url.split("/")[-1]

    return latest_version > current_version


def check_for_updates(root_window):
    # Replace 'current_version' with your current version number
    current_version = 'your_current_version'

    if is_update_needed(current_version):
        response = messagebox.askyesno("Update Available",
                                       "A new update is available. Do you want to download and install it?")
        if response == YES:
            download_and_install_update(root_window)


def download_and_install_update(root_window):
    # Replace 'username' and 'repo' with your GitHub username and repository name
    download_url = 'https://github.com/Ne1ght/Wiki_Lite/archive/main.zip'

    response = requests.get(download_url)

    with open('latest_release.zip', 'wb') as file:
        file.write(response.content)

    with zipfile.ZipFile('latest_release.zip', 'r') as zip_ref:
        zip_ref.extractall('.')

    os.remove('latest_release.zip')

    messagebox.showinfo("Update Installed", "The update has been installed. Please restart the program.")
    restart_program(root_window)


def restart_program(root):
    root.destroy()
    # Re-run your main script to restart the program

con = sqlite3.connect("DataBase.db")
cur = con.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS Head_category (
        id_Head_category INTEGER PRIMARY KEY,
        Head_category_name TEXT,
        image_filename TEXT,
        category_type TEXT
        )
""")
con.commit()

cur.execute("""
    CREATE TABLE IF NOT EXISTS sub_category (
    id INTEGER PRIMARY KEY,
    Header_Info_name TEXT,
    Sub_Category_name TEXT,
    image_filename TEXT
    )
""")
con.commit()

cur.execute("""
    CREATE TABLE IF NOT EXISTS category_Infomation (
    id_category_infomation INTEGER PRIMARY KEY,
    Header_info_name TEXT,
    Info_name TEXT,
    Info_Sum_Text TEXT,
    Info_Full_Text TEXT
    )
""")
con.commit()


class AddWindow:
    def __init__(self, root_window):
        self.mainroot = root_window

        self.Info_Header_Name = None  # Initialize Info_Header_Name

        self.selected_file = None  # Initialize self.selected_file to None

        self.add_window = Toplevel(self.mainroot)
        self.add_window.title("Add Window")
        self.add_window.geometry("800x400")

        validate_cmd = self.mainroot.register(self.on_validate)


        self.add_frame = Frame(self.add_window)
        self.add_frame.pack()

        cur.execute("SELECT Head_category_name from Head_category")
        self.Head_table_categorys = cur.fetchall()
        print(self.Head_table_categorys)

        cur.execute("SELECT Header_Info_name, Sub_Category_name FROM sub_category")
        self.Sub_table_categorys = cur.fetchall()
        print(self.Sub_table_categorys)

        self.Main_listbox = Listbox(self.add_frame,
                               selectmode=SINGLE,
                               font=("Myriad Pro", 15)
                               )
        self.Main_listbox.grid(row=1, column=1)

        for entry in self.Head_table_categorys:
            self.Main_listbox.insert(END, entry[0])  # Extracting the value from the single-element tuple

        self.Main_listbox.bind('<<ListboxSelect>>', self.on_select_headlist)

        self.Sub_listbox = Listbox(self.add_frame,
                                   selectmode=SINGLE,
                                   font=("Myriad Pro", 15)
                                   )
        self.Sub_listbox.grid(row=1, column=2)

        self.Sub_listbox.bind('<<ListboxSelect>>', self.on_select_sublist)

        self.add_Info_button = Button(self.add_frame,
                                 text="Add Infomation",
                                 font=("Myriad Pro", 20),
                                 relief=RAISED,
                                 command=self.add_infomation
                                      )
        self.add_Info_button.grid(row=2, column=1)

        self.add_sub_category_button = Button(self.add_frame,
                                              text="Add Sub Category",
                                              font=("Myriad Pro", 20),
                                              relief=RAISED,
                                              command=self.add_sub_category
                                              )
        self.add_sub_category_button.grid(row=2, column=2)

        self.add_sub_category_frame = Frame(self.add_window)

        self.add_sub_category_label = Label(self.add_sub_category_frame,
                                            text="Enter Values for the sub Cat",
                                            font=("Myriad Pro", 20),
                                            relief=RAISED)

        self.head_categoryis_label = Label(self.add_sub_category_frame,
                                           text="",
                                           font=("Myriad Pro", 20),
                                           relief=RAISED)

        self.enter_cate_name = Label(self.add_sub_category_frame,
                                     text="Enter a name",
                                     font=("Myriad Pro", 20),
                                     relief=RAISED)
        self.entry_cate_name = Entry(self.add_sub_category_frame)

        self.select_file_label = Label(self.add_sub_category_frame,
                                       text="Select a file",
                                       font=("Myriad Pro", 20),
                                       relief=RAISED)

        self.select_file_button = Button(self.add_sub_category_frame,
                                         text="Select",
                                         font=("Myriad Pro", 20),
                                         relief=RAISED,
                                         command=self.select_file)

        self.add_sub_category = Button(self.add_sub_category_frame,
                                       text="Add category",
                                       font=("Myriad Pro", 20),
                                       relief=RAISED,
                                       command=self.add_sub_category
                                       )

        self.add_Infomation_frame = Frame(self.add_window)

        self.add_Infomation_label = Label(self.add_Infomation_frame,
                                            text="Enter Values for the Infomation",
                                            font=("Myriad Pro", 20),
                                            relief=RAISED)

        self.head_categoryis_finfo_label = Label(self.add_Infomation_frame,
                                           text="",
                                           font=("Myriad Pro", 20),
                                           relief=RAISED)

        self.add_Infomation_name = Label(self.add_Infomation_frame,
                                     text="Enter a name",
                                     font=("Myriad Pro", 20),
                                     relief=RAISED)
        self.enrty_Infomation_name = Entry(self.add_Infomation_frame)

        self.add_Infomation_sum_Label = Label(self.add_Infomation_frame,
                                              text="Enter a Summary",
                                              font=("Myriad Pro", 20),
                                              relief=RAISED)

        self.add_Infomation_sum_Text = Text(self.add_Infomation_frame,
                                             height=30,
                                             width=75,
                                             wrap="word",
                                             insertborderwidth=2,
                                             padx=5,
                                             pady=5)

        self.add_Infomation_sum_Text_scrollbar = Scrollbar(self.add_Infomation_frame,
                                                           command=self.add_Infomation_sum_Text.yview)

        self.error_label = Label(self.add_Infomation_frame)

        self.add_Infomation_sum_Text.bind('<Key>', lambda e: self.on_validate(e.char))

        self.add_Infomation_full_Label = Label(self.add_Infomation_frame,
                                              text="Enter the Full Version",
                                              font=("Myriad Pro", 20),
                                              relief=RAISED)

        self.add_Infomation_full_Text = Text(self.add_Infomation_frame,
                                            height=30,
                                            width=75,
                                            wrap="word",
                                            insertborderwidth=2,
                                            padx=5,
                                            pady=5)

        self.add_Infomation_full_Text_scrollbar = Scrollbar(self.add_Infomation_frame)


        self.add_Infomation = Button(self.add_Infomation_frame,
                                       text="Add Infomation",
                                       font=("Myriad Pro", 20),
                                       relief=RAISED,
                                       command=self.add_infomation
                                       )


    def on_select_headlist(self, event):
        if self.Main_listbox.curselection():
            selected_index = self.Main_listbox.curselection()[0]
            print(selected_index)
            selected = self.Main_listbox.get(selected_index)
            print("Selected from list 1:", selected)  # Print value from list 1
            self.filter_list2(selected)

            self.Info_Header_Name = selected

    def on_select_sublist(self, event):
        if self.Sub_listbox.curselection():
            selected_index = self.Sub_listbox.curselection()[0]
            selected = self.Sub_listbox.get(selected_index)
            print("Selected from list 2:", selected)  # Print value from list 2

            self.Info_Header_Name = selected

    def filter_list2(self, selected):
        self.Sub_listbox.delete(0, END)
        filtered_entries = [entry[1] for entry in self.Sub_table_categorys if entry[0] == selected]
        for entry in filtered_entries:
            self.Sub_listbox.insert(END, entry)

            self.Info_Header_Name = selected

    def select_file(self):
        self.add_frame.grab_set()
        file_object = filedialog.askopenfile(filetypes=[("Image Files", "*.jpg *.png")])
        self.selected_file = file_object
        self.add_frame.grab_release()

    def on_validate(self, char):
        # Get the current content of the Text widget
        current_text = self.add_Infomation_sum_Text.get("1.0", "end-1c")

        if len(current_text) >= 600:
            self.mainroot.bell()  # Produces a system alert to notify the user (optional)
            self.mainroot.after(10, self.show_error)  # Call show_error function after a slight delay

            # Truncate the text to the desired length
            self.add_Infomation_sum_Text.delete("1.600", "end-1c")
            return False

        return True

    def show_error(self):
        self.error_label.config(text="Character limit reached", fg="red")

    def clear_error(self):
        self.error_label.config(text="")  # Clear the error message

    def add_sub_category(self):
        Info_Header_Name = self.Info_Header_Name
        print(Info_Header_Name)
        Sub_Category_name = self.entry_cate_name.get()
        image_file_name = self.selected_file
        self.add_frame.pack_forget()

        self.add_sub_category_frame.pack()
        self.add_sub_category_label.grid(row=0, column=1)

        self.head_categoryis_label.grid(row=1, column=0, pady=10)
        self.head_categoryis_label.config(text=f"Head_category_is: {Info_Header_Name}")

        self.enter_cate_name.grid(row=2, column=0)
        self.entry_cate_name.grid(row=2, column=2)

        self.select_file_label.grid(row=3, column=0)
        self.select_file_button.grid(row=3, column=2)

        self.add_sub_category.grid(row=4, column=1)

        # Initialize selected_file_path to the default image path
        selected_file_path = "C:/Users/Maxim/PycharmProjects/RE BOC Leitfaden/Images/No Image.jpg"

        if self.selected_file is not None:
            selected_file_path = self.selected_file.name

        img = Image.open(selected_file_path)
        photo_resized = img.resize((80, 80), PIL.Image.LANCZOS)
        self.photo_resized = ImageTk.PhotoImage(photo_resized)

        cur.execute("SELECT * FROM sub_category WHERE Header_Info_name=? AND Sub_Category_name=? AND image_filename=?",
                    (Info_Header_Name, Sub_Category_name, selected_file_path)
                    )

        existing_button = cur.fetchone()

        print(existing_button)

        # Check if there is an exact match for all three values

        if existing_button:
            top = Toplevel(self.add_window)
            top.title("Custom Modal Error")

            error_message = "Category all ready exist please check if that is the case"

            label = Label(top,
                          text=error_message,
                          font=("Myriad Pro", 15),
                          )
            label.pack()

            ok_button = Button(top,
                               text="OK",
                               font=("Myriad Pro", 20),
                               command=top.destroy,
                               )
            ok_button.pack()

            # Make the message box modal
            top.grab_set()

        elif Sub_Category_name is None:
            top = Toplevel(self.add_window)
            top.title("Custom Modal Error")

            error_message = "Please input Values in the Text Boxes"

            label = Label(top,
                          text=error_message,
                          font=("Myriad Pro", 15),
                          )
            label.pack()

            ok_button = Button(top,
                               text="OK",
                               font=("Myriad Pro", 20),
                               command=top.destroy,
                               )
            ok_button.pack()

            # Make the message box modal
            top.grab_set()

        else:
            cur.execute(
                """INSERT INTO sub_category (Header_Info_name, sub_Category_name, image_filename) VALUES (?, ?, ?)""",
                (Info_Header_Name, Sub_Category_name, selected_file_path)
            )
            con.commit()



    def add_infomation(self):
        self.add_window.geometry("1600x800")
        Info_Header_Name = self.Info_Header_Name
        Info_name = self.enrty_Infomation_name.get()
        Info_Sum_Text = self.add_Infomation_sum_Text.get("1.0", "end-1c")
        Info_Full_Text = self.add_Infomation_full_Text.get("1.0", "end-1c")
        self.add_frame.pack_forget()

        self.add_Infomation_frame.pack()
        self.add_Infomation_label.grid(row=0, column=2)

        self.head_categoryis_finfo_label.grid(row=1, column=0, pady=10)
        self.head_categoryis_finfo_label.config(text=f"Head_category_is: {Info_Header_Name}")

        self.add_Infomation_name.grid(row=2, column=0)
        self.enrty_Infomation_name.grid(row=2, column=2)

        self.add_Infomation_sum_Label.grid(row=3, column=0, pady=10)
        self.add_Infomation_sum_Text.grid(row=4, column=0, sticky="nsew")
        self.add_Infomation_sum_Text_scrollbar.grid(row=4, column=1, sticky="ns")
        self.add_Infomation_sum_Text.config(yscrollcommand=self.add_Infomation_sum_Text_scrollbar.set)
        self.error_label.grid(row=5, column=0)

        self.add_Infomation_full_Label.grid(row=3, column=3, pady=10)
        self.add_Infomation_full_Text.grid(row=4, column=3, sticky="nsew", padx=5)
        self.add_Infomation_full_Text_scrollbar.grid(row=4, column=4, sticky="ns")

        self.add_Infomation.grid(row=6, column=2)

        cur.execute("SELECT * FROM category_Infomation WHERE Header_Info_name=? AND Info_name=? AND Info_Sum_text=? AND info_Full_text=?",
                    (Info_Header_Name, Info_name, Info_Sum_Text, Info_Full_Text)
                    )

        existing_button = cur.fetchone()

        print(existing_button)

        if existing_button:
            top = Toplevel(self.add_window)
            top.title("Custom Modal Error")

            error_message = "Category all ready exist please check if that is the case"

            label = Label(top,
                          text=error_message,
                          font=("Myriad Pro", 15),
                          )
            label.pack()

            ok_button = Button(top,
                               text="OK",
                               font=("Myriad Pro", 20),
                               command=top.destroy,
                               )
            ok_button.pack()

            # Make the message box modal
            top.grab_set()

        elif Info_name is None:
            top = Toplevel(self.add_window)
            top.title("Custom Modal Error")

            error_message = "Please input Values in the Text Boxes"

            label = Label(top,
                          text=error_message,
                          font=("Myriad Pro", 15),
                          )
            label.pack()

            ok_button = Button(top,
                               text="OK",
                               font=("Myriad Pro", 20),
                               command=top.destroy,
                               )
            ok_button.pack()

            # Make the message box modal
            top.grab_set()

        else:

            print(Info_Header_Name)
            print(Info_name)
            print(Info_Sum_Text)
            print(Info_Full_Text)
            cur.execute(
                """INSERT INTO category_infomation (Header_Info_name, Info_name, Info_Sum_text, Info_Full_text) VALUES (?, ?, ?, ?)""",
                (Info_Header_Name, Info_name, Info_Sum_Text, Info_Full_Text)
            )
            con.commit()

            messagebox.showinfo("Erstellung", f"{Info_name} wurde erstellt. ")




class ChangeWindow:
    def __init__(self, root_window):
        self.mainroot = root_window

        self.selected_category_source = None

        self.Info_Header_Name = None

        self.selected_file = None

        validate_cmd = self.mainroot.register(self.on_validate)

        self.change_window = Toplevel(self.mainroot)
        self.change_window.title("Change Window")
        self.change_window.geometry("1200x400")

        self.change_frame = Frame(self.change_window)
        self.change_frame.pack()

        cur.execute("SELECT Head_category_name from Head_category")
        self.Head_table_categorys = cur.fetchall()
        print(self.Head_table_categorys)

        cur.execute("SELECT Header_Info_name, Sub_Category_name FROM sub_category")
        self.Sub_table_categorys = cur.fetchall()
        print(self.Sub_table_categorys)

        cur.execute("SELECT Header_Info_name, Info_name FROM category_infomation")
        self.info_table_categorys = cur.fetchall()
        print(self.info_table_categorys)

        self.Main_listbox = Listbox(self.change_frame,
                                    selectmode=SINGLE,
                                    font=("Myriad Pro", 15)
                                    )
        self.Main_listbox.grid(row=1, column=0)

        for entry in self.Head_table_categorys:
            self.Main_listbox.insert(END, entry[0])  # Extracting the value from the single-element tuple

        self.Main_listbox.bind('<<ListboxSelect>>', self.on_select_headlist)

        self.Sub_listbox = Listbox(self.change_frame,
                                   selectmode=SINGLE,
                                   font=("Myriad Pro", 15)
                                   )
        self.Sub_listbox.grid(row=1, column=1)

        self.Sub_listbox.bind('<<ListboxSelect>>', self.on_select_sublist)

        self.infomation_listbox = Listbox(self.change_frame,
                                          selectmode=SINGLE,
                                          font=("Myriad Pro", 15)
                                          )
        self.infomation_listbox.grid(row=1, column=2)

        self.infomation_listbox.bind('<<ListboxSelect>>', self.on_select_infoamtionlist)

        self.change_label = Label(self.change_frame,
                                  text="What Category do you want to Change",
                                  font=("Myriad Pro", 20, "bold"),
                                  relief=RAISED
                                  )
        self.change_label.grid(row=0, column=1)

        self.change_open_button = Button(self.change_frame,
                                         text="Open category",
                                         font=("Myriad Pro", 20, "bold"),
                                         relief=RAISED,
                                         command=self.open_change_view
                                         )
        self.change_open_button.grid(row=3, column=1)

        self.input_change_frame = Frame(self.change_window)

        self.input_change_label = Label(self.input_change_frame,
                                        text="Please input new Infomation",
                                        font=("Myriad Pro", 20),
                                        relief=RAISED
                                        )

        self.new_button_name = Entry(self.input_change_frame)
        self.new_image_file = Button(self.input_change_frame,
                                     text="select new Image",
                                     font=("Myriad Pro", 20),
                                     relief=RAISED,
                                     command=self.select_file
                                     )
        self.new_category_type = Entry(self.input_change_frame)

        self.new_old_Info_Sum_label = Label(self.input_change_frame,
                                            text="Enter a Summary",
                                            font=("Myriad Pro", 20),
                                            relief=RAISED
                                            )

        self.new_old_Info_Sum_text = Text(self.input_change_frame,
                                            height=30,
                                            width=75,
                                            wrap="word",
                                            insertborderwidth=2,
                                            padx=5,
                                            pady=5)

        self.new_old_Info_sum_scrollbar = Scrollbar(self.input_change_frame,
                                                           command=self.new_old_Info_Sum_text.yview)

        self.error_label = Label(self.input_change_frame)

        self.new_old_Info_Sum_text.bind('<Key>', lambda e: self.on_validate(e.char))

        self.new_old_Info_full_label = Label(self.input_change_frame,
                                             text="Enter a Full Version",
                                             font=("Myriad Pro", 20),
                                             relief=RAISED)

        self.new_old_Info_full_text = Text(self.input_change_frame,
                                            height=30,
                                            width=75,
                                            wrap="word",
                                            insertborderwidth=2,
                                            padx=5,
                                            pady=5)

        self.new_old_Info_full_scrollbar = Scrollbar(self.input_change_frame)

        self.old_button_name = Label(self.input_change_frame,
                                     text="",
                                     font=("Myriad Pro", 20),
                                     relief=RAISED
                                    )
        self.old_image_file = Label(self.input_change_frame,
                                    text="",
                                    font=("Myriad Pro", 20),
                                    relief=RAISED
                                    )
        self.old_category_type = Label(self.input_change_frame,
                                       text="",
                                       font=("Myriad Pro", 20),
                                       relief=RAISED
                                    )


        self.change_old_info_button = Button(self.input_change_frame,
                                             text="Change",
                                             font=("Myriad Pro", 20),
                                             relief=RAISED,
                                             command=self.update_databse
                                             )

    def on_select_headlist(self, event):
        if self.Main_listbox.curselection():
            selected_index = self.Main_listbox.curselection()[0]
            selected = self.Main_listbox.get(selected_index)
            self.filter_list2(selected)
            self.filter_list3(selected)

            self.Info_Header_Name = selected

            self.selected_category_source = "Head"

    def on_select_sublist(self, event):
        if self.Sub_listbox.curselection():
            selected_index = self.Sub_listbox.curselection()[0]
            selected = self.Sub_listbox.get(selected_index)
            self.filter_list3(selected)

            self.Info_Header_Name = selected

            self.selected_category_source = "Sub"

    def on_select_infoamtionlist(self, event):
        if self.infomation_listbox.curselection():
            selected_index = self.infomation_listbox.curselection()[0]
            selected = self.infomation_listbox.get(selected_index)

            self.Info_Header_Name = selected

            self.selected_category_source = "Info"

    def filter_list2(self, selected):
        self.Sub_listbox.delete(0, END)
        filtered_entries = [entry[1] for entry in self.Sub_table_categorys if entry[0] == selected]
        for entry in filtered_entries:
            self.Sub_listbox.insert(END, entry)

            self.Info_Header_Name = selected

    def filter_list3(self, selected):
        self.infomation_listbox.delete(0, END)
        filtered_entries = [entry[1] for entry in self.info_table_categorys if entry[0] == selected]
        for entry in filtered_entries:
            self.infomation_listbox.insert(END, entry)

            self.Info_Header_Name = selected

    def select_file(self):
        self.input_change_frame.grab_set()
        file_object = filedialog.askopenfile(filetypes=[("Image Files", "*.jpg *.png")])
        self.selected_file = file_object
        self.input_change_frame.grab_release()

    def on_validate(self, char):
        # Get the current content of the Text widget
        current_text = self.new_old_Info_Sum_text.get("1.0", "end-1c")

        if len(current_text) >= 1000:
            self.mainroot.bell()  # Produces a system alert to notify the user (optional)
            self.mainroot.after(10, self.show_error)  # Call show_error function after a slight delay

                # Truncate the text to the desired length
            self.new_old_Info_Sum_text.delete("1.1000", "end-1c")
            return False

        return True

    def show_error(self):
        self.error_label.config(text="Character limit reached", fg="red")

    def clear_error(self):
        self.error_label.config(text="")  # Clear the error message

    def update_databse(self, file_source, selected_button):
        self.file_source = file_source
        print(selected_button)


        # Process the values based on the number of arguments
        if self.file_source == "Head":
            new_Head_name = None
            new_Head_name = self.new_button_name.get()

            if not new_Head_name:
                cur.execute("SELECT Head_category_name FROM Head_category WHERE Head_category_name=?",
                            (selected_button,))
                new_Head_name = cur.fetchone()


            new_Image_path = None
            new_Image_path = self.selected_file.name


            if not new_Image_path:
                cur.execute("SELECT image_filename FROM Head_category WHERE Head_category_name=?",
                            (selected_button,))
                new_Image_path = cur.fetchone()


            new_category_type = None
            new_category_type = self.new_category_type.get()

            if not new_category_type:
                cur.execute("SELECT category_type FROM Head_category WHERE Head_category_name=?",
                            (selected_button,))
                new_category_type = cur.fetchone()

            print(new_Head_name)
            print(new_Image_path)
            print(new_category_type)

            cur.execute("UPDATE Head_category SET Head_category_name=?, image_filename=?, category_type=? WHERE Head_category_name=?",
                        (new_Head_name, new_Image_path, new_category_type, selected_button))
            con.commit()

        elif self.file_source == "Sub":
            new_Sub_name = None
            new_Sub_name = self.new_button_name.get()

            if not new_Sub_name:
                cur.execute("SELECT Sub_Category_name FROM sub_category WHERE Sub_Category_name=?",
                            (selected_button,))
                new_Sub_name = cur.fetchone()

            new_Image_path = None
            new_Image_path = self.selected_file.name

            if not new_Image_path:
                cur.execute("SELECT image_filename FROM sub_category WHERE Sub_Category_name=?",
                            (selected_button,))
                new_Image_path = cur.fetchone()

            print(new_Sub_name)
            print(new_Image_path)

            cur.execute("UPDATE sub_category SET Sub_Category_name=?, image_filename=? WHERE Sub_Category_name=?",
                        (new_Sub_name, new_Image_path, selected_button))
            con.commit()

        elif self.file_source == "Info":
            new_Info_name = None
            new_Info_name = self.new_button_name.get()

            if not new_Info_name:
                cur.execute("SELECT Info_name FROM category_Infomation WHERE Info_name=?",
                            (selected_button,))
                new_Info_name = cur.fetchone()

            new_Sum_text = None
            new_Sum_text = self.new_old_Info_Sum_text.get("1.0", "end-1c")

            if not new_Sum_text:
                cur.execute("SELECT Info_Sum_Text FROM category_Infomation WHERE Info_name=?",
                            (selected_button,))
                new_Sum_text = cur.fetchone()

            new_Full_text = None
            new_Full_text = self.new_old_Info_full_text.get("1.0", "end-1c")

            if not new_Full_text:
                cur.execute("SELECT Info_Full_Text FROM category_Infomation WHERE Info_name=?",
                            (selected_button,))
                new_Full_text = cur.fetchone()

            print(new_Info_name)
            print(new_Sum_text)
            print(new_Full_text)

            cur.execute("UPDATE category_infomation SET Info_name=?, Info_Sum_Text=?, Info_Full_Text=? WHERE Info_name=?",
                        (new_Info_name, new_Sum_text, new_Full_text, selected_button))
            con.commit()
        else:
            messagebox.showerror("Error", "Das ist ungewöhnliches verhalten des programmes bitte melden sie sich beim admin!")

    def open_change_view(self):
        selected_button = self.Info_Header_Name
        print(selected_button)

        if self.selected_category_source == "Head":
            cur.execute("SELECT Head_category_name, image_filename, category_type FROM Head_category WHERE Head_category_name=?",
                        (selected_button,))

            result = cur.fetchone()

            if result:
                button_name, image_filename, category_type = result

                file_path = image_filename
                file_name = os.path.basename(file_path)

                self.old_button_name.config(text=f"Head_category_name: {button_name}")
                self.old_image_file.config(text=f"Image_filename: {file_name}")
                self.old_category_type.config(text=f"category_type: {category_type}")

            self.change_frame.pack_forget()
            self.input_change_frame.pack()
            self.input_change_label.grid(row=0, column=1)

            self.old_button_name.grid(row=1, column=0, pady=10)
            self.old_image_file.grid(row=2, column=0, pady=10)
            self.old_category_type.grid(row=3, column=0, pady=10)

            self.new_button_name.grid(row=1, column=2, pady=10)
            self.new_image_file.grid(row=2, column=2, pady=10)
            self.new_category_type.grid(row=3, column=2, pady=10)

            file_source = self.selected_category_source


            self.change_old_info_button.grid(row=4, column=1)
            self.change_old_info_button.config(command=lambda: self.update_databse(file_source, selected_button))

        elif self.selected_category_source == "Sub":
            cur.execute("SELECT Sub_Category_name, image_filename FROM sub_category WHERE Sub_Category_name =?",
                        (selected_button,))

            result = cur.fetchone()

            if result:
                button_name, image_filename,  = result

                file_path = image_filename
                file_name = os.path.basename(file_path)

                self.old_button_name.config(text=f"Sub_name: {button_name}")
                self.old_image_file.config(text=f"Image_filename: {file_name}")

            self.change_frame.pack_forget()
            self.input_change_frame.pack()
            self.input_change_label.grid(row=0, column=1)

            self.old_button_name.grid(row=1, column=0, pady=10)
            self.old_image_file.grid(row=2, column=0, pady=10)

            self.new_button_name.grid(row=1, column=2, pady=10)
            self.new_image_file.grid(row=2, column=2, pady=10)

            file_source = self.selected_category_source

            self.change_old_info_button.grid(row=4, column=1)
            self.change_old_info_button.config(command=lambda: self.update_databse(file_source, selected_button))

        elif self.selected_category_source == "Info":
            self.change_window.geometry("1600x800")
            cur.execute("SELECT Info_name, Info_Sum_text, Info_Full_text FROM category_Infomation WHERE Info_name=?",
                        (selected_button,))

            result = cur.fetchone()

            if result:
                button_name, Sum_text, Full_text = result
                self.old_button_name.config(text=f"Info name: {button_name}")
                self.new_old_Info_Sum_text.insert("1.0", Sum_text)
                self.new_old_Info_full_text.insert("1.0", Full_text)

            self.change_frame.pack_forget()
            self.input_change_frame.pack()
            self.input_change_label.grid(row=0, column=1)

            self.old_button_name.grid(row=1, column=0, pady=10)
            self.new_old_Info_Sum_label.grid(row=2, column=0, pady=10)
            self.new_old_Info_Sum_text.grid(row=3, column=0, padx=10)
            self.new_old_Info_Sum_text.config(yscrollcommand=self.new_old_Info_sum_scrollbar.set)
            self.error_label.grid(row=5, column=0)

            self.new_button_name.grid(row=1, column=2, pady=10)
            self.new_old_Info_full_label.grid(row=2, column=2, pady=10)
            self.new_old_Info_full_text.grid(row=3, column=2, sticky="nsew")
            self.new_old_Info_full_scrollbar.grid(row=3, column=3, sticky="ns")

            file_source = self.selected_category_source

            self.change_old_info_button.grid(row=4, column=1)
            self.change_old_info_button.config(command=lambda: self.update_databse(file_source, selected_button))




class DeleteWindow:
    def __init__(self, root_window, content_frame):
        self.mainroot = root_window
        self.content_frame = content_frame

        self.delete_window = Toplevel(self.mainroot)
        self.delete_window.title("Delete Window")
        self.delete_window.geometry("800x400")

        self.delete_frame = Frame(self.delete_window)
        self.delete_frame.pack()

        self.delete_label = Label(self.delete_frame,
                                  text="What Category do you want to delete",
                                  font=("Myriad Pro", 20, "bold"),
                                  relief=RAISED
                                  )
        self.delete_label.grid(row=0, column=1)

        self.listbox = Listbox(self.delete_frame,
                               selectmode=SINGLE
                               )
        self.listbox.grid(row=1, column=1)

        self.delete_button = Button(self.delete_frame,
                                    text="Delete",
                                    font=("Myriad Pro", 15, "bold"),
                                    command=self.delete_head_category
                                    )
        self.delete_button.grid(row=3, column=1)

        self.populate_listbox()

    def populate_listbox(self):
        cur.execute("SELECT Head_category_name, image_filename, category_type FROM Head_category")
        existing_buttons = cur.fetchall()
        for button_data in existing_buttons:
            button_name, _, _ = button_data  # Extract the button name
            self.listbox.insert(END, button_name)

    def delete_head_category(self):
        selected_button = self.listbox.get(self.listbox.curselection())
        result = messagebox.askokcancel("Confirm Deletion", f"Delete button: {selected_button}")
        if result:
            # Delete the database entry
            cur.execute("DELETE FROM Head_category WHERE Head_category_name=?", (selected_button,))
            con.commit()

            # Delete the corresponding module (.py file)
            module_name = selected_button + ".py"
            if os.path.exists(module_name):
                os.remove(module_name)

            # Remove the selected item from the listbox
            self.listbox.delete(self.listbox.curselection())

            app.display_existing_buttons(self.content_frame)


# Opens a Window that allows the creation of Category Buttons
class CreatedWindow:
    def __init__(self, root_window, content_frame):
        self.mainroot = root_window
        self.content_frame = content_frame
        self.selected_file = None  # Initialize self.selected_file to None

        self.created_buttons = []
        self.images = {}

        # creates the frame to hold the creation wigets
        self.input_window = Toplevel(self.mainroot,)
        self.input_window.title("Create Window")
        self.input_window.geometry("800x400")

        self.ask_frame = Frame(self.input_window,)
        self.ask_frame.pack(expand=True, fill=BOTH)

        # asks the user what he wants to do
        self.ask_type = Label(self.ask_frame,
                              text="Do you want to Created a Singel or Multi Head Catogory ?",
                              font=("Myriad Pro", 20),
                              relief=RAISED,
                              bd=10
                              )
        self.ask_type.grid(row=0, column=0, columnspan=3, pady=10)

        self.modual_name = Label(self.ask_frame,
                                  text="Input a Name",
                                  font=("Myriad Pro", 20),
                                 relief=RAISED,
                                 )
        self.modual_name.grid(row=1, column=0)

        self.modual_entry = Entry(self.ask_frame)
        self.modual_entry.grid(row=1, column=2)

        self.modual_image = Label(self.ask_frame,
                                  text="Select a Image",
                                  font=("Myriad Pro", 20),
                                  relief=RAISED,
                                  )
        self.modual_image.grid(row=2, column=0)

        self.image_button = Button(self.ask_frame,
                                   text="Select file",
                                   font=("Myriad Pro", 20),
                                   command=self.select_file
                                   )
        self.image_button.grid(row=2, column=2)

        self.ask_type = Label(self.ask_frame,
                              text="Singel or Multi ?",
                              font=("Myriad Pro", 20),
                              relief=RAISED,
                              )
        self.ask_type.grid(row=3, column=0)

        self.ask_type_entry = Entry(self.ask_frame)
        self.ask_type_entry.grid(row=3, column=2)

        self.created_button = Button(self.ask_frame,
                                     text="Created new Category",
                                     font=("Myriad Pro", 20),
                                     command=self.created_category
                                     )
        self.created_button.grid(row=4, column=1)

    # select the image file for the button that leads to the modual that is created
    def select_file(self):
        self.ask_frame.grab_set()
        file_object = filedialog.askopenfile(filetypes=[("Image Files", "*.jpg *.png")])
        self.selected_file = file_object
        self.ask_frame.grab_release()

    # creates the modual with the user input and creates the button for the infomation
    def created_category(self):
        Category_name = self.modual_entry.get()
        Category_type = self.ask_type_entry.get().lower()  # Convert to lowercase for case-insensitive comparison

        # Initialize selected_file_path to the default image path
        selected_file_path = "C:/Users/Maxim/PycharmProjects/RE BOC Leitfaden/Images/No Image.jpg"

        if self.selected_file is not None:
            selected_file_path = self.selected_file.name

        img = Image.open(selected_file_path)
        photo_resized = img.resize((80, 80), PIL.Image.LANCZOS)
        self.photo_resized = ImageTk.PhotoImage(photo_resized)

        cur.execute("SELECT * FROM Head_category WHERE Head_category_name=? AND image_filename=? AND category_type=?",
                    (Category_name, selected_file_path, Category_type)
                    )

        existing_button = cur.fetchone()

        # Check if there is an exact match for all three values

        if existing_button:
            top = Toplevel(self.input_window)
            top.title("Custom Modal Error")

            error_message = "Category all ready exist please check if that is the case"

            label = Label(top,
                          text=error_message,
                          font=("Myriad Pro", 15),
                          )
            label.pack()

            ok_button = Button(top,
                               text="OK",
                               font=("Myriad Pro", 20),
                               command=top.destroy,
                               )
            ok_button.pack()

            # Make the message box modal
            top.grab_set()


        # if multi
        elif Category_type == "multi":
            button_name = Button(self.content_frame,
                                text=Category_name,
                                font=("Myriad Pro", 20),
                                image=self.photo_resized,
                                compound="left"
                                )

            button_name.image = self.photo_resized  # Store the image object
            self.created_buttons.append(button_name)
            self.images[Category_name] = self.photo_resized  # Store the image in the dictionary

            cur.execute(
                """INSERT INTO Head_category (Head_category_name, image_filename, category_type) VALUES (?, ?, ?)""",
                        (Category_name, selected_file_path, Category_type)
            )
            con.commit()

            messagebox.showinfo("Success", f"{Category_name} was created. ")

            app.display_existing_buttons(self.content_frame)


        elif Category_type == "singel":
            button_name = Button(self.content_frame,
                                 text=Category_name,
                                 font=("Myriad Pro", 20),
                                 image=self.photo_resized,
                                 compound="left"
                                 )

            button_name.image = self.photo_resized  # Store the image object
            self.created_buttons.append(button_name)
            self.images[Category_name] = self.photo_resized  # Store the image in the dictionary

            cur.execute(
                """INSERT INTO Head_category (Head_category_name, image_filename, category_type) VALUES (?, ?, ?)""",
                (Category_name, selected_file_path, Category_type)
            )
            con.commit()

            messagebox.showinfo("Success", f"{Category_name} was created. ")

            app.display_existing_buttons(self.content_frame)


        else:
            top = Toplevel(self.input_window)
            top.title("Custom Modal Error")

            error_message = "Please input a File Type Multi or Singel"

            label = Label(top,
                          text=error_message,
                          font=("Myriad Pro", 15),
                          )
            label.pack()

            ok_button = Button(top,
                               text="OK",
                               font=("Myriad Pro", 20),
                               command=top.destroy,
                               )
            ok_button.pack()

            # Make the message box modal
            top.grab_set()


# login for the creation, adding, changing or deleting for infomation catogorys
class LoginFrame:
    def __init__(self, root_window, content_frame):
        self.mainroot = root_window
        self.content_frame = content_frame

        self.login_frame = Frame(self.mainroot)
        self.login_frame.pack()

        self.login_button = Button(self.login_frame,
                              text="Login",
                              font=("Myriad Pro", 25, "bold", "underline"),
                              relief=RAISED,
                              command=self.password_check

                              )
        self.login_button.grid(row=1, column=1, padx=80, pady=5)

        self.logout_button = Button(self.login_frame,
                               text="Logout",
                               font=("Myriad Pro", 25, "bold", "underline"),
                               relief=RAISED,
                               command=self.logout
                               )

        self.admin_entry = Entry(self.login_frame,
                            show="*",
                            bg="#AAAFA8",
                            fg="black",
                            relief=RIDGE
                                        )
        self.admin_entry.grid(row=2, column=1)

        self.created_button = Button(self.login_frame,
                                text="Created",
                                font=("Myriad Pro", 20, "bold", "underline"),
                                relief=RAISED,
                                command=self.open_created_window
                                )

        self.change_button = Button(self.login_frame,
                               text="Change",
                               font=("Myriad Pro", 20, "bold", "underline"),
                               relief=RAISED,
                               command=self.open_change_window
                               )

        self.delete_button = Button(self.login_frame,
                               text="Delete",
                               font=("Myriad Pro", 20, "bold", "underline"),
                               relief=RAISED,
                               width=7,
                               command=self.open_delete_window
                               )

        self.add_button = Button(self.login_frame,
                                 text="Add",
                                 font=("Myriad Pro", 20, "bold", "underline"),
                                 relief=RAISED,
                                 width=7,
                                 command=self.open_add_window
                                 )

    def password_check(self):
        admin_password = self.admin_entry.get()
        if admin_password == "1":
            self.created_button.grid(row=1, column=2, sticky=E, padx=15, pady=25)
            self.delete_button.grid(row=2, column=2)
            self.change_button.grid(row=1, column=3, pady=10)
            self.add_button.grid(row=2, column=3)
            self.login_button.grid_forget()
            self.logout_button.grid(row=1, column=1, padx=80, pady=5)

        else:
            pass

    def logout(self):
        self.logout_button.grid_forget()
        self.change_button.grid_forget()
        self.created_button.grid_forget()
        self.delete_button.grid_forget()
        self.add_button.grid_forget()
        self.login_button.grid(row=1, column=1, padx=80, pady=5)

    def open_created_window(self):
        created_window = CreatedWindow(self.mainroot, self.content_frame)

    def open_delete_window(self):
        delete_window = DeleteWindow(self.mainroot, self.content_frame)

    def open_change_window(self):
        change_window = ChangeWindow(self.mainroot)

    def open_add_window(self):
        add_window = AddWindow(self.mainroot)




# Zwischen Notiz Funktion so umschreiben das sich der letzte frame/classe gemerkt wird um den dan wirder zu callen
def switch_to_frame(current_frame, current_content_frame):
    current_frame.pack_forget()
    current_content_frame.pack_forget()




# main window for the wiegets and frames
class MainWindow:
    def __init__(self, root_window):
        self.mainroot = root_window
        self.mainroot.title("Wiki Lite")
        self.mainroot.geometry("2560x1600")
        self.mainroot.state("zoomed")

        self.pages = []
        self.current_page = 0
        self.buttons_per_page = 12

        cwd = os.getcwd()
        files=os.listdir(cwd)

        print("Current Working Directory:", os.getcwd())
        print(files)

        folder_name = "Images"
        image_file_name = "BOC_Leasing.png"

        # Store information about created buttons
        self.created_buttons_info = {}
        self.created_subcategory_ingo = {}

        script_dir = os.path.dirname(os.path.abspath(__file__))

        image_path = os.path.join(script_dir, folder_name, image_file_name)

        print(image_path)

        try:
            img = Image.open(image_path)
            photo_resized = img.resize((160, 160), Image.LANCZOS)
            self.BOC_Main_icon = ImageTk.PhotoImage(photo_resized)
        except FileNotFoundError as e:
            print(f"Error opening image: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


        self.main_frame = Frame(self.mainroot)
        self.main_frame.pack()

        self.main_label = Label(self.main_frame,
                           text="Wiki Lite",
                           font=("Myriad Pro", 40, "bold", "underline"),
                           relief=RAISED,
                           image=self.BOC_Main_icon,
                           compound="bottom",
                           bd=10,
                           padx=10,
                           pady=10,
                           width=425
                           )
        self.main_label.pack()

        self.content_frame = Frame(root_window)
        self.content_frame.pack(fill=BOTH, expand=True)

        self.display_existing_buttons(self.content_frame)

        top_left = LoginFrame(root_window, self.content_frame)
        top_left.login_frame.place(x=1, height=200, width=620)

    def display_existing_buttons(self, content_frame):

        self.page = Frame(content_frame)
        self.pages.append(self.page)
        print(self.page)
        for widget in self.page.winfo_children():
            widget.destroy()

        cur.execute("SELECT Head_category_name, image_filename, category_type FROM Head_category")
        existing_buttons = cur.fetchall()

        button_start = self.current_page * self.buttons_per_page
        button_end = min((self.current_page + 1) * self.buttons_per_page, len(existing_buttons))

        # Iterate over the button_data for the current page
        for i, (label, image_path, button_type) in enumerate(existing_buttons[button_start:button_end]):

            if button_type == "multi":
                img = Image.open(image_path)
                photo_resized = img.resize((80, 80), PIL.Image.LANCZOS)
                photo_resized = ImageTk.PhotoImage(photo_resized)
                button = Button(self.page,
                                text=label,
                                font=("Myriad Pro", 25),
                                image=photo_resized,
                                compound="left",
                                command=lambda category_name=label, category_image=photo_resized, old_frame=self.main_frame, old_content_frame=self.content_frame: self.open_category(category_name, category_image, old_frame, old_content_frame))
                button.grid(row=i // 4, column=i % 4, padx=50, pady=50)
                button.photo = photo_resized  # Keep a reference to the image to prevent garbage collection

            if button_type == "singel":
                img = Image.open(image_path)
                photo_resized = img.resize((80, 80), PIL.Image.LANCZOS)
                photo_resized = ImageTk.PhotoImage(photo_resized)
                button = Button(self.page,
                                text=label,
                                font=("Myriad Pro", 25),
                                image=photo_resized,
                                compound="left",
                                command=lambda category_name=label, category_image=photo_resized, old_frame=self.main_frame, old_content_frame=self.content_frame: self.open_infomation(category_name, category_image, old_frame, old_content_frame))
                button.grid(row=i // 4, column=i % 4, padx=50, pady=50)
                button.photo = photo_resized  # Keep a reference to the image to prevent garbage collection

        total_buttons = len(existing_buttons)
        remaining_buttons = total_buttons - button_end

        if self.current_page > 0:
            prev_button = Button(self.page, text="Previous Page", command=lambda: self.prev_page(content_frame))
            prev_button.grid(row=self.buttons_per_page // 3, column=0, pady=5)

        if remaining_buttons > 0:
            next_button = Button(self.page, text="Next Page", command=lambda: self.next_page(content_frame))
            next_button.grid(row=self.buttons_per_page // 3, column=2, pady=5)

        self.show_page()


    def prev_page(self, content_frame):
        self.current_page -= 1
        self.display_existing_buttons(content_frame)

    def next_page(self, content_frame):
        self.current_page += 1
        self.display_existing_buttons(content_frame)

    def show_page(self):
        if 0 <= self.current_page < len(self.pages):
            for page in self.pages:
                page.pack_forget()

            self.pages[self.current_page].pack(side="top", fill="both", expand=True)
        else:
            print("Invalid page index")

    def get_total_buttons(self):
        conn = sqlite3.connect("button_data.db")
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM buttons')
        total_buttons = cur.fetchone()[0]
        conn.close()
        return total_buttons

    def open_category(self, category_name, category_image, old_frame, old_content_frame):
        self.main_frame.pack_forget()
        self.content_frame.pack_forget()

        open_sub_category = sub_categorys(self.mainroot, category_name, category_image, old_frame, old_content_frame)

    def open_infomation(self, category_name, category_image, old_frame, old_content_frame):
        self.main_frame.pack_forget()
        self.content_frame.pack_forget()

        open_infomation = display_infomation(self.mainroot, category_name, category_image, old_frame, old_content_frame)

class sub_categorys:
    def __init__(self, root_window, category_name, category_image, old_frame, old_content_frame):

        self.mainroot = root_window
        self.category_frame = Frame(self.mainroot)
        self.category_frame.pack()

        self.pages = []
        self.current_page = 0
        self.buttons_per_page = 6


        self.created_sub_category = {}

        self.category_label = Label(self.category_frame,
                                    text=category_name,
                                    font=("Myriad Pro", 40),
                                    relief=RAISED,
                                    compound="left",
                                    image=category_image)
        self.category_label.pack()

        self.back_button = Button(self.category_frame,
                                  text="Main Menu",
                                  font=("Myriad Pro", 30),
                                  relief=RAISED,
                                  command=lambda old_frame=old_frame, old_content_frame=old_content_frame: self.open_MainWindow(old_frame, old_content_frame),
                                  )
        self.back_button.pack()

        self.sub_content_frame = Frame(self.mainroot)
        self.sub_content_frame.pack(fill=BOTH, expand=True)

        self.display_existing_subcategory(category_name, self.sub_content_frame)

    def open_infomation(self, category_name, category_image, old_frame, old_content_frame):
        self.category_frame.pack_forget()
        self.sub_content_frame.pack_forget()

        open_infomation = display_infomation(self.mainroot, category_name, category_image, old_frame, old_content_frame)

    def open_MainWindow(self, old_frame, old_content_frame):
        self.category_frame.pack_forget()
        self.sub_content_frame.pack_forget()

        old_frame.pack()
        old_content_frame.pack()

    def display_existing_subcategory(self,category_name, sub_content):
        self.page = Frame(sub_content)
        self.pages.append(self.page)
        print(self.page)
        for widget in self.page.winfo_children():
            widget.destroy()

        Header_Info_name_to_check = category_name

        cur.execute('''
            SELECT *
            FROM sub_category sc
            JOIN Head_category hc ON sc.Header_Info_name = hc.Head_category_name
            WHERE sc.Header_Info_name = ?
            ''', (Header_Info_name_to_check,))

        result = cur.fetchall()



        # Function to check the presence of the desired value in the dataset
        def check_desired_value(dataset, desired_value):
            matched_entries = [entry for entry in dataset if
                               entry[1] == desired_value]  # Assuming the second column is for 'category_name'
            # print(matched_entries)
            for entry in dataset:
                if entry[0] == desired_value:
                    matched_entries.append(entry)
            # print(matched_entries)
            return matched_entries

        result_message = check_desired_value(result, category_name)

        extracted_values = [(entry[1], entry[2], entry[3]) for entry in result_message]

        button_start = self.current_page * self.buttons_per_page
        button_end = min((self.current_page + 1) * self.buttons_per_page, len(extracted_values))

        # Iterate over the button_data for the current page
        for i, (Header_info_name, Sub_category_name, image_file_name) in enumerate(extracted_values[button_start:button_end]):
            img = Image.open(image_file_name)
            photo_resized = img.resize((80, 80), PIL.Image.LANCZOS)
            photo_resized = ImageTk.PhotoImage(photo_resized)
            button = Button(self.page,
                            text=Sub_category_name,
                            font=("Myriad Pro", 25),
                            image=photo_resized,
                            compound="left",
                            command=lambda category_name=Sub_category_name, category_image=photo_resized,
                                           old_frame=self.category_frame,
                                           old_content_frame=self.sub_content_frame: self.open_infomation(category_name,
                                                                                                          category_image,
                                                                                                          old_frame,
                                                                                                          old_content_frame)
                            )
            button.grid(row=i // 3, column=i % 3, padx=50, pady=50)
            button.photo = photo_resized  # Keep a reference to the image to prevent garbage collection

        total_buttons = len(extracted_values)
        remaining_buttons = total_buttons - button_end

        if self.current_page > 0:
            prev_button = Button(self.page, text="Previous Page", command=lambda: self.prev_page(category_name, self.sub_content_frame))
            prev_button.grid(row=self.buttons_per_page // 3, column=0, pady=5)

        if remaining_buttons > 0:
            next_button = Button(self.page, text="Next Page", command=lambda: self.next_page(category_name, sub_content))
            next_button.grid(row=self.buttons_per_page // 3, column=2, pady=5)

        self.show_page()

    def prev_page(self, category_name, content_frame):
        self.current_page -= 1
        self.display_existing_subcategory(category_name, content_frame)

    def next_page(self,category_name, content_frame):
        self.current_page += 1
        self.display_existing_subcategory(category_name, content_frame)

    def show_page(self):
        if 0 <= self.current_page < len(self.pages):
            for page in self.pages:
                page.pack_forget()

            self.pages[self.current_page].pack(side="top", fill="both", expand=True)
        else:
            print("Invalid page index")

    def get_total_buttons(self):
        conn = sqlite3.connect("button_data.db")
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM buttons')
        total_buttons = cur.fetchone()[0]
        conn.close()
        return total_buttons


class display_infomation:
    def __init__(self, root_window, category_name, category_image, old_frame, old_content_frame):

        self.mainroot = root_window
        self.category_frame = Frame(self.mainroot)
        self.category_frame.pack()

        self.pages = []
        self.current_page = 0
        self.buttons_per_page = 6

        self.sub_content_frame = Frame(self.mainroot)
        self.sub_content_frame.pack(fill=BOTH, expand=True)

        self.created_Info_category = {}

        self.category_label = Label(self.category_frame,
                                    text=category_name,
                                    font=("Myriad Pro", 40),
                                    relief=RAISED,
                                    compound="left",
                                    image=category_image)
        self.category_label.pack()

        self.back_button = Button(self.category_frame,
                                  text="Main Menu",
                                  font=("Myriad Pro", 30),
                                  relief=RAISED,
                                  command=lambda current_frame=self.category_frame, current_content_frame=self.sub_content_frame, old_frame=old_frame, old_content_frame=old_content_frame: self.go_back_to_previous(current_frame, current_content_frame, old_frame, old_content_frame)
                                  )
        self.back_button.pack()



        self.display_existing_Infoamtion(category_name, self.sub_content_frame)

    def go_back_to_previous(self, current_frame, current_content_frame, old_frame, old_content_frame):
        current_frame.pack_forget()
        current_content_frame.pack_forget()

        old_frame.pack()
        old_content_frame.pack()

    def display_existing_Infoamtion(self, category_name, Info_content_frame):
        self.page = Frame(Info_content_frame)
        self.pages.append(self.page)
        print(self.page)
        for widget in self.page.winfo_children():
            widget.destroy()

        Header_Info_name_to_check = category_name

        cur.execute("SELECT Header_info_name, Info_name FROM category_Infomation WHERE Header_info_name=?",
                    (Header_Info_name_to_check,))
        extracted_values = cur.fetchall()

        print(extracted_values)

        button_start = self.current_page * self.buttons_per_page
        button_end = min((self.current_page + 1) * self.buttons_per_page, len(extracted_values))

        # Iterate over the button_data for the current page
        for i, (Header_info_name, Info_name) in enumerate(extracted_values[button_start:button_end]):
            button = Button(self.page,
                            text=Info_name,
                            font=("Myriad Pro", 25),
                            command=lambda header_info=Header_info_name, info=Info_name, category_frame=self.category_frame, sub_content_frame=self.sub_content_frame: self.open_Infomation_text(header_info, info, category_frame, sub_content_frame)
                            )
            button.grid(row=i // 3, column=i % 3, padx=50, pady=50)


        total_buttons = len(extracted_values)
        remaining_buttons = total_buttons - button_end

        if self.current_page > 0:
            prev_button = Button(self.page, text="Previous Page",
                                 command=lambda: self.prev_page(category_name, self.sub_content_frame))
            prev_button.grid(row=self.buttons_per_page // 3, column=0, pady=5)

        if remaining_buttons > 0:
            next_button = Button(self.page, text="Next Page",
                                 command=lambda: self.next_page(category_name, Info_content_frame))
            next_button.grid(row=self.buttons_per_page // 3, column=2, pady=5)

        self.show_page()

    def prev_page(self, category_name, content_frame):
        self.current_page -= 1
        self.display_existing_Infoamtion(category_name, content_frame)

    def next_page(self, category_name, content_frame):
        self.current_page += 1
        self.display_existing_Infoamtion(category_name, content_frame)

    def show_page(self):
        if 0 <= self.current_page < len(self.pages):
            for page in self.pages:
                page.pack_forget()

            self.pages[self.current_page].pack(side="top", fill="both", expand=True)
        else:
            print("Invalid page index")

    def get_total_buttons(self):
        conn = sqlite3.connect("button_data.db")
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM buttons')
        total_buttons = cur.fetchone()[0]
        conn.close()
        return total_buttons

    def Back_to_Infomation_name(self, current_frame, current_content_frame, new_frame, new_content_frame):
        current_frame.pack_forget()
        current_content_frame.pack_forget()

        new_frame.pack()
        new_content_frame.pack()


    def open_Infomation_text(self, Header_Info_name, Info_name, category_name, sub_content_name):

        cur.execute("SELECT Header_Info_name, Info_name, Info_Sum_text, Info_Full_text FROM category_Infomation WHERE Header_Info_name=? AND Info_name=?",
                    (Header_Info_name, Info_name))

        result = cur.fetchone()

        Summery_Text = result[2]

        Full_Text = result[3]

        self.category_frame.pack_forget()
        self.sub_content_frame.pack_forget()

        self.Infomation_category = Frame(self.mainroot)
        self.Infomation_category.pack(pady=15)

        self.Info_sum_content_frame = Frame(self.mainroot)
        self.Info_sum_content_frame.pack(fill=BOTH, expand=True)


        self.created_Infomation_category = {}

        self.category_label = Label(self.Infomation_category,
                                    text=Info_name,
                                    font=("Myriad Pro", 40),
                                    relief=RAISED,
                                    compound="left",
                                    )
        self.category_label.pack()

        self.back_button = Button(self.Infomation_category,
                                  text=Header_Info_name,
                                  font=("Myriad Pro", 30),
                                  relief=RAISED,
                                  command=lambda current_frame=self.Infomation_category, current_content_frame=self.Info_sum_content_frame, new_frame=category_name, new_conent_frame=sub_content_name: self.Back_to_Infomation_name(current_frame, current_content_frame, new_frame, new_conent_frame)
                                  )
        self.back_button.pack(side="left")

        self.go_to_Full_button = Button(self.Infomation_category,
                                        text="Full Version",
                                        font=("Myriad Pro", 30),
                                        relief=RAISED,
                                        command=lambda Full_text=Full_Text: self.show_full_version(Full_text)
                                        )
        self.go_to_Full_button.pack(side="right")



        self.Info_sum_text = Text(self.Info_sum_content_frame,
                                  wrap="word",
                                  height=50,
                                  width=200,
                                  font=("Myriad Pro", 30)
                                  )
        self.Info_sum_text.grid(row=0, column=0, sticky="nsew")

        self.Info_sum_scrollbar = Scrollbar(self.Info_sum_content_frame,
                                            command=self.Info_sum_text.yview
                                            )
        self.Info_sum_scrollbar.grid(row=0, column=1, sticky="ns")

        self.Info_sum_text.insert("1.0", Summery_Text)

        self.Info_sum_text.config(yscrollcommand=self.Info_sum_scrollbar.set)
        self.Info_sum_text.config(state="disabled")

        self.Info_sum_content_frame.columnconfigure(0, weight=1)





    def show_full_version(self, Full_text):

        self.Info_sum_text.grid_forget()
        self.Info_sum_scrollbar.grid_forget()
        self.go_to_Full_button.pack_forget()

        self.go_to_Sum_button = Button(self.Infomation_category,
                                        text="Sum Version",
                                        font=("Myriad Pro", 30),
                                        relief=RAISED,
                                        command=self.go_back_to_sum
                                        )
        self.go_to_Sum_button.pack(side="right")

        self.Info_full_text = Text(self.Info_sum_content_frame,
                                   wrap="word",
                                   height=50,
                                   width=200,
                                   font=("Myriad Pro", 30)
                                   )
        self.Info_full_scrollbar = Scrollbar(self.Info_sum_content_frame)

        self.Info_full_text.grid(row=0, column=0, sticky="nsew")
        self.Info_full_scrollbar.grid(row=0, column=1, sticky="ns")

        self.Info_full_text.insert("1.0", Full_text)

        self.Info_full_text.config(yscrollcommand=self.Info_full_scrollbar.set)
        self.Info_sum_text.config(state="disabled")

        self.Info_sum_content_frame.columnconfigure(0, weight=1)

    def go_back_to_sum(self):
        self.go_to_Sum_button.pack_forget()
        self.Info_full_text.grid_forget()
        self.Info_full_scrollbar.grid_forget()

        self.go_to_Full_button.pack(side="right")
        self.Info_sum_text.grid(row=0, column=0, sticky="nsew")
        self.Info_sum_scrollbar.grid(row=0, column=1, sticky="ns")


if __name__ == "__main__":
    main()
    root_window = Tk()
    check_for_updates(root_window)
    app = MainWindow(root_window)
    root_window.mainloop()