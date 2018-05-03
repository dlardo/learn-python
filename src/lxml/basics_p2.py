from lxml import etree

#XML with Attributes
bookstoreXML = '''
<bookstore>
  <book category="COOKING"><title lang="en">Everyday Italian</title>
    <author>Giada De Laurentiis</author>
    <year>2005</year>
    <price>30.00</price>
  </book>
  <book category="CHILDREN">
    <title lang="en">Harry Potter</title>
    <author>J K. Rowling</author>
    <year>2005</year>
    <price>29.99</price>
  </book>
  <book category="WEB">
    <title lang="en">Learning XML</title>
    <author>Erik T. Ray</author>
    <year>2003</year>
    <price>39.95</price>
  </book>
</bookstore>
'''

print("Importing XML into LXML object")
parser = etree.XMLParser(remove_blank_text=True)
bookstoreObj = etree.XML(bookstoreXML, parser)

#Note that this line also works but it makes pretty printing fail due to whitespaces.
# bookstoreObj = etree.fromstring(bookstoreXML)

print("Add a New Book called 'Learning OpenStack' to the tree")
bookObj = etree.SubElement(bookstoreObj, "book", category="DevOps")
etree.SubElement(bookObj, "title", lang="en").text = "Learning OpenStack"
etree.SubElement(bookObj, "author").text = "Doug StackdaMack"
etree.SubElement(bookObj, "year").text = "2015"
etree.SubElement(bookObj, "price").text = "100.00"
etree.SubElement(bookObj, "rating").text = "4 stars"

#XPath Deep Dive - http://lxml.de/xpathxslt.html#xpath and http://www.w3schools.com/xpath/xpath_syntax.asp
#When xpath() is used on an Element, the XPath expression is evaluated against the element (if relative) or against the root tree (if absolute)

#There are seven kinds of nodes: element, attribute, text, namespace, processing-instruction, comment, and document nodes.
#XML documents are treated as trees of nodes. The topmost element of the tree is called the root element.

#Expression  Description
# nodename    Selects all nodes with the name "nodename"
#    /        Selects from the root node
#   //        Selects nodes in the document from the current node that match the selection no matter where they are
#    .        Selects the current node
#   ..        Selects the parent of the current node
#    @        Selects attributes

print("Removing new book's rating element")
for bad in bookObj.xpath("rating"):
    bad.getparent().remove(bad)

print("Removing all year elements from the tree")
for item in bookObj.xpath("//year"):
    item.getparent().remove(item)

print("Adding year back in everywhere, but now it's 1999")
for item in bookObj.xpath("//book"):
    etree.SubElement(item, "year").text = "1999"

print("Changing price on harry potter to 40.00")
for item in bookObj.xpath("/bookstore/book/title"):
    if item.text == "Harry Potter":
        for price in item.getparent().xpath("price"):
            price.text = "40.00"

print("Adding 1.50 to the price of Learning XML")
from decimal import *  #Thanks floating point
for item in bookObj.xpath("/bookstore/book/title"):
    if item.text == "Learning XML":
        for price in item.getparent().xpath("price"):
            price.text = str(Decimal(price.text) + Decimal('1.50'))

print("\nFull XML:")
print(etree.tostring(bookstoreObj, pretty_print=True))

