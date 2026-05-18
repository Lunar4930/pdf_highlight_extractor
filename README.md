# pdf_highlight_extractor

Extracts highlights and annotation notes from PDF documents as a summary. An open-source, free, and private alternative to paid PDF annotation extractors like [SumNotes](https://www.sumnotes.net/).

Access the tool at <https://aravindgopala.github.io/pdf_highlight_extractor/>.

#### Support the developers

| aravindgopala | Lunar4930 |
| ------------------- | ------------------ |
| [!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/aravinddatla) | [!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/bowrey) |


## ✨ Why this exists

Extracting highlights from PDFs is surprisingly difficult without paid software or privacy-compromising online converters. This tool solves that by:

- **100% Privacy:** All processing happens in your browser. No files are uploaded to a server.
- **Zero Cost:** MIT Licensed and open-source.
- **Note-Taking Ready:** Export highlights and annotation notes directly to Markdown for apps like Obsidian, Notion, or Roam Research.

## 🌐 Web App Usage

1. Visit the live tool: **<https://aravindgopala.github.io/pdf_highlight_extractor>**
2. Drag and drop your PDF into the upload zone.
3. Review your highlights and notes on the screen.
4. Click **Download .MD** or **Download .TXT** to save your notes.

## ⌨️ CLI Usage

The Python script is a command-line tool that can process one or more PDFs, outputting the extracted highlights and notes to `.txt` or `.md` files. 
A prebuilt Linux-only binary, `pdf_highlight_extractor.bin`, is available for running the CLI without installing Python dependencies. Download and run the binary directly on Linux systems. 
Otherwise, follow the instructions below to set up and run the CLI on any platform with Python 3.

#### Dependencies & Setup

You must have Python installed before using the CLI.

Clone the repository:

```bash
git clone <repository-url>
cd pdf_highlight_extractor
```

Install the dependencies from `requirements.txt`:

```bash
python3 -m pip install -r requirements.txt
```

Make the script executable:

```bash
chmod +x pdf_highlight_extractor.py
```

#### Execution & Parameters

**Basic Usage:**

```bash
./pdf_highlight_extractor.py document.pdf
```

**Options:**

- `-f, --format {md, txt}`: Output format (default: `md`)
- `-o, --output-dir DIR`: Directory to save output files (created if it doesn't exist)

#### Example Output

```text
$ ./pdf_highlight_extractor.py --format md -o ./notes example.pdf

Processing example.pdf...
Created output directory: ./notes
Found 5 items (3 highlights, 2 notes).
Saved successfully to: ./notes/example_annotations.md
```

## 🛠 Technical Details

- Built with **HTML5/CSS3** and **Vanilla JavaScript**.
- Powered by **PDF.js** (Mozilla) for high-performance PDF parsing.
- Handles common PDF "hiccups" like broken line breaks and coordinate mapping.

## 🔍 Annotation Debug Flag

The browser app includes a `DEBUG_ANNOTATION_EXTRACTION` flag in `index.html`.
Set it to `true` when troubleshooting missing note text: it logs annotation id, subtype, and available keys in the browser console for annotations where no note text could be resolved.
Keep it `false` in normal use to avoid noisy debug logs.

## ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
The pdf can be highlighted using any of the popular tools like Adobe Acrobat, Foxit reader etc
The summary is saved in the same directory as the pdf file named as `<filename>_summary.txt`
