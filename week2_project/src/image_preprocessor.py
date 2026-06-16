def preprocess_image(image_path, output_path=None):
    try:
        from PIL import Image
    except ModuleNotFoundError as error:
        raise RuntimeError("Pillow is required for image preprocessing") from error

    image = Image.open(image_path)
    gray = image.convert("L")

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        gray.save(output_path)

    return gray
