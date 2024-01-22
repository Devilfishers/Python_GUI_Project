import ttkbootstrap as tb
import database
import languageMenu
import login
import mainMenu
import bookManagement
import memberManagement
import adminManagement
import bookManagementPopup
import memberManagementPopup
import lendingManagement

win = tb.Window(themename="flatly")
win.title("Library")
win.iconbitmap("assets//images//book_icon.ico") 

frames = {}


def switchLanguageHook():
    for frame_info in frames.values():
        frame_info["updateTexts"]()


languageMenu.languageMenu(win, switchLanguageHook)


def navigate_to(frame_name, object=None):
    if frame_name in frames:
        for frame_info in frames.values():
            frame_info["frame"].pack_forget()
        frames[frame_name]["frame"].pack(fill='both', expand=True)
        frames[frame_name]["beNavigatedInto"]()
        if object is not None:
            if frames[frame_name]["passObject"] is not None:
                frames[frame_name]["passObject"](object)
            else:
                print(f"No passObject for {frame_name}")
    else:
        print(f"No frame found for {frame_name}")


def create_frames():
    frames["login"] = {
        "frame": login.loginFrame(win, navigate_to, getText=lambda widget: languageMenu.getText("login", widget)),
        "updateTexts": lambda: login.updateTexts(getText=lambda widget: languageMenu.getText("login", widget)),
        "beNavigatedInto": lambda: login.beNavigatedInto(win, navigate_to)
    }
    frames["mainMenu"] = {
        "frame": mainMenu.mainMenuFrame(win, navigate_to, getText=lambda widget: languageMenu.getText("mainMenu", widget)),
        "updateTexts": lambda: mainMenu.updateTexts(getText=lambda widget: languageMenu.getText("mainMenu", widget)),
        "beNavigatedInto": lambda: mainMenu.beNavigatedInto(win, navigate_to)
    }
    frames["bookManagement"] = {
        "frame": bookManagement.bookManagementFrame(win, navigate_to, getText=lambda widget: languageMenu.getText("bookManagement", widget)),
        "updateTexts": lambda: bookManagement.updateTexts(getText=lambda widget: languageMenu.getText("bookManagement", widget)),
        "beNavigatedInto": lambda: bookManagement.beNavigatedInto(win, navigate_to)
    }
    frames["memberManagement"] = {
        "frame": memberManagement.memberManagementFrame(win, navigate_to, getText=lambda widget: languageMenu.getText("memberManagement", widget)),
        "updateTexts": lambda: memberManagement.updateTexts(getText=lambda widget: languageMenu.getText("memberManagement", widget)),
        "beNavigatedInto": lambda: memberManagement.beNavigatedInto(win, navigate_to)
    }
    frames["adminManagement"] = {
        "frame": adminManagement.adminManagementFrame(win, navigate_to, getText=lambda widget: languageMenu.getText("adminManagement", widget)),
        "updateTexts": lambda: adminManagement.updateTexts(getText=lambda widget: languageMenu.getText("adminManagement", widget)),
        "beNavigatedInto": lambda: adminManagement.beNavigatedInto(win, navigate_to)
    }
    frames["bookManagementPopup"] = {
        "frame": bookManagementPopup.bookManagementPopupFrame(win, navigate_to, getText=lambda widget: languageMenu.getText("bookManagementPopup", widget)),
        "updateTexts": lambda: bookManagementPopup.updateTexts(getText=lambda widget: languageMenu.getText("bookManagementPopup", widget)),
        "beNavigatedInto": lambda: bookManagementPopup.beNavigatedInto(win, navigate_to),
        "passObject": lambda object: bookManagementPopup.passObject(object)
    }
    frames["memberManagementPopup"] = {
        "frame": memberManagementPopup.memberManagementPopupFrame(win, navigate_to, getText=lambda widget: languageMenu.getText("memberManagementPopup", widget)),
        "updateTexts": lambda: memberManagementPopup.updateTexts(getText=lambda widget: languageMenu.getText("memberManagementPopup", widget)),
        "beNavigatedInto": lambda: memberManagementPopup.beNavigatedInto(win, navigate_to),
        "passObject": lambda object: memberManagementPopup.passObject(object)
    }
    frames["lendingManagement"] = {
        "frame": lendingManagement.lendingManagementFrame(win, navigate_to, getText=lambda widget: languageMenu.getText("lendingManagement", widget)),
        "updateTexts": lambda: lendingManagement.updateTexts(getText=lambda widget: languageMenu.getText("lendingManagement", widget)),
        "beNavigatedInto": lambda: lendingManagement.beNavigatedInto(win, navigate_to)
    }

    frames["login"]["frame"].pack(fill='both', expand=True)
    frames["login"]["beNavigatedInto"]()


create_frames()

database.setupDatabase()

window_width, window_height = 1500, 750
win.geometry(f"{window_width}x{window_height}+{int((win.winfo_screenwidth() - window_width) / 2)}+{int((win.winfo_screenheight() - window_height) / 2)}")

win.mainloop()
