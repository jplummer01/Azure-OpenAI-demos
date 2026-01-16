
def create_directories():
    """Dirs creation"""
    os.makedirs(IMAGES_DIR, exist_ok=True)
    os.makedirs(LABELS_DIR, exist_ok=True)
    os.makedirs(ZIP_DIR, exist_ok=True)
    print(f"✅ Done. OUTPUT_DIR: {OUTPUT_DIR}")


def get_trainer_client():
    """ Get Azure Custom Vision client """
    credentials = ApiKeyCredentials(in_headers={"Training-key": TRAINING_KEY})
    trainer = CustomVisionTrainingClient(ENDPOINT, credentials)
    print(f"✅ Done")
    return trainer


def get_all_tags(trainer, project_id):
    """ Get all tags from the project """
    tags = trainer.get_tags(project_id)
    tags_dict = {tag.id: tag.name for tag in tags}
    print(f"✅ Done")
    print(f"{len(tags_dict)} TAGS: {list(tags_dict.values())}")
    return tags_dict


def get_tagged_images(trainer, project_id, batch_size=50):
    """ All tagged images """
    all_images = []
    skip = 0

    while True:
        images = trainer.get_tagged_images(project_id,
                                           take=batch_size,
                                           skip=skip)

        if not images:
            break

        all_images.extend(images)
        print(f"Processed {len(all_images)} images...")
        skip += batch_size

        if len(images) < batch_size:
            break

    print(f"\n✅ Done")
    print(f"Total: {len(all_images)} tagged images")
    return all_images


def download_image(url, filepath):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def list_projects(endpoint: str, training_key: str):
    """List all projects in the Custom Vision account."""
    credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
    trainer = CustomVisionTrainingClient(endpoint, credentials)

    projects = trainer.get_projects()
    print("Available projects:\n")
    
    for project in projects:
        print(f"  Name: {project.name}")
        print(f"  ID: {project.id}")
        print(f"  Description: {project.description or 'N/A'}")
        print()


def images_view(image_dir, n=12, cols=4):
    """
    Display images with size and dimension info.
    """
    valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}

    image_files = sorted([
        f for f in os.listdir(image_dir)
        if os.path.splitext(f)[1].lower() in valid_extensions
    ])[:n]

    if not image_files:
        print(f"⚠️ No images found in {image_dir}")
        return

    rows = (len(image_files) + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 4.5 * rows))
    axes = axes.flatten() if len(image_files) > 1 else [axes]

    print(f"🖼️ Displaying {len(image_files)} images from: {image_dir}\n")

    for idx, ax in enumerate(axes):
        if idx < len(image_files):
            img_path = os.path.join(image_dir, image_files[idx])
            img = Image.open(img_path)
            file_size = os.path.getsize(img_path) / 1024  # KB

            ax.imshow(img)
            ax.set_title(
                f"{image_files[idx][:15]}...\n{img.size[0]}x{img.size[1]} | {file_size:.1f}KB",
                fontsize=10)
            ax.axis('off')
        else:
            ax.axis('off')

    plt.tight_layout()
    plt.show()


