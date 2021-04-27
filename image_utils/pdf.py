import fitz  # fitz: pip install PyMuPDF


def pdf2images(stream, zoom=2, color='RGB'):
    """pdf to images
    example: 
        stream = open(/path/to/pdf, 'rb')
        images = pdf2images(stream)
    """
    doc = fitz.open(stream)
    mat = fitz.Matrix(zoom, zoom)
    images = []
    # mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
    # for pg in range(doc.pageCount):
        # page = doc[pg]
    for page in doc:
        pix = page.getPixmap(matrix=mat, alpha=False)
        images.append(Image.frombytes(color, [pix.width, pix.height], pix.samples))

    return images