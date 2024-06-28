# Structure

The basic building block of Malange is element. An
element can be divided into two types:
- Tag: An HTML element. Simple, right?
- Directive: A malange-exclusive feature that provides interactivity.
  - Long directive.
  - Short directive.

## Tag

Here, tag works a little differently. Especially on attributes.
Let's take a look at this example...

```malange
<!-- Traditional commenting system still works.-->

<h1>A simple element.</h1> # But Python commenting now works.

<h1>My name is: {name}</h1> # You can embbed a variable inside a tag.

# You can embbed a function too, even inside DOM event handlers.
<button on:click={check_name(event)}>Click me!</button>

# You can embbed a variable or a function or anything inside attributes.
<button style={check_name(event)}>Click me!</button>

# A function will always receive the event obj, which contains useful stuff.
# The event object will be explained later.

# You can use lambda function.
<button on:click={lambda event : check_name(event)}>Click me!</button>
```

The structure of a tag can be defined like this:

```malange
<element attr=attr_value eventdirective:eventname={handler}></element>
```

- element: The name of the element.
- attr: The attribute of the element.
- attr_value: The value of the attribute.
- eventdirective: Similar to Svelte directive.
- eventname: The name of the event, such as `click`.
- handler: A callable that receives event as its first default argument or keyword argument.

## Directive

A directive is a Malange-exclusive feature that can give some kind
of interactive functionality. Here are the examples:

```malange
# This is a directive.
[script]
    def change_property(event):
        event.target.innerText = "Yes"
[/script]

<h1>Do you love me?</h1>

<button on:click={change_property(event)}>Ask!</button>
```

Based on syntax, a directive can be divided into long and short directive.

A long directive is structured like this:

```malange
[directive]
    {subdirective} # Only needed for several directives.
[/directive]
```

A short directive is structured like this:

```malange
[directive :: ... /] # The three-dot is because it depends on what kind of directive.
```

Here are the list of directives:

### `[script]`

A script directive is the replacement for `<script>`
element. Unlike `<script>`, `[script]` requires
Python code. `[script]` also requires its code to be
indented.

```malange
[script]
    # This is ok.
# This is not ok.
[/script]
```

This directive can be one-liner, no indentation is required:

```malange
[script] ... [/script]
```

The short directive version:

```malange
[script :: code goes here /]
```

### `[match]`

Similar to Python 3.10 match and case. This is used for
conditional rendering. Providing default case is optional.
Here is how it works:

```malange
[script]
    # For the sake of simplification, let's assume the function returns 10.
    result = a_function()
[/script]

[match result]
{case 10}
    <h1>You are cool.</h1>
{case 9}
    <h1>You are not cool.</h1>
{case default} # We don't use underscores here.
    <h1>I don't know!</h1>
[/match]
```

The short directive version:

```malange
[match result :: 10: ... , 9: ... , default: ... /]
```

Tips: You can construct a ternary operator by using this directive.

```malange
[match result :: True: ... , False: ... /]
```

### `[cond]`

Similar to Python if-else. The plus of this directive
is that it allows you more flexibility on the conditioning.

```malange
[cond]
{case x < 10}
    ...
{case x < 10 and y == true}
    ...
{else}
    ...
[/cond]
```

The result is:

```html
<h1>You are cool.</h1>
```

The short directive version:

```malange
[cond x < 10: ... , x < 10 and y == true: ... , else: ... /]
```

### `[iterate]`

Similar to looping.

```malange
[script]
    variable = [1, 2, 3, 4]
[/script]

[each i in variable]
    <h1>Your score is: {i}</h1>
[/each]
```

The result:

```html
<h1>Your score is: 1</h1>
<h1>Your score is: 2</h1>
<h1>Your score is: 3</h1>
<h1>Your score is: 4</h1>
```

The short directive version:

```malange
[each i in variable :: <h1>Your score is: {i}</h1> /]
```
