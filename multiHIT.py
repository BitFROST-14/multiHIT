from tkinter import *
from tkinter import ttk
import requests

def fetchStatus():
    urls = inputUrl.get("1.0", END).strip().split("\n")

    for row in tree.get_children():
        tree.delete(row)

    for url in urls:
        url = url.strip()
        if not url:
            continue

        print(f"Checking URL: {url}")
        try:
            response = requests.get(url)
            status = "SUCCESSFUL" if response.status_code == 200 else "ERROR"
            short_response = response.text[:100] + ("..." if len(response.text) > 100 else "")
            tree.insert("", "end", values=(url, status, short_response, response.text))

        except requests.exceptions.RequestException as e:
            tree.insert("", "end", values=(url, "FAILURE", "Error occurred", str(e)))

def show_full_response(event):
    selected_item = tree.selection()
    if selected_item:
        item = tree.item(selected_item)
        full_response = item['values'][3]  

        # Show in a new popup
        popup = Toplevel(main)
        popup.title("Full Response")
        popup.geometry("600x400")

        text_area = Text(popup, wrap="word", height=20, width=70)
        text_area.insert(END, full_response)
        text_area.config(state=DISABLED)
        text_area.pack(expand=True, fill=BOTH)

        close_btn = Button(popup, text="Close", command=popup.destroy)
        close_btn.pack(pady=5)

# Main Window
main = Tk()
main.title("multiHIT")
main.geometry("900x500")

Label(main, text="Enter URLs (one per line):").pack(pady=5)
inputUrl = Text(main, height=5, width=80, wrap="word")
inputUrl.pack()

Button(main, text="Fetch Response", command=fetchStatus).pack(pady=5)

columns = ("URL", "Status", "Short Response", "Full Response")
tree = ttk.Treeview(main, columns=columns, show="headings", height=10)
tree.heading("URL", text="URL", anchor="w")
tree.heading("Status", text="Status", anchor="w")
tree.heading("Short Response", text="Short Response", anchor="w")


tree.column("Full Response", width=0, stretch=NO)


scroll_y = Scrollbar(main, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scroll_y.set)
scroll_y.pack(side=RIGHT, fill=Y)

tree.pack(expand=True, fill=BOTH, padx=10, pady=10)

tree.bind("<Double-1>", show_full_response)
Label(main, text="Made with \u2665 \n ㅇㅅㅇ BitFROST-14").pack(pady=5)
main.mainloop()
