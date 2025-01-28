from django.shortcuts import render
from django.http import HttpResponse
import os
import time
from PIL import Image
import numpy as np
import cv2
import io

def load_image(img_file) -> Image:
    """Load an image from an uploaded file."""
    try:
        image = Image.open(img_file)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        print(f"Loaded image shape: {image.size}")
        return image
    except Exception as e:
        raise Exception(f"Error loading image: {str(e)}")

def create_hex_pattern(radius: int) -> np.ndarray:
    """Generate a hexagonal mask with the given radius."""
    height = int(np.sqrt(3) * radius)
    width = 2 * radius
    mask = np.zeros((height, width), dtype=np.float32)
    points = np.array([
        [width // 2, 0],
        [width, height // 2],
        [width // 2, height],
        [0, height // 2]
    ], np.int32)
    cv2.fillPoly(mask, [points], 1.0)
    
    mask = cv2.GaussianBlur(mask, (3, 3), 0.8)
    return mask

def apply_hexagonal_grid(image: np.ndarray, hex_radius: int) -> np.ndarray:
    """Apply hexagonal grid sampling to the image, averaging regions in hexagonal chunks."""
    hex_mask = create_hex_pattern(hex_radius)
    hex_height, hex_width = hex_mask.shape
    rows, cols, _ = image.shape
    hex_image = image.copy() 
    
    stride_y = hex_height // 3
    stride_x = hex_radius // 2
    
    for y in range(0, rows - hex_height + 1, stride_y):
        for x in range(0, cols - hex_width + 1, stride_x):
            region = image[y:y + hex_height, x:x + hex_width].astype(np.float32)
            

            masked_region = region * hex_mask[:, :, np.newaxis]
            mask_sum = np.sum(hex_mask)
            
            if mask_sum > 0:
                region_avg = np.sum(masked_region, axis=(0, 1)) / mask_sum
                
                blend_mask = hex_mask[:, :, np.newaxis]
                blended_region = (region * (1 - blend_mask * 0.8) +  
                                region_avg * blend_mask * 0.8) 
                
          
                current = hex_image[y:y + hex_height, x:x + hex_width]
                hex_image[y:y + hex_height, x:x + hex_width] = (
                    current * (1 - blend_mask * 0.7) + blended_region * blend_mask * 0.7
                ).astype(np.uint8)
    
    return hex_image

def compress_image(image: Image, quality: int = 50, hex_radius: int = 4) -> bytes:
    """Apply hexagonal grid processing and then compress the image using JPEG."""
    np_image = np.array(image)
    hex_image = apply_hexagonal_grid(np_image, hex_radius)
    hex_image_pil = Image.fromarray(hex_image.astype('uint8'))
    
    adjusted_quality = min(quality + 15, 90)  # More conservative quality boost
    
    buffer = io.BytesIO()
    hex_image_pil.save(buffer, format="JPEG", quality=adjusted_quality, optimize=True)
    return buffer.getvalue()

def compress_and_save(img_file, quality: int = 50, hex_radius: int = 4):
    """Main function to compress and save the image with hexagonal compression."""
    start_time = time.time()
    image = load_image(img_file)
    original_size = img_file.size
    print(f"Original image size: {original_size / (1024 * 1024):.2f} MB")
    
    compressed_data = compress_image(image, quality, hex_radius)
    compressed_size = len(compressed_data)
    print(f"Compressed image size: {compressed_size / (1024 * 1024):.2f} MB")
    print(f"Compression complete in {time.time() - start_time:.2f} seconds.")
    
    return compressed_data

def home(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            quality = int(request.POST.get('quality', 50))
            hex_radius = int(request.POST.get('hex_radius', 4))
            
            try:
                compressed_data = compress_and_save(image_file, quality, hex_radius)
                response = HttpResponse(compressed_data, content_type='image/jpeg')
                response['Content-Disposition'] = 'attachment; filename="compressed_image.jpg"'
                return response
            except Exception as e:
                return HttpResponse(f"Error processing image: {str(e)}", status=500)
    
    return render(request, 'compressor/index.html')