# Color PDF Splitter: 按黑白/彩色及双面打印规则拆分PDF

本项目用于将 PDF 文件按页面内容（黑白、彩色、空白）分类，并结合双面打印规则，自动拆分为适合不同打印方式的多个 PDF 文件。适用于需要节省彩色打印成本、优化打印流程的场景，例如学术论文、毕业论文、报告等。

## 功能特性

将单个 PDF 拆分成多个 PDF 文件，便于打印时分开打印单面/双面、黑白/彩色页面。

- 自动识别每页是黑白、彩色还是空白
- 按双面打印（每两页为一组）规则分组
- 输出四类 PDF 文件：
  - `single_black.pdf`：单页黑白
  - `single_color.pdf`：单页彩色
  - `double_black.pdf`：双页均为黑白
  - `double_color.pdf`：双页有彩色页
- 支持自定义判定阈值

## 依赖环境

- Python 3.7+
- [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/en/latest/)

安装依赖：
```sh
pip install pymupdf
```

## 使用方法

```sh
python split_pdf_color_bw.py input.pdf output_dir
```

可选参数：

- `--blank-threshold`：判定空白页的白色像素比例（默认 0.995）
- `--color-threshold`：判定彩色页的彩色像素比例（默认 0.001）

示例：
```sh
python split_pdf_color_bw.py thesis.pdf ./output --blank-threshold 0.99 --color-threshold 0.002
```

## 输出说明

在 `output_dir` 下会生成如下文件（视实际内容而定）：

- `single_black.pdf`
- `single_color.pdf`
- `double_black.pdf`
- `double_color.pdf`

## 代码结构

- `split_pdf_color_bw.py`：主程序，包含页面分类、分组、PDF 拆分与保存等功能

## 参考

- [PyMuPDF 文档](https://pymupdf.readthedocs.io/en/latest/)

---

如有建议或问题，欢迎提交 Issue！