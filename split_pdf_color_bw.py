import os
import argparse
import fitz  # pip install PyMuPDF
from pathlib import Path

def is_page_blank(page, blank_threshold=0.995):
    pix = page.get_pixmap(colorspace=fitz.csGRAY, alpha=False)
    data = pix.samples
    total = pix.width * pix.height
    white_pixels = sum(1 for v in data if v >= 250)
    return (white_pixels / total) >= blank_threshold


def is_page_color(page, color_threshold=0.01):
    pix = page.get_pixmap(colorspace=fitz.csRGB, alpha=False)
    data = pix.samples
    total = pix.width * pix.height
    color_pixels = sum(1 for i in range(0, len(data), 3)
                       if not (data[i] == data[i+1] == data[i+2]))
    return (color_pixels / total) >= color_threshold


def classify_pages(doc, blank_threshold, color_threshold):
    labels = []
    for page in doc:
        if is_page_blank(page, blank_threshold):
            labels.append('blank')
        elif is_page_color(page, color_threshold):
            labels.append('color')
        else:
            labels.append('black')
    return labels


def process_pairs(labels):
    categories = {
        'single_black': [],
        'single_color': [],
        'double_black': [],
        'double_color': []
    }
    n = len(labels)
    i = 0
    while i < n:
        p1 = i + 1
        lab1 = labels[i]
        lab2 = labels[i+1] if i+1 < n else None
        # 跳过纯空白对
        if lab1 == 'blank' and (lab2 == 'blank' if lab2 else True):
            pass
        else:
            # 判断 single 或 double
            if lab2 is None or lab1 == 'blank' or lab2 == 'blank':
                # single: 只保存非空白页
                pages = []
                if lab1 != 'blank':
                    pages.append(p1)
                if lab2 and lab2 != 'blank':
                    pages.append(p1+1)
                # 分类
                key = 'single_color' if any(labels[p-1] == 'color' for p in pages) else 'single_black'
                categories[key].extend(pages)
            else:
                # double: 保留两页
                pages = [p1, p1+1]
                key = 'double_color' if (lab1 == 'color' or lab2 == 'color') else 'double_black'
                categories[key].extend(pages)
        i += 2
    return categories


def split_and_write(src_path, out_dir, categories):
    src_doc = fitz.open(src_path)
    for cat, pages in categories.items():
        if not pages:
            continue
        out_doc = fitz.open()
        for p in pages:
            out_doc.insert_pdf(src_doc, from_page=p-1, to_page=p-1)
        out_path = Path(out_dir) / f"{cat}.pdf"
        out_doc.save(out_path)
        print(f"Written {len(pages)} pages to {out_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Split PDF into black-and-white and color parts considering duplex printing rules."
    )
    parser.add_argument('src', help='Source PDF file')
    parser.add_argument('outdir', help='Output directory')
    parser.add_argument('--blank-threshold', type=float, default=0.995,
                        help='Fraction of white pixels to consider a page blank')
    parser.add_argument('--color-threshold', type=float, default=0.001,
                        help='Fraction of color pixels to consider a page color')
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    doc = fitz.open(args.src)

    print("Classifying pages...")
    labels = classify_pages(doc, args.blank_threshold, args.color_threshold)
    black_pages = [i+1 for i, lab in enumerate(labels) if lab == 'black']
    color_pages = [i+1 for i, lab in enumerate(labels) if lab == 'color']
    blank_pages = [i+1 for i, lab in enumerate(labels) if lab == 'blank']
    print(f"Black pages: {black_pages}")
    print(f"Color pages: {color_pages}")
    print(f"Blank pages: {blank_pages}")

    print("Processing page pairs...")
    cats = process_pairs(labels)
    for k, v in cats.items():
        print(f"{k}: {v}")

    print("Splitting and saving PDFs...")
    split_and_write(args.src, args.outdir, cats)

if __name__ == '__main__':
    main()