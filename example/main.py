import tkinter as tk
import tks


def main():
    # Define a stylesheet and main window.
    stylesheet = tks.Stylesheet("./main.css")
    root = tks.Window("Test!", stylesheet)

    # Add some text.
    root.add(tk.Label, text="This is text!")
    root.add(tk.Label, text="This is some more text!")

    # Add a button and give it some functionality.
    btn = root.add(tk.Button, text="Click me!")
    btn.bind("<Button-1>", lambda _: print(btn.style))

    # Add a frame which contains a second button.
    frm = root.add(tk.Frame)

    btn2 = frm.add(tk.Button, text="Click me next!")
    btn2.bind(
        "<Button-1>",
        lambda _: (btn.configure(bg="var(--green)", text="Click me again!")),
    )

    # CSS variables work within the Element's configure method.
    btn2.configure(bg="var(--blue)", fg="#fff")

    root.mainloop()


if __name__ == "__main__":
    main()
