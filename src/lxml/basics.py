
from lxml import etree

#Simple XML Example
noteXML = '''
<note>
  <to>Tove</to>
  <from>Jani</from>
  <heading>Reminder</heading>
  <body>Don't forget me this weekend!</body>
</note>
'''

#Literal XML Example
literalXML = '''
<root>
   <element key='value'>text</element>
   <element>text</element>tail
   <empty-element/>
</root>
'''

#Working with lxml - http://lxml.de/tutorial.html

#Here we will construct the NoteXML above, using lxml and etree.

#Define a new tree.  Make the first element, which will become the root.
print("Building XML Tree")
noteXMLobj = etree.Element("note")

#Add subelements to the root element.  Also include the text values (optional)
etree.SubElement(noteXMLobj, "to").text = "Tove"
etree.SubElement(noteXMLobj, "from").text = "Jani"
etree.SubElement(noteXMLobj, "heading").text = "Reminder"
etree.SubElement(noteXMLobj, "body").text = "Don't forget me this weekend!"

#Find values using xpath.
#xpath searches the (entire?) tree for elements that match the pattern and outputs a list.
#If you are only expecting one result, you use list[0].text
print("\nSearching for body with xpath:")
findelement = noteXMLobj.xpath("body")

print("Found a <body> element:")
print("\t" + findelement[0].text)

#XML supports multiple tags with the same name under the same parent, and it's common.
#Example
# <siblings>
#   <name>bob</name>
#   <name>matt</name>
# </siblings>

#Add in a second body element
print("\nNow adding a second body element to the root tree & searching with xpath again:")
etree.SubElement(noteXMLobj, "body").text = "Bring an umbrella too!"

#Do another xpath lookup, this time returning 2 results.
findelement = noteXMLobj.xpath("body")

#If you might find more than one, loop through them
print("Found " + str(len(findelement)) + " items with XPath:")
for item in findelement:        #item is of <type 'lxml.etree._Element'>
    print("\t" + item.text)

print("\nFull XML:")
print(etree.tostring(noteXMLobj, pretty_print=True))

#Reference
'''
<type 'lxml.etree._Element'>
['__class__', '__contains__', '__copy__', '__deepcopy__', '__delattr__', '__delitem__', '__doc__', '__format__', '__getattribute__', '__getitem__', '__hash__', '__init__', '__iter__', '__len__', '__new__', '__nonzero__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', '_init', 'addnext', 'addprevious', 'append', 'attrib', 'base', 'clear', 'extend', 'find', 'findall', 'findtext', 'get', 'getchildren', 'getiterator', 'getnext', 'getparent', 'getprevious', 'getroottree', 'index', 'insert', 'items', 'iter', 'iterancestors', 'iterchildren', 'iterdescendants', 'iterfind', 'itersiblings', 'itertext', 'keys', 'makeelement', 'nsmap', 'prefix', 'remove', 'replace', 'set', 'sourceline', 'tag', 'tail', 'text', 'values', 'xpath']
'''


