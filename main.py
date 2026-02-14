from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import json
import os


def save_tasks_to_file():
    tasks = []
    for item in tree.get_children():
        tasks.append(tree.item(item, "values"))

    with open("tasks.json", "w") as file:
        json.dump(tasks, file)


def load_tasks_from_file():
    try:
        with open("tasks.json", "r") as file:
            tasks = json.load(file)

            for task in tasks:
                if task[2] == "Completed":
                    tree.insert("", "end", values=task, tags=("completed",))
                else:
                    tree.insert("", "end", values=task)

    except FileNotFoundError:
        pass


def add_task():
    new_window = Toplevel()

    Label(new_window, text="Task name: ").grid(row=0, column=0)
    entry_taskname = Entry(new_window)
    entry_taskname.grid(row=0, column=1)

    Label(new_window, text="Task type: ").grid(row=1, column=0)
    choices1 = ["Study", "Assignment", "exam", "personal", "other"]
    entry_tasktype = ttk.Combobox(
        new_window, values=choices1, state="readonly", width=17
    )
    entry_tasktype.set("Study")
    entry_tasktype.grid(row=1, column=1)

    Label(new_window, text="Task status: ").grid(row=2, column=0)
    choices = ["Completed", "Pending"]
    entry_taskstatus = ttk.Combobox(
        new_window, values=choices, state="readonly", width=17
    )
    entry_taskstatus.set("Pending")
    entry_taskstatus.grid(row=2, column=1)

    def save_task():
        taskname = entry_taskname.get()
        tasktype = entry_tasktype.get()
        taskstatus = entry_taskstatus.get()

        if taskstatus == "Completed":
            tree.insert(
                "", "end", values=(taskname, tasktype, taskstatus), tags=("completed",)
            )
        else:
            tree.insert("", "end", values=(taskname, tasktype, taskstatus))

        new_window.destroy()

    Button(new_window, text="save", font=("Arial", 10), command=save_task).grid(
        row=3, column=1
    )


def del_task():
    try:
        selected = tree.selection()
        tree.delete(selected)
    except Exception:
        pass


def delete_all():
    for item in tree.get_children():
        tree.delete(item)


def edit_task():
    try:
        item_id = tree.selection()[0]
        values = tree.item(item_id, "values")
    except IndexError:
        return

    new_window = Toplevel()

    Label(new_window, text="Task name:").grid(row=0, column=0)
    entry_taskname = Entry(new_window)
    entry_taskname.insert(0, values[0])
    entry_taskname.grid(row=0, column=1)

    Label(new_window, text="Task type:").grid(row=1, column=0)
    choices1 = ["Study", "Assignment", "exam", "personal", "other"]
    entry_tasktype = ttk.Combobox(
        new_window, values=choices1, state="readonly", width=17
    )
    entry_tasktype.set(values[1])
    entry_tasktype.grid(row=1, column=1)

    Label(new_window, text="Task status:").grid(row=2, column=0)
    choices = ["Completed", "Pending"]
    entry_taskstatus = ttk.Combobox(
        new_window, values=choices, state="readonly", width=17
    )
    entry_taskstatus.set(values[2])
    entry_taskstatus.grid(row=2, column=1)

    def save_task():
        if entry_taskstatus.get() == "Completed":
            tree.item(
                item_id,
                values=(
                    entry_taskname.get(),
                    entry_tasktype.get(),
                    entry_taskstatus.get(),
                ),
                tags=("completed",),
            )
        else:
            tree.item(
                item_id,
                values=(
                    entry_taskname.get(),
                    entry_tasktype.get(),
                    entry_taskstatus.get(),
                ),
                tags=(),
            )
        new_window.destroy()

    Button(new_window, text="Save", command=save_task).grid(row=3, column=1)


def upload_data():
    completed = 0
    data = tree.get_children()

    for i in data:
        values = tree.item(i, "values")
        if values[2] == "Completed":
            completed += 1

    total = len(data)
    if total == 0:
        efficiency = 0
    else:
        efficiency = (completed / total) * 100

    new_new_window = Toplevel()
    Label(
        new_new_window, text="Efficiency is: " + str(round(efficiency, 2)) + "%"
    ).pack(pady=5)

    def graph_upload():
        new_new_new_window = Toplevel()
        new_new_new_window.title("Select Date")

        Label(new_new_new_window, text="Select date:").pack(pady=5)

        cal = DateEntry(new_new_new_window, width=15, date_pattern="yyyy-mm-dd")
        cal.pack(pady=5)

        def save_efficiency():
            selected_date = cal.get()

            new_entry = {"date": selected_date, "efficiency": efficiency}

            data = []
            if os.path.exists("efficiency.json"):
                with open("efficiency.json", "r") as f:
                    data = json.load(f)

            for item in data:
                if item["date"] == selected_date:
                    item["efficiency"] = efficiency
                    break
            else:
                data.append(new_entry)

            with open("efficiency.json", "w") as f:
                json.dump(data, f, indent=4)

            new_new_new_window.destroy()

        Button(new_new_new_window, text="Save", command=save_efficiency).pack(pady=10)

    Button(new_new_window, text="Upload to graph", command=graph_upload).pack(pady=10)


def plot_graph():
    import matplotlib.pyplot as plt
    import numpy as np

    with open("efficiency.json", "r") as f:
        data = json.load(f)

    if not data:
        print("No data to plot")
        return

    dates = np.array([e["date"] for e in data])
    eff = np.array([e["efficiency"] for e in data])

    plt.figure()
    plt.plot(dates, eff)
    plt.title("Your Efficiency Data")
    plt.xlabel("Date")
    plt.ylabel("Efficiency (%)")
    plt.xticks(rotation=90)
    plt.tight_layout()

    plt.show()


window = Tk()
window.title("To Do List")

columns = ("task", "type", "status")

style = ttk.Style()
style.theme_use("clam")

tree = ttk.Treeview(window, columns=columns, show="headings", height=8)

style.map(
    "Treeview", background=[("selected", "#e6f2ff")], foreground=[("selected", "black")]
)

tree.heading("task", text="Task")
tree.heading("type", text="Type")
tree.heading("status", text="Status")

tree.grid(row=0, column=0, padx=10, pady=10)
tree.tag_configure("completed", background="#a3c585")

load_tasks_from_file()

frame = Frame(window)
frame.grid(row=0, column=3)

Button(frame, text="add task", font=("Arial", 10), width=20, command=add_task).pack()
Button(frame, text="delete task", font=("Arial", 10), width=20, command=del_task).pack()
Button(
    frame, text="Delete all", font=("Arial", 10), width=20, command=delete_all
).pack()
Button(frame, text="edit task", font=("Arial", 10), width=20, command=edit_task).pack()
Button(
    frame, text="upload data", font=("Arial", 10), width=20, command=upload_data
).pack()
Button(
    frame, text="plot graph", font=("Arial", 10), width=20, command=plot_graph
).pack()


def on_close():
    save_tasks_to_file()
    window.destroy()


window.protocol("WM_DELETE_WINDOW", on_close)
window.mainloop()
