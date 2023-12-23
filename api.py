# from fastapi import FastAPI
# from prometheus_fastapi_instrumentator import Instrumentator
# from starlette.responses import JSONResponse
# import uvicorn
# import os
# from dotenv import load_dotenv, find_dotenv
# import storage

# load_dotenv(find_dotenv())

# app = FastAPI()
# Instrumentator().instrument(app).expose(app)

# """
# Отправка файла в хранилище и в брокер
# добавление состояния в таблицу
# """


# @app.post("/user/{vk_id}/{full_name}")
# async def create_user(vk_id: int, full_name: str):
#     storage.create_user(
#         vk_id=vk_id, full_name=full_name, contact="https://vk.com/id" + str(vk_id)
#     )
#     return JSONResponse({"status": 200})


# @app.get("/")
# async def homepage():
#     return JSONResponse({"hello": os.getenv(key="TEST")})


# @app.get("/user/{vk_id}")
# async def get_user(vk_id: int):
#     row = storage.get_user(vk_id=vk_id)
#     print("data: ", row)
#     return {
#         "status": 200,
#         "id": row[0],
#         "full_name": row[1],
#         "contact": row[2],
#         "role": row[3],
#         "balance": row[4],
#     }


# # @app.post("/upload/{end_ext}", tags=["file"])
# # def upload_file_api(file: UploadFile, end_ext: str):
# #     file_id = str(uuid4())
# #     try:
# #         filename = file.filename.split(".")[:-1]
# #         filename = "".join(filename)
# #         add_file(
# #             uuid=file_id,
# #             filename=filename,
# #             start_ext=file.filename.split(".")[-1],
# #             end_ext=end_ext,
# #         )
# #         upload_file(file=file.file, file_id=file_id)
# #         send_msg(text=file_id)
# #         change_status(uuid=file_id, state=1)
# #         return {
# #             "status": 200,
# #             "id": file_id,
# #             "response": "Проверить состояние файла",
# #             "url": f"http://127.0.0.1:8000/check/{file_id}",
# #         }
# #     except Exception as err:
# #         return {"status": 500, "error": err}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
