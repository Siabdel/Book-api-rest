from PyPDF2 import PdfFileWriter, PdfFileReader
import io
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Read CSV into pandas dataframe and assign columns as variables
csv = '/myfilepath/test.csv'
df = pd.read_csv(csv)
Name = df['First Name'].values + " " + df['Last Name'].values
OrderID = df['Order Number'].values

packet = io.BytesIO()

# create a new PDF with Reportlab
can = canvas.Canvas(packet, pagesize=letter)
can.setFont("Helvetica", 12)
if OrderID is not None:
    can.drawString(80, 655, '#' + str(OrderID)[1:-1])

can.setFont("Helvetica", 16)
if Name is not None:
    can.drawString(315, 630, str(Name)[2:-2]
can.save()

# move to the beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)

# read your existing PDF
existing_pdf = PdfFileReader(open("Unique1.pdf", "rb"))
output = PdfFileWriter()

# add the new pdf to the existing page
page = existing_pdf.getPage(0)
page2 = new_pdf.getPage(0)
page.mergePage(page2)
output.addPage(page)

# finally, write "output" to a real file
outputStream = open("Output.pdf", "wb")
output.write(outputStream)
outputStream.close()
