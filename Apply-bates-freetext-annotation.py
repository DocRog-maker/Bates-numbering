import os
from  apryse_sdk import PDFDoc, PDFNet, Stamper, PageSet, ColorPt, Font, Annot, Point, Rect, FreeText, BorderStyle

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

doc = PDFDoc("042338.pdf")
doc.InitSecurityHandler()

sdfdoc = doc.GetSDFDoc()


for i in range(1, doc.GetPageCount() + 1):
    ann = FreeText.Create(sdfdoc,  Rect(400, 10, 550, 25))
    ann.SetContents(get_bates_number())
    ann.SetQuaddingFormat(2)

    # Set the border width to zero to make it invisible
    ann.SetBorderStyle( BorderStyle( BorderStyle.e_solid, 0, 10, 20 ), True )
    o = ann.GetSDFObj()
    o.PutText("T", "Bates")
    red = ColorPt(1, 0, 0)
    # you need to specify the number of color components, in this case 3 for RGB
    ann.SetTextColor(red, 3)
    #remember to refresh appearance, else changes may not be visible
    ann.RefreshAppearance()
    # You can make the annotation readonly if you wish
    ann.SetFlag(Annot.e_read_only, True) 

    page = doc.GetPage(i)
    page.AnnotPushBack(ann)

    id = ann.GetUniqueID()
    print(f"Annotation ID on page {i} is: {id.GetAsPDFText()}")

doc.Save("output_freetext-red3aRightReadonly.pdf", 0)
doc.Close()

PDFNet.Terminate()
