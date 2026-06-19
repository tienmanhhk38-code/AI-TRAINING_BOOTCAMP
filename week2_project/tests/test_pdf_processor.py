import sys
import types
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pdf_processor
from pdf_processor import extract_pdf_text


class FakePixmap:
    def tobytes(self, image_format):
        if image_format != "png":
            raise AssertionError(f"Unexpected image format: {image_format}")
        return b"fake-png-bytes"


class FakeScannedPage:
    def get_text(self, mode):
        if mode != "text":
            raise AssertionError(f"Unexpected text mode: {mode}")
        return ""

    def get_pixmap(self, matrix=None, alpha=False):
        return FakePixmap()


class FakeDoc:
    page_count = 1

    def __iter__(self):
        return iter([FakeScannedPage()])


class PdfProcessorTest(unittest.TestCase):
    def test_ocr_scanned_pdf_page_when_text_layer_is_empty(self):
        fake_fitz = types.SimpleNamespace(
            Matrix=lambda width, height: (width, height),
            open=lambda path: FakeDoc(),
        )
        fake_image_module = types.SimpleNamespace(open=lambda image_bytes: "image")
        fake_pil = types.SimpleNamespace(Image=fake_image_module)
        fake_tesseract = types.SimpleNamespace(
            image_to_string=lambda image, lang="eng": "OCR text",
            pytesseract=types.SimpleNamespace(tesseract_cmd=None),
        )

        original_modules = {
            name: sys.modules.get(name)
            for name in ("fitz", "PIL", "PIL.Image", "pytesseract")
        }

        sys.modules["fitz"] = fake_fitz
        sys.modules["PIL"] = fake_pil
        sys.modules["PIL.Image"] = fake_image_module
        sys.modules["pytesseract"] = fake_tesseract

        try:
            result = extract_pdf_text("scanned.pdf")
        finally:
            for name, original in original_modules.items():
                if original is None:
                    sys.modules.pop(name, None)
                else:
                    sys.modules[name] = original

        self.assertEqual(result, "--- Page 1 ---\nOCR text")

    def test_configures_tesseract_command_from_candidate_path(self):
        configure = getattr(pdf_processor, "configure_tesseract_command", None)
        self.assertIsNotNone(configure)

        with TemporaryDirectory() as temp_dir:
            tesseract_path = Path(temp_dir) / "tesseract.exe"
            tesseract_path.write_text("", encoding="utf-8")
            fake_tesseract = types.SimpleNamespace(
                pytesseract=types.SimpleNamespace(tesseract_cmd=None)
            )

            configured_path = configure(fake_tesseract, candidates=[tesseract_path])

        self.assertEqual(configured_path, str(tesseract_path))
        self.assertEqual(fake_tesseract.pytesseract.tesseract_cmd, str(tesseract_path))


if __name__ == "__main__":
    unittest.main()
