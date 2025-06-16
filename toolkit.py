def get_sample_image(breed, sample_image_folder="breeds_sample_images"):
    """
    Returns a sample image for the input breed.
    """
    filename = breed.lower()
    filename = " ".join(filename.split("-"))
    filename = "_".join(filename.split(" "))
    return f"{sample_image_folder}/{filename}.jpg"
