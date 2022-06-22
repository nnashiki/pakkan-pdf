# pakkan-pdf

PDF 内の text や image へのアクセスをコンテキストマネージャーを使ってシンプルに行える。
[pdfminer/pdfminer.six](https://github.com/pdfminer/pdfminer.six) の Wrapper ライブラリです。

# install

`pip install pakkan-pdf`

# 使い方

- PdfExtractor の pdf_path に pdf のパスを与え、work_dir に存在するディレクトリを指定する
  - work_dir に image を書き出すための一時ディレクトリが作成さえる
- extractor.text を使うと、PDF の text を取得できる
- extractor.image_file_paths を使うと、PDF の image (file path) を取得できる

``` python3
from pakkanpdf import PdfExtractor

def test_sample():
    with PdfExtractor(pdf_path="data/example.pdf", work_dir="demo_work_dir") as extractor:
        assert "これはサンプルのPDFです" in extractor.text
        assert extractor.image_file_paths == ["demo_work_dir/work_images/X8.jpg"]

```