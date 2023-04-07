import os
import shutil
import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import *
import customtkinter as ck
from PIL import ImageTk, Image

window = tk.Tk()
window.title('YPOC')
width = 800
height = 500
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/4) - (height/4)
window.geometry("%dx%d+%d+%d" % (width, height, x, y))
window.resizable(0, 0)


def cp_tree():
    src_folder = filedialog.askdirectory(title="Select Source Folder")

    if src_folder:
        dst_folder = filedialog.askdirectory(title="Select Destination Folder")

        if dst_folder:
            for dirpath, dirnames, filenames in os.walk(src_folder):
                relative_path = os.path.relpath(dirpath, src_folder)
                new_dir_path = os.path.join(dst_folder, relative_path)
                os.makedirs(new_dir_path, exist_ok=True)

            tk.messagebox.showinfo("Success", "Folder structure copied successfully!")

def cp_files():
    source = filedialog.askdirectory(initialdir="/", title="Select Source")
    destination = filedialog.askdirectory(initialdir="/", title="Select Destination")

    shutil.copytree(source, destination, dirs_exist_ok=True)

    tk.messagebox.showinfo("Copy Complete", "The files have been copied successfully.")

def cp_newer():
    source_dir = filedialog.askdirectory(title="Select source directory")
    destination_dir = filedialog.askdirectory(title="Select destination directory")

    for root_dir, _, files in os.walk(source_dir):
        dest_dir = os.path.join(destination_dir, os.path.relpath(root_dir, source_dir))
        os.makedirs(dest_dir, exist_ok=True)
        for file in files:
            src_file = os.path.join(root_dir, file)
            dest_file = os.path.join(dest_dir, file)
            # Copy the file if it is newer
            if os.path.exists(dest_file):
                if os.path.getmtime(src_file) > os.path.getmtime(dest_file):
                    shutil.copy2(src_file, dest_file)
            else:
                shutil.copy2(src_file, dest_file)

    tk.messagebox.showinfo("Success", "Newer items copied successfully!")

def gather():
    folder_path = filedialog.askdirectory()
    file_paths = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_paths.append(os.path.join(root, file))

    with open('list_files.txt', 'w') as f:
            for item in file_paths:
                f.write('%s\n' % item)
    
    tk.messagebox.showinfo("Success", "Paths list copied successfully!")

def edited_files():
    source_dir = filedialog.askdirectory(title="Select source directory")
    destination_dir = filedialog.askdirectory(title="Select destination directory")

    for root_dir, _, files in os.walk(source_dir):
        dest_dir = os.path.join(destination_dir, os.path.relpath(root_dir, source_dir))
        if not os.path.exists(dest_dir):
            continue
        for file in files:
            src_file = os.path.join(root_dir, file)
            dest_file = os.path.join(dest_dir, file)
            if not os.path.exists(dest_file):
                continue
            if os.path.getmtime(src_file) > os.path.getmtime(dest_file):
                shutil.copy2(src_file, dest_file)

    tk.messagebox.showinfo("Success", "Edited files copied successfully!")

def delete_files():
    folder_path = filedialog.askdirectory(title="Select source directory")
    count = 0
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            for filenamee in os.listdir(folder_path):
                count += 1
    
    tk.messagebox.showinfo("Success", f"Files deleted successfully!\n Files left: {count}")

def move_files():
    source_dir = filedialog.askdirectory(title="Select source directory")
    destination_dir = filedialog.askdirectory(title="Select destination directory")
    for file_name in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file_name)
        if os.path.isfile(file_path):
            os.rename(file_path, os.path.join(destination_dir, file_name))
        elif os.path.isdir(file_path):
            os.rename(file_path, os.path.join(destination_dir, file_name))

    tk.messagebox.showinfo("Success", "Files moved successfully!")

frame = tk.Frame(window, width=800, height=500, borderwidth=0, highlightthickness=0)
frame.pack()
image = Image.open("/Users/jonathanduthil/Documents/GitHub/Ypoc/bg.png")
img = ImageTk.PhotoImage(image)

