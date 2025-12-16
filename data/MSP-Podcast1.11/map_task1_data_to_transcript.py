
import argparse
import csv
import json
import re
from pathlib import Path

SPAN_COLS = ["Gold_Spans", "Annot1", "Annot2", "Annot3"]

def tokenize_with_spans(text):
    tokens = []
    for match in re.finditer(r"\S+", text):
        start, end = match.span()
        raw = text[start:end].strip().lower()
        norm = re.sub(r"^[^a-z0-9']+|[^a-z0-9']+$", "", raw)
        if norm:
            tokens.append((norm, start, end))
    return tokens


def apply_ranges_as_markers(transcript, ranges):
    tokens = tokenize_with_spans(transcript)
    if not tokens or not ranges:
        return transcript

    # Convert word-index ranges into character spans in the original string.
    spans = []
    for start_idx, end_idx in ranges:
        start_char = tokens[start_idx][1]
        end_char = tokens[end_idx - 1][2]
        spans.append((start_char, end_char))

    if not spans:
        return transcript

    # Build new string with ** markers inserted (assumes ranges are valid and non-overlapping).
    spans.sort()
    out_parts = []
    prev = 0
    for s, e in spans:
        out_parts.append(transcript[prev:s])
        out_parts.append("**" + transcript[s:e] + "**")
        prev = e
    out_parts.append(transcript[prev:])

    return "".join(out_parts)


def process_row(row, transcripts_dir):
    fname = (row.get("FileName") or "").strip()
    if not fname:
        return row

    stem = Path(fname).stem  # "MSP-PODCAST_0597_0382"
    txt_path = transcripts_dir / f"{stem}.txt"
    if not txt_path.exists():
        return row

    transcript = txt_path.read_text(encoding="utf-8")

    for col in SPAN_COLS:
        raw_val = row.get(col, "")
        if not raw_val:
            row[col] = transcript
            continue

        ranges = json.loads(raw_val)
        marked = apply_ranges_as_markers(transcript, ranges)
        row[col] = marked

    return row


def run(input_csv, transcripts_dir, output_csv):
    if not input_csv.exists():
        raise FileNotFoundError(f"Input CSV not found: {input_csv}")
    if not transcripts_dir.exists():
        raise FileNotFoundError(f"Transcript directory not found: {transcripts_dir}")

    with input_csv.open("r", encoding="utf-8", newline="") as f_in:
        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames
        if not fieldnames:
            raise ValueError(f"No header row found in {input_csv}")

        output_csv.parent.mkdir(parents=True, exist_ok=True)
        with output_csv.open("w", encoding="utf-8", newline="") as f_out:
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                updated = process_row(row, transcripts_dir=transcripts_dir)
                writer.writerow(updated)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Map Task 1 MSP-Podcast release CSV span ranges back to local "
            "manual transcripts with inline ** markers."
        )
    )
    parser.add_argument(
        "--input_csv",
        type=Path,
        help="Input Task1 release CSV",
        default='Task1_Data_Podcast_Release.csv'
    )
    parser.add_argument(
        "--transcript_dir",
        type=Path,
        help="Directory containing MSP-Podcast manual transcripts",
        required=True
    )
    parser.add_argument(
        "--output_csv",
        type=Path,
        help="Output CSV with inline spans",
        default='Task1_Data_Podcast_Reconstructed.csv'
    )
    args = parser.parse_args()
    run(
        input_csv=args.input_csv,
        transcripts_dir=args.transcript_dir,
        output_csv=args.output_csv,
    )