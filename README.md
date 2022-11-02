- [Documentation](https://piccoloser.github.io/tkx/)
- [Development Roadmap](https://github.com/piccoloser/tkx/wiki/Development-Roadmap)

# tkx (tkinter (e)xtension) *
tkx (pronounced "tics") is a GUI library built on top of tkinter with the intention of minimizing pain while setting up user interfaces. As it stands, tkx is *heavily* under development and it could be quite a while before it reaches maturity.

One of the first ideas in the conception of tkx was implementing support for CSS, the straightforward syntax of which would make styling tkinter widgets far less painful and verbose. This will also allow developers to separate visual styles from logic.

As it stands, tkx doesn't change much. Here are two code examples with identical output:

### Without tkx
```python
import tkinter as tk


def main():
    # Create a window.
    root = tk.Tk()
    root.title("Hello, World!")
    root.pack_propagate(0)

    # Add some text.
    tk.Label(root, text="This is some text.").pack()

    # Run the application.
    root.mainloop()


if __name__ == "__main__":
    main()
```
*Note: `root.pack_propagate(0)` is used to prevent the window from resizing to match the size of the `tk.Label` object. This is the default behavior in tkx, as shown below.*

### With tkx
```python
import tkinter as tk
import tkx


def main():
    # Create a window.
    root = tkx.Window("Hello, World!")

    # Add some text.
    root.add(tk.Label, text="This is some text.")

    # Run the application.
    root.mainloop()


if __name__ == "__main__":
    main()
```

On Windows systems, both programs above will output a window resembling the following:

![Standard tkinter window with bright background and black text](../media/images/before.jpg)

# CSS Stylesheets

All it takes to style elements with tkx is a CSS file and a `Stylesheet` object. Consider the following code:

```python
import tkinter as tk
import tkx


def main():
    # Define a stylesheet and main window.
    stylesheet = tkx.Stylesheet("./main.css")
    root = tkx.Window("Test!", stylesheet)

    # Add a button and give it some functionality.
    btn = root.add(tk.Button, text="Click me!")
    btn.bind("<Button-1>", lambda _: print("Hello, World!"))

    # Add some text.
    root.add(tk.Label, text="This is text!")
    root.add(tk.Label, text="This is some more text!")

    root.mainloop()


if __name__ == "__main__":
    main()

```

And the following CSS stylesheet:

```css
/* main.css */

:root {
    --bg: #333;
    --fg: #ddd;
    --blue: #0ac;
}

Window {
    background: var(--bg);
    width: 300;
    height: 120;
}

Button {
    background: var(--blue);
    border-style: flat;
    color: black;
}

Label {
    background: var(--bg);
    border-style: flat;
    border-width: 2;
    color: var(--fg);
}
```

The above code outputs the following:

![Dark gray window with a blue button and white text](../media/images/after.jpg)

<sup>* Name is subject to change.</sup>
