---
layout: post
title:  "The aforementioned 'with'-research file"
date:   2018-03-22 16:21:00 +0100
categories: with class trait type definition
---

`with` is both an expression and a definition in daf. They allow for scoped modifications to a type, or temporary casting.
It will also allow for manually setting uncertain-states of variables.
The third use is a pseudo-operator between types. That is the case we will look at first.

#### Inheritance thorough `with`
Basic inheritance is done in the following way:
```
typedef SuperClass := class {
    pub field:i32;
};

typedef BaseClass := class with SuperClass {
    pub anotherField:i32;
}
```
In the example given, `BaseClass` inherits the aptly named `field` from `SuperClass`, and as such, any method requiring the latter can be given an instance of the first instead.
Basically, there now exists an implicit type conversion from `BaseClass` to `SuperClass`.
All functions defined in the super class are also accessible through the base class.
If any of these functions were virtual, one could override them, and get the new behavior even in code that knows nothing of our base class.
  
#### Modifying types using `with`
In daf, you can modify any type in a given scope.
It has its limitations, as you can't change the size of variables on the fly, but all other transformations are allowed.
In the following example, `i32`s get an implementation of Comparable:
```
with :i32 as Comparable with {
    pub def smallerThan(a:i32, b:i32):=a<b;
};
```
This definition uses a `with` operator between the two types `Comparable` and the implementation of Comparable for `ì32`s.
The resulting type is a new trait which an `i32` can be converted to implicitly without issue.
I still have to find rules for what the resulting type is when `with`ing together traits and classes, but then again, I haven't really decided how the differences work, yet.

Please read the future research post about "class, trait, This and Impl".
There are a lot of nuances surrounding `this` is methods. Is it a pointer, a reference, what about when you implement methods in traits?
