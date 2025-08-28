import cv2, numpy as np

BF = "BF1.png"          # path to your brightfield
HE = "HE1.png"          # path to your H&E

bf = cv2.imread(BF, cv2.IMREAD_COLOR)
he = cv2.imread(HE, cv2.IMREAD_COLOR)
assert bf is not None and he is not None, "Check BF/HE paths"

# resize HE to BF size if needed (keeps aspect by simple scale)
he = cv2.resize(he, (bf.shape[1], bf.shape[0]), interpolation=cv2.INTER_LINEAR)

# grayscale
g1 = cv2.cvtColor(bf, cv2.COLOR_BGR2GRAY)
g2 = cv2.cvtColor(he, cv2.COLOR_BGR2GRAY)

# ECC-based affine (robust & simple)
warp_mode = cv2.MOTION_AFFINE  # 2x3
warp = np.eye(2, 3, dtype=np.float32)
crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 5000, 1e-7)

(cc, warp) = cv2.findTransformECC(
    templateImage=g1, inputImage=g2, warpMatrix=warp,
    motionType=warp_mode, criteria=crit, inputMask=None, gaussFiltSize=5
)

he_aligned = cv2.warpAffine(he, warp, (bf.shape[1], bf.shape[0]),
                            flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REFLECT)

cv2.imwrite("HE _aligned1.png", he_aligned)
print("Saved HE_aligned1.png")