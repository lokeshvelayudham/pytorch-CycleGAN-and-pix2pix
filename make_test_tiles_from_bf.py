from PIL import Image
import os, argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bf", default="BF1.png")
    ap.add_argument("--out", default="./datasets/cryoviz_AB/test")
    ap.add_argument("--tile", type=int, default=128)
    ap.add_argument("--overlap", type=int, default=32)
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    im = Image.open(args.bf).convert("RGB")
    W, H = im.size

    TILE, OVERLAP = args.tile, args.overlap
    stride = TILE - OVERLAP

    ix, grid = 0, []
    for y in range(0, max(1, H - TILE + 1), stride):
        row = []
        for x in range(0, max(1, W - TILE + 1), stride):
            im.crop((x, y, x+TILE, y+TILE)).save(f"{args.out}/a_{ix:05d}.png")
            row.append((x, y)); ix += 1
        grid.append(row)

    with open(f"{args.out}/grid.txt", "w") as f:
        f.write(f"{W} {H} {TILE} {OVERLAP}\n")
        for r in grid:
            f.write(",".join(f"{x}:{y}" for x, y in r) + "\n")

    print("Test tiles:", ix, "→", args.out)

if __name__ == "__main__":
    main()