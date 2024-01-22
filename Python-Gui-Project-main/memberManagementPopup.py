import ttkbootstrap as tb
import database

widget_refs = {}
object_widget_refs = {}

frame = None

selectedItem = None
itemSelecterLambda = None
refreshTreeViewLambda = None
book_treeview = None
current_filter = None
add_book_error_label_location = None

error_labels = []

passedObject = None


def searchFrame(container, perform_search):
    search_frame = tb.Frame(container, bootstyle="info")
    search_frame.grid(row=3, column=1, sticky='nsew')

    search_frame.grid_columnconfigure(0, weight=1)
    search_frame.grid_columnconfigure(1, weight=1)
    
    search_frame.grid_rowconfigure(0, weight=1)
    search_frame.grid_rowconfigure(1, weight=1)
    search_frame.grid_rowconfigure(2, weight=1)
    search_frame.grid_rowconfigure(3, weight=1)

    search_entry = tb.Entry(search_frame)
    search_entry.grid(row=0, column=0, columnspan=2,
                      sticky='ew', padx=5, pady=5)

    search_button = tb.Button(search_frame, command=lambda: perform_search())
    search_button.grid(row=1, column=0, columnspan=2,
                       sticky='nsew', padx=5, pady=5)

    search_var = tb.StringVar(value="title")

    style = tb.Style()
    style.configure('bg_info-fg_default.TRadiobutton',
                    background=style.colors.info)

    columns = ["isbn", "title", "author", "genre"]
    for i, column in enumerate(columns):
        rb = tb.Radiobutton(search_frame, variable=search_var,
                            value=column, style="bg_info-fg_default.TRadiobutton")
        widget_refs[f"{column}_radiobutton"] = rb
        grid_row = 2 + (i // 2)
        grid_column = i % 2
        rb.grid(row=grid_row, column=grid_column, sticky="nws", padx=5, pady=5)

    widget_refs["search_button"] = search_button

    return search_entry, search_var


def selectedBookReturnFrame(container):
    selected_book_return_frame = tb.Frame(container, bootstyle="info")
    selected_book_return_frame.grid(row=5, column=1, sticky='nsew')
    
    selected_book_return_frame.grid_columnconfigure(0, weight=1)
    selected_book_return_frame.grid_columnconfigure(1, weight=1)
    
    selected_book_return_frame.grid_rowconfigure(0, weight=1)
    selected_book_return_frame.grid_rowconfigure(1, weight=1)
    selected_book_return_frame.grid_rowconfigure(2, weight=1)
    selected_book_return_frame.grid_rowconfigure(3, weight=1)


    style = tb.Style()
    style.configure('bg_info-fg_default.TLabel', background=style.colors.info)
    style.configure('bg_info-fg_danger.TLabel', background=style.colors.info, foreground=style.colors.danger)

    user_fields = ['student_id', 'name']

    global object_widget_refs

    for i, field in enumerate(user_fields):
        widget_refs[f"{field}_label"] = tb.Label(
            selected_book_return_frame, style="bg_info-fg_default.TLabel")
        widget_refs[f"{field}_label"].grid(row=i, column=0, padx=5, pady=5, sticky='ew')

        object_widget_refs[f"{field}"] = tb.Label(
            selected_book_return_frame, style="bg_info-fg_default.TLabel")
        object_widget_refs[f"{field}"].grid(row=i, column=1, padx=5, pady=5, sticky='ew')

    global selectedItem, passedObject, lend_book_error_label_location

    error_labels.append(tb.Label(selected_book_return_frame, style="bg_info-fg_danger.TLabel", width= 30))
    error_labels.append(tb.Label(selected_book_return_frame, style="bg_info-fg_danger.TLabel", width= 30))
    error_labels.append(tb.Label(selected_book_return_frame, style="bg_info-fg_danger.TLabel", width= 30))

    lend_book_error_label_location = len(user_fields) + 1
    error_labels[0].grid(row=lend_book_error_label_location, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

    def return_selected_book():

        if selectedItem is None or passedObject is None:
            for label in error_labels:
                label.grid_forget()
            error_labels[2].grid(row=lend_book_error_label_location, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
            return
        
        user_id = passedObject[0]
        isbn = book_treeview.item(selectedItem, 'values')[0]

        result = database.return_book(user_id, isbn)
        
        if result == "Book returned successfully.":
            for label in error_labels:
                label.grid_forget()
            error_labels[0].grid(row=lend_book_error_label_location, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
            refreshTreeViewLambda()
        elif result == "No such borrowed book record found.":
            for label in error_labels:
                label.grid_forget()
            error_labels[1].grid(row=lend_book_error_label_location, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

    
    return_book_button = tb.Button(selected_book_return_frame, bootstyle="success", command=return_selected_book)
    return_book_button.grid(row=len(user_fields) + 2, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

    widget_refs["return_book_button"] = return_book_button
    widget_refs["return_book_error_label"] = error_labels[0]
    widget_refs["return_book_error_label_1"] = error_labels[1]
    widget_refs["return_book_error_label_2"] = error_labels[2]
    




def memberManagementPopupFrame(container, navigate_to, getText):

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
    left_frame.grid_rowconfigure(1, weight=3)
    left_frame.grid_rowconfigure(2, weight=1)
    left_frame.grid_rowconfigure(3, weight=2)
    left_frame.grid_rowconfigure(4, weight=1)
    left_frame.grid_rowconfigure(5, weight=5)
    left_frame.grid_rowconfigure(6, weight=1)

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

    def perform_search():
        global current_filter
        search_term = search_entry.get().lower()
        search_column = search_var.get()

        current_filter = {'column': search_column, 'term': search_term}
        refreshTreeView()

    def refreshTreeView():
        global current_filter
        book_treeview.delete(*book_treeview.get_children())
        bookList = database.list_borrowed_books_by_user(passedObject[0])

        if current_filter:
            column_indices = {
                "isbn": 0,
                "title": 1,
                "author": 2,
                "genre": 3
            }
            search_index = column_indices[current_filter['column']]
            bookList = [book for book in bookList if current_filter['term'] in str(
                book[search_index]).lower()]

        for book in bookList:
            book_treeview.insert("", "end", values=(
                book[0], book[1], book[2], book[3]))

    global refreshTreeViewLambda
    refreshTreeViewLambda = lambda: refreshTreeView()

    back_button = tb.Button(left_frame, command=lambda: (navigate_to("memberManagement"), navigateOut()), bootstyle="dark")
    back_button.grid(row=1, column=1, sticky='nsew')

    search_entry, search_var = searchFrame(left_frame, perform_search)

    selectedBookReturnFrame(left_frame)

    global book_treeview

    book_treeview = tb.Treeview(right_frame, show="headings", selectmode="browse",
                                columns=("isbn", "title", "author", "genre"), height=20, bootstyle="info")
    book_treeview.grid(row=0, column=0, sticky='nsew')

    book_treeview.heading("isbn", anchor="center")
    book_treeview.heading("title", anchor="center")
    book_treeview.heading("author", anchor="center")
    book_treeview.heading("genre", anchor="center")

    book_treeview.column("isbn", width=100)
    book_treeview.column("title", width=100)
    book_treeview.column("author", width=100)
    book_treeview.column("genre", width=100)

    yscrollbar = tb.Scrollbar(
        right_frame, orient="vertical", command=book_treeview.yview)
    book_treeview.configure(yscrollcommand=yscrollbar.set)
    yscrollbar.grid(row=0, column=1, sticky="ns")

    def itemSelect():
        global selectedItem
        selection = book_treeview.selection()

        if selection and len(selection) == 1:
            selectedItem = selection[0]

    global itemSelecterLambda
    itemSelecterLambda = itemSelect

    widget_refs['book_treeview_columns'] = {
        'isbn': book_treeview,
        'title': book_treeview,
        'author': book_treeview,
        'genre': book_treeview,
    }

    widget_refs["back_button"] = back_button

    updateTexts(getText)
    return frame


def updateTexts(getText):
    for widget_key in widget_refs:
        widget = widget_refs[widget_key]
        if widget_key == 'book_treeview_columns':
            for column_key in widget:
                treeview = widget[column_key]
                treeview.heading(column_key, text=getText(
                    f"{column_key}_book_treeview"))
        else:
            widget.configure(text=getText(widget_key))


def beNavigatedInto(container, navigate_to):
    global selectedItem
    selectedItem = None
    book_treeview.bind("<<TreeviewSelect>>", lambda e: itemSelecterLambda())
    frame.focus_set()


def clearErrorLabels():
    for label in error_labels:
        label.grid_forget()
    error_labels[0].grid(row=add_book_error_label_location, column=0, columnspan=2, padx=5, pady=5, sticky='ew')


def navigateOut():
    book_treeview.unbind("<Double-1>")
    clearErrorLabels()
    global selectedItem
    selectedItem = None

def passObject(object):
    global passedObject
    passedObject = list(object)
    
    field_indices = {
        'student_id': 0,
        'name': 1,
    }
    
    for field, widget in object_widget_refs.items():
        index = field_indices[field]
        value = passedObject[index]
        widget.configure(text=value)
        
    refreshTreeViewLambda()
