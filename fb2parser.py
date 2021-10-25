import xml.etree.ElementTree as ET
import chardet
import os
import glob
from shutil import copyfile
from xml.dom import minidom


class FBBook:
    def __init__(self, title, author, genre, annotation, text):
        self.title = title
        self.author = author
        self.genre = genre
        self.annotation = annotation
        self.text = text


class FB2Parser:
    def __init__(self):
        self.ns = {'prefix': 'http://www.gribuser.ru/xml/fictionbook/2.0'}

    def get_title(self, root):
        node = root.find('.//prefix:book-title', self.ns)
        if node is None or node.text is None:
            return 'Undefined title'
        else:
            return node.text

    def get_author(self, root):
        author = list()

        node_ln = root.find('.//prefix:last-name', self.ns)
        if node_ln is not None and node_ln.text is not None:
            author += [node_ln.text.strip()]

        node_fn = root.find('.//prefix:first-name', self.ns)
        if node_fn is not None and node_fn.text is not None:
            author += [node_fn.text.strip()]

        if author == []:
            return 'Undefined author'
        else:
            return ' '.join(author)

    def get_genre(self, root):
        node = root.find('.//prefix:genre', self.ns)
        if node is None or node.text is None:
            return 'Undefined genre'
        else:
            return node.text

    def get_annotation(self, root):
        annotation = "\n".join([(el.text if el.text is not None else "") 
            for el in root.findall('.//prefix:annotation//*', self.ns) 
            if len(el) == 0 and el is not None])

        if annotation.strip() == '':
            return 'Undefined annotation'
        else:
            return annotation


    def parse(self, filepath):
        """
        Create FBBook from the given xml file.

        filepath: path to the file
        return: FBBook
        """

        root = ET.parse(filepath).getroot()

        title = self.get_title(root)
        author = self.get_author(root)
        genre = self.get_genre(root)

        annotation = self.get_annotation(root)

        text = "\n".join([(el.text if el.text is not None else "") 
            for el in root.findall('.//prefix:body//*', self.ns) 
            if len(el) == 0 and el is not None])

        return FBBook(title, author, genre, annotation, text)


def get_books(directory):
    files = sorted(glob.glob(os.path.join(directory, "*.fb2")))

    books = dict()
    parser = FB2Parser()
    for filepath in files:
        book = parser.parse(filepath)
        books[filepath] = book
        # print("Read", filepath)
        yield book


if __name__ == '__main__':
    directory = './Books/'

        # print(*list(book.description.items()), sep='\n')
        # print(book.text)
        # author = book.description['last-name'] + " " + book.description['first-name']
        # title = book.description['title']
        # new_filepath = os.path.join(
        #     './',
        #     "{} - {}.fb2".format(author, title))
        # copyfile(filepath, new_filepath)
