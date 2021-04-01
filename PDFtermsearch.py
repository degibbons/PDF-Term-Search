from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
import PyPDF2
import csv
import time
import re


def set_dpi_awareness():
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass


set_dpi_awareness()


class PDFtermscan(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PDF Term Reader")
        self.geometry("800x220")

        self.frame = UserInputFrame(self)
        self.frame.grid(row=0, column=0, sticky="NSEW")


class UserInputFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.pdf_filename = tk.StringVar()
        self.term_filename = tk.StringVar()
        self.status = tk.StringVar()
        self.status.set("Not Running")

        PDFlabel = ttk.Label(self, width=65, wraplength=600, textvariable=self.pdf_filename)
        TermListLabel = ttk.Label(self, width=65, wraplength=600, textvariable=self.term_filename)
        buttonPDF = ttk.Button(self, text="Select Your PDF File", command=self.browseforpdf)
        buttonTermList = ttk.Button(self, text="Select your .csv list of terms", command=self.browseforterms)
        buttonAnalyze = ttk.Button(self, text="Analyze", command=self.termscan)
        statusLabel = ttk.Label(self, textvariable=self.status)
        self.canvas = tk.Canvas(self, width=47, height=47, bg="black")
        self.canvas.grid(row=2, column=2)
        self.myrectangle = self.canvas.create_rectangle(5, 5, 45, 45, fill='red')

        buttonPDF.grid(column=0, row=0, sticky="NSW", padx=15, pady=15)
        buttonTermList.grid(column=0, row=1, sticky="NSW", padx=15, pady=15)
        PDFlabel.grid(column=1, row=0, sticky='NW', padx=15, pady=15)
        TermListLabel.grid(column=1, row=1, sticky='W', padx=15, pady=15)
        buttonAnalyze.grid(column=0, row=2, padx=15, pady=15, sticky="EW")
        statusLabel.grid(column=1, row=2, padx=15, pady=15, sticky="EW")

    def browseforpdf(self):
        temp_pdf_filename = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                                       filetypes=(("PDF files", "*.pdf*"), ("all files", "*.*")))
        self.pdf_filename.set(temp_pdf_filename)

    def browseforterms(self):
        temp_term_filename = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                                        filetypes=(("CSV files", "*.csv*"), ("all files", "*.*")))
        self.term_filename.set(temp_term_filename)

    def termscan(self):
        self.status.set("Currently Running")
        self.canvas.itemconfig(self.myrectangle, fill='yellow')
        fullTermList = []
        originalTermList = []
        fullTermCount = []
        with open(self.term_filename.get(), newline='') as csvfile:
            termList = csv.reader(csvfile, delimiter=',')
            for row in termList:
                term = row[0].rstrip()
                originalTermList.append(term)
                result = re.search('/', term)
                result2 = re.search('OR', term)
                if (result is None) and (result2 is None):
                    fullTermList.append([term])
                    fullTermCount.append([0])
                elif result is not None:
                    result1 = re.split(' / ', term)
                    if len(result1) == 2:
                        fullTermList.append([result1[0], result1[1]])
                        tempZeros = [0] * 2
                        fullTermCount.append(tempZeros)
                    elif len(result1) == 3:
                        fullTermList.append([result1[0], result1[1], result1[2]])
                        tempZeros = [0] * 3
                        fullTermCount.append(tempZeros)
                    elif len(result1) == 4:
                        fullTermList.append([result1[0], result1[1], result1[2], result1[3]])
                        tempZeros = [0] * 4
                        fullTermCount.append(tempZeros)
                    elif len(result1) == 5:
                        fullTermList.append([result1[0], result1[1], result1[2], result1[3], result1[4]])
                        tempZeros = [0] * 5
                        fullTermCount.append(tempZeros)
                    elif len(result1) == 6:
                        fullTermList.append([result1[0], result1[1], result1[2], result1[3], result1[4], result1[5]])
                        tempZeros = [0] * 6
                        fullTermCount.append(tempZeros)
                    elif len(result1) == 7:
                        fullTermList.append([result1[0], result1[1], result1[2], result1[3], result1[4], result1[5],
                                             result1[6]])
                        tempZeros = [0] * 7
                        fullTermCount.append(tempZeros)
                    elif len(result1) == 8:
                        fullTermList.append([result1[0], result1[1], result1[2], result1[3], result1[4], result1[5],
                                             result1[6], result1[7]])
                        tempZeros = [0] * 8
                        fullTermCount.append(tempZeros)
                    elif len(result1) == 9:
                        fullTermList.append([result1[0], result1[1], result1[2], result1[3], result1[4], result1[5],
                                             result1[6], result1[7], result1[8]])
                        tempZeros = [0] * 9
                        fullTermCount.append(tempZeros)
                    elif len(result1) == 10:
                        fullTermList.append([result1[0], result1[1], result1[2], result1[3], result1[4], result1[5],
                                             result1[6], result1[7], result1[8], result1[9]])
                        tempZeros = [0] * 10
                        fullTermCount.append(tempZeros)
                elif result2 is not None:
                    result1 = re.split(' OR ', term)
                    if len(result1) == 2:
                        fullTermList.append([result1[0], result1[1]])
                        tempZeros = [0] * 2
                        fullTermCount.append(tempZeros)
                    elif len(result1) == 3:
                        fullTermList.append([result1[0], result1[1], result1[2]])
                        tempZeros = [0] * 3
                        fullTermCount.append(tempZeros)
                    elif len(result1) == 4:
                        fullTermList.append([result1[0], result1[1], result1[2], result1[3]])
                        tempZeros = [0] * 4
                        fullTermCount.append(tempZeros)
                    elif len(result1) == 5:
                        fullTermList.append([result1[0], result1[1], result1[2], result1[3], result1[4]])
                        tempZeros = [0] * 5
                        fullTermCount.append(tempZeros)
                    elif len(result1) == 6:
                        fullTermList.append([result1[0], result1[1], result1[2], result1[3], result1[4], result1[5]])
                        tempZeros = [0] * 6
                        fullTermCount.append(tempZeros)
                    elif len(result1) == 7:
                        fullTermList.append([result1[0], result1[1], result1[2], result1[3], result1[4], result1[5],
                                             result1[6]])
                        tempZeros = [0] * 7
                        fullTermCount.append(tempZeros)
                    elif len(result1) == 8:
                        fullTermList.append([result1[0], result1[1], result1[2], result1[3], result1[4], result1[5],
                                             result1[6], result1[7]])
                        tempZeros = [0] * 8
                        fullTermCount.append(tempZeros)
                    elif len(result1) == 9:
                        fullTermList.append([result1[0], result1[1], result1[2], result1[3], result1[4], result1[5],
                                             result1[6], result1[7], result1[8]])
                        tempZeros = [0] * 9
                        fullTermCount.append(tempZeros)
                    elif len(result1) == 10:
                        fullTermList.append([result1[0], result1[1], result1[2], result1[3], result1[4], result1[5],
                                             result1[6], result1[7], result1[8], result1[9]])
                        tempZeros = [0] * 10
                        fullTermCount.append(tempZeros)
        # creating a pdf file object
        pdfFileObj = open(self.pdf_filename.get(), 'rb')
        # creating a pdf reader object
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        # printing number of pages in pdf file
        print(pdfReader.numPages)
        pageNumber = pdfReader.numPages
        for i in range(1, pageNumber):
            pageObj = pdfReader.getPage(i)
            fullstring = pageObj.extractText()
            termIndex = 0
            innerTermIndex = 0
            for x in fullTermList:
                for eachTerm in x:
                    y = '[^a-z]' + eachTerm + '[^a-z]'
                    occurrences = 0
                    for matches in re.finditer(y, fullstring, flags=re.IGNORECASE):
                        occurrences += 1
                    fullTermCount[termIndex][innerTermIndex] += occurrences
                    innerTermIndex += 1
                termIndex += 1
                innerTermIndex = 0
        pdfFileObj.close()
        finalTermCount = []
        for c in fullTermCount:
            finalTermCount.append(sum(c))

        with open('ResultsOut.csv', 'w') as output:
            index = 0
            for key in originalTermList:
                output.write("%s,%d\n" % (key, finalTermCount[index]))
                index += 1
        self.status.set("Finished")
        self.canvas.itemconfig(self.myrectangle, fill='green')


root = PDFtermscan()
root.mainloop()
