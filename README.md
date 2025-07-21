# 🖥️ Personal CLI Assistant

**Personal CLI Assistant** is an autonomous command-line application that helps you manage contacts, notes, and birthdays directly from your terminal. Built with Python and bundled as a standalone `.exe` file using PyInstaller.

---

## ⚙️ Features

- 📇 Manage contacts (add, update, all, remove)
- 🎂 Save and view upcoming birthdays
- 📝 Manage notes (create, update, remove, filter, sort)
- 🧠 Persistent data storage between sessions
- 🎨 Rich-colored terminal interface
- ⚡ Fast fuzzy matching for commands

---

## 💾 Download

> The final version is available as a standalone `.exe` file — **no Python installation required**.

**🔗 [Download Personal CLI Assistant v1.0.0](https://github.com/YuliiaDubyniuk/personal-cli-assistant/blob/main/dist/personal-assistant.exe)**

---

## 🚀 How to Run (Windows)

1. Download the `.exe` file
2. Open `cmd` or PowerShell
3. Navigate to the folder with the file
4. Run:

```bash
personal-assistant.exe
```

After launching, you’ll be able to use interactive commands directly from the terminal.

---

## 📂 Project Structure (before packaging)

```
src/
│
├── main.py                 # Entry point
├── decorators.py           # Command decorators
├── utilities.py            # Shared utilities
│
├── contacts/
│   ├── contacts.py         # Contact, AddressBook classes
│   └── contact_handler.py  # Contact-related command logic
│
└── notes/
    ├── notes.py            # Note, NoteBook classes
    └── note_handler.py     # Note-related command logic
```

---

## 📦 Technologies Used

    •	Python 3.10+
    •	PyInstaller — for building the .exe
    •	rich — terminal formatting and tables
    •	rapidfuzz — fuzzy command search
    •	Pygments, mdurl — additional formatting dependencies

---

## 🛠️ Build the Project Manually (for developers)

If you want to build the .exe yourself:

```
pip install -r requirements.txt
pyinstaller -- onefile src/main.py -n personal-assistant
```

After building, the standalone file will be located in the dist/ folder.

---

## 💬 Example Commands

1. contacts
2. add <name> <phone>
3. notes
4. help
5. all
6. exit
7. etc...

---

## 👤 Author

This project was created as part of the Python Core course (GoIT) by Olkhovetska Bohdana, Yuliia Dubyniuk and Kateryna Kyrylchuk .

---

## 📜 License

MIT License — free to use, share, and modify with attribution.
