import os
from  apryse_sdk import PDFDoc, PDFNet

prefix = "ANNOT-"
start_number = 1
current_number = 0
def get_bates_number():
    global current_number
    if (current_number == 0) :
        current_number = start_number
    else:
        current_number +=1
    return f"{prefix}{current_number:06d}"

PDFNet.Initialize(os.getenv("APRYSE_SDK_KEY"))

doc = PDFDoc("output_freetext.pdf")
doc.InitSecurityHandler()

doc.FlattenAnnotations()

doc.Save("output_freetext-flat.pdf", 0)
doc.Close()

PDFNet.Terminate()
