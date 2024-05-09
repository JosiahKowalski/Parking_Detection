import PIL


class Parking_Lot:
    def __init__(self, name, image_path, parking_spots):
        self.name = name
        self.image_path = image_path
        self.parking_spots = parking_spots

    def get_pil_image(self):
        return PIL.Image.open(self.image_path)

    # to string
    def __str__(self):
        return self.name
