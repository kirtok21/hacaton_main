from fastapi import FastAPI, Request , Form
from pydantic_core.core_schema import time_schema
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
import os


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def show_time_form(request: Request):
    return templates.TemplateResponse("create_booking.html", {"request": request})



@app.post("/booking")
async def handle_time(
        room: str = Form(...),
        time_start: int = Form(...),
        time_end: int = Form(...),
        size: str = Form(...),
        week_day: str = Form(...)
):
    if time_start > time_end or time_start == time_end:
        return "время начала не может быть больше или быть равным времени конца"
    time_list = []
    file_path = "booking/"+week_day+"/"+size+".txt"

    if os.path.exists(file_path):
        with open(file_path, "r", encoding='utf-8') as f:
            for line in f:
                line = line.strip().split()
                if len(line) < 4:
                    continue
                if line[0] == room:
                    if time_start < int(line[2]) and time_end > int(line[1]):
                        return f'время занято.'
    with open(file_path, "a", encoding='utf-8') as f:
        f.write(f"{room} {time_start} {time_end} {current_user}\n")
        return f'вы успешно забронировали комнату {size} на время с {time_start} до {time_end}.'