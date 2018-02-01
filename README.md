# Mdx Truly Sane Lists
An extension for [Python-Markdown](https://github.com/Python-Markdown/markdown) that makes lists truly sane. Features custom indents for nested lists and fix for messy linebreaks and paragraphs between lists.


## Features

* `nested_indent` option: Custom indent for nested lists. Defaults to `2`. Doesn't mess with code indents, which is still 4. 

* `sane` option: Makes linebreaks and paragraphs in lists behave as usually expected by user. No longer adds weird `p`, no extra linebreaks, no longer fuses lists together when they shouldn't be fused (see screenshots and examples below). Defaults to `True`.

* Inherits [sane lists](https://python-markdown.github.io/extensions/sane_lists/) behavior, which doesn't allow the mixing of ordered and unordered lists.


## Installation

Pypi, manual and blah blah. TBD

Directly from git:

```console
pip install git+git://github.com/radude/mdx_truly_sane_lists
```

## Usage

Basic:

```python
from markdown import markdown

# Default config is sane: Tue, nested_lists: 2
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
                 'sane': True,
             }},
         )
```

## Screenshots and examples

TBD  
Live TBD
