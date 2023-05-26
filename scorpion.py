import sys
from PIL import Image
from PIL.ExifTags import TAGS

def display_image_metadata(image_paths :list):
	i = 0
	while i < len(image_paths):
		try:
			image = Image.open(image_paths[i])
			print(f"{i+1}.Image Metadata for: ", image_paths[i])
			exif_data = image._getexif()
			if exif_data is not None:
				for tag, value in exif_data.items():
					tag_name = TAGS.get(tag, tag)
					print(f"{tag_name}: {value}")

				print("---------------------------------")
			else:
				print("No EXIF metadata found.")
		except IOError:
			print(f"Error opening image: {image_paths[i]}")
		i +=1

# Extract the image file paths from command-line arguments (excluding the program name)
image_paths = sys.argv[1:]

# Check file extensions and call the function
valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
valid_image_paths =[]
for path in image_paths:
	if path.lower().endswith(valid_extensions):
		valid_image_paths.append(path)
display_image_metadata(valid_image_paths)
