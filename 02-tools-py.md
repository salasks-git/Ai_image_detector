---

### 2. `02-tools-py.md`

```md
# Step 2: The Forensic Tools Backend

This file holds the image forensic logic. It rips EXIF data and creates an Error Level Analysis (ELA) heatmap to highlight compression differences (a common marker of AI manipulation).

## Instructions
1. Create a file named `tools.py` in your project folder.
2. Paste the following code and save it:

```python
import os
from PIL import Image, ImageChops, ImageEnhance
from PIL.ExifTags import TAGS

def extract_metadata(image_path: str) -> str:
    """Safely extracts hidden EXIF metadata from the image file."""
    try:
        img = Image.open(image_path)
        exif_data = img.getexif()
        if not exif_data:
            return "No hidden EXIF metadata found."
        
        metadata = []
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            metadata.append(f"{tag}: {value}")
        return "\n".join(metadata)
    except Exception as e:
        return f"Error reading metadata: {str(e)}"

def generate_ela_heatmap(image_path: str) -> str:
    """Generates an ELA heatmap by analyzing pixel compression differences."""
    heatmap_filename = "ela_heatmap.png"
    temp_filename = "temp_compression.jpg"
    
    try:
        # Open original and save a 90% quality JPEG copy
        img = Image.open(image_path).convert('RGB')
        img.save(temp_filename, 'JPEG', quality=90)
        temp_img = Image.open(temp_filename)
        
        # Calculate pixel-by-pixel mathematical difference
        ela_image = ImageChops.difference(img, temp_img)
        
        # Amplify the difference for the VLM
        extrema = ela_image.getextrema()
        max_diff = max([ex[1] for ex in extrema]) if extrema else 1
        scale = 255.0 / (max_diff if max_diff != 0 else 1)
        
        ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
        ela_image.save(heatmap_filename)
    finally:
        # Guarantee cleanup of temporary files to prevent disk bloating
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
            
    return heatmap_filename