from docx import Document
from docx.text.paragraph import Paragraph

f = open('test.docx', 'rb')
document = Document(f)
f.close()

paragraphs = []
for paragraph in  document.paragraphs:    
    texts = paragraph.text
    if texts:
        paragraphs.append(''.join(texts))


print("Done")
