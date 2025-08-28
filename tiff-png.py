from PIL import Image
import os

def tiff_stack_to_png(input_tiff, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Open the stacked TIFF
    with Image.open(input_tiff) as img:
        # Loop through frames (slices)
        for i in range(img.n_frames):
            img.seek(i)  # Go to frame i
            frame = img.convert("RGBA")  # Convert for transparency support if needed
            output_path = os.path.join(output_folder, f"slice_{i:03d}.png")
            frame.save(output_path)
            print(f"Saved: {output_path}")

if __name__ == "__main__":
    input_tiff = "HE_no_compression.tif"  # path to your stacked TIFF
    output_folder = "png_slices2"     # folder to save PNGs
    tiff_stack_to_png(input_tiff, output_folder)