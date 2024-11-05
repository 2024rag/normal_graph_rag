from model.mllm import describe_image

class image_obj():
    def __init__(self, img_obj, img_name):
        self.img_description = ""
        self.img_obj = img_obj
        self.img_name = img_name

    def describe(self):
        self.img_description = describe_image(self.img_obj, "请描述这个图片：")

