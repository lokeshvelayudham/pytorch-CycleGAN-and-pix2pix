

# stitch_tiles_generic.py
from PIL import Image
import numpy as np, os, re, argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--images", required=True, help="folder with tile outputs (e.g. ./results/cryo_pix2pix_128/test_latest/images)")
    ap.add_argument("--grid",   required=True, help="grid.txt saved during tiling (e.g. ./datasets/cryoviz_AB/test/grid.txt)")
    ap.add_argument("--out",    default="stitched.png", help="output path")
    ap.add_argument("--pattern", default=r"^(a_\d+)_fake.*\.png$", help="regex to match fake tiles")
    args = ap.parse_args()

    # read grid
    with open(args.grid) as f:
        W, H, TILE, OVERLAP = map(int, f.readline().split())
        rows = [line.strip() for line in f if line.strip()]
    coords = [[tuple(map(int, p.split(":"))) for p in row.split(",")] for row in rows]

    # collect tiles
    pat = re.compile(args.pattern, re.IGNORECASE)
    files = {m.group(1): fn for fn in os.listdir(args.images) if (m:=pat.match(fn))}
    if not files:
        raise SystemExit(f"No tiles matched in {args.images} with pattern {args.pattern}")

    # weight mask
    w = np.ones((TILE, TILE), dtype=np.float32)
    edge = OVERLAP // 2 if OVERLAP > 0 else 0
    if edge > 0:
        ramp = np.linspace(0, 1, edge, dtype=np.float32)
        w[:edge, :] *= ramp[:, None]; w[-edge:, :] *= ramp[::-1][:, None]
        w[:, :edge] *= ramp[None, :]; w[:, -edge:] *= ramp[None, ::-1]
    Wacc = np.zeros((H, W, 3), dtype=np.float32)
    Wsum = np.zeros((H, W, 1), dtype=np.float32)

    # place tiles in scan order a_00000, a_00001, ...
    idx = 0
    for row in coords:
        for (x, y) in row:
            key = f"a_{idx:05d}"
            fn = files.get(key)
            if fn:
                im = np.array(Image.open(os.path.join(args.images, fn)).convert("RGB"), dtype=np.float32)
                Wacc[y:y+TILE, x:x+TILE] += im * w[..., None]
                Wsum[y:y+TILE, x:x+TILE] += w[..., None]
            idx += 1

    out = (Wacc / np.maximum(Wsum, 1e-6)).clip(0,255).astype(np.uint8)
    Image.fromarray(out).save(args.out)
    print("Saved", args.out)

if __name__ == "__main__":
    main()