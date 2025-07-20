
class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        list = []
        if self.props:
            for x, y in self.props.items():
                list.append(f' {x}="{y}"')
            return "".join(list)
        return ""
    
    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )
        
    def __repr__(self):
        return (
            f"HTMLNode(Tag: {self.tag}, "
            f"Value: {self.value}, Children: {self.children}, Props: {self.props}"
        )


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if not self.value:
            raise ValueError("leaf nodes must have a value")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"    
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        if not self.tag:
            raise ValueError("parent nodes must have a tag")
        if not self.children:
            raise ValueError("child node missing")
        collect = ""
        for i in self.children:
            collect += i.to_html()
        return f"<{self.tag}{self.props_to_html()}>{collect}</{self.tag}>"

    def repr(self):
        return f"Parentnode({self.tag}, children:{self.children}, {self.props})"
        
