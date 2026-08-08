from fastapi import FastAPI ,Request ,Form
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
import json
import datetime
import random

admin_pass="admin"
app = FastAPI()
templates = Jinja2Templates(directory="templates")
user=[""]*5
room_list=list()
with open("rooms.txt",'r') as f:
    splt=f.read().split('\n')
    for i in splt:
        room_list.append(i.split()[1])

week_days=["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse(request, "main.html")

@app.get("/reg", response_class=HTMLResponse)
async def reg(request: Request):
    return templates.TemplateResponse(request, "reg.html")

@app.post("/reg", response_class=HTMLResponse)
async def reg1(request: Request,
               login: str=Form(...),
               password: str=Form(...),
               email: str=Form(...),
               name: str=Form(...),
               surname: str=Form(...)):
    global user
    data = await request.form()
    # login = data['login']
    # password = data['password']
    # email = data['email']
    # name = data['name']
    # surname = data['surname']
    f=open("profiles.txt",'a+')
    a=f.read()
    if login not in a:
        user=[login,password,email,name,surname]
        a=login+" "+password+" "+email+" "+name+" "+surname
        f.write(login+" "+password+" "+email+" "+name+" "+surname+" "+'\n')
        f.close()
        values = {
            "reply": None,
            "result": "hub"
        }
        return templates.TemplateResponse(request, "hub.html",values)
    else:
        values={
            "reply" : "Пользователь с таким логином уже есть, попробуйте авторизацию",
            "result": "reg"
        }
        return templates.TemplateResponse(request, "auth.html",values)

@app.get("/auth", response_class=HTMLResponse)
async def auth(request: Request):
    return templates.TemplateResponse(request, "auth.html")

@app.post("/auth", response_class=HTMLResponse)
async def auth1(request: Request,
                username: str=Form(...),
                password: str=Form(...)):
    global user
    authorisation = False
    data = await request.form()
    # username=data['name']
    # password=data['password']
    with open("profiles.txt", "r", encoding="utf-8") as file:
        for line in file:
            cleaned_line = line.strip()
            parts = cleaned_line.split()
            file_login = parts[0]
            file_password = parts[1]
            print(username,password)
            print(parts)
            print(file_login == username)
            print(file_password == password)
            if file_login == username and file_password == password:
                user = list(parts)
                print(parts)
                authorisation = True
                values = {
                    "name": user[3],
                    "surname": user[4],
                    "email": user[2],
                    "login": user[0]
                }
                break

    if not(authorisation):
        values = {
            "reply": "Неправильный пароль / Пользователя с таким логином не сущевствует"
        }
        return templates.TemplateResponse(request, "main.html",values)
    else:
        return templates.TemplateResponse(request, "hub.html", values)

@app.get("/hub", response_class=HTMLResponse)
async def hub(request: Request):
    return templates.TemplateResponse(request, "hub.html")

@app.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    global user
    values = {
        "name":user[3],
        "surname": user[4],
        "email": user[2],
        "login": user[0],
    }
    return templates.TemplateResponse(request, "profile.html",values)
@app.get("/clear_bookings", response_class=HTMLResponse):
async def clear_bookings(request: Request,
                         pasw: str=Form(...)):
    global admin_pass
    global room_list
    global
    if admin_pass==pasw:
        room_list = list()
        with open("rooms.txt", 'r') as f:
            splt = f.read().split('\n')
            for i in splt:
                room_list.append(i.split()[1])
        print(room_list)
        for i in room_list:
            for j in

@app.get("/all_bookings", response_class=HTMLResponse)
async def all_bookings(request: Request):
