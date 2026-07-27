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

def shrink_page_content(page):
    original_crop_box = page.GetCropBox()
    original_media_box = page.GetMediaBox()

    scale = 0.90
    page.Scale(scale)

    scaledCropBox = page.GetCropBox()
    centered_box = center_box(original_crop_box, scaledCropBox)    
    page.SetCropBox(centered_box)

    scaledMediaBox = page.GetMediaBox()
    centered_box = center_box(original_media_box, scaledMediaBox)
    page.SetMediaBox(centered_box)

def center_box(original_box, box):
    box.x1 = box.x1 - (original_box.Width() - box.Width()) / 2
    box.y1 = box.y1 - (original_box.Height() - box.Height()) / 2
    box.x2 = box.x1 + original_box.Width()
    box.y2 = box.y1 +original_box.Height()
    return box


PDFNet.Initialize(os.getenv("APRYSE_SDK_KEY"))

doc = PDFDoc("NoMargins.pdf")
doc.InitSecurityHandler()

# Configure the stamper
stamper = Stamper(Stamper.e_font_size, 12, 0)
stamper.SetAlignment(Stamper.e_horizontal_right, Stamper.e_vertical_bottom)
stamper.SetPosition(0.04, 0.02, True)
red = ColorPt(1, 0, 0)
font = Font.Create(doc.GetSDFDoc(), Font.e_courier, True)
stamper.SetFont(font)
stamper.SetFontColor(red)

for i in range(1, doc.GetPageCount() + 1):
    page = doc.GetPage(i)
    shrink_page_content(page)

    stamper.StampText(doc, get_bates_number(),  PageSet(i))

doc.Save("NoMargins_shrunk.pdf", 0)
doc.Close()

PDFNet.Terminate()
