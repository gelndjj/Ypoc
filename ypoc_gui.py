import tkinter as tk, shutil, webbrowser, os
from tkinter import filedialog
from tkinter import *
import customtkinter as ck, zipfile
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
            total_dirs = sum([len(dirs) for _, dirs, _ in os.walk(src_folder)])
            created_dirs = 0

            stop_flag = False
            def stop_copy():
                nonlocal stop_flag
                stop_flag = True

            window.bind('a', lambda event: stop_copy())

            for dirpath, dirnames, filenames in os.walk(src_folder):
                if stop_flag:
                    break
                relative_path = os.path.relpath(dirpath, src_folder)
                new_dir_path = os.path.join(dst_folder, relative_path)
                os.makedirs(new_dir_path, exist_ok=True)
                created_dirs += 1

                percent = int((created_dirs / total_dirs) * 100)
                percent_str = f"{percent}%"
                percent_label.configure(text=percent_str)
                percent_label.update()

                abort_str = 'Press \'a\' to abort'
                abort_label.configure(text=abort_str)

            percent_label.configure(text="")
            abort_label.configure(text="")

            if stop_flag:
                tk.messagebox.showinfo("Stop", "Copy process was stopped.")
            else:
                tk.messagebox.showinfo("Success", "Folder structure copied successfully!")

def cp_files():
    source = filedialog.askdirectory(initialdir="/", title="Select Source")
    if source:
        destination = filedialog.askdirectory(initialdir="/", title="Select Destination")

        total_size = sum(os.path.getsize(os.path.join(foldername, filename)) for foldername, subfolders, filenames in os.walk(source) for filename in filenames)
        copied_size = 0
        stop_flag = False

        def stop_copy():
            nonlocal stop_flag
            stop_flag = True

        window.bind('a', lambda event: stop_copy())

        for foldername, subfolders, filenames in os.walk(source):
            for filename in filenames:
                src_file = os.path.join(foldername, filename)
                dest_file = src_file.replace(source, destination, 1)

                os.makedirs(os.path.dirname(dest_file), exist_ok=True)

                if stop_flag:
                    tk.messagebox.showinfo("Stop", "Copy process was stopped.")
                    percent_label.configure(text="")
                    abort_label.configure(text="")
                    return

                shutil.copy2(src_file, dest_file)
                copied_size += os.path.getsize(src_file)
                percent = int(copied_size/total_size * 100)
                percent_label.configure(text=f"{percent}%")
                percent_label.update()

                abort_str = 'Press \'a\' to abort'
                abort_label.configure(text=abort_str)

        percent_label.configure(text="")
        abort_label.configure(text="")

        tk.messagebox.showinfo("Copy Complete", "The files have been copied successfully.")

def cp_zip():
    source = filedialog.askdirectory(initialdir="/", title="Select Source")
    if source:
        destination = filedialog.askdirectory(initialdir="/", title="Select Destination")
        if destination:
            folder_name = os.path.basename(source)
            zip_filename = os.path.join(destination, folder_name + '.zip')
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                total_size = sum(os.path.getsize(os.path.join(foldername, filename)) for foldername, subfolders, filenames in os.walk(source) for filename in filenames)
                copied_size = 0
                stop_flag = False

                def stop_copy():
                    nonlocal stop_flag
                    stop_flag = True

                window.bind('a', lambda event: stop_copy())

                for foldername, subfolders, filenames in os.walk(source):
                    for filename in filenames:
                        src_file = os.path.join(foldername, filename)
                        dest_file = src_file.replace(source, '', 1)

                        if stop_flag:
                            tk.messagebox.showinfo("Stop", "Copy process was stopped.")
                            percent_label.configure(text="")
                            abort_label.configure(text="")
                            return

                        zip_file.write(src_file, os.path.join(folder_name, dest_file))
                        copied_size += os.path.getsize(src_file)
                        percent = int(copied_size/total_size * 100)
                        percent_label.configure(text=f"{percent}%")
                        percent_label.update()

                        abort_str = 'Press \'a\' to abort'
                        abort_label.configure(text=abort_str)

                percent_label.configure(text="")
                abort_label.configure(text="")

                tk.messagebox.showinfo("Copy Complete", "The files have been copied and compressed as ZIP successfully.")

def cp_newer():
    source_dir = filedialog.askdirectory(title="Select source directory")
    if source_dir:
        destination_dir = filedialog.askdirectory(title="Select destination directory")

        total_size = sum(os.path.getsize(os.path.join(root_dir, file)) for root_dir, _, files in os.walk(source_dir) for file in files)
        bytes_copied = 0

        stop_flag = False
        def stop_copy():
            nonlocal stop_flag
            stop_flag = True

        window.bind('a', lambda event: stop_copy())

        for root_dir, _, files in os.walk(source_dir):
            dest_dir = os.path.join(destination_dir, os.path.relpath(root_dir, source_dir))
            os.makedirs(dest_dir, exist_ok=True)
            for file in files:
                if stop_flag:
                    break
                src_file = os.path.join(root_dir, file)
                dest_file = os.path.join(dest_dir, file)
                if os.path.exists(dest_file):
                    if os.path.getmtime(src_file) > os.path.getmtime(dest_file):
                        shutil.copy2(src_file, dest_file)
                else:
                    shutil.copy2(src_file, dest_file)
                file_size = os.path.getsize(src_file)
                bytes_copied += file_size
                percent = int(bytes_copied / total_size * 100)
                percent_label.configure(text=f"{percent}%")
                percent_label.update()

                abort_str = 'Press \'a\' to abort'
                abort_label.configure(text=abort_str)

                if stop_flag:
                    break

            percent_label.configure(text="")
            abort_label.configure(text="")

        if stop_flag:
            tk.messagebox.showinfo("Copy Aborted", "The copy process was aborted.")
        else:
            tk.messagebox.showinfo("Success", "Newer items copied successfully!")

