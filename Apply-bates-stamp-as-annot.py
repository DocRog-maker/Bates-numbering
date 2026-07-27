import os
from  apryse_sdk import PDFDoc, PDFNet, Stamper, PageSet, ColorPt, Font

prefix = "STAMPED-ANNOT-"
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

doc = PDFDoc("Bates_Numbering_Red_Background.pdf")
doc.InitSecurityHandler()

# Configure the stamper
stamper = Stamper(Stamper.e_font_size, 12, 0)
stamper.SetAlignment(Stamper.e_horizontal_right, Stamper.e_vertical_bottom)
stamper.SetPosition(0.14, 0.02, True)
stamper.SetAsAnnotation(True)

red = ColorPt(1, 0, 0)
font = Font.Create(doc.GetSDFDoc(), Font.e_courier, True)
stamper.SetFont(font)
stamper.SetFontColor(red)
# Stamper allows arbitrary rotations
# //stamper.SetRotation(-22)

for i in range(1, doc.GetPageCount() + 1):
    bates = get_bates_number()
    stamper.StampText(doc, bates ,  PageSet(i))
    # you can get the id of the created annotation since it will be the last one on the page
    page = doc.GetPage(i)
    lastAnnotNum= page.GetNumAnnots()
    lastAnnot = page.GetAnnot(lastAnnotNum-1)
    lastAnnot.SetContents(bates)
    id = lastAnnot.GetUniqueID()
    o = lastAnnot.GetSDFObj()
    o.PutText("T", "Bates")
    lastAnnot.RefreshAppearance()
    print(f"Annotation ID on page {i} is: {id.GetAsPDFText()}")

doc.Save("output_stamped_annotation.pdf", 0)
doc.Close()

PDFNet.Terminate()