---
layout: post
title:  "Doing trait implementation thorugh virtual methods or using templates"
date:   2018-03-22 16:21:00 +0100
categories: virtual polymorphism OOP override class trait
---

The syntax in this post is not final. All code is used to discuss trait ideas.
The basic idea is that implementing a trait can be done in at least three ways.
In both cases you end up with a class that has the required behavior,
but how you then have to use this class is different.
Using polymorphism with virtual methods and dynamic dispatch, you can make a generic pointer to the trait, and invoke functionality from the implementation.
This requires the object to have a vtable, which a) can't be done after the class definition, and b) introduces pointer de-referencing.
  
There is a simple fix for problem a). By introducing a fat pointer containing both the object pointer and a vtable pointer, the vtable can be added in post.
However, this doesn't allow dynamic dispatch inside the methods already defined in the object.
  
Third option, which avoids all dynamic dispatch, is simply to use templates to re-compile every use of the trait for every implementation.
You no longer have the ability to make generic trait-pointers, but you also get predictable run-time behavior, as if there was no trait.
  
So, question is: When do you do which, and what is the daf-syntax for each?
Below is a sketch of how this all might work.

```
typedef Entity := trait {
    prot x, y:f32=0;
	pub def update;
};

typedef CrateEntity := class with Entity {
    xSpeed, ySpeed:f32=0;
	pub def update() {
	    x+=xSpeed;
		y+=ySpeed;
	};
};

typedef VEntity := virt Entity; //Makes all functions virtual in the class, introducing a vtable
typedef VCreateEntity := class with CreateEntity with VEntity; //New class filling VEntity's vtable

def main() {
    mut world := Vec(&mut VEntity);
	for range(40)
	    world.append(new(VCreateEntity{3, 5, 2, 7}));
    for world
	    it.update();
}
```

I'd recommend reading the `with`-research-file which at a later date will finalize the inheritance syntax.

