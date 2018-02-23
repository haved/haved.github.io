---
layout: post
title:  "The Grand ConcreteType Plan"
date:   2018-02-23 23:59:59 +0100
categories: daf compiler ConcreteType FunctionExpression
---

So the FunctionExpression refactor went great, and the code is more readable and makes way more sense than before.
It is now close to obvious that a ConcreteType is unique, letting us get away with using `==` on the pointers.
Since last time I've also moved most of TypeConversion.cpp into virtual methods in the ConcreteType classes themselves. This looks way better, especially now that ConcreteType got its own separate files from Type. I have yet to move the `getPossibleConversion()` function, which is going to be just as important in the coming weeks.
  
  
This grand plan allows lots of tiny pieces of code elsewhere be removed, in favor of type conversion.
It's probably best explained through an example, so lets look at the method that gave me these ideas originally:
```
bool FunctionExpression::canBeCalledImplicitlyOnce() {
	return getParameters().empty();
}
```
In daf, a function that doesn't take any parameters can be called implicitly.
This method tells you just this. The reason it's suffixed with "Once" is that the result type
of this function may be another function, which then may or may not be possible to call implicitly.
This method is used several places, also outside of the FunctionExpression class.
One such place is in FunctionCallExpression, which will when given the wrong amount of arguments for
a function, ask the function if it perhaps has zero arguments but returns another function.
This then goes recursively down until the function has the right amount of arguments,
or it has the wrong amount, but not zero either. That is when `canBeCalledImplicitlyOnce()` is false.
  
  
I don't like this code use very much. I'd much rather have `canBeCalledImplicitlyOnce()` be private.
That is also the plan. The grand plan.  
The idea is to have the FunctionCallExpression ask its target for a ConcreteType it can be converted to
that supports the parameters it has. The FunctionExpression will then see that it doesn't take parameters,
but can therefore ask its return type, if it can handle the parameters.
Thus, the information about what can and can't be evaluated never leaves the class.
  
There is also a field in the FunctionExpression I'd like to remove completely.
`m_implicitCallReturnTypeInfo` in an optional that contains the return type you'd get
if you implicitly called every function all the way down to some other type, if possible.
Each FunctionExpression with 0 parameters (aka. `canBeCalledImplicitlyOnce()` is true),
checks if its returnType is a function, and in which case copies its `m_implicitCallReturnTypeInfo`.
If the return type is something other than a function, you've arrived at your goal,
and if you have parameters, you don't have an `m_implicitCallReturnTypeInfo`.
This field is used when you define a let with a function as its assignment.
The let can't have a function type, and will thus use the implicitCallReturnTypeInfo,
which it gets from a special function written in the TypeConversion.cpp file.
  
Ideally I'd want to just ask the expression side of a `let` for a Type that isn't a Function.
Again, the implicitCallReturnTypeInfo never has to leave the FunctionExpression, and the code becomes less entangled.
  
The final obvious benefit with the "what type can you convert to that fits these criteria"-system is overloading.
If a def has multiple definitions, just make a type for the combination,
and whenever someone requires one of the types, give them that type.
The signature of this function might not be pretty, but the rest of the code base should reap benefits.
