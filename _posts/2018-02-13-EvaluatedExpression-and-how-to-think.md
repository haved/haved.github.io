---
layout: post
title:  "EvaluatedExpression and how to think"
date:   2018-02-13 21:38:33 +0100
categories: daf compiler EvaluatedExpression expression
---

So today I was adding the llvm code generation for the pointer operator, while on a trip in Vienna.
The programming conditions weren't ideal, but the code would be straight-forward enough to allow a few casual minutes of coding.
At least so I thought, until I got stuck looking for an llvm instruction for getting the pointer to a value.
Anyone who knows llvm knows this is impossible (or I've really misunderstood something).
The compiler itself is also not designed to require such an instruction.
The operand of the "pointer-to"-operator is evaluated to an EvaluatedExpression, and type conversion is used to get an lvalue.
When you then have some lvalue as an EvaluatedExpression, the llvm::Value* in the class _is_ a pointer.
This is the case whenever an EvaluatedExpression comes from an Expression with a reference ValueKind (LVALUE or MUT_LVALUE).
When you then require the value, EvaluatedExpression::getValue() will load the pointer its llvm::Value* contains.
  
The EvaluatedExpression contains a pointer to its ExprTypeInfo. This is often gotten from a reference, which is very iffy.
If you ever make a temporary ExprTypeInfo and use it for an EvaluatedExpression, you'll end up with a garbage pointer.
One possible fix is to check a given pointer if it looks like a heap pointer, the thought of which makes me ill, as well as sounding super un-portable.
Another alternative is having the EvaluatedExpression take a pointer to its expression. It doesn't have to store it, but it makes sense,
seeing as the EvaluatedExpression is just an Evaluated Expression. An llvm::Value* and an Expression*.
These Expression pointers currently feel very stable and predictable, and the ExprTypeInfo reference you receive from it should be just as safe, as it is a field in the Expression.
It still feels very C++ and bad, though I don't have a better alternative in daf. The only daf-positive thing I can say is that a redesign to a better system would be easier to pull of.
