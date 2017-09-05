import subprocess

def pdf2image(pathPDF, pathImage):
    params = ['magick', 'convert',
              # '-verbose',
              '-density', '200x200',
              # '-trim',
              pathPDF,
              '-quality', '100',
              # '-flatten',
              # '-sharpen', '0x1.0',
              pathImage]
    subprocess.check_call(params)

if __name__ == "__main__":
    pdf2image('sample_pdf/24072017105237.pdf', 'tmp/24072017105237.jpg')
