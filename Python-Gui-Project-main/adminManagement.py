import ttkbootstrap as tb
import database

widget_refs = {}
frame = None

selectedItem = None
itemSelecterLambda = None
refreshTreeViewLambda = None
admin_treeview = None
current_filter = None
add_admin_error_label_location = None

error_labels = []

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
    style.configure('bg_info-fg_default.TRadiobutton', background=style.colors.info)

    columns = ["name", "email", "phone_number"]
    for i, column in enumerate(columns):
        rb = tb.Radiobutton(search_frame, variable=search_var,
                            value=column, style="bg_info-fg_default.TRadiobutton")
        widget_refs[f"{column}_radiobutton"] = rb
        grid_row = 2 + (i // 2)
        grid_column = i % 2
        rb.grid(row=grid_row, column=grid_column, sticky="nws", padx=5, pady=5)

    widget_refs["search_button"] = search_button

    return search_entry, search_var


def addAdminFrame(container, admin_fields, try_add_admin):
    add_admin_frame = tb.Frame(container, bootstyle="info")
    add_admin_frame.grid(row=5, column=1, sticky='nsew')

    add_admin_frame.grid_columnconfigure(0, weight=1)
    add_admin_frame.grid_columnconfigure(1, weight=1)

    style = tb.Style()
    style.configure('bg_info-fg_default.TLabel', background=style.colors.info)
    style.configure('bg_info-fg_danger.TLabel', background=style.colors.info, foreground=style.colors.light)

    entries = {}
    for i, field in enumerate(admin_fields):
        add_admin_frame.grid_rowconfigure(i, weight=1)
        label = tb.Label(
            add_admin_frame, style="bg_info-fg_default.TLabel", width=10)
        widget_refs[f"{field}_add_label"] = label
        label.grid(row=i, column=0, padx=5, pady=5, sticky='ew')
        entry = tb.Entry(add_admin_frame)
        entry.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
        entries[field] = entry

    global error_labels

    error_labels.append(tb.Label(add_admin_frame, style="bg_info-fg_danger.TLabel"))
    error_labels.append(tb.Label(add_admin_frame, style="bg_info-fg_danger.TLabel"))
    error_labels.append(tb.Label(add_admin_frame, style="bg_info-fg_danger.TLabel"))
    error_labels.append(tb.Label(add_admin_frame, style="bg_info-fg_danger.TLabel"))

    global add_admin_error_label_location
    add_admin_error_label_location = len(admin_fields)

    error_labels[0].grid(row=add_admin_error_label_location, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

    add_admin_button = tb.Button(add_admin_frame, command=try_add_admin)
    add_admin_button.grid(row=add_admin_error_label_location+1, column=0,columnspan=2, padx=5, pady=5, sticky='ew')

    widget_refs["add_admin_button"] = add_admin_button
    widget_refs["add_admin_error_label"] = error_labels[0]
    widget_refs["add_admin_error_label_1"] = error_labels[1]
    widget_refs["add_admin_error_label_2"] = error_labels[2]
    widget_refs["add_admin_error_label_3"] = error_labels[3]

    return entries


def adminManagementFrame(container, navigate_to, getText):

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
    left_frame.grid_rowconfigure(0, weight=2)
    left_frame.grid_rowconfigure(1, weight=5)
    left_frame.grid_rowconfigure(2, weight=1)
    left_frame.grid_rowconfigure(3, weight=5)
    left_frame.grid_rowconfigure(4, weight=1)
    left_frame.grid_rowconfigure(5, weight=5)
    left_frame.grid_rowconfigure(6, weight=1)
    left_frame.grid_rowconfigure(7, weight=5)
    left_frame.grid_rowconfigure(8, weight=2)

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
    spacer_vertical_5.grid(row=8, column=1, sticky="nsew")

    def perform_search():
        global current_filter
        search_term = search_entry.get().lower()
        search_column = search_var.get()

        current_filter = {'column': search_column, 'term': search_term}
        refreshTreeView()

    def remove_selected_admin():
        if selectedItem:
            database.delete_admin(admin_treeview.item(selectedItem, 'values')[0])
            refreshTreeView()

    admin_fields = ['name', 'email', 'phone_number', 'password', 'password_retype']

    def try_add_admin():
        admin_data = {field: entries[field].get() for field in admin_fields}
        
        if all(admin_data.values()):
            if admin_data['password'] == admin_data['password_retype']:
                admin_info = {key: admin_data[key] for key in ['name', 'email', 'phone_number', 'password']}
                result = database.add_admin(**admin_info)
                for entry in entries.values():
                    entry.delete(0, 'end')

                if result == "Admin with this name already exists.":
                    for label in error_labels:
                        label.grid_forget()
                    error_labels[1].grid(row=add_admin_error_label_location, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
                else:
                    for label in error_labels:
                        label.grid_forget()
                    error_labels[0].grid(row=add_admin_error_label_location, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
                    refreshTreeView()
            else:
                for label in error_labels:
                    label.grid_forget()
                error_labels[3].grid(row=add_admin_error_label_location, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
        else:
            for label in error_labels:
                label.grid_forget()
            error_labels[2].grid(row=add_admin_error_label_location, column=0, columnspan=2, padx=5, pady=5, sticky='ew')


    def refreshTreeView():
        global current_filter
        admin_treeview.delete(*admin_treeview.get_children())
        adminList = database.list_all_admins()

        if current_filter:
            column_indices = {
                "name": 0,
                "email": 1,
                "phone_number": 2,
            }
            search_index = column_indices[current_filter['column']]
            adminList = [admin for admin in adminList if current_filter['term'] in str(
                admin[search_index]).lower()]

        for admin in adminList:
            admin_treeview.insert("", "end", values=(admin[0], admin[1], admin[2]))
            
    global refreshTreeViewLambda
    refreshTreeViewLambda = lambda: refreshTreeView()

    back_button = tb.Button(
        left_frame, command=lambda: (navigate_to("mainMenu"), navigateOut()), bootstyle="dark")
    back_button.grid(row=1, column=1, sticky='nsew')

    search_entry, search_var = searchFrame(left_frame, perform_search)

    entries = addAdminFrame(left_frame, admin_fields, try_add_admin)

    remove_selected_button = tb.Button(left_frame, command=remove_selected_admin, bootstyle="danger")
    remove_selected_button.grid(row=7, column=1, sticky='nsew')
    global admin_treeview

    admin_treeview = tb.Treeview(right_frame, show="headings", selectmode="browse", columns=(
        "name", "email", "phone_number"), height=20, bootstyle="info")
    admin_treeview.grid(row=0, column=0, sticky='nsew')

    admin_treeview.heading("name", text="Name", anchor="center")
    admin_treeview.heading("email", text="Email", anchor="center")
    admin_treeview.heading("phone_number", text="Phone Number", anchor="center")

    admin_treeview.column("name", width=100)
    admin_treeview.column("email", width=150)
    admin_treeview.column("phone_number", width=150)

    yscrollbar = tb.Scrollbar(
        right_frame, orient="vertical", command=admin_treeview.yview)
    admin_treeview.configure(yscrollcommand=yscrollbar.set)
    yscrollbar.grid(row=0, column=1, sticky="ns")

    def itemSelect():
        global selectedItem
        selection = admin_treeview.selection()

        if selection and len(selection) == 1:
            selectedItem = selection[0]

    global itemSelecterLambda
    itemSelecterLambda = itemSelect

    widget_refs['admin_treeview_columns'] = {
        'name': admin_treeview,
        'email': admin_treeview,
        'phone_number': admin_treeview
    }

    widget_refs['back_button'] = back_button
    widget_refs['remove_selected_button'] = remove_selected_button

    updateTexts(getText)
    return frame


def updateTexts(getText):
    for widget_key in widget_refs:
        widget = widget_refs[widget_key]
        if widget_key == 'admin_treeview_columns':
            for column_key in widget:
                treeview = widget[column_key]
                treeview.heading(column_key, text=getText(
                    f"{column_key}_admin_treeview"))
        else:
            widget.configure(text=getText(widget_key))


def clearErrorLabels():
    for label in error_labels:
        label.grid_forget()
    error_labels[0].grid(row=add_admin_error_label_location, column=0, columnspan=2, padx=5, pady=5, sticky='ew')


def beNavigatedInto(container, navigate_to):
    global selectedItem
    selectedItem = None
    admin_treeview.bind("<<TreeviewSelect>>", lambda e: itemSelecterLambda())
    refreshTreeViewLambda()
    frame.focus_set()


def navigateOut():
    admin_treeview.unbind("<<TreeviewSelect>>")
    clearErrorLabels()
    global selectedItem
    selectedItem = None