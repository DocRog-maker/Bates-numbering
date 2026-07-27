import os
from apryse_sdk import PDFDoc, PDFNet

INPUT_PATH = "output_freetext-added-annots.pdf"
OUTPUT_PATH = "output_freetext-added-annots-flat.pdf"
BATES_TITLE = "Bates"


def get_annotation_title(annot):
    sdf_obj = annot.GetSDFObj()
    if not sdf_obj:
        return ""
    title_obj = sdf_obj.FindObj("T")
    if not title_obj:
        return ""
    return title_obj.GetAsPDFText()


def remove_annotations_not_matching_title(doc, title_to_keep):
    page_iter = doc.GetPageIterator()
    while page_iter.HasNext():
        page = page_iter.Current()
        index = 0
        while index < page.GetNumAnnots():
            annot = page.GetAnnot(index)
            if get_annotation_title(annot) != title_to_keep:
                page.AnnotRemove(index)
            else:
                index += 1
        page_iter.Next()


def remove_annotations_matching_title(doc, title_to_remove):
    page_iter = doc.GetPageIterator()
    while page_iter.HasNext():
        page = page_iter.Current()
        index = 0
        while index < page.GetNumAnnots():
            annot = page.GetAnnot(index)
            if get_annotation_title(annot) == title_to_remove:
                page.AnnotRemove(index)
            else:
                index += 1
        page_iter.Next()


PDFNet.Initialize(os.getenv("APRYSE_SDK_KEY"))

doc_bates_only = PDFDoc(INPUT_PATH)
doc_non_bates_only = PDFDoc(INPUT_PATH)

# # Keep only Bates annotations in this document, then flatten them.
remove_annotations_not_matching_title(doc_bates_only, BATES_TITLE)
doc_bates_only.FlattenAnnotations()

# Keep only non-Bates annotations in this document, then export them.
remove_annotations_matching_title(doc_non_bates_only, BATES_TITLE)
non_bates_fdf = doc_non_bates_only.FDFExtract(PDFDoc.e_annots_only)


# Re-apply non-Bates annotations after Bates annotations are flattened.
doc_bates_only.FDFUpdate(non_bates_fdf)

doc_bates_only.Save(OUTPUT_PATH, 0)
doc_non_bates_only.Close()
doc_bates_only.Close()

PDFNet.Terminate()
