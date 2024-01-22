import ttkbootstrap as tb
import os


def switchLanguage(language, switchLanguageHook):
    global current_language
    current_language = language
    switchLanguageHook()


def getAllTextFromFile():
    base_path = os.path.join("assets", "Language")

    all_text = {}
    for lang in os.listdir(base_path):
        lang_path = os.path.join(base_path, lang)
        if os.path.isdir(lang_path):
            all_text[lang] = {}
            for file in os.listdir(lang_path):
                if file.endswith('.txt'):
                    section = file.split('.')[0] 
                    file_path = os.path.join(lang_path, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            text_entries = {}
                            for line in file:
                                if ':' in line:
                                    key, value = line.strip().split(':', 1)
                                    text_entries[key] = value
                            all_text[lang][section] = text_entries
                    except FileNotFoundError:
                        print(f"File not found: {file_path}")
                    except Exception as e:
                        print(f"An error occurred: {e}")

    return all_text


def languageMenu(root, switchLanguageHook):
    global all_text

    all_text = getAllTextFromFile()

    global current_language
    current_language = 'en'

    menubar = tb.Menu(root)
    language_menu = tb.Menu(menubar, tearoff=0)

    language_menu.add_checkbutton(label="English", variable=current_language, onvalue='en', offvalue='en', command=lambda: switchLanguage('en', switchLanguageHook))
    language_menu.add_checkbutton(label="Turkish", variable=current_language, onvalue='tr', offvalue='tr', command=lambda: switchLanguage('tr', switchLanguageHook))

    menubar.add_cascade(label="Language", menu=language_menu)
    root.config(menu=menubar)


def getText(frame_name, widget):
    return all_text[current_language][frame_name][widget]