canvas = tk.Canvas(frame, width=800, height=500, highlightthickness=0)
canvas.pack()
canvas.create_image(0, 0, anchor=tk.NW, image=img)

canvas2 = tk.Canvas(frame, width=700, height=400, highlightthickness=0)
canvas2.place(x=200,y=100)
canvas2.create_rectangle(0, 0, 698, 398, outline="black", width=6)

cp_tree_img = ck.CTkImage(light_image=Image.open("/Users/jonathanduthil/Documents/GitHub/Ypoc/cp_tree.png"),
                                  size=(45, 45))
cp_files_img = ck.CTkImage(light_image=Image.open("/Users/jonathanduthil/Documents/GitHub/Ypoc/cp_files.png"),
                                  size=(45, 45))
cp_newer_img = ck.CTkImage(light_image=Image.open("/Users/jonathanduthil/Documents/GitHub/Ypoc/cp_newer.png"),
                                  size=(60, 60))
cp_gather_img = ck.CTkImage(light_image=Image.open("/Users/jonathanduthil/Documents/GitHub/Ypoc/gather.png"),
                                  size=(45, 45))
cp_edited_img = ck.CTkImage(light_image=Image.open("/Users/jonathanduthil/Documents/GitHub/Ypoc/edited2.png"),
                                  size=(35, 35))
cp_del_img = ck.CTkImage(light_image=Image.open("/Users/jonathanduthil/Documents/GitHub/Ypoc/del.png"),
                                  size=(35,35))
cp_mv_img = ck.CTkImage(light_image=Image.open("/Users/jonathanduthil/Documents/GitHub/Ypoc/mv.png"),
                                  size=(35,35))

btn_cp_tree = ck.CTkButton(canvas2, text='Copy Structure', width=400, height=200, fg_color='white', hover_color='#9adffc', text_color='black', border_width=2, border_color='#d7dee0', image=cp_tree_img, compound=TOP, command=cp_tree)
btn_cp_tree.place(x=10, y=10)
btn_cp = ck.CTkButton(canvas2, text='Copy Files', width=150, height=200, fg_color='white', hover_color='#9adffc', text_color='black', image=cp_files_img, border_width=2, border_color='#d7dee0',compound=TOP, command=cp_files)
btn_cp.place(x=420, y=10)
btn_newer = ck.CTkButton(canvas2, text='Copy\n Newer Files', width=150, height=150, fg_color='white', hover_color='#9adffc', text_color='black', image=cp_newer_img, border_width=2, border_color='#d7dee0',compound=TOP, command=cp_newer)
btn_newer.place(x=420, y=230)
btn_gather = ck.CTkButton(canvas2, text='Create\n Paths List', width=100, height=150, fg_color='white', hover_color='#9adffc', text_color='black', image=cp_gather_img, border_width=2, border_color='#d7dee0',compound=TOP, command=gather)
btn_gather.place(x=10, y=230)
btn_edited = ck.CTkButton(canvas2, text='Copy Only\n Edited Files', width=150, height=150, fg_color='white', hover_color='#9adffc', text_color='black', image=cp_edited_img, border_width=2, border_color='#d7dee0',compound=TOP, command=edited_files)
btn_edited.place(x=260, y=230)
btn_del = ck.CTkButton(canvas2, text='Wipe Out\n Destination', width=100, height=75, fg_color='white', hover_color='#9adffc', text_color='black',image=cp_del_img, border_width=2, border_color='#d7dee0', command=edited_files)
btn_del.place(x=120, y=230)
btn_mv = ck.CTkButton(canvas2, text='Move\n Files', width=132, height=75, fg_color='white', hover_color='#9adffc', text_color='black',image=cp_mv_img, border_width=2, border_color='#d7dee0', command=move_files)
btn_mv.place(x=120, y=306)

window.mainloop()