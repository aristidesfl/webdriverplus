from selenium.webdriver.remote.webelement import WebElement as _WebElement
from webdriverplus.selectors import SelectorMixin
from webdriverplus.wrappers import Style, Attributes, Size, Location


class WebElement(SelectorMixin, _WebElement):
    @property
    def _xpath_prefix(self):
        return './/*'

    # Traversal
    def parent(self, *args, **kwargs):
        """
        Note: We're overriding the default WebElement.parent behaviour here.
        (Normally .parent is a property that returns the WebDriver object.)
        """
        ret = self.find(xpath='..')
        if args or kwargs:
            ret = ret.filter(*args, **kwargs)
        return ret

    def children(self, *args, **kwargs):
        return self.find(xpath='./*')

    def descendants(self, *args, **kwargs):
        return self.find(xpath='./descendant::*')

    def ancestors(self, *args, **kwargs):
        return self.find(xpath='./ancestor::*')

    def next(self, *args, **kwargs):
        return self.find(xpath='./following-sibling::*[1]')

    def prev(self, *args, **kwargs):
        return self.find(xpath='./preceding-sibling::*[1]')

    def next_all(self, *args, **kwargs):
        return self.find(xpath='./following-sibling::*')

    def prev_all(self, *args, **kwargs):
        return self.find(xpath='./preceding-sibling::*')

    def siblings(self, *args, **kwargs):
        return self.prev_all() | self.next_all()

    # Inspection & Manipulation
    @property
    def id(self):
        return self.get_attribute('id')

    @property
    def type(self):
        return self.get_attribute('type')

    @property
    def value(self):
        return self.get_attribute('value')

    @property
    def is_checked(self):
        return self.get_attribute('checked') is not None

    @property
    def is_selected(self):
        return super(WebElement, self).is_selected()

    @property
    def is_displayed(self):
        return super(WebElement, self).is_displayed()

    @property
    def is_enabled(self):
        return super(WebElement, self).is_enabled()

    @property
    def inner_html(self):
        return self.get_attribute('innerHTML')

    @property
    def html(self):
        # http://stackoverflow.com/questions/1763479/how-to-get-the-html-for-a-dom-element-in-javascript
        script = """
            var container = document.createElement("div");
            container.appendChild(arguments[0].cloneNode(true));
            return container.innerHTML;
        """
        return self._parent.execute_script(script, self)

    @property
    def index(self):
        return len(self.prev_all())

    @property
    def style(self):
        return Style(self)

    @property
    def size(self):
        val = super(WebElement, self).size
        return Size(val['width'], val['height'])

    @property
    def location(self):
        val = super(WebElement, self).location
        return Location(val['x'], val['y'])

    @property
    def attributes(self):
        return Attributes(self)

    def javascript(self, script):
        script = "return arguments[0].%s;" % script
        return  self._parent.execute_script(script, self)

    def jquery(self, script):
        script = "return $(arguments[0]).%s;" % script
        return  self._parent.execute_script(script, self)

    def __repr__(self):
        ret = self.html
        ret = ' '.join(ret.split())
        if len(ret) > 78:
            ret = ret[:75] + '...'
        #self.style.backgroundColor = '#f9edbe'
        #self.style.borderColor = '#f9edbe'
        #self.style.outline = '1px solid black'
        return ret

    def __hash__(self):
        return hash(self._id)

    def __eq__(self, other):
        return self._id == other._id
