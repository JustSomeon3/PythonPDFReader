import re
import PyPDF2 as pd
from googletrans import Translator


def read_pdf(file):
    pdf_file = open(file, 'rb')
    reader = pd.PdfFileReader(pdf_file)
    number_pages = reader.getNumPages()
    print(f'hay {number_pages} páginas')

    words = ""

    # Save all words as a string
    for page in range(number_pages):
        words += reader.getPage(page).extractText().lower()
        words += '\n'

    # Every url found in the pdf
    urls = re.findall("www\.[a0-z9]{1,}\.com", words, re.MULTILINE | re.IGNORECASE)

    # Every email found in the pdf
    emails = re.findall(".[^\s]+@.+\..[^\s]+", words, re.MULTILINE | re.IGNORECASE)

    # Every word from the pdf, no numbers or special characters
    every_word = re.findall("[A-Z\u00C0-\u017F]{2,}", words, re.MULTILINE | re.IGNORECASE)

    return every_word, urls, emails


def translatewords(words, bookName, links, mails):
    diction = dict()
    translator = Translator()
    count = 0
    file = open(f"Dictionary of {bookName}.txt", "a+")
    file.write(f"ENLACES : {links}\nEMAILS: {mails}\nWORDS:\n")
    # Translate and save in dictionary
    for i in words:
        translated = translator.translate(i, src='es', dest='en').text

        if i == translated:
            count += 1
            continue
        elif i in diction.keys():
            count += 1
            continue
        else:
            file.write(f"- {i}: {translated}\n")  # Appends the word and the translation in the file
            diction[words[count]] = translated  # saves the word in dictionary
        count += 1
    file.close()
    print("El archivo ha sido traducido, verifique la carpeta con el diccionario")


if __name__ == '__main__':
    # Detect every word in the pdf file. except connectors with length = 1
    book = 'Caperucita Roja.pdf'
    capturedWords, url, email = read_pdf(book)

    # Translate every word found in the book
    translatewords(capturedWords, book, url, email)
