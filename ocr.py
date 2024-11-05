from flask import Flask, request
import base64
import os
from PIL import Image
from surya.detection import batch_text_detection
from surya.layout import batch_layout_detection
from surya.model.detection.segformer import load_model, load_processor
from surya.settings import settings
from PIL import Image
from unstructured.partition.pdf import partition_pdf


model = load_model(checkpoint=settings.LAYOUT_MODEL_CHECKPOINT)
processor = load_processor(checkpoint=settings.LAYOUT_MODEL_CHECKPOINT)
det_model = load_model()
det_processor = load_processor()


app = Flask(__name__)

@app.route('/unstructure',methods=['POST'])
def unstructure():
    file = request.files['file']
    extension=request.form.get("extension")
    name=request.form.get("name")
    file.save(f"./cache/{name}")
    if extension==".pdf":
        elements = partition_pdf(filename=f"./cache/{name}",
                      infer_table_structure=True,
                      strategy='hi_res',
                      languages=["zh"]
        )
        return [ [element.category, element.metadata.text_as_html,element.metadata.page_number]   for element in elements if element.category=="Table" ]



@app.route('/process_image', methods=['POST'])
def process_image():
    def image_to_base64(image):
        # 将图像转换为字节流
        img_byte_array = Image.new("RGB", image.size)
        img_byte_array.paste(image)
        with BytesIO() as buffer:
            img_byte_array.save(buffer, format="JPEG")
            img_bytes = buffer.getvalue()
        # 将字节流转换为 Base64 编码字符串
        base64_image = base64.b64encode(img_bytes).decode()
        return base64_image


    
    data = request.form.get('image_data')
    name = request.form.get('name')
    if data:
        try:
            # 解码 Base64 图片数据
            image_data = base64.b64decode(data)
            src="cache"
            # 这里可以对图片进行处理，比如保存到文件中等等
            # 你也可以将处理后的结果返回给客户端
            with open(os.path.join(src,name),'wb') as f:
                f.write(image_data)

            image=Image.open(os.path.join(src,name))
            # layout_predictions is a list of dicts, one per image
            line_predictions = batch_text_detection([image], det_model, det_processor)
            layout_predictions = batch_layout_detection([image], model, processor, line_predictions)
            
            return [ [layout.label,layout.bbox]  for layout in layout_predictions[0].bboxes]

                
        except Exception as e:
            return f'Error processing image: {str(e)}'
    else:
        return 'No image data received.'


if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=False, port=31500)