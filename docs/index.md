# tks (tkinter superset) *
## Disclaimers
* This project was written in Python version 3.10 and has yet to be tested with earlier versions of the language.
* Developers using WSL may encounter issues stemming from their `DISPLAY` environment variable. The author has yet to find a solution to this problem.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Example Project](#example-project)
3. [Documentation](#documentation)

# Getting Started
### Installation
First, make sure you have a compatible version of Python installed along with tkinter. The author also recommends using a virtual environment when following this guide.

Run the following command:
```
python -m pip install git+https://github.com/piccoloser/tks.git
```

If you don't get any errors, tks should be successfully installed.

# Example project
*This section will disregard comparisons to tkinter's syntax in favor of being concise.*

Let's create a project folder and within it add a new Python file called `main.py`, then paste the following code.
```python
# main.py

import tkinter as tk
import tks


def main():
    root = tks.Window("My Application")
    root.mainloop()


if __name__ == "__main__":
    main()

```

Running this script will open the following window:

![Basic tks Window](./images/gs_window.jpg)

To add a new text label to this window, we'll use the `add` method **before** `root.mainloop()`.

```python
# main.py
# ...

root = tks.Window("My Application")

root.add(tk.Label, text="This is some text!")

root.mainloop()

# ...
```

Now the window should display some text.

![Basic tks Window with text label](./images/gs_window_label.jpg)

A major feature of tks is the ability to style widgets with Cascading Style Sheets (CSS), a language used heavily in the world of web design for the purpose of describing how HTML elements look.

Let's create another file in our project folder and name it `style.css`. In this file, paste the following:

```css
Window {
    background: black;
    width: 300;
    height: 120;
}

Label {
    background: black;
    color: white;
}
```

Now in `main.py`, **above** where we defined our window, we'll add a line for the stylesheet, and pass it to `root` as an argument:

```python
# main.py
# ...

stylesheet = tks.Stylesheet("./style.css")
root = tks.Window("My Application", stylesheet)

# ...
```

The window should now appear with a black background and white text.

![Basic styled tks window.](./images/gs_window_styled.jpg)

We use a relative path `./style.css` to refer to our new CSS file. This path is validated using `pathlib` and the file contents are automatically parsed into usable Python code as soon as we create the `tks.Stylesheet`.

Next, let's change the color of our text when the user clicks a button. First, we'll add the button itself...

```python
# main.py
# ...

root.add(tk.Label, text="This is some text!")

my_button = root.add(tk.Button, text="Click me!")

# ...
```

*Notice how in order to reference our element (in this case, a button) we need only assign it to a variable.*

Then, we'll assign our label to a variable so it can be referenced in our function...

```python
# main.py
# ...

my_label = root.add(tk.Label, text="This is some text!")

# ...
```

Then, we'll add the actual functionality to our button. Here's the full code snippet:

```python
import tkinter as tk
import tks


def change_color(label, color):
    """Change the foreground (fg) color of a given label."""
    label.configure(fg=color)


def main():
    stylesheet = tks.Stylesheet("./style.css")
    root = tks.Window("My Application", stylesheet)

    my_label = root.add(tk.Label, text="This is some text!")

    root.add(
        tk.Button,
        text="Click me!",
        command=lambda: change_color(my_label, "cyan"),
    )

    root.mainloop()
    

if __name__ == "__main__":
    main()

```

*Explaining the use of `lambda` in the declaration of our button is beyond the scope of this guide. Please refer to this [W3Schools](https://www.w3schools.com/python/python_lambda.asp) page for more details about lambda functions.*

Here's what the result looks like:

![Styled tks window with button](./images/gs_window_button.jpg)

Great! Clicking this button will change the color of our text from white to cyan. Now let's add some styling to the button:

```css
/* main.css */
/* ... */

Button {
    background: blue;
    color: white;
    border-style: flat /* tkinter equivalent of "solid" */
}

/* ... */
```

Now you'll see that the button is blue with white text and a solid border.

![Styled tks window with button](./images/gs_window_button_styled.jpg)

Before wrapping up this guide, we can reduce repetition in our CSS by using variables. In CSS, variables are defined using a selector called `:root` and referenced using the `var()` function.

Update your CSS such that it matches the following:

```css
/* CSS variables must begin with double hyphens. */
:root {
    --background: #000; /* You can use hex values as well. */
    --foreground: #fff;
    --blue: #00f;
}

Window {
    background: var(--background);
    width: 300;
    height: 120;
}

Button {
    background: var(--blue);
    color: var(--foreground);
    border-style: flat;
}

Label {
    background: var(--background);
    color: var(--foreground);
}
```

*Running the program after making these changes will display the exact same window.*

This way, we can update items that share those variables without having to change each and every one of them.

**Congratulations**, you've created your first program using tks!

# Documentation

## Classes
### ClassList
The `ClassList` class is a custom collection which contains CSS class names and objects to which those classes are assigned. String-indexing into this class returns a `set[`[`Element`](#element)`]`.

#### `ClassList` Attributes
* **`classes`** &mdash; `dict[str, set[Element]]` containing class names and a `set` of the Elements to which each class is assigned.

### Element
*Implements [`@tks_element`](#tks_element)*

The `Element` class is a wrapper around a tkinter widget, and should be created indirectly via its parent's `add` method (see: [@tks_element](#tks_element)). The root of the hierarchy should be a [`Window`](#window).

#### `Element` Attributes
* **`elements`** &mdash; List of `Elements` contained within this object.
* **`parent`** &mdash; The `Element` or `Window` which contains this object.
* **`style`** &mdash; This `Element`'s style as a `dict[str, str]` or `None` if it does not exist.
* **`widget`** &mdash; The tkinter `Widget` that this `Element` wraps.

##### **Not Fully Implemented**
* **`cl`** &mdash; Describes the element's CSS `class`, which can be used in a stylesheet to target that element and others with the same class.
    * **Important:** `class` is a restricted keyword in Python which cannot and should not be used outside the context of creating a Python class. `cl` is the only accepted word for this property.
    * As of writing, only **one** class can be assigned to an element.
    * As of writing, elements with both `cl` and `id` will only be styled according to their `id` attribute.
* **`id`** &mdash; Describes the element's `id`, which can be used in a stylesheet to target that specific element.

#### `Element` Methods
* **`bind()`** &mdash; This method directly wraps the `bind` method of this `Element`'s widget. See the [tkinter](https://tkdocs.com/shipman/binding-levels.html) and [Tkl/Tk](https://www.tcl.tk/man/tcl8.6/TkCmd/bind.html) documentation for more information on the `bind` method.
* **`configure()`** &mdash; This method handles keyword arguments specific to `Element`, then passes the rest directly to the `configure` method of the `Element`'s widget. See the [tkinter](https://tkdocs.com/shipman/std-attrs.html) documentation for the standard attributes which can be applied using the `configure` method.

### Stylesheet
The `Stylesheet` class is a CSS parser and container for parsed styles. A `Stylesheet` can be passed to a [`Window`](#window) in order to apply styles to it and its child elements.

#### `Stylesheet` Attributes
* **`styles`** &mdash; A `dict[str, dict[str, str]]` of the style values read from a CSS file.
* **`source_min`** &mdash; The minified CSS source code of this object.

#### `Stylesheet` Methods
* **`format_properties`** &mdash; Replaces all values matching CSS variables (eg. `var(--my-variable)`) with their corresponding values in the CSS `:root` block.
* **`get`** &mdash; Returns the CSS block associated with the given selector or `None` if it does not exist.
* **`get_blocks`** &mdash; Returns a list of CSS blocks as defined in the CSS source code.
* **`get_property`** &mdash; Returns the value of a property given a selector and property name. If not found, this method returns `None`.
* **`get_selectors`** &mdash; Returns a list of CSS selectors as defined in the CSS source code.
* **`minify_css`** &mdash; Given the contents of a CSS file as a string, returns the contents with unnecessary spaces and comments removed.
* **`parse_blocks`** &mdash; Returns a minified CSS block as a `dict[str, str]`, where CSS key names have been translated to tkinter-supported key names.
* **`var`** &mdash; If a value matches the syntax of a CSS variable (eg. `var(--my-variable)`), returns the associated value from the CSS stylesheet's `:root`, otherwise returns the unchanged value.

### Window
*Implements [`@tks_element`](#tks_element)*

The `Window` class is a subclass of tkinter's `Tk` widget. The only visual change from tkinter's default behavior is that `self.pack_propagate(0)` is called on instantiation.

#### Creating a `Window`
Optional title `str` and `Stylesheet` arguments can be passed directly to the `Window.__init__` method, making the creation of a titled window with an applied stylesheet a one-liner. The `width`, `height`, `x`, and `y` attributes are also automatically recalculated and ready for use once the object has been instantiated.

If a stylesheet has not been passed to the `__init__` method, `self.style` will be equal to `None`.

#### Window Attributes
* **`cls`** &mdash; `ClassList` containing every CSS class used by this object's child elements (automatically populated).
* **`elements`** &mdash; List of `Elements` contained within this object.
* **`ids`** &mdash; `dict[str, Element]` mapping CSS ids to their respective `Element` within this object's child elements.
* **`stylesheet`** &mdash; The `stylesheet` passed to this object during instantiation.
* **`style`** &mdash; This `Element`'s style as a `dict[str, str]` or `None` if it does not exist.

## Decorators

### `@tks_element`
*Class Decorator*

This decorator applies functionality relevant to tks elements.

#### Implemented By
* [`Element`](#element)
* [`Window`](#window)

#### Introduced Methods
* **`add()`** &mdash; Creates a new `Element` containing the specified widget with `self` as the `Element`'s parent. Also appends the new object to `self.elements`.
* **`get_style_of`** &mdash; Returns the style of a widget which has been defined in a stylesheet, given the widget name (eg. `tk.Frame.__name__ -> "Frame"`), or optionally the style of another `fallback` widget.
* **`parent()`** &mdash; Returns the element's container. If the element is a `Window`, this method returns `self`.

#### Introduced Properties
* **`root`** &mdash; Returns the root `Window`.

### `@update_style`
*Function Decorator*

This decorator extends the `configure` method of objects implementing [`@tks_element`](#tks_element).

Methods extended by this decorator will have their argument values parsed as CSS properties *into* valid tkinter values. Already valid values will be unchanged, whereas values containing CSS-specific syntax will be translated.

#### Functionality
* CSS Variables (depends on an associated `Stylesheet`)
* Percent Values (depends on the same values in the object's parent)

#### Implemented By
* [`Element`](#element)`.configure`
* [`Window`](#window)`.configure`