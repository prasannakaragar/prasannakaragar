import os
import numpy as np
from PIL import Image

src_path = r'C:\Users\Prasanna\.gemini\antigravity\brain\03ea2eae-0516-43d0-8dd1-78773706b7e0\.user_uploaded\media_1794277170434_c39d6592.png'
out_dir = r'C:\Projects\prasannakaragar\assets'

im = Image.open(src_path).convert('RGBA')
w, h = im.size

# We know the split column is between 428 and 435 where col_sum == 0
# Left is the stylized portrait (chest-up)
# Right is the pointing character (waist-up)

# Let's crop with appropriate margins
# Left character: x from 0 to 432
left_crop = im.crop((0, 0, 432, h))
# Right character: x from 432 to w
right_crop = im.crop((432, 0, w, h))

# Bounding box for right character to trim excessive right/bottom empty space while keeping padding
arr_right = np.array(right_crop)[:, :, 3]
rows = np.any(arr_right > 0, axis=1)
cols = np.any(arr_right > 0, axis=0)
rmin, rmax = np.where(rows)[0][[0, -1]]
cmin, cmax = np.where(cols)[0][[0, -1]]

# Add 8px breathing room around right character
pad = 8
cmin = max(0, cmin - pad)
cmax = min(right_crop.width - 1, cmax + pad)
rmin = max(0, rmin - pad)
rmax = min(right_crop.height - 1, rmax + pad)

right_final = right_crop.crop((cmin, rmin, cmax + 1, rmax + 1))

# For the left character (portrait), keep full height from top hair to bottom arc
arr_left = np.array(left_crop)[:, :, 3]
rows_l = np.any(arr_left > 0, axis=1)
cols_l = np.any(arr_left > 0, axis=0)
rmin_l, rmax_l = np.where(rows_l)[0][[0, -1]]
cmin_l, cmax_l = np.where(cols_l)[0][[0, -1]]

rmin_l = max(0, rmin_l - pad)
rmax_l = min(left_crop.height - 1, rmax_l + pad)
cmin_l = 0  # keep left shoulder intact
cmax_l = min(left_crop.width - 1, cmax_l + pad)

left_final = left_crop.crop((cmin_l, rmin_l, cmax_l + 1, rmax_l + 1))

id_path = os.path.join(out_dir, 'id.png')
rp_path = os.path.join(out_dir, 'right_pointing.png')

left_final.save(id_path, format='PNG', optimize=True)
right_final.save(rp_path, format='PNG', optimize=True)

print(f"Saved {id_path} with size {left_final.size}")
print(f"Saved {rp_path} with size {right_final.size}")

# Test composites on dark and light
dark_bg = Image.new('RGBA', left_final.size, (7, 11, 22, 255))
dark_composite = Image.alpha_composite(dark_bg, left_final)
light_bg = Image.new('RGBA', left_final.size, (255, 255, 255, 255))
light_composite = Image.alpha_composite(light_bg, left_final)

print("Alpha compositing test successful!")
