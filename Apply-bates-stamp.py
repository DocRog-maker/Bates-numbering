import os
from  apryse_sdk import PDFDoc, PDFNet, Stamper, PageSet, ColorPt, Font

prefix = "STAMPER-"
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

# Configure the stamper
stamper = Stamper(Stamper.e_font_size, 12, 0)
stamper.SetAlignment(Stamper.e_horizontal_right, Stamper.e_vertical_bottom)
stamper.SetPosition(0.04, 0.02, True)
red = ColorPt(1, 0, 0)
font = Font.Create(doc.GetSDFDoc(), Font.e_courier, True)
stamper.SetFont(font)
stamper.SetFontColor(red)
# stamper.SetRotation(-45)

for i in range(1, doc.GetPageCount() + 1):
    stamper.StampText(doc, get_bates_number(),  PageSet(i))

doc.Save("output_stamper.pdf", 0)
doc.Close()

PDFNet.Terminate()
