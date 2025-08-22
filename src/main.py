from textnode import TextType, TextNode

def main():
    print("hello world") 
    textnode = TextNode("This is some anchor text", TextType.LINK_TEXT, "https://www.boot.dev")
    print(textnode)

if __name__ == "__main__":
    main()
