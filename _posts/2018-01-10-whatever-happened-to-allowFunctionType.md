---
layout: post
title:  "Whatever happened to allowFunctionType()"
date:   2018-01-10 16:21:00 +0100
categories: old replaced thoughts
---

>### Update 2018-01-18: 
>General text improvements.
>I'm not a good writer, and only really write for myself on this blog. It shall serve as a time stamped archive of thoughts about language.
>My previous system consisted of text files forgotten in `Specs/probablyOutdated_2017_12_23/dafScratchpad`, until they eventually got banished to the depths of git.
>On this blog I'll get a bit more structure, and writing as if someone else is reading will hopefully allow myself to look back and understand what I was thinking.
>On that note, the text below is difficult to read for you and me both. No headings and a generally confusing flow.

I don't just want this blog to discuss language design. I also need a place to write down the past, present and future of the compiler.

Of all the lines written for the DafCompiler, very few remain. Most of it comes down to bad code getting replaced, but quite often I'll realize a well-implemented feature is better handled elsewhere.
The prime example of this is the `Expression.enableFunctionReturn()`-method. It would allow a given expression to have a Function type.
A function type is a unique type for every function defined in the language. A `FunctionCallExpression` would then use this type to get the `FunctionExpression` and call its LLVM prototype.
The problem is that not every expression wants a function type. If you give a function, it should be implicitly called to get its return type, if possible (no parameters).
So the default behavior for a `VariableExpression` referencing a def (a named FunctionExpression) was to take its implicit return type.
If the VariableExpression had been told `enableFunctionReturn()`, it would instead take the def's explicit type, i.e. the function's type.
  
The alternative came once type conversions were implemented.
Now, whenever you reference a function by name, that VaribaleExpression has the function type.
Any time you don't want a function type, you'll just use the normal type casting system to get the desired type.
You would have to try invoke casting either way, in case the implicit function return type had to be converted.
Take the following example:
```
def getI8 := 5i8;
def main() {
    mut x:i32=5;
	x += getI8();
	x += getI8;
};
```

The type of `getI8` here becomes `():i8`. In the first `+=`-operation, the function call expression takes this function type and calls it.
The resulting type of `getI8()` then becomes `i8`. When adding this to an `i32`, it is implicitly extended to 32 bits.
In the second `+=`-operation, the type of the right hand side is a function. That is however no match for the type caster.
The operation requires the right hand side to be `i32`, and thus, an `i32` is requested. The function type has no parameters, and can thus be implicitly evaluated to `i8`.
The type caster then recursively invokes itself, asking if an implicit conversion from `i8` to `i32` is possible, which it is.
When codegen comes along, the type caster will do the needed instructions to get from type A to B.

Now things get worse in the following example:
```
def main() {
    mut x := 6;
    def mut xRef := x;
    xRef = 4;
};
```

In this example, you have assignment. The type of the right hand side has to match the left, but it's not quite that easy.
The left hand side must also be a mutable expression. A function type isn't, but as you can see from its signature, `():mut i32`, it can implicitly be evaluated to one.
The problem is that you can't really cast this, because you don't have the target type.
What I'm doing now is checking if the left hand side is a function type. This check happens just before the assignment-operator complains that it's LHS isn't mutable.
  
Now this fix doesn't feel good. I'd like to use `isFunctionType()` as little as possible,
and rather have a general function that tries to turn a type into a target with a specific ValueKind or ConcreteTypeKind.
This would also be used in the numeric operators. They just know they add primitives.

This system can get a lot more complex once overloading arrives, but for now it's quite manageable.

