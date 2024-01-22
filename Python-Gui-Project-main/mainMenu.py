import ttkbootstrap as tb


widget_refs = {}
frame = None

def mainMenuFrame(container, navigate_to, getText):
    global frame
    frame = tb.Frame(container, bootstyle="primary")
    
    frame.grid_rowconfigure(0, weight=2)
    frame.grid_rowconfigure(1, weight=9)
    frame.grid_rowconfigure(2, weight=4)
    frame.grid_rowconfigure(3, weight=5)
    frame.grid_rowconfigure(4, weight=2)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=3)
    frame.grid_columnconfigure(2, weight=1)
    frame.grid_columnconfigure(3, weight=3)
    frame.grid_columnconfigure(4, weight=1)
    frame.grid_columnconfigure(5, weight=3)
    frame.grid_columnconfigure(6, weight=1)
    frame.grid_columnconfigure(7, weight=3)
    frame.grid_columnconfigure(8, weight=1)


    spacer_vertical_1_frame = tb.Frame(frame, bootstyle="primary")
    spacer_vertical_1_frame.grid(row=0, column=0, columnspan=4, sticky="nsew")

    
    spacer_horizontal_1 = tb.Frame(frame, bootstyle="primary")
    spacer_horizontal_1.grid(row=1, column=0, sticky="nsew")
    
    book_management_button = tb.Button(frame, width=10, bootstyle="info", command=lambda: (navigateOut(container), navigate_to("bookManagement")))
    book_management_button.grid(row=1, column=1, sticky="nsew")
    
    spacer_horizontal_2 = tb.Frame(frame, bootstyle="primary")
    spacer_horizontal_2.grid(row=1, column=2, sticky="nsew")

    
    member_management_button = tb.Button(frame, width=10, bootstyle="info", command=lambda: (navigateOut(container), navigate_to("memberManagement")))
    member_management_button.grid(row=1, column=3, sticky="nsew")
    
    spacer_horizontal_3 = tb.Frame(frame, bootstyle="primary")
    spacer_horizontal_3.grid(row=1, column=4, sticky="nsew")

    
    admin_management_button = tb.Button(frame, width=10, bootstyle="info", command=lambda: (navigateOut(container), navigate_to("adminManagement")))
    admin_management_button.grid(row=1, column=5, sticky="nsew")
    
    spacer_horizontal_4 = tb.Frame(frame, bootstyle="primary")
    spacer_horizontal_4.grid(row=1, column=6, sticky="nsew")

    
    lending_management_button = tb.Button(frame, width=10, bootstyle="info", command=lambda: (navigateOut(container), navigate_to("lendingManagement")))
    lending_management_button.grid(row=1, column=7, sticky="nsew")
    
    spacer_horizontal_5 = tb.Frame(frame, bootstyle="primary")
    spacer_horizontal_5.grid(row=1, column=8, sticky="nsew")

    
    spacer_vertical_2_frame = tb.Frame(frame, bootstyle="primary")
    spacer_vertical_2_frame.grid(row=2, column=0, columnspan=4, sticky="nsew")
    
    logout_button = tb.Button(frame, width=10, bootstyle="info", command=lambda: (navigateOut(container), navigate_to("login")))
    logout_button.grid(row=3, column=7, sticky="nsew")
    
    spacer_vertical_3_frame = tb.Frame(frame, bootstyle="primary")
    spacer_vertical_3_frame.grid(row=4, column=0, columnspan=4, sticky="nsew")

    widget_refs['book_management_button'] = book_management_button
    widget_refs['member_management_button'] = member_management_button
    widget_refs['admin_management_button'] = admin_management_button
    widget_refs['lending_management_button'] = lending_management_button
    widget_refs['logout_button'] = logout_button
        
    updateTexts(getText)
    return frame


def updateTexts(getText):
    for widget_key in widget_refs:
        widget_refs[widget_key].configure(text=getText(widget_key))

def beNavigatedInto(container, navigate_to):
    container.bind('1', lambda e: (navigateOut(container), navigate_to("bookManagement")))
    container.bind('2', lambda e: (navigateOut(container), navigate_to("memberManagement")))
    container.bind('3', lambda e: (navigateOut(container), navigate_to("adminManagement")))
    container.bind('4', lambda e: (navigateOut(container), navigate_to("lendingManagement")))
    container.bind('<BackSpace>', lambda e: (navigateOut(container), navigate_to("login")))
    frame.focus_set()


def navigateOut(container):
    container.unbind('1')
    container.unbind('2')
    container.unbind('3')
    container.unbind('4')
    container.unbind('<BackSpace>')