def export_to_yolo_format(images, tags_dict, labels_dir):
    """
    Export annotations to YOLO format with debugging.
    """
    # Create mapping tag_id -> class_id
    tag_ids = list(tags_dict.keys())
    tag_to_class = {tag_id: idx for idx, tag_id in enumerate(tag_ids)}

    # Save classes.txt
    classes_file = os.path.join(os.path.dirname(labels_dir), "classes.txt")
    with open(classes_file, 'w', encoding='utf-8') as f:
        for tag_id in tag_ids:
            f.write(f"{tags_dict[tag_id]}\n")

    # Debug: Check first image
    print(f"\n🔍 Debug - First image inspection:")
    if images:
        img = images[0]
        print(f"   Image ID: {img.id}")
        print(f"   Has regions attr: {hasattr(img, 'regions')}")
        print(f"   Regions: {img.regions}")
        print(f"   Regions type: {type(img.regions)}")
        if img.regions:
            print(f"   Number of regions: {len(img.regions)}")
            region = img.regions[0]
            print(f"   First region: {region}")
            print(f"   Region attributes: {dir(region)}")
            print(f"   tag_id: {region.tag_id}")
            print(f"   left: {region.left}, top: {region.top}")
            print(f"   width: {region.width}, height: {region.height}")

    files_with_annotations = 0
    total_annotations = 0

    for image in images:
        filename = f"{image.id}.txt"
        filepath = os.path.join(labels_dir, filename)

        with open(filepath, 'w') as f:
            if image.regions and len(image.regions) > 0:
                for region in image.regions:
                    class_id = tag_to_class.get(region.tag_id, 0)

                    # Convert (left, top, width, height) to (x_center, y_center, width, height)
                    x_center = region.left + region.width / 2
                    y_center = region.top + region.height / 2

                    f.write(
                        f"{class_id} {x_center:.6f} {y_center:.6f} {region.width:.6f} {region.height:.6f}\n"
                    )
                    total_annotations += 1

                files_with_annotations += 1

    print(f"\n📊 YOLO Export Summary:")
    print(f"   📁 Total files created: {len(images)}")
    print(f"   ✅ Files with annotations: {files_with_annotations}")
    print(f"   🏷️  Total annotations written: {total_annotations}")
    print(f"   ⚠️  Empty files: {len(images) - files_with_annotations}")


def parse_yolo_label(label_path, img_width, img_height):
    """Parse YOLO format label file and convert to pixel coordinates."""
    boxes = []
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 5:
                    class_id = int(parts[0])
                    x_center = float(parts[1]) * img_width
                    y_center = float(parts[2]) * img_height
                    width = float(parts[3]) * img_width
                    height = float(parts[4]) * img_height

                    # Convert to top-left corner
                    x1 = x_center - width / 2
                    y1 = y_center - height / 2

                    boxes.append((class_id, x1, y1, width, height))
    return boxes


def images_view(images_dir, labels_dir, num_images=10):
    """Display images with their bounding boxes."""
    # Get image files
    image_extensions = ('.jpg', '.jpeg', '.png')
    image_files = sorted([
        f for f in os.listdir(images_dir)
        if f.lower().endswith(image_extensions)
    ])[:num_images]

    # Create figure
    cols = 2
    rows = (len(image_files) + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(20, 4 * rows))
    axes = axes.flatten() if len(image_files) > 1 else [axes]

    for idx, img_file in enumerate(image_files):
        # Load image
        img_path = os.path.join(images_dir, img_file)
        img = Image.open(img_path)
        img_width, img_height = img.size

        # Get corresponding label file
        label_file = os.path.splitext(img_file)[0] + '.txt'
        label_path = os.path.join(labels_dir, label_file)

        # Parse labels
        boxes = parse_yolo_label(label_path, img_width, img_height)

        # Display image
        axes[idx].imshow(img)
        axes[idx].set_title(f"{img_file}\n({len(boxes)} objects)", fontsize=14)
        axes[idx].axis('off')

        # Draw bounding boxes
        colors = [
            'red', 'green', 'blue', 'orange', 'purple', 
            'cyan', 'magenta', 'lime', 'pink', 'yellow', 
            'teal', 'coral', 'navy', 'maroon', 'salmon',
        ]
        
        for class_id, x, y, w, h in boxes:
            color = colors[class_id % len(colors)]
            rect = patches.Rectangle((x, y),
                                     w,
                                     h,
                                     linewidth=5,
                                     edgecolor=color,
                                     facecolor='none',
                                    )
            axes[idx].add_patch(rect)
            
            axes[idx].text(x,
                           y - 30,
                           f'Label {class_id+1}: {list(tags_dict.values())[class_id]}',
                           color=color,
                           fontsize=12,
                           bbox=dict(boxstyle='round',
                                     facecolor='white',
                                     alpha=0.8))

    # Hide empty subplots
    for idx in range(len(image_files), len(axes)):
        axes[idx].axis('off')

    plt.tight_layout()
    plt.show()


