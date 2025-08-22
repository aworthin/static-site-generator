import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://www.aw.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "http://www.aw.com")
        self.assertEqual(node, node2)

    def test_text_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a bold node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_type_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_neq(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://www.aw.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "http://www.caw.com")
        self.assertNotEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://www.aw.com")
        node2 = TextNode("This is a italic node", TextType.ITALIC, "http://www.caw.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.PLAIN, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, plain, https://www.boot.dev)", repr(node)
        )

if __name__ == "__main__":
    unittest.main()