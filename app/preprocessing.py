import io

import numpy as np
from PIL import Image


# ImageNet normalization values used by most ResNet-50 models.
IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
IMAGENET_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)


def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """Convert an image file into a tensor compatible with ResNet-50 ONNX.

    Returns:
        np.ndarray with shape [1, 3, 224, 224] and dtype float32.
    """
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((224, 224))

    image_array = np.asarray(image).astype(np.float32) / 255.0
    image_array = (image_array - IMAGENET_MEAN) / IMAGENET_STD
    image_array = image_array.transpose(2, 0, 1)
    image_array = np.expand_dims(image_array, axis=0)

    return image_array.astype(np.float32)
