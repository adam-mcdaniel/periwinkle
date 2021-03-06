# periwinkle
Language inspired by Python, Rust, and C++

Wouldn't you like a language with the expressiveness of Python, the beauty of Rust, and the power of C++?

I know I do :)


## Features

- Statically Compiled
- Dynamically Typed
- Object Oriented Programming
- Functional Programming
- Interoperability with C++ (with an easy FFI)

## Example

Here's an implementation of the Maybe type.

```fsharp
class Maybe {
    Just = (value) {
        self.value = value
        self.is_some = true

        return self
    }

    Nothing = () {
        self.value = @ // @ basically is Python's `None`
        self.is_some = false

        return self
    }

    __bool__ = () {
        return self.is_some
    }

    __str__ = () {
        if boolean(self) {
            return "Just " + str(self.value)
        }

        if not boolean(self) {
            return "Nothing"
        }
    }
}


// Demonstration of lambda
let Just = (x) => Maybe().Just(x)

let Nothing = Maybe().Nothing()

// Using the Maybe type
let five = Just(5)
putln(five)

let none = Nothing
putln(none)
```


## Get Started

```bash
```