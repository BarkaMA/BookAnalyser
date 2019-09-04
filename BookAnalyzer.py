from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from re import findall
# --------------------------------------------------------------------------
# basic functions
# --------------------------------------------------------------------------


# read and convert PDF to TXT
def convert_pdf_to_txt(pdf_path, output_txt_file_path=None):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(pdf_path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,
                                  caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()
    if output_txt_file_path:
        with open(output_txt_file_path, "w") as ofp:

            ofp.write(text)

        return text
    else:
        return text


# count letters
def count_letters(txt):

    return len(findall('[a-zA-z]', txt))


# count words
def count_words(txt):

    return len(findall('([a-zA-z]{1,20})', txt))


# count numbers
def count_numbers(txt):

    return len(findall('([0-9]+)', txt))


# count_digits
def count_digits(txt):

    return len(findall('[0-9]', txt))


# count repetitions
def count_repetitions(pattern, txt):
    mixed = ''
    for index in range(len(pattern)):
        mixed += '({}|{})'.format(pattern[index].upper(), pattern[index].lower())
    return len(findall(mixed, txt))


# -------------------------------------------------------------------------
# Console ui
# -------------------------------------------------------------------------
print('         Welcome to BookAnalyzer \n')
pdf = input('Please copy the full path to your PDF file:\n>>> ')
txt = convert_pdf_to_txt(pdf)


def main():

    ch = input('select an option\n\n'
               '     0) about this script\n'
               '     1) count letters\n'
               '     2) count words\n'
               '     3) count repetitions of a Word/Phrase\n'
               '     4) count numbers ("1234" is counted as one number)\n'
               '     5) count digits  ("1234" is counted as 4 digits"\n'
               '     6) quit\n'
               '>>> ')

    if ch == '0':
        print('this script will help getting statistics of a pdf file content\n'
              '     hit ENTER to return')
        input()
        main()
    elif ch == '1':
        print('letters: ', count_letters(txt))
        input()
        main()
    elif ch == '2':
        print('words:   ', count_words(txt))
        input()
        main()
    elif ch == '3':
        pattern = input('type the word/Phrase:  ')
        print('"{}" was repeated {} times'.format(pattern, count_repetitions(pattern, txt)))
        input()
        main()
    elif ch == '4':
        print('numbers: ', count_numbers(txt))
        input()
        main()
    elif ch == '5':
        print('digits:  ', count_digits(txt))
    elif ch == '6':
        return 0


if __name__ == '__main__':
    main()
