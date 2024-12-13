# Malange Syntax

Malange is supposed to be a template language that is
not just powerful as a template language, but can act
like a front-end template language, e.g. Svelte.

The goal of Malange is:
- The ability to use Javascript and Python APIs.
- Can use static files.
- Template system in a simple manner.
- Simple and easy-to-understand syntax.

## Injection

Malange, just like Svelte, supports the injection of
variables from the script to the HTML.

```malange
[/script:::
name = "Davy Jones"
/]

<p>Hello there, my name is {name}</p>

```

You use the curly braces to inject variables.

----

Injecting return value of a function is also supported.

```malange
[/script:::
def return_something():
    return "Davy Jones"
/]

<!-- You must call the function. -->
<p>Hello there, my name is {return_something()}</p>
```

Note that Malange can provide the `event` object (for event management),
you need to provide a dollar sign before injection for `event` to be delivered.

```malange
<p>Hello there, my name is ${return_something(event)}
```

##  Reactivity

To support reactivity (e.g. Svelte reactivity), you use the dollar sign. Any changes
in the variable will be updated automatically. To use it, you must append the sign to
the beginning of the variable during declaration only.

```malange
[/script:::

$data = "1 + 2 + 3"
increment = 3

def add_number():
    data += f"{increment+1}"
/]

<p>{data}</p>

<button on:click={add_number}>Add number</button>
```

So if the button is clicked, the paragraph element will
automatically update. Simple, right?

----

And yes, this also applies to function.

## Binding

A way to represent a HTML element is through binding.

```malange
[/script:::
something variable_name.x
/]

<element bind:{variable_name}></element>
```

## Listener

Malange provides 'browser' library that can be imported,
this allows you an access to the Document interface.

```malange
[/script:::
# Root represents the entire element of the file.
from browser import root

def do_something():
    ...

root.on_load(do_something())
/]
```

## Block

Block is another feature of Malange that allows you to render
the HTML elements in a 'more flexible' way.

```malange
[/script:::
from my_custom_library import get_score

exam_result = get_score(class='xi-a', exam='mid-semester-exam',
    lesson='social-studies', retry=false)
]

[/for (name, score) in exam_result
<p>{name}, your score is {score}.</p>
/]
```

The block started with the `[/`, folllowed by the block type, then the attribute
(e.g. `(name, score) in exam_result`) plus ':::', followed by the HTML content, then after that
it ends with `/]` sign. This particular block will loop over `exam_result` to inject
`name` and `score` to a paragraph element, then it will render each paragraph element.
If `exam_result` length is 10 items, there will be ten `<p>` elements.

Note that it is not possible to declare a block within a block.

There are several types of block:

----

*SCRIPT BLOCK:*

Script block is used to inject Python code. All contents inside
the script block will be treated as Python code.

```malange
[/script:::

contents (if src argument is provided, the content will be ignored)

/]
```

Several attributes exist:

```malange
[/script backend=(plot, data):::
...
/]
```

The backend attribute allows you to access exported modules
from the backend with ease.

And if you want to seperate the script, you can do this:

```malange
[/script src=/path/to/the/script.py backend=(plot, data):::/]
```

----

*FOR BLOCK:*

This is useful for rendering multiple items whose data is sourced
from a list or a dictionary.

```malange
[/for i in a_list:::
    <p>{i}</p> # variable i is only available within this block.
/]
```

----

*SWITCH BLOCK:*

Switch block is useful for conditional rendering.

```malange
[/switch i:::

[/case 0:::
    a
/]

[/case 1:::
    b
/]

[/case::: <!--For "else" condition.-->
    c
/]

/]
```

----

*IF BLOCK:*

Similar to switch block.

```malange
[/if i < j:::
    a
[/elif i == j:::
    b
/]
[/else:::
    c
/]
/]
```

## Backend

Accessing Python libraries in the backend is difficult due to
some libraries being able to work only on the backend (e.g. `sys`).
And as such, the only available library is the needed library for
frontend. For the rest, it has to be done by sending the data to
the backend.

Let's say you want to render a matplotlib into a HTML canvas element.

The normal process will goes like this:
- Store the plotted data into a variable.
- The frontend will fetch that variable from the backend.
- The frontend will render the variable into the canvas.

In Malange, it is much simpler.
- Plot and store the data in the backend through a Python file.
- Include the module containing the data in Malange file.
- Render.

```python
import matplotlib.pyplot as plt
from malange.api.backend import Manager

manager = Manager(name='python_file')

def create_plot(data):
    # Create a plot.
    plt.figure()
    plt.plot(data)
    plt.title("A Plot")

    # Save the plot to a variable.
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Encode and return.
    return base64.b64encode(buf.getvalue()).decode('utf-8')

# Use the function to create the image data.
data = [1, 2, 3, 4, 5]
image_data = create_plot(data)

# Export the image data.
manager.export_module(image_data)
```

Then on Malange:

```malange
[/script:::
include python_file

from malange import on_load
from browser import Image

base64Image = python_file.image; // The Base64 string

img = Image();

img.src = `data:image/png;base64,${base64Image}`;

img.on_load(render_canvas);

def render_canvas():
    const ctx = canvas.getContext('2d');
    canvas.width = img.width;
    canvas.height = img.height;
    ctx.drawImage(img, 0, 0);

/]

<canvas bind:{canvas}></canvas>

```

## Structure

Malange will be divided into several components:
- Lexer: Which will process Malange file into tokens.
- Parser: Tokens will be organized into AST.
- Scanner: Syntax errors will be checked.
- Optimizer: Redundant elements will be removed.
- Structurer: The now clean AST will be converted into JS code.
- Loader: Backend modules will be loaded.
- Executor: The JS Code will be served, while the backend is ready for service.

