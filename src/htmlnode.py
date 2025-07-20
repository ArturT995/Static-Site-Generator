
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