def gather():
    folder_path = filedialog.askdirectory()
    if folder_path:
        file_paths = []

        total_files = 0
        copied_files = 0

        for root, dirs, files in os.walk(folder_path):
            total_files += len(files)

        stop_flag = False
        def stop_copy():
            nonlocal stop_flag
            stop_flag = True

        window.bind('a', lambda event: stop_copy())

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if stop_flag:
                    break
                file_paths.append(os.path.join(root, file))

                copied_files += 1
                progress_text = "{}/{}".format(copied_files, total_files)
                percent_label.configure(text=progress_text)
                percent_label.update()
                abort_str = 'Press \'a\' to abort'
                abort_label.configure(text=abort_str)

            if stop_flag:
                break

        with open('list_files.txt', 'w') as f:
            for item in file_paths:
                if stop_flag:
                    break
                f.write('%s\n' % item)

                copied_files += 1
                progress_text = "{}/{}".format(copied_files, total_files)
                percent_label.configure(text=progress_text)
                percent_label.update()

                abort_str = 'Press \'a\' to abort'
                abort_label.configure(text=abort_str)

            percent_label.configure(text="")
            abort_label.configure(text="")

        if stop_flag:
            tk.messagebox.showwarning("Aborted", "Copy process aborted.")
        else:
            tk.messagebox.showinfo("Success", "Paths list copied successfully!")

def edited_files():
    source_dir = filedialog.askdirectory(title="Select source directory")
    if source_dir:
        destination_dir = filedialog.askdirectory(title="Select destination directory")

        total_files = sum([len(files) for root_dir, _, files in os.walk(source_dir)])
        copied_files = 0
        stop_flag = False

        def stop_copy(event=None):
            nonlocal stop_flag
            stop_flag = True
        window.bind("a", stop_copy)

        for root_dir, _, files in os.walk(source_dir):
            dest_dir = os.path.join(destination_dir, os.path.relpath(root_dir, source_dir))
            if not os.path.exists(dest_dir):
                continue
            for file in files:
                if stop_flag:
                    tk.messagebox.showinfo("Stop", "Copy process aborted.")
                    abort_label.configure(text="")
                    percent_label.configure(text="")
                    return
                src_file = os.path.join(root_dir, file)
                dest_file = os.path.join(dest_dir, file)
                if not os.path.exists(dest_file):
                    continue
                if os.path.getmtime(src_file) > os.path.getmtime(dest_file):
                    shutil.copy2(src_file, dest_file)
                copied_files += 1
                progress_percent = int(copied_files / total_files * 100)
                percent_label.configure(text=f"{progress_percent}%")
                percent_label.update()
                abort_str = 'Press \'a\' to abort'
                abort_label.configure(text=abort_str)

        percent_label.configure(text="")
        abort_label.configure(text="")

        tk.messagebox.showinfo("Success", "Edited files copied successfully!")

def delete_files():
    folder_path = filedialog.askdirectory(title="Select source directory")
    if folder_path:

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
    if source_dir:

        destination_dir = filedialog.askdirectory(title="Select destination directory")

        stop_flag = False

        def stop_moving(event):
            nonlocal stop_flag
            stop_flag = True

        window.bind('a', stop_moving)

        num_files = len(os.listdir(source_dir))
        completed = 0

        for file_name in os.listdir(source_dir):
            if stop_flag:
                break
            file_path = os.path.join(source_dir, file_name)
            if os.path.isfile(file_path):
                shutil.move(file_path, os.path.join(destination_dir, file_name))
            elif os.path.isdir(file_path):
                shutil.move(file_path, os.path.join(destination_dir, file_name))

            completed += 1
            progress_percent = (completed / num_files) * 100
            percent_label.configure(text=f"{progress_percent:.1f}%")
            percent_label.update()

            abort_str = 'Press \'a\' to abort'
            abort_label.configure(text=abort_str)

        percent_label.configure(text="")
        abort_label.configure(text="")

        if not stop_flag:
            tk.messagebox.showinfo("Success", "Files moved successfully!")
        else:
            tk.messagebox.showinfo("Abort", "Moving files aborted!")

        window.unbind('a')

def open_github_profile():
    webbrowser.open_new("https://github.com/gelndjj?tab=repositories")

def kofi():
    webbrowser.open_new("https://ko-fi.com/gelndjj")

