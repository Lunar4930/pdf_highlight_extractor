#!/usr/bin/env python3
"""
PDF Highlight Extractor CLI

A command-line tool to extract highlights and annotation notes from PDF files.
Outputs can be formatted as plain text (.txt) or Markdown (.md) and saved to a specified directory.

Usage:
    python3 pdf_highlight_extractor.py [OPTIONS] PDF_FILES...

Arguments:
    PDF_FILES...            One or more PDF files to process

Options:
    -f, --format {txt,md}   Output format (default: txt)
    -o, --output-dir DIR    Directory to save output files. Created if it doesn't exist.

Examples:
    # Extract from a single file to Markdown in the current directory:
    python3 pdf_highlight_extractor.py --format md document.pdf

    # Extract from multiple files to a specific directory as .txt:
    python3 pdf_highlight_extractor.py -f txt -o ./notes doc1.pdf doc2.pdf
"""

import argparse
import os

import pymupdf

# PDF annotation types in PyMuPDF
ANNOT_TEXT = 0  # Text annotation code (often represented as a sticky note icon)
ANNOT_FREE_TEXT = 2  # Free Text annotation (text typed directly onto the page)
ANNOT_HIGHLIGHT = (
    8  # Highlight annotation code (text that has been highlighted with a marker tool)
)


def normalize_text(text):
    if not text:
        return ""
    return " ".join(text.split()).strip()


def format_item(item, out_format):
    if out_format == "md":
        block = f"Page {item['page']} \n"
        if item.get("highlightedText"):
            block += f'- Highlighted text: "_{item["highlightedText"]}_"\n'
        if item.get("noteText"):
            block += f"- Note: {item['noteText']}\n"
        return block + "\n"

    # txt format
    block = f"[Page {item['page']}] \n"
    if item.get("highlightedText"):
        block += f"Highlighted text: {item['highlightedText']}\n"
    if item.get("noteText"):
        block += f"Note: {item['noteText']}\n"
    return block + "\n"


def resolve_output_path(original_pdf, output_dir, out_format):
    base_name = os.path.splitext(os.path.basename(original_pdf))[0]
    filename = f"{base_name}_annotations.{out_format}"
    base_path = os.path.join(output_dir, filename)

    # Handle collisions by appending a number if file exists
    final_path = base_path
    counter = 1
    while os.path.exists(final_path):
        final_path = os.path.join(
            output_dir, f"{base_name}_annotations_{counter}.{out_format}"
        )
        counter += 1

    return final_path


def main():
    parser = argparse.ArgumentParser(
        description="Extract highlights and notes from PDFs"
    )
    parser.add_argument("pdf_files", nargs="+", help="One or more PDF files to process")
    parser.add_argument(
        "-f",
        "--format",
        choices=["md", "txt"],
        default="md",
        help="Output format (default: md)",
    )
    parser.add_argument(
        "-o", "--output-dir", default=".", help="Directory to save output files"
    )

    args = parser.parse_args()

    # Create output dir if needed
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
        print(f"Created output directory: {args.output_dir}")

    for pdf_path in args.pdf_files:
        if not os.path.exists(pdf_path):
            print(f"Error: The file '{pdf_path}' was not found. Skipping.")
            continue

        print(f"Processing {pdf_path}...")
        try:
            doc = pymupdf.open(pdf_path)
        except Exception as e:
            print(f"Failed to open {pdf_path}: {e}")
            continue

        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        extracted_data = []

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            annots = page.annots()
            if not annots:
                continue

            for annot in annots:
                info = annot.info
                note_text = normalize_text(info.get("content", ""))
                annot_id = info.get("id", "")

                if annot.type[0] == ANNOT_HIGHLIGHT:
                    highlighted_text = normalize_text(
                        page.get_text("text", clip=annot.rect)
                    )
                    if highlighted_text or note_text:
                        extracted_data.append(
                            {
                                "page": page_num + 1,
                                "type": "Highlight",
                                "highlightedText": highlighted_text,
                                "noteText": note_text,
                            }
                        )
                elif annot.type[0] in [ANNOT_TEXT, ANNOT_FREE_TEXT]:
                    subtype_str = "Text" if annot.type[0] == ANNOT_TEXT else "FreeText"
                    if not note_text:
                        id_text = f", id: {annot_id}" if annot_id else ""
                        note_text = f"No note text available (subtype: {subtype_str}{id_text}, page: {page_num + 1})"

                    extracted_data.append(
                        {
                            "page": page_num + 1,
                            "type": "Note",
                            "highlightedText": "",
                            "noteText": note_text,
                        }
                    )

        doc.close()

        if not extracted_data:
            print(f"No highlights or notes found in {pdf_path}.")
            continue

        output_path = resolve_output_path(pdf_path, args.output_dir, args.format)

        # Build the content block
        if args.format == "md":
            content = f"# Extracted Annotations for {base_name}\n\n"
        else:
            content = f"EXTRACTED ANNOTATIONS: {base_name}\n\n"

        for item in extracted_data:
            content += format_item(item, args.format)

        try:
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(content)

            highlight_count = sum(1 for i in extracted_data if i["type"] == "Highlight")
            note_count = sum(1 for i in extracted_data if i["type"] == "Note")

            print(
                f"Found {len(extracted_data)} items ({highlight_count} highlights, {note_count} notes)."
            )
            print(f"Saved successfully to: {output_path}")
        except IOError as e:
            print(f"Error saving file {output_path}: {e}")


if __name__ == "__main__":
    main()