def parse_label_file(label_path):
    labels = []
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if parts:
                    class_id = int(parts[0])
                    labels.append(class_id)
    return labels


def get_class_name(class_id):
    return CLASS_NAMES.get(class_id, f"class_{class_id}")


def build_dataset_df(images_dir, labels_dir):
    data = []  
    image_files = sorted([f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.jpeg'))])
    
    for img_file in image_files:
        img_path = os.path.join(images_dir, img_file)
        base_name = Path(img_file).stem
        label_file = f"{base_name}.txt"
        label_path = os.path.join(labels_dir, label_file)
        
        labels = parse_label_file(label_path)
        label_counts = Counter(labels)
        
        label_names_counts = {get_class_name(k): v for k, v in label_counts.items()}
        
        total_objects = len(labels)
        unique_classes = list(set(get_class_name(l) for l in labels))
        
        data.append({
            'image_file': img_file,
            'image_path': img_path,
            'label_file': label_file if os.path.exists(label_path) else None,
            'label_path': label_path if os.path.exists(label_path) else None,
            'has_labels': os.path.exists(label_path),
            'total_objects': total_objects,
            'unique_classes': unique_classes,
            'num_unique_classes': len(unique_classes),
            'label_counts': label_names_counts
        })
    
    return pd.DataFrame(data)


def get_exif_data(image: Image.Image) -> dict:
    """Extract EXIF metadata from an image."""
    exif_data = {}
    try:
        exif = image._getexif()
        if exif:
            for tag_id, value in exif.items():
                tag = TAGS.get(tag_id, tag_id)
                if isinstance(value, bytes):
                    try:
                        value = value.decode("utf-8", errors="ignore")
                    except:
                        value = str(value)[:50]
                exif_data[tag] = value
    except Exception:
        pass
    return exif_data


def get_image_info(filepath: Path) -> Optional[dict]:
    """Extract comprehensive information from a single image file."""
    try:
        stat = filepath.stat()
        
        # Basic file info
        info = {
            "filename": filepath.name,
            "filepath": str(filepath),
            "extension": filepath.suffix.lower(),
            "file_size_bytes": stat.st_size,
            "file_size_kb": round(stat.st_size / 1024, 2),
            "file_size_mb": round(stat.st_size / (1024 * 1024), 4),
            "created_date": datetime.datetime.fromtimestamp(stat.st_ctime),
            "modified_date": datetime.datetime.fromtimestamp(stat.st_mtime),
            "accessed_date": datetime.datetime.fromtimestamp(stat.st_atime),
        }
        
        # Open image and extract properties
        with Image.open(filepath) as img:
            info["width"] = img.width
            info["height"] = img.height
            info["aspect_ratio"] = round(img.width / img.height, 3) if img.height > 0 else None
            info["megapixels"] = round((img.width * img.height) / 1_000_000, 2)
            info["format"] = img.format
            info["mode"] = img.mode  # RGB, RGBA, L (grayscale), etc.
            info["is_animated"] = getattr(img, "is_animated", False)
            info["n_frames"] = getattr(img, "n_frames", 1)
            
            # Color depth / bits per pixel
            mode_to_bits = {
                "1": 1, "L": 8, "P": 8, "RGB": 24, "RGBA": 32,
                "CMYK": 32, "YCbCr": 24, "LAB": 24, "HSV": 24,
                "I": 32, "F": 32, "LA": 16, "PA": 16, "RGBa": 32,
                "La": 16, "PA": 16
            }
            info["bits_per_pixel"] = mode_to_bits.get(img.mode, None)
            info["n_channels"] = len(img.getbands())
            info["channels"] = ", ".join(img.getbands())
            
            # DPI info
            dpi = img.info.get("dpi")
            if dpi:
                info["dpi_x"] = dpi[0]
                info["dpi_y"] = dpi[1]
            else:
                info["dpi_x"] = None
                info["dpi_y"] = None
            
            # EXIF data
            exif = get_exif_data(img)
            info["camera_make"] = exif.get("Make")
            info["camera_model"] = exif.get("Model")
            info["date_taken"] = exif.get("DateTimeOriginal") or exif.get("DateTime")
            info["exposure_time"] = exif.get("ExposureTime")
            info["f_number"] = exif.get("FNumber")
            info["iso"] = exif.get("ISOSpeedRatings")
            info["focal_length"] = exif.get("FocalLength")
            info["flash"] = exif.get("Flash")
            info["orientation"] = exif.get("Orientation")
            info["software"] = exif.get("Software")
            info["has_exif"] = len(exif) > 0
            
            # Transparency
            info["has_transparency"] = img.mode in ("RGBA", "LA", "PA") or "transparency" in img.info
            
        return info
        
    except Exception as e:
        return {
            "filename": filepath.name,
            "filepath": str(filepath),
            "error": str(e)
        }


def compute_channelwise_histogram(image_dir: str, bins: int = 256):
    """
    Compute and plot channel-wise pixel value histograms for all images in a directory.
    
    Args:
        image_dir: Path to the directory containing images
        bins: Number of bins for the histogram (default: 256 for 8-bit images)
    """
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp'}
    
    # Initialize accumulators for each channel
    hist_r = np.zeros(bins, dtype=np.int64)
    hist_g = np.zeros(bins, dtype=np.int64)
    hist_b = np.zeros(bins, dtype=np.int64)
    
    image_dir = Path(image_dir)
    image_files = [f for f in image_dir.rglob('*') 
                   if f.suffix.lower() in image_extensions]
    
    if not image_files:
        print(f"No images found in {image_dir}")
        return
    
    print(f"Processing {len(image_files)} images...")
    
    for img_path in image_files:
        try:
            img = Image.open(img_path).convert('RGB')
            img_array = np.array(img)
            
            # Accumulate histograms for each channel
            hist_r += np.histogram(img_array[:, :, 0].flatten(), bins=bins, range=(0, 256))[0]
            hist_g += np.histogram(img_array[:, :, 1].flatten(), bins=bins, range=(0, 256))[0]
            hist_b += np.histogram(img_array[:, :, 2].flatten(), bins=bins, range=(0, 256))[0]
            
        except Exception as e:
            print(f"Error processing {img_path.name}: {e}")
    
    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    x = np.arange(bins)
    
    # Individual channel histograms
    axes[0, 0].fill_between(x, hist_r, color='red', alpha=0.7)
    axes[0, 0].set_title('Red Channel', fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel('Pixel Value')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].set_xlim(0, 255)
    
    axes[0, 1].fill_between(x, hist_g, color='green', alpha=0.7)
    axes[0, 1].set_title('Green Channel', fontsize=12, fontweight='bold')
    axes[0, 1].set_xlabel('Pixel Value')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].set_xlim(0, 255)
    
    axes[1, 0].fill_between(x, hist_b, color='blue', alpha=0.7)
    axes[1, 0].set_title('Blue Channel', fontsize=12, fontweight='bold')
    axes[1, 0].set_xlabel('Pixel Value')
    axes[1, 0].set_ylabel('Frequency')
    axes[1, 0].set_xlim(0, 255)
    
    # Combined overlay
    axes[1, 1].plot(x, hist_r, color='red', alpha=0.7, label='Red', linewidth=1.5)
    axes[1, 1].plot(x, hist_g, color='green', alpha=0.7, label='Green', linewidth=1.5)
    axes[1, 1].plot(x, hist_b, color='blue', alpha=0.7, label='Blue', linewidth=1.5)
    axes[1, 1].set_title('All Channels Overlay', fontsize=12, fontweight='bold')
    axes[1, 1].set_xlabel('Pixel Value')
    axes[1, 1].set_ylabel('Frequency')
    axes[1, 1].set_xlim(0, 255)
    axes[1, 1].legend()
    
    fig.suptitle(f'Channel-wise Pixel Histograms\n({len(image_files)} images from {image_dir.name})', 
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    output_path = image_dir / 'channelwise_histogram.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.show()
    
    print(f"\nHistogram saved to: {output_path}")
    
    return {'red': hist_r, 'green': hist_g, 'blue': hist_b}


def analyze_images(directory: str, recursive: bool = True) -> pd.DataFrame:
    """
    Analyze all images in a directory and return a DataFrame with metadata.
    
    Parameters:
    -----------
    directory : str
        Path to the directory containing images
    recursive : bool
        If True, search subdirectories as well
        
    Returns:
    --------
    pd.DataFrame
        DataFrame containing image metadata
    """
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", 
                        ".webp", ".ico", ".svg", ".heic", ".heif", ".raw", ".cr2", 
                        ".nef", ".arw", ".dng"}
    
    dir_path = Path(directory)
    if not dir_path.exists():
        raise ValueError(f"Directory not found: {directory}\n")
    
    # Find all image files
    if recursive:
        files = [f for f in dir_path.rglob("*") if f.suffix.lower() in image_extensions]
    else:
        files = [f for f in dir_path.glob("*") if f.suffix.lower() in image_extensions]
    
    print(f"Found {len(files)} image files in '{directory}'")
    
    # Process each image
    results = []
    for i, filepath in enumerate(files, 1):
        if i % 100 == 0:
            print(f"Processing {i}/{len(files)}...")
        info = get_image_info(filepath)
        if info:
            results.append(info)
    
    df = pd.DataFrame(results)
    
    # Reorder columns for better readability
    priority_cols = [
        "filename", "filepath", "extension", "format", "width", "height",
        "aspect_ratio", "megapixels", "mode", "n_channels", "channels",
        "bits_per_pixel", "file_size_kb", "file_size_mb",
        "created_date", "modified_date", "date_taken",
        "has_exif", "camera_make", "camera_model"
    ]
    
    other_cols = [c for c in df.columns if c not in priority_cols]
    ordered_cols = [c for c in priority_cols if c in df.columns] + other_cols
    df = df[ordered_cols]
    print("Done")
    
    return df


def print_summary(df: pd.DataFrame):
    """Print a summary of the image analysis."""
    print("\n" + "=" * 60)
    print("IMAGE DATASET SUMMARY")
    print("=" * 60)
    
    print(f"\nTotal images: {len(df)}")
    
    if "error" in df.columns:
        errors = df["error"].notna().sum()
        if errors > 0:
            print(f"Failed to process: {errors} images")
    
    # Format distribution
    if "format" in df.columns:
        print("\n📁 Format Distribution:")
        print(df["format"].value_counts().to_string())
    
    # Dimensions
    if "width" in df.columns and "height" in df.columns:
        print("\n📐 Dimensions:")
        print(f"  Width:  min={df['width'].min()}, max={df['width'].max()}, mean={df['width'].mean():.0f}")
        print(f"  Height: min={df['height'].min()}, max={df['height'].max()}, mean={df['height'].mean():.0f}")
    
    # File sizes
    if "file_size_mb" in df.columns:
        print("\n💾 File Sizes:")
        print(f"  Total: {df['file_size_mb'].sum():.2f} MB")
        print(f"  Mean:  {df['file_size_mb'].mean():.2f} MB")
        print(f"  Min:   {df['file_size_mb'].min():.4f} MB")
        print(f"  Max:   {df['file_size_mb'].max():.2f} MB")
    
    # Color modes
    if "mode" in df.columns:
        print("\n🎨 Color Modes:")
        print(df["mode"].value_counts().to_string())
    
    # EXIF data
    if "has_exif" in df.columns:
        exif_count = df["has_exif"].sum()
        print(f"\n📷 Images with EXIF data: {exif_count} ({100*exif_count/len(df):.1f}%)")
    
    # Cameras
    if "camera_model" in df.columns:
        cameras = df["camera_model"].dropna().value_counts()
        if len(cameras) > 0:
            print("\n📸 Camera Models:")
            print(cameras.head(10).to_string())

