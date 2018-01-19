---
layout: post
title:  "Why use org mode to blog"
date:   2018-01-08 20:38:33 +0100
categories: blog org emacs
---

>### Update 2018-01-19:
>Improve writing

So as a huge fan of Emacs, I just had to use org-mode to write this blog.
Too bad this very post is written in plain old markdown.
Not a bad markup language by any means; but not my first choice.
My number one reason for using org-mode is the code block support.
This blog is going to be quite code heavy, and will include quite a few code snippets.
With org-mode, Emacs uses the correct daf-mode when editing snippets,
and the syntax highlighting written for it will _supposedly_ get exported as well.
  
  
#### So why am I not using org mode for this file?
The exporting proved difficult. I managed to set up automatic publishing from `org_mode/` to html,
but the `ox-html`-package insisted on surrounding my inline HTML with tags.
This meant Jekyll didn't have its three dashes `---` on line 1, and no metadata there was no layout.
Without a layout the page is just HTML styled like it's 1994, with a serif font and text aligned to the left edge of the browser window. The metadata meant for Jekyll was printed nicely between the org-inserted table of contents and said contents.

```
* TODO: Make an alternative static site generator
```
