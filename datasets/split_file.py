import sys

def split_csv(input_file, parts=64):
    with open(input_file, 'r', encoding='utf-8') as f:
        header = f.readline()

        total_lines = sum(1 for line in f)
        f.seek(0)

        header_line = f.readline()
        lines_per_part = (total_lines + parts - 1) // parts

        for i in range(parts):
            output_file = f"{input_file}_part{i+1}.csv"
            with open(output_file, 'w', encoding='utf-8') as out_f:
                out_f.write(header_line)

                for _ in range(lines_per_part):
                    line = f.readline()
                    if not line:
                        break
                    out_f.write(line)

            print(f"Created {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python split_csv.py your_file.csv [parts=8]")
        sys.exit(1)

    input_file = sys.argv[1]
    parts = int(sys.argv[2]) if len(sys.argv) > 2 else 64
    split_csv(input_file, parts)