frame = tk.Frame(window, width=800, height=500, borderwidth=0, highlightthickness=0)
frame.pack()
image = Image.open("resources/bg.png")
img = ImageTk.PhotoImage(image)

canvas = tk.Canvas(frame, width=800, height=500, highlightthickness=0)
canvas.pack()
canvas.create_image(0, 0, anchor=tk.NW, image=img)

canvas2 = tk.Canvas(frame, width=700, height=400, highlightthickness=0)
canvas2.place(x=200,y=100)
canvas2.create_rectangle(0, 0, 698, 398, outline="black", width=6)

percent_label = ck.CTkLabel(canvas2, text='',bg_color='#ebeceb', text_color='red')
percent_label.place(x=15,y=205)

abort_label = ck.CTkLabel(canvas2, text='',bg_color='#ebeceb', text_color='red')
abort_label.place(x=130,y=205)

cp_tree_img = ck.CTkImage(light_image=Image.open("resources/cp_tree.png"),
                                  size=(45, 45))
cp_files_img = ck.CTkImage(light_image=Image.open("resources/cp_files.png"),
                                  size=(45, 45))
cp_zip_img = ck.CTkImage(light_image=Image.open("resources/zip2.png"),
                                  size=(45, 45))
cp_newer_img = ck.CTkImage(light_image=Image.open("resources/cp_newer.png"),
                                  size=(60, 60))
cp_gather_img = ck.CTkImage(light_image=Image.open("resources/gather.png"),
                                  size=(45, 45))
cp_edited_img = ck.CTkImage(light_image=Image.open("resources/edited.png"),
                                  size=(35, 35))
cp_del_img = ck.CTkImage(light_image=Image.open("resources/del.png"),
                                  size=(35,35))
cp_mv_img = ck.CTkImage(light_image=Image.open("resources/mv.png"),
                                  size=(35,35))

btn_cp_tree = ck.CTkButton(canvas2, text='Copy Structure', width=240, height=200, fg_color='white', hover_color='#9adffc', text_color='black', border_width=2, border_color='#d7dee0', image=cp_tree_img, compound=TOP, command=cp_tree)
btn_cp_tree.place(x=10, y=10)
btn_cp = ck.CTkButton(canvas2, text='Copy Files', width=310, height=100, fg_color='white', hover_color='#9adffc', text_color='black', image=cp_files_img, border_width=2, border_color='#d7dee0',compound=TOP, command=cp_files)
btn_cp.place(x=260, y=10)
btn_bk = ck.CTkButton(canvas2, text='Copy Files as ZIP', width=310, height=90, fg_color='white', hover_color='#9adffc', text_color='black', image=cp_zip_img, border_width=2, border_color='#d7dee0',compound=TOP, command=cp_zip)
btn_bk.place(x=260, y=120)
btn_newer = ck.CTkButton(canvas2, text='Copy\n Newer Files', width=150, height=150, fg_color='white', hover_color='#9adffc', text_color='black', image=cp_newer_img, border_width=2, border_color='#d7dee0',compound=TOP, command=cp_newer)
btn_newer.place(x=420, y=230)
btn_gather = ck.CTkButton(canvas2, text='Create\n Paths List', width=100, height=150, fg_color='white', hover_color='#9adffc', text_color='black', image=cp_gather_img, border_width=2, border_color='#d7dee0',compound=TOP, command=gather)
btn_gather.place(x=10, y=230)
btn_edited = ck.CTkButton(canvas2, text='Copy Only\n Edited Files', width=150, height=150, fg_color='white', hover_color='#9adffc', text_color='black', image=cp_edited_img, border_width=2, border_color='#d7dee0',compound=TOP, command=edited_files)
btn_edited.place(x=260, y=230)
btn_del = ck.CTkButton(canvas2, text='Wipe Out\n Destination', width=100, height=75, fg_color='white', hover_color='#9adffc', text_color='black',image=cp_del_img, border_width=2, border_color='#d7dee0', command=delete_files)
btn_del.place(x=120, y=230)
btn_mv = ck.CTkButton(canvas2, text='Move\n Files', width=132, height=75, fg_color='white', hover_color='#9adffc', text_color='black',image=cp_mv_img, border_width=2, border_color='#d7dee0', command=move_files)
btn_mv.place(x=120, y=306)
btn_git = ck.CTkButton(frame, text='Other Projects', width=60, fg_color='#101a24', bg_color='#0f1b24', hover_color='blue', text_color='white', border_width=2, border_color='black', command=open_github_profile)
btn_git.place(x=10, y=435)
btn_kofi = ck.CTkButton(frame, text='Tip ☕️', width=40, fg_color='#101a24', bg_color='#0f1b24', hover_color='blue', text_color='white', border_width=2, border_color='black', command=kofi)
btn_kofi.place(x=10, y=400)
btn_quit = ck.CTkButton(frame, text='Quit', width=130, fg_color='#101a24', bg_color='#0f1b24', hover_color='red', text_color='white', border_width=2, border_color='black', command=lambda:window.destroy())
btn_quit.place(x=10, y=470)

window.mainloop()