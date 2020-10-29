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
        self.canvas.grid(row=2, column=1)
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
        termDict = {}
        combTerms = []
        time.sleep(1)
        with open(self.term_filename.get(), newline='') as csvfile:
            termList = csv.reader(csvfile, delimiter=',')
            for row in termList:
                term = row[0]
                termDict[term] = 0
            test = list(termDict.keys())
            for termA in test:
                result = re.search('/', termA)
                if result is None:
                    termDict[termA] = 0
                else:
                    result1 = re.split(' / ', termA)
                    if len(result1) == 2:
                        combTerms.append((result1[0], result1[1]))
                    elif len(result1) == 3:
                        combTerms.append((result1[0], result1[1], result1[2]))
                    for i in range(0, len(result1)):
                        termDict[result1[i]] = 0
            for a in combTerms:
                if len(a) == 2:
                    termDict[a[0]] = 0
                    termDict[a[1]] = 0
                elif len(a) == 3:
                    termDict[a[0]] = 0
                    termDict[a[1]] = 0
                    termDict[a[2]] = 0
            lines = len(list(termList))
            # print(combTerms)
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
            for x in termDict:
                occurences = fullstring.count(x)
                termDict[x] = termDict[x] + occurences
        pdfFileObj.close()
        for c in combTerms:
            if len(c) == 2:
                termDict[f'{c[0]} / {c[1]}'] = termDict[c[0]] + termDict[c[1]]
                termDict.pop(c[0], None)
                termDict.pop(c[1], None)
            elif len(c) == 3:
                termDict[f'{c[0]} / {c[1]} / {c[2]}'] = termDict[c[0]] + termDict[c[1]] + termDict[c[2]]
                termDict.pop(c[0], None)
                termDict.pop(c[1], None)
                termDict.pop(c[2], None)
        with open('ResultsOut.csv', 'w') as output:
            for key in termDict.keys():
                output.write("%s,%d\n" % (key, termDict[key]))
        self.status.set("Finished")
        self.canvas.itemconfig(self.myrectangle, fill='green')


root = PDFtermscan()
root.mainloop()
