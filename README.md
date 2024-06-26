# Malange

Malange is a framework that allows developers to write
Python code for the front-end. It is like Svelte, but is
not Svelte. Since Svelte transformed ```.svelte``` files
into HTML+JS files, Svelte is technically a compiler. But
Malange does it's way in a different manner. Malange only
allows for SSR, due to the limitation of Python.

```malange

<!-- This is not an element, but a directive -->
[script]

    # Print is still the same.
    print("Hello, world!")

    # There are: let, const, and bind.
    bind name: str        = "None"
    const list: list[str] = ["Anna", "Dave", "Rick", "John", "Tom"]
    let counter: int      = 0

    def change_the_name():
        name = list[counter]
        counter++

[/script]

<p>My name is: {name}</p>

<button on:click={change_the_name()}>Change the Name</button>

```