#Reference
'''
<type 'lxml.etree._Element'>
['__class__', '__contains__', '__copy__', '__deepcopy__', '__delattr__', '__delitem__', '__doc__', '__format__', '__getattribute__', '__getitem__', '__hash__', '__init__', '__iter__', '__len__', '__new__', '__nonzero__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', '_init', 'addnext', 'addprevious', 'append', 'attrib', 'base', 'clear', 'extend', 'find', 'findall', 'findtext', 'get', 'getchildren', 'getiterator', 'getnext', 'getparent', 'getprevious', 'getroottree', 'index', 'insert', 'items', 'iter', 'iterancestors', 'iterchildren', 'iterdescendants', 'iterfind', 'itersiblings', 'itertext', 'keys', 'makeelement', 'nsmap', 'prefix', 'remove', 'replace', 'set', 'sourceline', 'tag', 'tail', 'text', 'values', 'xpath']

<type 'module'> (etree)
['AncestorsIterator', 'AttributeBasedElementClassLookup', 'C14NError', 'CDATA', 'Comment', 'CommentBase', 'CustomElementClassLookup', 'DEBUG', 'DTD', 'DTDError', 'DTDParseError', 'DTDValidateError', 'DocInfo', 'DocumentInvalid', 'ETCompatXMLParser', 'ETXPath', 'Element', 'ElementBase', 'ElementChildIterator', 'ElementClassLookup', 'ElementDefaultClassLookup', 'ElementDepthFirstIterator', 'ElementNamespaceClassLookup', 'ElementTextIterator', 'ElementTree', 'Entity', 'EntityBase', 'Error', 'ErrorDomains', 'ErrorLevels', 'ErrorTypes', 'Extension', 'FallbackElementClassLookup', 'FunctionNamespace', 'HTML', 'HTMLParser', 'HTMLPullParser', 'LIBXML_COMPILED_VERSION', 'LIBXML_VERSION', 'LIBXSLT_COMPILED_VERSION', 'LIBXSLT_VERSION', 'LXML_VERSION', 'LxmlError', 'LxmlRegistryError', 'LxmlSyntaxError', 'NamespaceRegistryError', 'PI', 'PIBase', 'ParseError', 'ParserBasedElementClassLookup', 'ParserError', 'ProcessingInstruction', 'PyErrorLog', 'PythonElementClassLookup', 'QName', 'RelaxNG', 'RelaxNGError', 'RelaxNGErrorTypes', 'RelaxNGParseError', 'RelaxNGValidateError', 'Resolver', 'Schematron', 'SchematronError', 'SchematronParseError', 'SchematronValidateError', 'SerialisationError', 'SiblingsIterator', 'SubElement', 'TreeBuilder', 'XInclude', 'XIncludeError', 'XML', 'XMLDTDID', 'XMLID', 'XMLParser', 'XMLPullParser', 'XMLSchema', 'XMLSchemaError', 'XMLSchemaParseError', 'XMLSchemaValidateError', 'XMLSyntaxError', 'XMLTreeBuilder', 'XPath', 'XPathDocumentEvaluator', 'XPathElementEvaluator', 'XPathError','XPathEvalError', 'XPathEvaluator', 'XPathFunctionError', 'XPathResultError', 'XPathSyntaxError', 'XSLT', 'XSLTAccessControl', 'XSLTApplyError', 'XSLTError', 'XSLTExtension', 'XSLTExtensionError', 'XSLTParseError', 'XSLTSaveError', '_Attrib', '_BaseErrorLog', '_Comment', '_Document', '_DomainErrorLog', '_Element', '_ElementIterator', '_ElementMatchIterator', '_ElementStringResult', '_ElementTagMatcher', '_ElementTree', '_ElementUnicodeResult', '_Entity', '_ErrorLog', '_FeedParser', '_IDDict', '_ListErrorLog', '_LogEntry', '_ProcessingInstruction', '_RotatingErrorLog', '_SaxParserTarget', '_TargetParserResult', '_Validator', '_XPathEvaluatorBase', '_XSLTProcessingInstruction', '_XSLTResultTree', '__all__', '__builtins__', '__doc__', '__docformat__', '__file__', '__name__', '__package__', '__pyx_capi__', '__test__', '__version__', 'cleanup_namespaces', 'clear_error_log', 'dump', 'fromstring', 'fromstringlist', 'get_default_parser', 'htmlfile', 'iselement', 'iterparse', 'iterwalk', 'memory_debugger', 'parse', 'parseid', 'register_namespace', 'set_default_parser', 'set_element_class_lookup', 'strip_attributes', 'strip_elements', 'strip_tags', 'tostring', 'tostringlist', 'tounicode', 'use_global_python_log', 'xmlfile']

'''
