import os
import io
import PIL
import requests

from fastapi import FastAPI
from roboflow import Roboflow
from io import BytesIO
from PIL import Image, ImageEnhance
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse ,FileResponse
from urllib.parse import urlparse

app = FastAPI()

rf = Roboflow(api_key="1F89RWy0r54slRLr8Uy6")
project = rf.workspace().project("floor_plan_detection")
model = project.version(3).model


@app.get('/')
def index():
    """Sample Function"""
    return("Hi User!")


@app.post("/get_image_by_file")
async def insert_image_by_file(insert_image: UploadFile=File(...)):

    contents = await insert_image.read() #Building image
    input_image = Image.open(BytesIO(contents)).convert("RGB")
    input_image.save("input_img.jpg")
    img_path = insert_image.filename

    def get_content_type(format_):
        
        type_ = "image/jpg"
        
        if format_ == "gif":
            type_ = "image/gif"
        elif format_ == "webp":
            type_ = "image/webp"
        elif format_ == "png":
            type_ = "image/png"
        elif format_ == "jpeg":
            type_ = "image/jpeg"
        
        return type_

    output_image = model.predict("input_img.jpg", confidence=40, overlap=30)
    output_image.save("result.jpg")    
    output_image = Image.open("result.jpg")
    format_ = output_image.format.lower()
    filename_img = os.path.basename(img_path)
    
    buf = BytesIO()
    output_image.save(buf,format=format_, quality=100)
    buf.seek(0)

    return StreamingResponse(buf,media_type=get_content_type(format_),headers={'Content-Disposition': 'inline; filename="%s"' %(filename_img)})


@app.post("/get_coordinates_by_file")
async def insert_image_by_file(insert_image: UploadFile=File(...)):

    contents = await insert_image.read() #Building image
    input_image = Image.open(BytesIO(contents)).convert("RGB")
    input_image.save("input_img.jpg")
    img_path = "input_img.jpg"

    obj_coordinates = model.predict("input_img.jpg", confidence=40, overlap=30).json()
    output_image = model.predict("input_img.jpg", confidence=40, overlap=30)
    output_image.save("result.jpg")    
    output_image = Image.open("result.jpg")
    format_ = output_image.format.lower()

    filename1 = (os.path.basename(img_path))
    buf = BytesIO()
    output_image.save(buf,format=format_, quality=100)
    buf.seek(0)

    return {"response" : obj_coordinates }


@app.post("/get_image_by_url")
async def insert_image_by_url(insert_image:str):
    try:
        response = requests.get(insert_image)
        
        if response.status_code == 200:
            
            image_bytes = io.BytesIO(response.content)
            input_image = Image.open(image_bytes).convert("RGB")
            input_image.save("input_img.jpg")

            def get_content_type(format_):
                
                type_ = "image/jpg"
                
                if format_ == "gif":
                    type_ = "image/gif"
                elif format_ == "webp":
                    type_ = "image/webp"
                elif format_ == "png":
                    type_ = "image/png"
                elif format_ == "jpeg":
                    type_ = "image/jpeg"
                
                return type_

            output_image = model.predict("input_img.jpg", confidence=40, overlap=30)
            output_image.save("result.jpg")    
            output_image = Image.open("result.jpg")
            format_ = output_image.format.lower()

            parsed = urlparse(insert_image)
            filename_img = os.path.basename(parsed.path)

            buf = BytesIO()
            output_image.save(buf,format=format_, quality=100)
            buf.seek(0)

            return StreamingResponse(buf,media_type=get_content_type(format_),headers={'Content-Disposition': 'inline; filename="%s"' %(filename_img)})
        else:
            return {"Invalid image url"}
    except:
        return {"Invalid image url"}


@app.post("/get_coordinate_by_url")
async def insert_image_by_url(insert_image:str):
    
    try:
        response = requests.get(insert_image)

        if response.status_code == 200:

            image_bytes = io.BytesIO(response.content)
            input_image = Image.open(image_bytes).convert("RGB")
            input_image.save("input_img.jpg")


            obj_coordinates = model.predict("input_img.jpg", confidence=40, overlap=30).json()
            output_image = model.predict("input_img.jpg", confidence=40, overlap=30)
            output_image.save("result.jpg")    
            output_image = Image.open("result.jpg")
            format_ = output_image.format.lower()
            
            parsed = urlparse(insert_image)
            filename_img = os.path.basename(parsed.path)
            
            buf = BytesIO()
            output_image.save(buf,format=format_, quality=100)
            buf.seek(0)

            return {"response" : obj_coordinates }
            
        else:
            return{"Invalid image url"}
    except:
        return{"Invalid image url"}
