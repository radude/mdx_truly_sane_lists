"""
https://github.com/radude/mdx_truly_sane_lists
"""

import re

from markdown import Extension, util
from markdown import version as md_version
from markdown.blockprocessors import OListProcessor, ListIndentProcessor, BlockProcessor


class TrulySaneListExtension(Extension):

    def __init__(self, *args, **kwargs):
        self.config = {
            "nested_indent": [2, 'Sets indent for nested lists. Defaults to 2'],
            "truly_sane": [True, "True to stop messing up paragraps and linebreaks. Defaults to True"],
        }

        super(TrulySaneListExtension, self).__init__(*args, **kwargs)
        TrulySaneBlockProcessorMixin.truly_sane_tab_length = self.getConfigs()['nested_indent']
        TrulySaneBlockProcessorMixin.truly_sane = self.getConfigs()['truly_sane']

    def _extendMarkdown3(self, md):
        md.parser.blockprocessors.register(TrulySaneOListProcessor(md.parser), 'olist', 50)
        md.parser.blockprocessors.register(TrulySaneUListProcessor(md.parser), 'ulist', 40)
        md.parser.blockprocessors.register(TrulySaneListIndentProcessor(md.parser), 'indent', 95)

    def _extendMarkdown2(self, md, md_globals):
        md.parser.blockprocessors['olist'] = TrulySaneOListProcessor(md.parser)
        md.parser.blockprocessors['ulist'] = TrulySaneUListProcessor(md.parser)
        md.parser.blockprocessors['indent'] = TrulySaneListIndentProcessor(md.parser)

    # supporting both 2 and 3 version of markdown
    if md_version >= '3.0':
        extendMarkdown = _extendMarkdown3
    else:
        extendMarkdown = _extendMarkdown2


def makeExtension(*args, **kwargs):
    return TrulySaneListExtension(*args, **kwargs)


class TrulySaneBlockProcessorMixin(BlockProcessor):
    truly_sane_tab_length = 2
    truly_sane = True

    def __init__(self, parser):
        super(TrulySaneBlockProcessorMixin, self).__init__(parser)
        self.tab_length = self.truly_sane_tab_length


class TrulySaneListIndentProcessor(ListIndentProcessor, TrulySaneBlockProcessorMixin):

    def __init__(self, *args):
        super(TrulySaneListIndentProcessor, self).__init__(*args)


class TrulySaneOListProcessor(OListProcessor, TrulySaneBlockProcessorMixin):
    SIBLING_TAGS = ['ol']  # from sane lists

    def __init__(self, *args, **kwargs):

        super(TrulySaneOListProcessor, self).__init__(*args, **kwargs)
        self.CHILD_RE = re.compile(r'^[ ]{0,%d}((\d+\.))[ ]+(.*)' % (self.tab_length - 1))  # from sane_lists

    def run(self, parent, blocks):

        items = self.get_items(blocks.pop(0))
        sibling = self.lastChild(parent)

        if not self.truly_sane and (sibling is not None and sibling.tag in self.SIBLING_TAGS):
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
            if md_version >= '3.0':
                if not self.LAZY_OL and self.STARTSWITH != '1':
                    lst.attrib['start'] = self.STARTSWITH
            else:
                if not self.parser.markdown.lazy_ol and self.STARTSWITH != '1':
                    lst.attrib['start'] = self.STARTSWITH

        self.parser.state.set('list')
        for item in items:
            if item.startswith(' ' * self.tab_length):
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
        self.RE = re.compile(r'^[ ]{0,%d}[*+-][ ]+(.*)' % (self.tab_length - 1))
        self.CHILD_RE = re.compile(r'^[ ]{0,%d}(([*+-]))[ ]+(.*)' % (self.tab_length - 1))  # from sane_lists
