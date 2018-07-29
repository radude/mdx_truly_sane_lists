# Mdx Truly Sane Lists

[![Build Status](https://travis-ci.org/radude/mdx_truly_sane_lists.svg?branch=master)](https://travis-ci.org/radude/mdx_truly_sane_lists)


An extension for [Python-Markdown](https://github.com/Python-Markdown/markdown) that makes lists truly sane. Features custom indents for nested lists and fix for messy linebreaks and paragraphs between lists.


## Features

* `nested_indent` option: Custom indent for nested lists. Defaults to `2`. Doesn't mess with code indents, which is still 4. 

* `truly_sane` option: Makes linebreaks and paragraphs in lists behave as usually expected by user. No longer adds weird `p`, no extra linebreaks, no longer fuses lists together when they shouldn't be fused (see screenshots and examples below). Defaults to `True`.

* Inherits [sane lists](https://python-markdown.github.io/extensions/sane_lists/) behavior, which doesn't allow the mixing of ordered and unordered lists.


## Installation

##### [Pypi](https://pypi.python.org/pypi/mdx-truly-sane-lists):

```console
pip3 install mdx_truly_sane_lists
```

##### Directly from git:

```console
pip3 install git+git://github.com/radude/mdx_truly_sane_lists
```

## Usage

Basic:

```python
from markdown import markdown

# Default config is truly_sane: True, nested_indent: 2
markdown(text='some text', extensions=['mdx_truly_sane_lists']) 
```

With explicit config:

```python
from markdown import markdown

markdown(text='some text',
         extensions=[
             'mdx_truly_sane_lists',
         ],
         extension_configs={
             'mdx_truly_sane_lists': {
                 'nested_indent': 2,
                 'truly_sane': True,
             }},
         )
```

## Screenshots and examples

You can preview the new behaviour live at [rentry.co](https://rentry.co/) (uses `nested_indent: 2, truly_sane: True`)


Some ugly screenshots because I'm lazy and cannot into gimp:

![](https://i.imgur.com/7l2bWLY.png)
![](https://i.imgur.com/Ruwfb2A.png)

## HTML

Data:
```markdown
- attributes
 
- customer 
    - first_name
    - family_name
    - email
- person
    - first_name
    - family_name
    - birth_date
- subscription_id

- request
```

No extension:
```html before
<ul>
<li>
<p>attributes</p>
</li>
<li>
<p>customer </p>
<ul>
<li>first_name</li>
<li>family_name</li>
<li>email</li>
</ul>
</li>
<li>person<ul>
<li>first_name</li>
<li>family_name</li>
<li>birth_date</li>
</ul>
</li>
<li>
<p>subscription_id</p>
</li>
<li>
<p>request</p>
</li>
</ul>
```

Truly sane + 4 spaces:
```html
<ul>
<li>attributes</li>
</ul>
<ul>
<li>customer <ul>
<li>first_name</li>
<li>family_name</li>
<li>email</li>
</ul>
</li>
<li>person<ul>
<li>first_name</li>
<li>family_name</li>
<li>birth_date</li>
</ul>
</li>
<li>subscription_id</li>
</ul>
<ul>
<li>request</li>
</ul>
```
