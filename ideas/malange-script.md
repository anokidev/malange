# Malange Script

Malange Script is the slightly modified version
of Python. It added a few features.

## Reactive Variables

For variables, you can add the dollar sign to the start
of your variable name to make the variable reactive. That is
if the variable is updated the elements that are affected by it
will be re-rendered respectively, thus reactive.

```malange
[script]
    $reactive_variable = 1
[/script]

<p>The number is: {$reactive_variable}</p>

<button on:click={lambda : reactive_variable += 1}>Increment!</button>
```

## Importing `.py` Files

Importing Python files still works. However, there is a mechanism
on how Malange works. First, the `.mala` file will be compiled
to a Python file, linked, and then executed to generate a JS code.
So for example if you asked a library to generate the data, you need
to capture the steam of that data to make it available on the frontend.
You can't for example execute `matplotlib` function in the frontend,
you have to execute the function on the backend, capture the stream, and
then send the stream to the frontend.

For example, let's see this `.mala` code
from file `./home/+page.mala`:

```malange
[script]
    include content.a as A
    $reactive_variable = 1
    list_of_things = ["Apple", "Banana", "Chocolate"]
[/script]

<p>The number is: {$reactive_variable}</p>

<button on:click={lambda : reactive_variable += 1}>Increment!</button>

[each i in list_of_things :: <h1>Your food is: {i}</h1>]

<A>
```

This code will be roughly translated to:

```python
class Home_pluspage(MalangeFileTemplate):
    def __main__(self):
        self._define_element_direc(
            name="script",
            instruct=[
                self._script_include(src="content.a", alias="A"),
                self._define_variable(
                    name="$reactive_variable", datatype=int, value="1", reactive=True),
                self._define_variable(
                    name="list_of_things",
                    datatype=list[str],
                    value=["Apple", "Banana", "Chocolate"]
                )
            ]
        )
        self._define_element_tag(
            name="p",
            attribute={},
            content="The number is: {$reactive_variable}"
        )
        self._define_element_tag(
            name="button",
            attribute={
                "on:click" : "{lambda : reactive_variable += 1}"
            },
            content="Increment!"
        )
        self._define_element_tag(
            name="A",
            attribute={},
            content=None
        )
```

## Including `.mala` Files

For importing `.mala` files, use the word `include` instead of `import`.

Let's import the file `./content/a.mala`:

```malange
[script]
    # the malange module name must be the same as the file name.
    include content.a
[/script]

<content.a> # This is how you include a .mala file.
```

There are several alternatives:

```malange
[script]
    include content.a as A
    from content include a
    from content include a as A
[/script]
```

## Python features?

One thing that you might asked is how about several
features that are available on certain Python versions.
That's why Malange needs to be configured first.
