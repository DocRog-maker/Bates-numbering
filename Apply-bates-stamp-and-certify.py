import os
from apryse_sdk import (
    PDFDoc,
    PDFNet,
    Stamper,
    PageSet,
    ColorPt,
    Font,
    Rect,
    SignatureWidget,
    DigitalSignatureField,
    VerificationOptions
	)

prefix = "STAMPER-"
start_number = 1
current_number = 0


def get_bates_number():
    global current_number
    if current_number == 0:
        current_number = start_number
    else:
        current_number += 1
    return f"{prefix}{current_number:06d}"


def require_env(name):
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value

def VerifySimple(in_docpath, in_public_key_file_path):
	doc = PDFDoc(in_docpath)
	print("==========")
	opts = VerificationOptions(VerificationOptions.e_compatibility_and_archiving)
	opts.EnableDigestVerification(True)


	result = doc.VerifySignedDigitalSignatures(opts)
		
	if result == PDFDoc.e_unsigned:
		print("Document has no signed signature fields.")
		return False
		# e_failure == bad doc status, digest status, or permissions status
		# (i.e. does not include trust issues, because those are flaky due to being network/config-related)
	elif result == PDFDoc.e_failure:
		print("Hard failure in verification on at least one signature.")
		return False
	elif result == PDFDoc.e_untrusted:
		print("Could not verify trust for at least one signature.")
		return False
	elif result == PDFDoc.e_unsupported:
		# If necessary, call GetUnsupportedFeatures on VerificationResult to check which
		# unsupported features were encountered (requires verification using 'detailed' APIs)
		print("At least one signature contains unsupported features.")
		return False
		# unsigned sigs skipped; parts of document may be unsigned (check GetByteRanges on signed sigs to find out)
	elif result == PDFDoc.e_verified:
		print("All signed signatures in document verified.")
		return True
	else:
		print(f"Document verification status {result}")
		

PDFNet.Initialize(require_env("APRYSE_SDK_KEY"))

source_pdf = "042338.pdf"
unsigned_output_pdf = "042338_bates_unsigned.pdf"
signed_output_pdf = "042338_bates_certified-hidden-widget.pdf"
edited_pdf = "042338_bates_certified-hidden-widget-edited.pdf"

doc = PDFDoc(source_pdf)
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
    stamper.StampText(doc, get_bates_number(), PageSet(i))

doc.Save(unsigned_output_pdf, 0)
doc.Close()

signing_doc = PDFDoc(unsigned_output_pdf)
signing_doc.InitSecurityHandler()
signature_field = signing_doc.CreateDigitalSignatureField("DocIntegritySignature")
signature_widget = SignatureWidget.Create(
    signing_doc, Rect(0,0,0,0), signature_field
)
signing_doc.GetPage(1).AnnotPushBack(signature_widget)

signature_field.SetDocumentPermissions(DigitalSignatureField.e_no_changes_allowed)
pfx_path = "./apryse.pfx"
pfx_password = "password"
signature_field.CertifyOnNextSave(pfx_path, pfx_password)
signature_field.SetReason("Document integrity protection")
signature_field.SetLocation("Automated workflow")

signing_doc.Save(signed_output_pdf, 0)
signing_doc.Close()

# This should pass
VerifySimple(signed_output_pdf, "./apryse.cer")

# This edited document should fail
VerifySimple(edited_pdf, "./apryse.cer")

PDFNet.Terminate()
