from rest_framework_xml import parsers


class XMLParser(parsers.XMLParser):
    """XML parser."""
    def _xml_convert(self, element):
        """Convert the xml `element` intor the corresponding python object.
        Since the parser provided by django cannot handle list item. I force overwrite
        this function to support this case.
        """
        children = list(element)

        if len(children) == 0:
            return self._type_convert(element.text)
        else:
            # if the fist child tag is list-item means all children are list-item
            if children[0].tag == 'element':
                data = []
                for child in children:
                    data.append(self._xml_convert(child))
            else:
                data = {}
                for child in children:
                    data[child.tag] = self._xml_convert(child)

            return data

