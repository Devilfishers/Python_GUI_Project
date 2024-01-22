import ttkbootstrap as tb
import database

widget_refs = {}
object_widget_refs = {}

frame = None

selectedItem = None
itemSelecterLambda = None
refreshTreeViewLambda = None
member_treeview = None
current_filter = None
lend_book_error_label_location = None

error_labels = []

passedObject = None


def searchFrame(container, perform_search):
    search_frame = tb.Frame(container, bootstyle="info")
    search_frame.grid(row=3, column=1, sticky='nsew')

    search_frame.grid_columnconfigure(0, weight=1)
    search_frame.grid_columnconfigure(1, weight=1)

    search_entry = tb.Entry(search_frame)
    search_entry.grid(row=0, column=0, columnspan=2,
                      sticky='ew', padx=5, pady=5)

    search_button = tb.Button(search_frame, command=lambda: perform_search())
    search_button.grid(row=1, column=0, columnspan=2,
                       sticky='nsew', padx=5, pady=5)

    search_var = tb.StringVar(value="name")

    style = tb.Style()
    style.configure('bg_info-fg_default.TRadiobutton',
                    background=style.colors.info)

    columns = ["student_id", "name"]
    for i, column in enumerate(columns):
        rb = tb.Radiobutton(search_frame, variable=search_var,
                            value=column, style="bg_info-fg_default.TRadiobutton")
        widget_refs[f"{column}_radiobutton"] = rb
        grid_row = 2 + (i // 2)
        grid_column = i % 2
        rb.grid(row=grid_row, column=grid_column, sticky="nws", padx=5, pady=5)

    widget_refs["search_button"] = search_button

    return search_entry, search_var


def selectedBookLendFrame(container):
    selected_book_lend_frame = tb.Frame(container, bootstyle="info")
    selected_book_lend_frame.grid(row=5, column=1, sticky='nsew')

    selected_book_lend_frame.grid_columnconfigure(0, weight=1)
    selected_book_lend_frame.grid_columnconfigure(1, weight=1)

    selected_book_lend_frame.grid_rowconfigure(0, weight=1)
    selected_book_lend_frame.grid_rowconfigure(1, weight=1)
    selected_book_lend_frame.grid_rowconfigure(2, weight=1)
    selected_book_lend_frame.grid_rowconfigure(3, weight=1)
    selected_book_lend_frame.grid_rowconfigure(4, weight=1)
    selected_book_lend_frame.grid_rowconfigure(5, weight=1)


    style = tb.Style()
    style.configure('bg_info-fg_default.TLabel', background=style.colors.info)
    style.configure('bg_info-fg_danger.TLabel', background=style.colors.info, foreground=style.colors.danger)

    book_fields = ['isbn', 'title', 'author', 'genre', 'quantity', "available", "borrowed" ]
    
    global object_widget_refs

    for i, field in enumerate(book_fields):
        widget_refs[f"{field}_label"] = tb.Label(
            selected_book_lend_frame, style="bg_info-fg_default.TLabel")
        widget_refs[f"{field}_label"].grid(row=i, column=0, padx=5, pady=5, sticky='ew')

        object_widget_refs[f"{field}"] = tb.Label(
            selected_book_lend_frame, style="bg_info-fg_default.TLabel")
        object_widget_refs[f"{field}"].grid(row=i, column=1, padx=5, pady=5, sticky='ew')

    global selectedItem, passedObject, lend_book_error_label_location

    error_labels.append(tb.Label(selected_book_lend_frame, style="bg_info-fg_danger.TLabel", width= 30))
    error_labels.append(tb.Label(selected_book_lend_frame, style="bg_info-fg_danger.TLabel", width= 30))
    error_labels.append(tb.Label(selected_book_lend_frame, style="bg_info-fg_danger.TLabel", width= 30))
    error_labels.append(tb.Label(selected_book_lend_frame, style="bg_info-fg_danger.TLabel", width= 30))

    lend_book_error_label_location = len(book_fields) + 1
    error_labels[0].grid(row=lend_book_error_label_location, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

    def borrow_selected_book():

        if selectedItem is None or passedObject is None:
            for label in error_labels:
                label.grid_remove()
            error_labels[3].grid(row=lend_book_error_label_location, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
            return

        if int(passedObject[5]) == 0:
            for label in error_labels:
                label.grid_remove()
            error_labels[2].grid(row=lend_book_error_label_location, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
            return

        user_id = member_treeview.item(selectedItem, 'values')[0]
        isbn = passedObject[0]

        result = database.borrow_book(user_id, isbn)

        for label in error_labels:
            label.grid_remove()

        if result == "Book borrowed successfully.":
            error_labels[0].grid(row=lend_book_error_label_location, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

            passedObject[5] = str(int(passedObject[5]) - 1)
            passedObject[6] = str(int(passedObject[6]) + 1)

            object_widget_refs['available'].configure(text=passedObject[5])
            object_widget_refs['borrowed'].configure(text=passedObject[6])

        elif result == "User has already borrowed a copy of this book.":
            error_labels[1].grid(row=lend_book_error_label_location, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
            

    lend_book_button = tb.Button(selected_book_lend_frame, bootstyle="success", command=borrow_selected_book)
    lend_book_button.grid(row=len(book_fields) + 2, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)

    widget_refs["lend_book_button"] = lend_book_button
    widget_refs["lend_book_error_label"] = error_labels[0]
    widget_refs["lend_book_error_label_1"] = error_labels[1]
    widget_refs["lend_book_error_label_2"] = error_labels[2]
    widget_refs["lend_book_error_label_3"] = error_labels[3]


def bookManagementPopupFrame(container, navigate_to, getText):

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
        member_treeview.delete(*member_treeview.get_children())
        userList = database.list_all_users()

        if current_filter:
            column_indices = {
                "student_id": 0,
                "name": 1,
            }
            search_index = column_indices[current_filter['column']]
            userList = [user for user in userList if current_filter['term'] in str(
                user[search_index]).lower()]

        for user in userList:
            member_treeview.insert("", "end", values=(user[0], user[1]))

    global refreshTreeViewLambda
    refreshTreeViewLambda = lambda: refreshTreeView()

    back_button = tb.Button(
        left_frame, command=lambda: (navigate_to("bookManagement"), navigateOut()), bootstyle="dark")
    back_button.grid(row=1, column=1, sticky='nsew')

    search_entry, search_var = searchFrame(left_frame, perform_search)

    selectedBookLendFrame(left_frame)

    global member_treeview

    member_treeview = tb.Treeview(right_frame, show="headings", selectmode="browse", columns=(
        "student_id", "name"), height=20, bootstyle="info")
    member_treeview.grid(row=0, column=0, sticky='nsew')

    member_treeview.heading("student_id", anchor="center")
    member_treeview.heading("name", anchor="center")

    member_treeview.column("student_id", width=100)
    member_treeview.column("name", width=100)

    yscrollbar = tb.Scrollbar(
        right_frame, orient="vertical", command=member_treeview.yview)
    member_treeview.configure(yscrollcommand=yscrollbar.set)
    yscrollbar.grid(row=0, column=1, sticky="ns")

    def itemSelect():
        global selectedItem
        selection = member_treeview.selection()

        if selection and len(selection) == 1:
            selectedItem = selection[0]

    global itemSelecterLambda
    itemSelecterLambda = itemSelect

    widget_refs['member_treeview_columns'] = {
        'student_id': member_treeview,
        'name': member_treeview
    }

    widget_refs['back_button'] = back_button

    updateTexts(getText)
    return frame


def updateTexts(getText):
    for widget_key in widget_refs:
        widget = widget_refs[widget_key]
        if widget_key == 'member_treeview_columns':
            for column_key in widget:
                treeview = widget[column_key]
                treeview.heading(column_key, text=getText(
                    f"{column_key}_member_treeview"))
        else:
            widget.configure(text=getText(widget_key))


def clearErrorLabels():
    for label in error_labels:
        label.grid_forget()
    error_labels[0].grid(row=lend_book_error_label_location, column=0, columnspan=2, padx=5, pady=5, sticky='ew')


def beNavigatedInto(container, navigate_to):
    global selectedItem
    selectedItem = None
    member_treeview.bind("<<TreeviewSelect>>", lambda e: itemSelecterLambda())
    refreshTreeViewLambda()
    frame.focus_set()


def navigateOut():
    member_treeview.unbind("<<TreeviewSelect>>")
    clearErrorLabels()
    global selectedItem
    selectedItem = None


def passObject(object):
    global passedObject
    passedObject = list(object)

    field_indices = {
        'isbn': 0,
        'title': 1,
        'author': 2,
        'genre': 3,
        'quantity': 4,
        "available": 5,
        "borrowed": 6,
    }
    
    for field, widget in object_widget_refs.items():
        index = field_indices[field]
        value = passedObject[index]
        widget.configure(text=value)
