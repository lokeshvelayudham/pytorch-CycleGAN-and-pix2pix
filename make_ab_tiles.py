from PIL import Image
import os

BF_PATH = "BF1.png"
HE_PATH = "HE_aligned1.png"
OUT_ROOT = "datasets/cryoviz_AB"
TILE = 128
OVERLAP = 32          # stride 96
VAL_EVERY = 6

os.makedirs(f"{OUT_ROOT}/train", exist_ok=True)
os.makedirs(f"{OUT_ROOT}/val", exist_ok=True)

bf = Image.open(BF_PATH).convert("RGB")
he = Image.open(HE_PATH).convert("RGB")
W, H = bf.size
assert he.size == (W, H), "Sizes differ; align first"

stride = TILE - OVERLAP
ix = 0
for y in range(0, max(1, H - TILE + 1), stride):
    for x in range(0, max(1, W - TILE + 1), stride):
        bf_t = bf.crop((x, y, x+TILE, y+TILE))
        he_t = he.crop((x, y, x+TILE, y+TILE))
        ab = Image.new("RGB", (TILE*2, TILE))
        ab.paste(bf_t, (0, 0))
        ab.paste(he_t, (TILE, 0))
        split = "val" if (ix % VAL_EVERY == 0) else "train"
        ab.save(f"{OUT_ROOT}/{split}/ab_{ix:05d}.png")
        ix += 1
print("Tiles written:", ix)