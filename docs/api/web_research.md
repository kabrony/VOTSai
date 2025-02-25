# web_research

## Classes

### BeautifulSoup

A data structure representing a parsed HTML or XML document.

    Most of the methods you'll call on a BeautifulSoup object are inherited from
    PageElement or Tag.

    Internally, this class defines the basic interface called by the
    tree builders when converting an HTML/XML document into a data
    structure. The interface abstracts away the differences between
    parsers. To write a new tree builder, you'll need to understand
    these methods as a whole.

    These methods will be called by the BeautifulSoup constructor:
      * reset()
      * feed(markup)

    The tree builder may call these methods from its feed() implementation:
      * handle_starttag(name, attrs) # See note about return value
      * handle_endtag(name)
      * handle_data(data) # Appends to the current data node
      * endData(containerClass) # Ends the current data node

    No matter how complicated the underlying parser is, you should be
    able to build a tree using 'start tag' events, 'end tag' events,
    'data' events, and "done with data" events.

    If you encounter an empty-element tag (aka a self-closing tag,
    like HTML's <br> tag), call handle_starttag and then
    handle_endtag.

#### Methods

##### __init__

```python
__init__(self, markup: Union[str, bytes, IO[str], IO[bytes]] = '', features: Union[str, Sequence[str], NoneType] = None, builder: Union[bs4.builder.TreeBuilder, Type[bs4.builder.TreeBuilder], NoneType] = None, parse_only: Optional[bs4.filter.SoupStrainer] = None, from_encoding: Optional[str] = None, exclude_encodings: Optional[Iterable[str]] = None, element_classes: Optional[Dict[Type[bs4.element.PageElement], Type[bs4.element.PageElement]]] = None, **kwargs: Any)
```

Constructor.

        :param markup: A string or a file-like object representing
         markup to be parsed.

        :param features: Desirable features of the parser to be
         used. This may be the name of a specific parser ("lxml",
         "lxml-xml", "html.parser", or "html5lib") or it may be the
         type of markup to be used ("html", "html5", "xml"). It's
         recommended that you name a specific parser, so that
         Beautiful Soup gives you the same results across platforms
         and virtual environments.

        :param builder: A TreeBuilder subclass to instantiate (or
         instance to use) instead of looking one up based on
         `features`. You only need to use this if you've implemented a
         custom TreeBuilder.

        :param parse_only: A SoupStrainer. Only parts of the document
         matching the SoupStrainer will be considered. This is useful
         when parsing part of a document that would otherwise be too
         large to fit into memory.

        :param from_encoding: A string indicating the encoding of the
         document to be parsed. Pass this in if Beautiful Soup is
         guessing wrongly about the document's encoding.

        :param exclude_encodings: A list of strings indicating
         encodings known to be wrong. Pass this in if you don't know
         the document's encoding but you know Beautiful Soup's guess is
         wrong.

        :param element_classes: A dictionary mapping BeautifulSoup
         classes like Tag and NavigableString, to other classes you'd
         like to be instantiated instead as the parse tree is
         built. This is useful for subclassing Tag or NavigableString
         to modify default behavior.

        :param kwargs: For backwards compatibility purposes, the
         constructor accepts certain keyword arguments used in
         Beautiful Soup 3. None of these arguments do anything in
         Beautiful Soup 4; they will result in a warning and then be
         ignored.

         Apart from this, any keyword arguments passed into the
         BeautifulSoup constructor are propagated to the TreeBuilder
         constructor. This makes it possible to configure a
         TreeBuilder by passing in arguments, not just by saying which
         one to use.

##### append

```python
append(self, tag: '_InsertableElement')
```

Appends the given `PageElement` to the contents of this `Tag`.

        :param tag: A PageElement.

        :return The newly appended PageElement.

##### childGenerator

```python
childGenerator(self)
```

Deprecated generator.

        :meta private:

##### clear

```python
clear(self, decompose: 'bool' = False)
```

Destroy all children of this `Tag` by calling
           `PageElement.extract` on them.

        :param decompose: If this is True, `PageElement.decompose` (a
            more destructive method) will be called instead of
            `PageElement.extract`.

##### copy_self

```python
copy_self(self)
```

Create a new BeautifulSoup object with the same TreeBuilder,
        but not associated with any markup.

        This is the first step of the deepcopy process.

##### decode

```python
decode(self, indent_level: Optional[int] = None, eventual_encoding: str = 'utf-8', formatter: Union[bs4.formatter.Formatter, str] = 'minimal', iterator: Optional[Iterator[bs4.element.PageElement]] = None, **kwargs: Any)
```

Returns a string representation of the parse tree
            as a full HTML or XML document.

        :param indent_level: Each line of the rendering will be
           indented this many levels. (The ``formatter`` decides what a
           'level' means, in terms of spaces or other characters
           output.) This is used internally in recursive calls while
           pretty-printing.
        :param eventual_encoding: The encoding of the final document.
            If this is None, the document will be a Unicode string.
        :param formatter: Either a `Formatter` object, or a string naming one of
            the standard formatters.
        :param iterator: The iterator to use when navigating over the
            parse tree. This is only used by `Tag.decode_contents` and
            you probably won't need to use it.

##### decode_contents

```python
decode_contents(self, indent_level: 'Optional[int]' = None, eventual_encoding: '_Encoding' = 'utf-8', formatter: '_FormatterOrName' = 'minimal')
```

Renders the contents of this tag as a Unicode string.

        :param indent_level: Each line of the rendering will be
           indented this many levels. (The formatter decides what a
           'level' means in terms of spaces or other characters
           output.) Used internally in recursive calls while
           pretty-printing.

        :param eventual_encoding: The tag is destined to be
           encoded into this encoding. decode_contents() is *not*
           responsible for performing that encoding. This information
           is needed so that a real encoding can be substituted in if
           the document contains an encoding declaration (e.g. in a
           <meta> tag).

        :param formatter: A `Formatter` object, or a string naming one of
            the standard Formatters.

##### decompose

```python
decompose(self)
```

Recursively destroys this `PageElement` and its children.

        The element will be removed from the tree and wiped out; so
        will everything beneath it.

        The behavior of a decomposed `PageElement` is undefined and you
        should never use one for anything, but if you need to *check*
        whether an element has been decomposed, you can use the
        `PageElement.decomposed` property.

##### encode

```python
encode(self, encoding: '_Encoding' = 'utf-8', indent_level: 'Optional[int]' = None, formatter: '_FormatterOrName' = 'minimal', errors: 'str' = 'xmlcharrefreplace')
```

Render this `Tag` and its contents as a bytestring.

        :param encoding: The encoding to use when converting to
           a bytestring. This may also affect the text of the document,
           specifically any encoding declarations within the document.
        :param indent_level: Each line of the rendering will be
           indented this many levels. (The ``formatter`` decides what a
           'level' means, in terms of spaces or other characters
           output.) This is used internally in recursive calls while
           pretty-printing.
        :param formatter: Either a `Formatter` object, or a string naming one of
            the standard formatters.
        :param errors: An error handling strategy such as
            'xmlcharrefreplace'. This value is passed along into
            :py:meth:`str.encode` and its value should be one of the `error
            handling constants defined by Python's codecs module
            <https://docs.python.org/3/library/codecs.html#error-handlers>`_.

##### encode_contents

```python
encode_contents(self, indent_level: 'Optional[int]' = None, encoding: '_Encoding' = 'utf-8', formatter: '_FormatterOrName' = 'minimal')
```

Renders the contents of this PageElement as a bytestring.

        :param indent_level: Each line of the rendering will be
           indented this many levels. (The ``formatter`` decides what a
           'level' means, in terms of spaces or other characters
           output.) This is used internally in recursive calls while
           pretty-printing.
        :param formatter: Either a `Formatter` object, or a string naming one of
            the standard formatters.
        :param encoding: The bytestring will be in this encoding.

##### endData

```python
endData(self, containerClass: Optional[Type[bs4.element.NavigableString]] = None)
```

Method called by the TreeBuilder when the end of a data segment
        occurs.

        :param containerClass: The class to use when incorporating the
        data segment into the parse tree.

        :meta private:

##### extend

```python
extend(self, tags: 'Union[Iterable[_InsertableElement], Tag]')
```

Appends one or more objects to the contents of this
        `Tag`.

        :param tags: If a list of `PageElement` objects is provided,
            they will be appended to this tag's contents, one at a time.
            If a single `Tag` is provided, its `Tag.contents` will be
            used to extend this object's `Tag.contents`.

        :return The list of PageElements that were appended.

##### extract

```python
extract(self, _self_index: 'Optional[int]' = None)
```

Destructively rips this element out of the tree.

        :param _self_index: The location of this element in its parent's
           .contents, if known. Passing this in allows for a performance
           optimization.

        :return: this `PageElement`, no longer part of the tree.

##### fetchAllPrevious

```python
fetchAllPrevious(self, *args: Any, **kwargs: Any)
```

:meta private:

##### fetchNextSiblings

```python
fetchNextSiblings(self, *args: Any, **kwargs: Any)
```

:meta private:

##### fetchParents

```python
fetchParents(self, *args: Any, **kwargs: Any)
```

:meta private:

##### fetchPreviousSiblings

```python
fetchPreviousSiblings(self, *args: Any, **kwargs: Any)
```

:meta private:

##### find

```python
find(self, name: '_FindMethodName' = None, attrs: '_StrainableAttributes' = {}, recursive: 'bool' = True, string: 'Optional[_StrainableString]' = None, **kwargs: '_StrainableAttribute')
```

Look in the children of this PageElement and find the first
        PageElement that matches the given criteria.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: Additional filters on attribute values.
        :param recursive: If this is True, find() will perform a
            recursive search of this Tag's children. Otherwise,
            only the direct children will be considered.
        :param string: A filter on the `Tag.string` attribute.
        :param limit: Stop looking after finding this many results.
        :kwargs: Additional filters on attribute values.

##### findAll

```python
findAll(self, *args: Any, **kwargs: Any)
```

:meta private:

##### findAllNext

```python
findAllNext(self, *args: Any, **kwargs: Any)
```

:meta private:

##### findAllPrevious

```python
findAllPrevious(self, *args: Any, **kwargs: Any)
```

:meta private:

##### findChild

```python
findChild(self, *args: Any, **kwargs: Any)
```

:meta private:

##### findChildren

```python
findChildren(self, *args: Any, **kwargs: Any)
```

:meta private:

##### findNext

```python
findNext(self, *args: Any, **kwargs: Any)
```

:meta private:

##### findNextSibling

```python
findNextSibling(self, *args: Any, **kwargs: Any)
```

:meta private:

##### findNextSiblings

```python
findNextSiblings(self, *args: Any, **kwargs: Any)
```

:meta private:

##### findParent

```python
findParent(self, *args: Any, **kwargs: Any)
```

:meta private:

##### findParents

```python
findParents(self, *args: Any, **kwargs: Any)
```

:meta private:

##### findPrevious

```python
findPrevious(self, *args: Any, **kwargs: Any)
```

:meta private:

##### findPreviousSibling

```python
findPreviousSibling(self, *args: Any, **kwargs: Any)
```

:meta private:

##### findPreviousSiblings

```python
findPreviousSiblings(self, *args: Any, **kwargs: Any)
```

:meta private:

##### find_all

```python
find_all(self, name: '_FindMethodName' = None, attrs: '_StrainableAttributes' = {}, recursive: 'bool' = True, string: 'Optional[_StrainableString]' = None, limit: 'Optional[int]' = None, _stacklevel: 'int' = 2, **kwargs: '_StrainableAttribute')
```

Look in the children of this `PageElement` and find all
        `PageElement` objects that match the given criteria.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: Additional filters on attribute values.
        :param recursive: If this is True, find_all() will perform a
            recursive search of this PageElement's children. Otherwise,
            only the direct children will be considered.
        :param limit: Stop looking after finding this many results.
        :param _stacklevel: Used internally to improve warning messages.
        :kwargs: Additional filters on attribute values.

##### find_all_next

```python
find_all_next(self, name: '_FindMethodName' = None, attrs: '_StrainableAttributes' = {}, string: 'Optional[_StrainableString]' = None, limit: 'Optional[int]' = None, _stacklevel: 'int' = 2, **kwargs: '_StrainableAttribute')
```

Find all `PageElement` objects that match the given criteria and
        appear later in the document than this `PageElement`.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: Additional filters on attribute values.
        :param string: A filter for a NavigableString with specific text.
        :param limit: Stop looking after finding this many results.
        :param _stacklevel: Used internally to improve warning messages.
        :kwargs: Additional filters on attribute values.

##### find_all_previous

```python
find_all_previous(self, name: '_FindMethodName' = None, attrs: '_StrainableAttributes' = {}, string: 'Optional[_StrainableString]' = None, limit: 'Optional[int]' = None, _stacklevel: 'int' = 2, **kwargs: '_StrainableAttribute')
```

Look backwards in the document from this `PageElement` and find all
        `PageElement` that match the given criteria.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: Additional filters on attribute values.
        :param string: A filter for a `NavigableString` with specific text.
        :param limit: Stop looking after finding this many results.
        :param _stacklevel: Used internally to improve warning messages.
        :kwargs: Additional filters on attribute values.

##### find_next

```python
find_next(self, name: '_FindMethodName' = None, attrs: '_StrainableAttributes' = {}, string: 'Optional[_StrainableString]' = None, **kwargs: '_StrainableAttribute')
```

Find the first PageElement that matches the given criteria and
        appears later in the document than this PageElement.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: Additional filters on attribute values.
        :param string: A filter for a NavigableString with specific text.
        :kwargs: Additional filters on attribute values.

##### find_next_sibling

```python
find_next_sibling(self, name: '_FindMethodName' = None, attrs: '_StrainableAttributes' = {}, string: 'Optional[_StrainableString]' = None, **kwargs: '_StrainableAttribute')
```

Find the closest sibling to this PageElement that matches the
        given criteria and appears later in the document.

        All find_* methods take a common set of arguments. See the
        online documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: Additional filters on attribute values.
        :param string: A filter for a `NavigableString` with specific text.
        :kwargs: Additional filters on attribute values.

##### find_next_siblings

```python
find_next_siblings(self, name: '_FindMethodName' = None, attrs: '_StrainableAttributes' = {}, string: 'Optional[_StrainableString]' = None, limit: 'Optional[int]' = None, _stacklevel: 'int' = 2, **kwargs: '_StrainableAttribute')
```

Find all siblings of this `PageElement` that match the given criteria
        and appear later in the document.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: Additional filters on attribute values.
        :param string: A filter for a `NavigableString` with specific text.
        :param limit: Stop looking after finding this many results.
        :param _stacklevel: Used internally to improve warning messages.
        :kwargs: Additional filters on attribute values.

##### find_parent

```python
find_parent(self, name: '_FindMethodName' = None, attrs: '_StrainableAttributes' = {}, **kwargs: '_StrainableAttribute')
```

Find the closest parent of this PageElement that matches the given
        criteria.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: Additional filters on attribute values.
        :param self: Whether the PageElement itself should be considered
           as one of its 'parents'.
        :kwargs: Additional filters on attribute values.

##### find_parents

```python
find_parents(self, name: '_FindMethodName' = None, attrs: '_StrainableAttributes' = {}, limit: 'Optional[int]' = None, _stacklevel: 'int' = 2, **kwargs: '_StrainableAttribute')
```

Find all parents of this `PageElement` that match the given criteria.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: Additional filters on attribute values.
        :param limit: Stop looking after finding this many results.
        :param _stacklevel: Used internally to improve warning messages.
        :kwargs: Additional filters on attribute values.

##### find_previous

```python
find_previous(self, name: '_FindMethodName' = None, attrs: '_StrainableAttributes' = {}, string: 'Optional[_StrainableString]' = None, **kwargs: '_StrainableAttribute')
```

Look backwards in the document from this `PageElement` and find the
        first `PageElement` that matches the given criteria.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: Additional filters on attribute values.
        :param string: A filter for a `NavigableString` with specific text.
        :kwargs: Additional filters on attribute values.

##### find_previous_sibling

```python
find_previous_sibling(self, name: '_FindMethodName' = None, attrs: '_StrainableAttributes' = {}, string: 'Optional[_StrainableString]' = None, **kwargs: '_StrainableAttribute')
```

Returns the closest sibling to this `PageElement` that matches the
        given criteria and appears earlier in the document.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: Additional filters on attribute values.
        :param string: A filter for a `NavigableString` with specific text.
        :kwargs: Additional filters on attribute values.

##### find_previous_siblings

```python
find_previous_siblings(self, name: '_FindMethodName' = None, attrs: '_StrainableAttributes' = {}, string: 'Optional[_StrainableString]' = None, limit: 'Optional[int]' = None, _stacklevel: 'int' = 2, **kwargs: '_StrainableAttribute')
```

Returns all siblings to this PageElement that match the
        given criteria and appear earlier in the document.

        All find_* methods take a common set of arguments. See the online
        documentation for detailed explanations.

        :param name: A filter on tag name.
        :param attrs: Additional filters on attribute values.
        :param string: A filter for a NavigableString with specific text.
        :param limit: Stop looking after finding this many results.
        :param _stacklevel: Used internally to improve warning messages.
        :kwargs: Additional filters on attribute values.

##### format_string

```python
format_string(self, s: 'str', formatter: 'Optional[_FormatterOrName]')
```

Format the given string using the given formatter.

        :param s: A string.
        :param formatter: A Formatter object, or a string naming one of the standard formatters.

##### formatter_for_name

```python
formatter_for_name(self, formatter_name: 'Union[_FormatterOrName, _EntitySubstitutionFunction]')
```

Look up or create a Formatter for the given identifier,
        if necessary.

        :param formatter: Can be a `Formatter` object (used as-is), a
            function (used as the entity substitution hook for an
            `bs4.formatter.XMLFormatter` or
            `bs4.formatter.HTMLFormatter`), or a string (used to look
            up an `bs4.formatter.XMLFormatter` or
            `bs4.formatter.HTMLFormatter` in the appropriate registry.

##### get

```python
get(self, key: 'str', default: 'Optional[_AttributeValue]' = None)
```

Returns the value of the 'key' attribute for the tag, or
        the value given for 'default' if it doesn't have that
        attribute.

        :param key: The attribute to look for.
        :param default: Use this value if the attribute is not present
            on this `Tag`.

##### getText

```python
getText(self, separator: 'str' = '', strip: 'bool' = False, types: 'Iterable[Type[NavigableString]]' = ())
```

Get all child strings of this PageElement, concatenated using the
        given separator.

        :param separator: Strings will be concatenated using this separator.

        :param strip: If True, strings will be stripped before being
            concatenated.

        :param types: A tuple of NavigableString subclasses. Any
            strings of a subclass not found in this list will be
            ignored. Although there are exceptions, the default
            behavior in most cases is to consider only NavigableString
            and CData objects. That means no comments, processing
            instructions, etc.

        :return: A string.

##### get_attribute_list

```python
get_attribute_list(self, key: 'str', default: 'Optional[AttributeValueList]' = None)
```

The same as get(), but always returns a (possibly empty) list.

        :param key: The attribute to look for.
        :param default: Use this value if the attribute is not present
            on this `Tag`.
        :return: A list of strings, usually empty or containing only a single
            value.

##### get_text

```python
get_text(self, separator: 'str' = '', strip: 'bool' = False, types: 'Iterable[Type[NavigableString]]' = ())
```

Get all child strings of this PageElement, concatenated using the
        given separator.

        :param separator: Strings will be concatenated using this separator.

        :param strip: If True, strings will be stripped before being
            concatenated.

        :param types: A tuple of NavigableString subclasses. Any
            strings of a subclass not found in this list will be
            ignored. Although there are exceptions, the default
            behavior in most cases is to consider only NavigableString
            and CData objects. That means no comments, processing
            instructions, etc.

        :return: A string.

##### handle_data

```python
handle_data(self, data: str)
```

Called by the tree builder when a chunk of textual data is
        encountered.

        :meta private:

##### handle_endtag

```python
handle_endtag(self, name: str, nsprefix: Optional[str] = None)
```

Called by the tree builder when an ending tag is encountered.

        :param name: Name of the tag.
        :param nsprefix: Namespace prefix for the tag.

        :meta private:

##### handle_starttag

```python
handle_starttag(self, name: str, namespace: Optional[str], nsprefix: Optional[str], attrs: 'Mapping[Union[str, NamespacedAttribute], _RawAttributeValue]', sourceline: Optional[int] = None, sourcepos: Optional[int] = None, namespaces: Optional[Dict[str, str]] = None)
```

Called by the tree builder when a new tag is encountered.

        :param name: Name of the tag.
        :param nsprefix: Namespace prefix for the tag.
        :param attrs: A dictionary of attribute values. Note that
           attribute values are expected to be simple strings; processing
           of multi-valued attributes such as "class" comes later.
        :param sourceline: The line number where this tag was found in its
            source document.
        :param sourcepos: The character position within `sourceline` where this
            tag was found.
        :param namespaces: A dictionary of all namespace prefix mappings
            currently in scope in the document.

        If this method returns None, the tag was rejected by an active
        `ElementFilter`. You should proceed as if the tag had not occurred
        in the document. For instance, if this was a self-closing tag,
        don't call handle_endtag.

        :meta private:

##### has_attr

```python
has_attr(self, key: 'str')
```

Does this `Tag` have an attribute with the given name?

##### has_key

```python
has_key(self, key: 'str')
```

Deprecated method. This was kind of misleading because has_key()
        (attributes) was different from __in__ (contents).

        has_key() is gone in Python 3, anyway.

        :meta private:

##### index

```python
index(self, element: 'PageElement')
```

Find the index of a child of this `Tag` (by identity, not value).

        Doing this by identity avoids issues when a `Tag` contains two
        children that have string equality.

        :param element: Look for this `PageElement` in this object's contents.

##### insert

```python
insert(self, position: 'int', *new_children: '_InsertableElement')
```

Insert one or more new PageElements as a child of this `Tag`.

        This works similarly to :py:meth:`list.insert`, except you can insert
        multiple elements at once.

        :param position: The numeric position that should be occupied
           in this Tag's `Tag.children` by the first new `PageElement`.

        :param new_children: The PageElements to insert.

        :return The newly inserted PageElements.

##### insert_after

```python
insert_after(self, *args: Union[ForwardRef('PageElement'), str])
```

This method is part of the PageElement API, but `BeautifulSoup` doesn't implement
        it because there is nothing before or after it in the parse tree.

##### insert_before

```python
insert_before(self, *args: Union[ForwardRef('PageElement'), str])
```

This method is part of the PageElement API, but `BeautifulSoup` doesn't implement
        it because there is nothing before or after it in the parse tree.

##### isSelfClosing

```python
isSelfClosing(self)
```

: :meta private:

##### new_string

```python
new_string(self, s: str, subclass: Optional[Type[bs4.element.NavigableString]] = None)
```

Create a new `NavigableString` associated with this `BeautifulSoup`
        object.

        :param s: The string content of the `NavigableString`
        :param subclass: The subclass of `NavigableString`, if any, to
               use. If a document is being processed, an appropriate
               subclass for the current location in the document will
               be determined automatically.

##### new_tag

```python
new_tag(self, name: str, namespace: Optional[str] = None, nsprefix: Optional[str] = None, attrs: Optional[ForwardRef('Mapping[Union[str, NamespacedAttribute], _RawAttributeValue]')] = None, sourceline: Optional[int] = None, sourcepos: Optional[int] = None, string: Optional[str] = None, **kwattrs: str)
```

Create a new Tag associated with this BeautifulSoup object.

        :param name: The name of the new Tag.
        :param namespace: The URI of the new Tag's XML namespace, if any.
        :param prefix: The prefix for the new Tag's XML namespace, if any.
        :param attrs: A dictionary of this Tag's attribute values; can
            be used instead of ``kwattrs`` for attributes like 'class'
            that are reserved words in Python.
        :param sourceline: The line number where this tag was
            (purportedly) found in its source document.
        :param sourcepos: The character position within ``sourceline`` where this
            tag was (purportedly) found.
        :param string: String content for the new Tag, if any.
        :param kwattrs: Keyword arguments for the new Tag's attribute values.

##### nextGenerator

```python
nextGenerator(self)
```

:meta private:

##### nextSiblingGenerator

```python
nextSiblingGenerator(self)
```

:meta private:

##### object_was_parsed

```python
object_was_parsed(self, o: bs4.element.PageElement, parent: Optional[bs4.element.Tag] = None, most_recent_element: Optional[bs4.element.PageElement] = None)
```

Method called by the TreeBuilder to integrate an object into the
        parse tree.

        :meta private:

##### parentGenerator

```python
parentGenerator(self)
```

:meta private:

##### popTag

```python
popTag(self)
```

Internal method called by _popToTag when a tag is closed.

        :meta private:

##### prettify

```python
prettify(self, encoding: 'Optional[_Encoding]' = None, formatter: '_FormatterOrName' = 'minimal')
```

Pretty-print this `Tag` as a string or bytestring.

        :param encoding: The encoding of the bytestring, or None if you want Unicode.
        :param formatter: A Formatter object, or a string naming one of
            the standard formatters.
        :return: A string (if no ``encoding`` is provided) or a bytestring
            (otherwise).

##### previousGenerator

```python
previousGenerator(self)
```

:meta private:

##### previousSiblingGenerator

```python
previousSiblingGenerator(self)
```

:meta private:

##### pushTag

```python
pushTag(self, tag: bs4.element.Tag)
```

Internal method called by handle_starttag when a tag is opened.

        :meta private:

##### recursiveChildGenerator

```python
recursiveChildGenerator(self)
```

Deprecated generator.

        :meta private:

##### renderContents

```python
renderContents(self, encoding: '_Encoding' = 'utf-8', prettyPrint: 'bool' = False, indentLevel: 'Optional[int]' = 0)
```

Deprecated method for BS3 compatibility.

        :meta private:

##### replaceWith

```python
replaceWith(self, *args: Any, **kwargs: Any)
```

:meta private:

##### replaceWithChildren

```python
replaceWithChildren(self)
```

: :meta private:

##### replace_with

```python
replace_with(self, *args: 'PageElement')
```

Replace this `PageElement` with one or more other `PageElement`,
        objects, keeping the rest of the tree the same.

        :return: This `PageElement`, no longer part of the tree.

##### replace_with_children

```python
replace_with_children(self)
```

Replace this `PageElement` with its contents.

        :return: This object, no longer part of the tree.

##### reset

```python
reset(self)
```

Reset this object to a state as though it had never parsed any
        markup.

##### select

```python
select(self, selector: 'str', namespaces: 'Optional[Dict[str, str]]' = None, limit: 'int' = 0, **kwargs: 'Any')
```

Perform a CSS selection operation on the current element.

        This uses the SoupSieve library.

        :param selector: A string containing a CSS selector.

        :param namespaces: A dictionary mapping namespace prefixes
           used in the CSS selector to namespace URIs. By default,
           Beautiful Soup will use the prefixes it encountered while
           parsing the document.

        :param limit: After finding this number of results, stop looking.

        :param kwargs: Keyword arguments to be passed into SoupSieve's
           soupsieve.select() method.

##### select_one

```python
select_one(self, selector: 'str', namespaces: 'Optional[Dict[str, str]]' = None, **kwargs: 'Any')
```

Perform a CSS selection operation on the current element.

        :param selector: A CSS selector.

        :param namespaces: A dictionary mapping namespace prefixes
           used in the CSS selector to namespace URIs. By default,
           Beautiful Soup will use the prefixes it encountered while
           parsing the document.

        :param kwargs: Keyword arguments to be passed into Soup Sieve's
           soupsieve.select() method.

##### setup

```python
setup(self, parent: 'Optional[Tag]' = None, previous_element: '_AtMostOneElement' = None, next_element: '_AtMostOneElement' = None, previous_sibling: '_AtMostOneElement' = None, next_sibling: '_AtMostOneElement' = None)
```

Sets up the initial relations between this element and
        other elements.

        :param parent: The parent of this element.

        :param previous_element: The element parsed immediately before
            this one.

        :param next_element: The element parsed immediately before
            this one.

        :param previous_sibling: The most recently encountered element
            on the same level of the parse tree as this one.

        :param previous_sibling: The next element to be encountered
            on the same level of the parse tree as this one.

##### smooth

```python
smooth(self)
```

Smooth out the children of this `Tag` by consolidating consecutive
        strings.

        If you perform a lot of operations that modify the tree,
        calling this method afterwards can make pretty-printed output
        look more natural.

##### string_container

```python
string_container(self, base_class: Optional[Type[bs4.element.NavigableString]] = None)
```

Find the class that should be instantiated to hold a given kind of
        string.

        This may be a built-in Beautiful Soup class or a custom class passed
        in to the BeautifulSoup constructor.

##### unwrap

```python
unwrap(self)
```

Replace this `PageElement` with its contents.

        :return: This object, no longer part of the tree.

##### wrap

```python
wrap(self, wrap_inside: 'Tag')
```

Wrap this `PageElement` inside a `Tag`.

        :return: ``wrap_inside``, occupying the position in the tree that used
           to be occupied by this object, and with this object now inside it.

### DDGS

DuckDuckgo_search class to get search results from duckduckgo.com.

#### Methods

##### __init__

```python
__init__(self, headers: 'dict[str, str] | None' = None, proxy: 'str | None' = None, proxies: 'dict[str, str] | str | None' = None, timeout: 'int | None' = 10, verify: 'bool' = True)
```

Initialize the DDGS object.

        Args:
            headers (dict, optional): Dictionary of headers for the HTTP client. Defaults to None.
            proxy (str, optional): proxy for the HTTP client, supports http/https/socks5 protocols.
                example: "http://user:pass@example.com:3128". Defaults to None.
            timeout (int, optional): Timeout value for the HTTP client. Defaults to 10.
            verify (bool): SSL verification when making the request. Defaults to True.

###### Parameters


##### chat

```python
chat(self, keywords: 'str', model: 'str' = 'gpt-4o-mini', timeout: 'int' = 30)
```

Initiates a chat session with DuckDuckGo AI.

        Args:
            keywords (str): The initial message or question to send to the AI.
            model (str): The model to use: "gpt-4o-mini", "llama-3.3-70b", "claude-3-haiku",
                "o3-mini", "mixtral-8x7b". Defaults to "gpt-4o-mini".
            timeout (int): Timeout value for the HTTP client. Defaults to 20.

        Returns:
            str: The response from the AI.

###### Parameters


###### Returns



##### images

```python
images(self, keywords: 'str', region: 'str' = 'wt-wt', safesearch: 'str' = 'moderate', timelimit: 'str | None' = None, size: 'str | None' = None, color: 'str | None' = None, type_image: 'str | None' = None, layout: 'str | None' = None, license_image: 'str | None' = None, max_results: 'int | None' = None)
```

DuckDuckGo images search. Query params: https://duckduckgo.com/params.

        Args:
            keywords: keywords for query.
            region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
            safesearch: on, moderate, off. Defaults to "moderate".
            timelimit: Day, Week, Month, Year. Defaults to None.
            size: Small, Medium, Large, Wallpaper. Defaults to None.
            color: color, Monochrome, Red, Orange, Yellow, Green, Blue,
                Purple, Pink, Brown, Black, Gray, Teal, White. Defaults to None.
            type_image: photo, clipart, gif, transparent, line.
                Defaults to None.
            layout: Square, Tall, Wide. Defaults to None.
            license_image: any (All Creative Commons), Public (PublicDomain),
                Share (Free to Share and Use), ShareCommercially (Free to Share and Use Commercially),
                Modify (Free to Modify, Share, and Use), ModifyCommercially (Free to Modify, Share, and
                Use Commercially). Defaults to None.
            max_results: max number of results. If None, returns results only from the first response. Defaults to None.

        Returns:
            List of dictionaries with images search results.

        Raises:
            DuckDuckGoSearchException: Base exception for duckduckgo_search errors.
            RatelimitException: Inherits from DuckDuckGoSearchException, raised for exceeding API request rate limits.
            TimeoutException: Inherits from DuckDuckGoSearchException, raised for API request timeouts.

###### Parameters

- **keywords**: keywords for query.
- **region**: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
- **safesearch**: on, moderate, off. Defaults to "moderate".
- **timelimit**: Day, Week, Month, Year. Defaults to None.
- **size**: Small, Medium, Large, Wallpaper. Defaults to None.
- **color**: color, Monochrome, Red, Orange, Yellow, Green, Blue,
                Purple, Pink, Brown, Black, Gray, Teal, White. Defaults to None.
- **type_image**: photo, clipart, gif, transparent, line.
                Defaults to None.
- **layout**: Square, Tall, Wide. Defaults to None.
- **license_image**: any (All Creative Commons), Public (PublicDomain),
                Share (Free to Share and Use), ShareCommercially (Free to Share and Use Commercially),
                Modify (Free to Modify, Share, and Use), ModifyCommercially (Free to Modify, Share, and
                Use Commercially). Defaults to None.
- **max_results**: max number of results. If None, returns results only from the first response. Defaults to None.

###### Returns

List of dictionaries with images search results.

##### news

```python
news(self, keywords: 'str', region: 'str' = 'wt-wt', safesearch: 'str' = 'moderate', timelimit: 'str | None' = None, max_results: 'int | None' = None)
```

DuckDuckGo news search. Query params: https://duckduckgo.com/params.

        Args:
            keywords: keywords for query.
            region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
            safesearch: on, moderate, off. Defaults to "moderate".
            timelimit: d, w, m. Defaults to None.
            max_results: max number of results. If None, returns results only from the first response. Defaults to None.

        Returns:
            List of dictionaries with news search results.

        Raises:
            DuckDuckGoSearchException: Base exception for duckduckgo_search errors.
            RatelimitException: Inherits from DuckDuckGoSearchException, raised for exceeding API request rate limits.
            TimeoutException: Inherits from DuckDuckGoSearchException, raised for API request timeouts.

###### Parameters

- **keywords**: keywords for query.
- **region**: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
- **safesearch**: on, moderate, off. Defaults to "moderate".
- **timelimit**: d, w, m. Defaults to None.
- **max_results**: max number of results. If None, returns results only from the first response. Defaults to None.

###### Returns

List of dictionaries with news search results.

##### text

```python
text(self, keywords: 'str', region: 'str' = 'wt-wt', safesearch: 'str' = 'moderate', timelimit: 'str | None' = None, backend: 'str' = 'auto', max_results: 'int | None' = None)
```

DuckDuckGo text search. Query params: https://duckduckgo.com/params.

        Args:
            keywords: keywords for query.
            region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
            safesearch: on, moderate, off. Defaults to "moderate".
            timelimit: d, w, m, y. Defaults to None.
            backend: auto, html, lite. Defaults to auto.
                auto - try all backends in random order,
                html - collect data from https://html.duckduckgo.com,
                lite - collect data from https://lite.duckduckgo.com.
            max_results: max number of results. If None, returns results only from the first response. Defaults to None.

        Returns:
            List of dictionaries with search results, or None if there was an error.

        Raises:
            DuckDuckGoSearchException: Base exception for duckduckgo_search errors.
            RatelimitException: Inherits from DuckDuckGoSearchException, raised for exceeding API request rate limits.
            TimeoutException: Inherits from DuckDuckGoSearchException, raised for API request timeouts.

###### Parameters

- **keywords**: keywords for query.
- **region**: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
- **safesearch**: on, moderate, off. Defaults to "moderate".
- **timelimit**: d, w, m, y. Defaults to None.
- **backend**: auto, html, lite. Defaults to auto.
                auto - try all backends in random order,
                html - collect data from https://html.duckduckgo.com,
                lite - collect data from https://lite.duckduckgo.com.
- **max_results**: max number of results. If None, returns results only from the first response. Defaults to None.

###### Returns

List of dictionaries with search results, or None if there was an error.

##### videos

```python
videos(self, keywords: 'str', region: 'str' = 'wt-wt', safesearch: 'str' = 'moderate', timelimit: 'str | None' = None, resolution: 'str | None' = None, duration: 'str | None' = None, license_videos: 'str | None' = None, max_results: 'int | None' = None)
```

DuckDuckGo videos search. Query params: https://duckduckgo.com/params.

        Args:
            keywords: keywords for query.
            region: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
            safesearch: on, moderate, off. Defaults to "moderate".
            timelimit: d, w, m. Defaults to None.
            resolution: high, standart. Defaults to None.
            duration: short, medium, long. Defaults to None.
            license_videos: creativeCommon, youtube. Defaults to None.
            max_results: max number of results. If None, returns results only from the first response. Defaults to None.

        Returns:
            List of dictionaries with videos search results.

        Raises:
            DuckDuckGoSearchException: Base exception for duckduckgo_search errors.
            RatelimitException: Inherits from DuckDuckGoSearchException, raised for exceeding API request rate limits.
            TimeoutException: Inherits from DuckDuckGoSearchException, raised for API request timeouts.

###### Parameters

- **keywords**: keywords for query.
- **region**: wt-wt, us-en, uk-en, ru-ru, etc. Defaults to "wt-wt".
- **safesearch**: on, moderate, off. Defaults to "moderate".
- **timelimit**: d, w, m. Defaults to None.
- **resolution**: high, standart. Defaults to None.
- **duration**: short, medium, long. Defaults to None.
- **license_videos**: creativeCommon, youtube. Defaults to None.
- **max_results**: max number of results. If None, returns results only from the first response. Defaults to None.

###### Returns

List of dictionaries with videos search results.

## Functions

### research_with_web

```python
research_with_web(query)
```

Generate a CoT-enhanced response with trends using web data.

### web_search

```python
web_search(query, max_results=3)
```

Perform a DuckDuckGo search and fetch web content.

