import json

import xmltodict


class Element(object):
    def __init__(self, name, attributes={}, cdata=""):
        self.attributes = attributes
        self._children = []
        self._is_root = False
        self.cdata = cdata
        self._origname = name

        if name:
            name = name.replace("-", "_")
            name = name.replace(".", "_")
            name = name.replace(":", "_")

        self._name = name

    def is_root(self, boolean):
        self._is_root = boolean

    def origname(self):
        if self._origname == "":
            return self._name
        return self._origname

    def create(self, name, attributes={}, cdata="",
               element=None):
        if not element:
            element = Element(name, attributes)
            element.cdata = cdata
        self._children.append(element)

    def add(self, element):
        self._children.append(element)

    def delete(self, name):
        index = 0
        for child in self._children:
            if child._origname == name:
                del self._children[index]
            index += 1

    def get_attributes(self, key=None):
        if key:
            return self.attributes.get(key)
        return self.attributes

    def get_elements(self, name=None):
        if name:
            return [e for e in self._children if e._name == name]
        else:
            return self._children

    def get_attributes_str(self):
        attr_string = ""
        if self.attributes and self.attributes != {}:
            for key in self.attributes.keys():
                value = self.attributes[key]
                attr_string += f" {key}=\"{value}\""
        return attr_string

    def dumps(self):
        xmlstr = ""
        attr_string = ""

        for child in self.get_elements():
            name = child.origname()
            cdata = child.cdata

            attr_string = ""
            attr_string = child.get_attributes_str()

            if child.get_elements() != [] or child.cdata != "":
                xmlstr += f"<{name}{attr_string}>"
            else:
                xmlstr += f"<{name}{attr_string}/>"

            if cdata != "":
                xmlstr += cdata

            xmlstr += child.dumps()

            if child.get_elements() != [] or child.cdata != "":
                xmlstr += f"</{name}>"

        return xmlstr

    def dumpj(self):
        data_dict = xmltodict.parse(self.dumps())
        json_data = json.dumps(data_dict)

        return json_data

    def __getitem__(self, key):
        return self.get_attributes(key=key)

    def __getattr__(self, key):
        matching_children = [x for x in self._children if x._name == key]
        if matching_children:
            if len(matching_children) == 1:
                self.__dict__[key] = matching_children[0]
                return matching_children[0]
            else:
                self.__dict__[key] = matching_children
                return matching_children
        else:
            raise AttributeError(
                "'%s' has no attribute '%s'" % (self._name, key))

    def __hasattribute__(self, name):
        if name in self.__dict__:
            return True
        return any(x._name == name for x in self._children)

    def __iter__(self):
        yield self

    def __str__(self):
        return self.cdata.strip()

    def __repr__(self):
        cdata = self.cdata.strip()

        return cdata

    def __bool__(self):
        return self._is_root or self._name is not None

    __nonzero__ = __bool__

    def __eq__(self, val):
        return self.cdata == val

    def __dir__(self):
        childrennames = [x._name for x in self._children]
        return childrennames

    def __len__(self):
        return len(self._children)

    def __contains__(self, key):
        return key in dir(self)
