import tkinter as tk
import tks


def main():
    # Define a stylesheet and main window.
    stylesheet = tks.Stylesheet("./main.css")
    root = tks.Window("Test!", stylesheet)

    # Add a button and give it some functionality.
    btn = root.add(tk.Button, text="Click me!")
    btn.bind("<Button-1>", lambda _: print("Hello, World!"))

    # Add some text.
    root.add(tk.Label, text="This is text!")
    root.add(tk.Label, text="This is some more text!")

    root.mainloop()


if __name__ == "__main__":
    main()

import tkinter as tk
import tks


# def main():
#     # Create a window.
#     stylesheet = tks.Stylesheet("./main.css")
#     root = tks.Window("Hello World", stylesheet)

#     # Add some text.
#     root.add(tk.Label, text="This is some text.")

#     # Run the application.
#     root.mainloop()


# if __name__ == "__main__":
#     main()
