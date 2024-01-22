import ttkbootstrap as tb
import database
from PIL import Image, ImageTk
import time
import threading

widget_refs = {}
on_login_click_lambda = None
frame = None

image_label = None
original_image = None
resized_image = None

resize_timer = None
resize_delay = 0.1
resize_lock = threading.Lock()

def login_admin(username, password):
    result = database.validate_admin(username, password)

    if result == "Success" or "Admin does not exist!" or "Password is incorrect":
        return result
    else:
        return "Unexpected error occurred!"

def resizeImage():
    global resize_timer

    if resize_timer is not None:
        resize_timer.cancel()

    resize_timer = threading.Timer(resize_delay, performResize)
    resize_timer.start()

def performResize():
    global image_label, original_image, resized_image

    new_width, new_height = image_label.winfo_width(), image_label.winfo_height()

    if resized_image and (resized_image.width() == new_width and resized_image.height() == new_height):
        return

    resized_image = ImageTk.PhotoImage(original_image.resize((new_width, new_height)))
    image_label.configure(image=resized_image)

def backgroundFrame(container):
    
    global image_label, original_image, resized_image
    
    right_frame = tb.Frame(container, bootstyle="secondary")
    
    image_label = tb.Label(right_frame)
    image_label.pack(fill="both", expand=True)
    
    original_image = Image.open("assets/images/loginImage.png")
    
    resized_image = ImageTk.PhotoImage(original_image.resize((1202,720)))
    
    image_label.configure(image=resized_image)
            

    return right_frame


def loginFrame(container, navigate_to, getText):
    global frame
    frame = tb.Frame(container)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=20)
    frame.grid_rowconfigure(0, weight=1)

    left_frame = tb.Frame(frame, bootstyle="primary", width=200, height=200)
    left_frame.grid(row=0, column=0, sticky='nsew')

    right_frame = backgroundFrame(frame)
    right_frame.grid(row=0, column=1, sticky='nsew')

    spacer = tb.Frame(left_frame, bootstyle="primary")
    spacer.grid(row=0, column=0, columnspan=2, sticky='nsew')
    left_frame.grid_rowconfigure(0, weight=1)
    left_frame.grid_columnconfigure(0, weight=1)
    left_frame.grid_columnconfigure(1, weight=1)


    username_label = tb.Label(left_frame, bootstyle="inverse-primary", width=10, anchor="e")
    username_label.grid(row=1,column=0, sticky="nse", padx=(5,10), pady=5)
    username_entry = tb.Entry(left_frame, width=15)
    username_entry.grid(row=1,column=1,sticky="nsw", padx=(10,5), pady=5)

    password_label = tb.Label(left_frame, bootstyle="inverse-primary", width=10, anchor="e")
    password_label.grid(row=2,column=0, sticky="nse", padx=(5,10), pady=5)
    password_entry = tb.Entry(left_frame, show="*", width=15)
    password_entry.grid(row=2,column=1, sticky="nsw", padx=(10,5), pady=5)

    style = tb.Style()
    style.configure('bg_primary-fg_danger.TLabel', background=style.colors.primary, foreground=style.colors.danger)

    error_label = tb.Label(left_frame, style='bg_primary-fg_danger.TLabel', width=20)
    error_label_1 = tb.Label(left_frame, style='bg_primary-fg_danger.TLabel', width=20)
    error_label_2 = tb.Label(left_frame, style='bg_primary-fg_danger.TLabel', width=20)
    error_label.grid(row=3, column=0, columnspan=2,  padx=5, pady=5)

    def on_login_click():
        username = username_entry.get()
        password = password_entry.get()
        validation_result = login_admin(username, password)

        if validation_result == "Success":
            navigate_to("mainMenu")
            navigateOut(container)
            username_entry.delete(0, 'end')
            password_entry.delete(0, 'end')
            error_label.grid_forget()
            error_label_1.grid_forget()
            error_label_2.grid_forget()
            error_label.grid(row=3, column=0, columnspan=2,  padx=5, pady=5)
        elif validation_result == "Admin does not exist!":
            error_label.grid_forget()
            error_label_1.grid_forget()
            error_label_2.grid_forget()
            error_label_1.grid(row=3, column=0, columnspan=2,  padx=5, pady=5)
            password_entry.delete(0, 'end')
        elif validation_result == "Password is incorrect!":
            error_label.grid_forget()
            error_label_1.grid_forget()
            error_label_2.grid_forget()
            error_label_2.grid(row=3, column=0, columnspan=2,  padx=5, pady=5)
            password_entry.delete(0, 'end')

    login_button = tb.Button(left_frame, bootstyle="info", command=on_login_click, width=10)
    login_button.grid(row=4, column=0, columnspan=2, padx=5, pady=(10, 20))

    global on_login_click_lambda
    on_login_click_lambda = lambda: on_login_click()

    widget_refs["username_label"] = username_label
    widget_refs["password_label"] = password_label
    widget_refs["error_label"] = error_label
    widget_refs["error_label_1"] = error_label_1
    widget_refs["error_label_2"] = error_label_2
    widget_refs["login_button"] = login_button

    updateTexts(getText)
    return frame


def updateTexts(getText):
    for widget_key in widget_refs:
        widget_refs[widget_key].configure(text=getText(widget_key))


def beNavigatedInto(container, navigate_to):
    database.setupDatabase()
    container.bind('<Return>', lambda e: on_login_click_lambda())
    container.bind('<Configure>', lambda e: resizeImage())
    frame.focus_set()


def navigateOut(container):
    container.unbind('<Return>')
    container.unbind('<Configure>')