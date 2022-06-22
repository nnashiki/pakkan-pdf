import mimetypes
import os
import pathlib
import shutil
from io import StringIO

from pdfminer.high_level import extract_text, extract_text_to_fp

from pakkanpdf import exceptions

output_string = StringIO()

ALLOW_IMAGE_FILE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".tif", ".tiff", ".bmp"]


class PdfExtractor:
    def __init__(self, pdf_path, work_dir=".", work_img_dir="work_images"):
        # check pdf_path
        if not os.path.isfile(pdf_path):
            raise exceptions.NotFoundPdfException(f"{os.path.join(pathlib.Path.cwd(), pdf_path)} に PDFファイルが存在しません")
        mime_type = mimetypes.guess_type(pdf_path)[0]
        if mime_type != "application/pdf":
            raise exceptions.NotFoundPdfException(f"{pdf_path} に PDFファイルが存在しません")
        self.pdf_path = pathlib.Path(pdf_path).resolve()

        # check work_dir
        if not os.path.exists(work_dir):
            raise exceptions.NotFoundWorkingDirectoryError("work_dir 直下に一時的なディレクトリを作成するため、必ず work_dir が存在する必要があります。")
        self.work_dir = work_dir

        # check work_img_dir
        self.work_img_dir = os.path.join(work_dir, work_img_dir)
        if os.path.exists(self.work_img_dir):
            raise exceptions.DuplicatedWorkingImageDirectoryError("work_img_dir は最終的に削除されるため、存在するディレクトリを指定することができません")
        os.makedirs(self.work_img_dir, exist_ok=False)

    def __enter__(self):
        with open(self.pdf_path, "rb") as fin:
            extract_text_to_fp(fin, output_string, output_dir=f"{self.work_img_dir}")

        image_file_paths = []
        for root, _, files in os.walk(self.work_img_dir):
            for file in files:
                file_extension = os.path.splitext(file)[1]
                if file_extension in ALLOW_IMAGE_FILE_EXTENSIONS:
                    file_path = os.path.join(root, file)
                    image_file_paths.append(file_path)

        self.image_file_paths = image_file_paths
        self.text = extract_text(self.pdf_path)
        return self

    def __exit__(self, _, __, ___):

        shutil.rmtree(self.work_img_dir)
