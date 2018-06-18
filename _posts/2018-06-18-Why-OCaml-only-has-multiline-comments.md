---
layout: post
title:  "Why OCaml only having (* *)-comments makes sense"
date:   2018-06-18 14:00:00 +0100
categories: compiler daf ocaml lexing
---

Out of all comment syntaxes invented there are ultimatly two that stand out.
```C
// C++ Line comment

/* C-style
   comment */
```
These have stood the test of time, being brought from language to language over half a decade. However, this does not mean they are concidered good.
The C-style comment is present in languages like rust, but the rust book never mentions it, citing it as non-ideomatic when asked[^1].
The reason is quite obvious to anyone who has ever tried to comment out a block of code.
Doing so should be as easy as prefixing with `/*` and suffixing with `*/`, right?

### Comments already in your block
If the block already contains C-style comments you can't span a comment over it.
```C
/*
int add(int a, int b) {
    /* Overflow */
    return a+b;
}
*/
```

The outer comment only goes as far as the first `*/`, which in this case is in the middle of the block.
You're left with unbalanced curly brackets and pain.

### Layered comments
The obvious solution for a language designer is to start counting layers of comments.
```C
/* /* layer2 */ layer1 /* /* layer3 */ */ */
```

This lets us keep C-style comments but still safely comment out blocks, right?
Well no...

### Even with layers
Take the following code:
```C
int cards = 4 */* hey */*my_ptr
```

God help you if you comment your code like this, but we desire fool-proof block comments.
If you were to comment this line out with C-style comments, even with layered comments, What would happen?
```C
/*
int cards = 4 */* hey */*my_ptr
*/
```

We have two instances of `*/*`, used to act as a comment start and comment end, but even with a layered comment parser, they would both switch roles when commented out.
The solution to this? Make `*/*` not affect the layer count perhaps?
Nope, the last `*/*` could have been just `*/`, which would require the first ambiguous one to increment the layer count,
conversly, if the first `*/*` turned into `/*`, the second would have to decrement the layer count.

### How do you idiomatically comment out multiple lines?
The consensus seems to be using an IDE to prefix every line with `//`.
If there was a comment there already, the resulting `////` will still work even if you un-comment the inner block before the outer.
This makes you quite dependant on IDE support, though, or spamming an emacs macro.
The extra effort might make me actaully banish old code to the depths of VC where it belongs,
but friction based refactoring is not a goal of mine.

## How about in OCaml?
OCaml doesn't have line comments. The ideomatic (and only) way to comment out a block of code is to use a `(*  *)`-comment.
It might look like it harbours all the problems of the C-syntax comment, but it does not.
OCaml is a thoroughly designed language, and it of course supports layering comments within eachother.
You avoid the `*/*` ambiguity because the start and end-blocks use different chars.

[^1]: [Issue from rust book GitHub repository](https://github.com/rust-lang/book/issues/693)
