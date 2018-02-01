"""
https://github.com/radude/mdx_linkify
"""

from markdown import Extension, util
from markdown.blockprocessors import OListProcessor, UListProcessor, ListIndentProcessor, BlockProcessor
import re


class TrulySaneListExtension(Extension):

    def __init__(self, *args, **kwargs):
        self.config = {
            "nested_indent": [2, 'Sets indent for nested lists. Defaults to 2'],
            "sane": [True, "True to stop messing up paragraps and linebreaks. Defaults to True"],
        }

        super(TrulySaneListExtension, self).__init__(*args, **kwargs)
        TrulySaneBlockProcessorMixin.truly_sane_tab_length = self.getConfigs()['nested_indent']
        TrulySaneBlockProcessorMixin.sane = self.getConfigs()['sane']

    def extendMarkdown(self, md, md_globals):
        md.parser.blockprocessors['olist'] = TrulySaneOListProcessor(md.parser)
        md.parser.blockprocessors['ulist'] = TrulySaneUListProcessor(md.parser)
        md.parser.blockprocessors['indent'] = TrulySaneListIndentProcessor(md.parser)


def makeExtension(*args, **kwargs):
    return TrulySaneListExtension(*args, **kwargs)


class TrulySaneBlockProcessorMixin(BlockProcessor):
    truly_sane_tab_length = 2

    def __init__(self, parser):
        super(TrulySaneBlockProcessorMixin, self).__init__(parser)

    def detab(self, text):
        newtext = []
        lines = text.split('\n')
        for line in lines:
            if line.startswith(' ' * self.truly_sane_tab_length):
                newtext.append(line[self.truly_sane_tab_length:])
            elif not line.strip():
                newtext.append('')
            else:
                break
        return '\n'.join(newtext), '\n'.join(lines[len(newtext):])

    def looseDetab(self, text, level=1):
        lines = text.split('\n')
        for i in range(len(lines)):
            if lines[i].startswith(' ' * self.truly_sane_tab_length * level):
                lines[i] = lines[i][self.truly_sane_tab_length * level:]
        return '\n'.join(lines)


class TrulySaneListIndentProcessor(ListIndentProcessor, TrulySaneBlockProcessorMixin):
    ITEM_TYPES = ['li']
    LIST_TYPES = ['ul', 'ol']

    def __init__(self, *args):
        super(TrulySaneListIndentProcessor, self).__init__(*args)
        self.INDENT_RE = re.compile(r'^(([ ]{%s})+)' % self.truly_sane_tab_length)

    def test(self, parent, block):
        return block.startswith(' ' * self.truly_sane_tab_length) and \
               not self.parser.state.isstate('detabbed') and \
               (parent.tag in self.ITEM_TYPES or
                (len(parent) and parent[-1] is not None and
                 (parent[-1].tag in self.LIST_TYPES)))

    def get_level(self, parent, block):
        m = self.INDENT_RE.match(block)
        if m:
            indent_level = len(m.group(1)) / self.truly_sane_tab_length
        else:
            indent_level = 0
        if self.parser.state.isstate('list'):
            level = 1
        else:
            level = 0
        while indent_level > level:
            child = self.lastChild(parent)
            if (child is not None and
                    (child.tag in self.LIST_TYPES or child.tag in self.ITEM_TYPES)):
                if child.tag in self.LIST_TYPES:
                    level += 1
                parent = child
            else:
                break
        return level, parent


class TrulySaneOListProcessor(OListProcessor, TrulySaneBlockProcessorMixin):
    SIBLING_TAGS = ['ol']

    def __init__(self, *args, **kwargs):

        super(TrulySaneOListProcessor, self).__init__(*args, **kwargs)
        self.RE = re.compile(r'^[ ]{0,%d}\d+\.[ ]+(.*)' % (self.truly_sane_tab_length - 1))
        # self.CHILD_RE = re.compile(r'^[ ]{0,%d}((\d+\.)|[*+-])[ ]+(.*)' % (self.truly_sane_tab_length - 1))  # original re
        self.CHILD_RE = re.compile(r'^[ ]{0,%d}((\d+\.))[ ]+(.*)' % (self.truly_sane_tab_length - 1))  # taken from sane_lists
        self.INDENT_RE = re.compile(r'^[ ]{%d,%d}((\d+\.)|[*+-])[ ]+.*' % (self.truly_sane_tab_length, self.truly_sane_tab_length * 2 - 1))

    def run(self, parent, blocks):

        items = self.get_items(blocks.pop(0))
        sibling = self.lastChild(parent)

        if not self.sane and (sibling is not None and sibling.tag in self.SIBLING_TAGS):
            lst = sibling
            if lst[-1].text:
                p = util.etree.Element('p')
                p.text = lst[-1].text
                lst[-1].text = ''
                lst[-1].insert(0, p)
            lch = self.lastChild(lst[-1])
            if lch is not None and lch.tail:
                p = util.etree.SubElement(lst[-1], 'p')
                p.text = lch.tail.lstrip()
                lch.tail = ''

            li = util.etree.SubElement(lst, 'li')
            self.parser.state.set('looselist')
            firstitem = items.pop(0)
            self.parser.parseBlocks(li, [firstitem])
            self.parser.state.reset()
        elif parent.tag in ['ol', 'ul']:
            lst = parent
        else:
            lst = util.etree.SubElement(parent, self.TAG)
            if not self.parser.markdown.lazy_ol and self.STARTSWITH != '1':
                lst.attrib['start'] = self.STARTSWITH

        self.parser.state.set('list')
        for item in items:
            if item.startswith(' ' * self.truly_sane_tab_length):
                self.parser.parseBlocks(lst[-1], [item])
            else:
                li = util.etree.SubElement(lst, 'li')
                self.parser.parseBlocks(li, [item])
        self.parser.state.reset()


class TrulySaneUListProcessor(TrulySaneOListProcessor, TrulySaneBlockProcessorMixin):
    TAG = 'ul'
    SIBLING_TAGS = ['ul']

    def __init__(self, parser):
        super(TrulySaneUListProcessor, self).__init__(parser)
        self.RE = re.compile(r'^[ ]{0,%d}[*+-][ ]+(.*)' % (self.truly_sane_tab_length - 1))
        self.CHILD_RE = re.compile(r'^[ ]{0,%d}(([*+-]))[ ]+(.*)' % (self.truly_sane_tab_length - 1))  # taken from sane_lists


def makeExtension(*args, **kwargs):
    return TrulySaneListExtension(*args, **kwargs)
