import ttkbootstrap as tb
import database

widget_refs = {}
frame = None

selectedItem = None
itemSelecterLambda = None
refreshTreeViewLambda = None
lending_treeview = None
current_filter = None

def searchFrame(container, perform_search):
    search_frame = tb.Frame(container, bootstyle="info")
    search_frame.grid(row=3, column=1, sticky='nsew')

    search_frame.grid_columnconfigure(0, weight=1)
    search_frame.grid_columnconfigure(1, weight=1)
    
    search_frame.grid_rowconfigure(0, weight=1)
    search_frame.grid_rowconfigure(1, weight=1)
    search_frame.grid_rowconfigure(2, weight=1)
    search_frame.grid_rowconfigure(3, weight=1)
    search_frame.grid_rowconfigure(4, weight=1)

    search_entry = tb.Entry(search_frame)
    search_entry.grid(row=0, column=0, columnspan=2,
                      sticky='ew', padx=5, pady=5)

    search_button = tb.Button(search_frame, command=lambda: perform_search())
    search_button.grid(row=1, column=0, columnspan=2,
                       sticky='nsew', padx=5, pady=5)

    search_var = tb.StringVar(value="name")

    style = tb.Style()
    style.configure('bg_info-fg_default.TRadiobutton', background=style.colors.info)

    columns = ["student_id", "name", "isbn", "title", "author", "genre"]
    for i, column in enumerate(columns):
        rb = tb.Radiobutton(search_frame, variable=search_var,
                            value=column, style="bg_info-fg_default.TRadiobutton")
        widget_refs[f"{column}_radiobutton"] = rb
        grid_row = 2 + (i // 2)
        grid_column = i % 2
        rb.grid(row=grid_row, column=grid_column, sticky="nws", padx=5, pady=5)

    widget_refs["search_button"] = search_button

    return search_entry, search_var


def lendingManagementFrame(container, navigate_to, getText):

    global frame
    frame = tb.Frame(container, bootstyle="info")

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=4)

    frame.grid_rowconfigure(0, weight=1)

    left_frame = tb.Frame(frame, bootstyle="primary", width=200, height=200)
    right_frame = tb.Frame(frame, bootstyle="secondary", width=200, height=200)

    left_frame.grid(row=0, column=0, sticky='nsew')
    right_frame.grid(row=0, column=1, sticky='nsew')

    right_frame.grid_columnconfigure(0, weight=1)
    right_frame.grid_rowconfigure(0, weight=1)

    left_frame.grid_columnconfigure(0, weight=1)
    left_frame.grid_columnconfigure(1, weight=10)
    left_frame.grid_columnconfigure(2, weight=1)
    left_frame.grid_rowconfigure(0, weight=1)
    left_frame.grid_rowconfigure(1, weight=2)
    left_frame.grid_rowconfigure(2, weight=1)
    left_frame.grid_rowconfigure(3, weight=7)
    left_frame.grid_rowconfigure(4, weight=1)
    left_frame.grid_rowconfigure(5, weight=7)
    left_frame.grid_rowconfigure(6, weight=1)
    left_frame.grid_rowconfigure(7, weight=2)
    left_frame.grid_rowconfigure(8, weight=1)

    spacer_horizontal_1 = tb.Frame(
        left_frame, bootstyle="primary", width=5, height=5)
    spacer_horizontal_1.grid(row=0, column=0, sticky="nsew")

    spacer_horizontal_2 = tb.Frame(
        left_frame, bootstyle="primary", width=5, height=5)
    spacer_horizontal_2.grid(row=0, column=2, sticky="nsew")

    spacer_vertical_1 = tb.Frame(
        left_frame, bootstyle="primary", width=5, height=5)
    spacer_vertical_1.grid(row=0, column=1, sticky="nsew")

    spacer_vertical_2 = tb.Frame(
        left_frame, bootstyle="primary", width=5, height=5)
    spacer_vertical_2.grid(row=2, column=1, sticky="nsew")

    spacer_vertical_3 = tb.Frame(
        left_frame, bootstyle="primary", width=5, height=5)
    spacer_vertical_3.grid(row=4, column=1, sticky="nsew")

    spacer_vertical_4 = tb.Frame(
        left_frame, bootstyle="primary", width=5, height=5)
    spacer_vertical_4.grid(row=6, column=1, sticky="nsew")
    
    spacer_vertical_5 = tb.Frame(
        left_frame, bootstyle="primary", width=1, height=1)
    spacer_vertical_5.grid(row=5, column=1, sticky="nsew")

    spacer_vertical_6 = tb.Frame(
        left_frame, bootstyle="primary", width=1, height=1)
    spacer_vertical_6.grid(row=8, column=1, sticky="nsew")
    
    def perform_search():
        global current_filter
        search_term = search_entry.get().lower()
        search_column = search_var.get()

        current_filter = {'column': search_column, 'term': search_term}
        refreshTreeView()

    def return_selected():
        if selectedItem:
            database.return_book(lending_treeview.item(selectedItem, 'values')[0], lending_treeview.item(selectedItem, 'values')[2])
            refreshTreeView()

    def refreshTreeView():
        global current_filter
        lending_treeview.delete(*lending_treeview.get_children())
        borrow_list = database.list_all_borrowed()
        
        if current_filter:
            column_indices = {
                "student_id": 0,
                "name": 1,
                "isbn": 2,
                "title": 3,
                "author": 4,
                "genre": 5,
            }
            search_index = column_indices[current_filter['column']]
            borrow_list = [borrow for borrow in borrow_list if current_filter['term'] in str(
                borrow[search_index]).lower()]

        for borrow in borrow_list:
            lending_treeview.insert("", "end", values=(borrow[0], borrow[1], borrow[2], borrow[3], borrow[4], borrow[5]))
    
    global refreshTreeViewLambda
    refreshTreeViewLambda = lambda: refreshTreeView()

    back_button = tb.Button(
        left_frame, command=lambda: (navigate_to("mainMenu"), navigateOut()), bootstyle="dark")
    back_button.grid(row=1, column=1, sticky='nsew')

    search_entry, search_var = searchFrame(left_frame, perform_search)

    remove_selected_button = tb.Button(left_frame, command=return_selected, bootstyle="danger")
    remove_selected_button.grid(row=7, column=1, sticky='nsew')
    global lending_treeview

    lending_treeview = tb.Treeview(right_frame, show="headings", selectmode="browse", columns=("student_id", "name", "isbn", "title", "author", "genre"), height=20, bootstyle="info")
    lending_treeview.grid(row=0, column=0, sticky='nsew')

    lending_treeview.heading("student_id", anchor="center")
    lending_treeview.heading("name", anchor="center")
    lending_treeview.heading("isbn", anchor="center")
    lending_treeview.heading("title", anchor="center")
    lending_treeview.heading("author", anchor="center")
    lending_treeview.heading("genre", anchor="center")

    lending_treeview.column("student_id", width=100)
    lending_treeview.column("name", width=100)
    lending_treeview.column("isbn", width=100)
    lending_treeview.column("title", width=100)
    lending_treeview.column("author", width=100)
    lending_treeview.column("genre", width=100)
    
    yscrollbar = tb.Scrollbar(
        right_frame, orient="vertical", command=lending_treeview.yview)
    lending_treeview.configure(yscrollcommand=yscrollbar.set)
    yscrollbar.grid(row=0, column=1, sticky="ns")

    def itemSelect():
        global selectedItem
        selection = lending_treeview.selection()

        if selection and len(selection) == 1:
            selectedItem = selection[0]

    global itemSelecterLambda
    itemSelecterLambda = itemSelect

    widget_refs['lending_treeview_columns'] = {
        'student_id': lending_treeview,
        'name': lending_treeview,
        'isbn': lending_treeview,
        'title': lending_treeview,
        'author': lending_treeview,
        'genre': lending_treeview,
    }

    widget_refs['back_button'] = back_button
    widget_refs['remove_selected_button'] = remove_selected_button

    updateTexts(getText)
    return frame


def updateTexts(getText):
    for widget_key in widget_refs:
        widget = widget_refs[widget_key]
        if widget_key == 'lending_treeview_columns':
            for column_key in widget:
                treeview = widget[column_key]
                treeview.heading(column_key, text=getText(
                    f"{column_key}_lending_treeview"))
        else:
            widget.configure(text=getText(widget_key))


def beNavigatedInto(container, navigate_to):
    global selectedItem
    selectedItem = None
    lending_treeview.bind("<<TreeviewSelect>>", lambda e: itemSelecterLambda())
    refreshTreeViewLambda()
    frame.focus_set()


def navigateOut():
    lending_treeview.unbind("<<TreeviewSelect>>")
    global selectedItem
    selectedItem = None
