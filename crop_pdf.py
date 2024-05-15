import sys
from pypdf import PdfWriter, PdfReader


def main():
  for arg in sys.argv:
    if arg.endswith("pdf"):
      crop_file(arg, 5)

def crop_file(fn:str, pages:int):
  # get pages.
  reader = PdfReader(fn)
  total_pages = len(reader.pages) 
  for i in range(0,total_pages,pages):
    page_start = i+1
    page_end = min(i+pages, total_pages)
    print(page_start, page_end)
    crop_pages(fn, page_start, page_end) # [page_start, page_end]


def crop_pages(fn:str, page_start:int, page_end:int):

  reader = PdfReader(fn)
  writer = PdfWriter()
  for i in range(page_start-1,page_end):
     print(i)
     writer.add_page(reader.pages[i])

  # add some Javascript to launch the print window on opening this PDF.
  # the password dialog may prevent the print dialog from being shown,
  # comment the the encryption lines, if that's the case, to try this out:
  writer.add_js("this.print({bUI:true,bSilent:false,bShrinkToFit:true});")

  # write to document-output.pdf
  with open(f"{fn}.{page_start}-{page_end}.pdf", "wb") as fp:
    writer.write(fp)

if __name__ == '__main__':
  main()