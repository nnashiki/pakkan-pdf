from pakkanpdf import PdfExtractor, __version__


def test_version():
    assert __version__ == "0.1.3"


def test_sample():
    with PdfExtractor(pdf_path="data/example.pdf", work_dir="demo_work_dir") as extractor:
        assert "これはサンプルのPDFです" in extractor.text
        assert extractor.image_file_paths == ["demo_work_dir/work_images/X8.jpg"]
