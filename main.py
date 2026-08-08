from fastapi import FastAPI ,Request ,Form
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from selenium import webdriver
import json
import datetime
import randint

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def show_root(request: Request):
    return templates.TemplateResponse(request, "main.html")

@app.get("/reg", response_class=HTMLResponse)
async def reg(request: Request):
    return templates.TemplateResponse(request, "reg.html")

@app.post("/reg", response_class=HTMLResponse)
async def reg1(request: Request):
    data = await request.form()
    login = data['login']
    password = data['password']
    email = data['email']
    name = data['name']
    surname = data['surname']
    f=open("profiles.txt",'a')
    if login not in f.read():
        a=login+" "+password+" "+email+" "+name+" "+surname
        f.write(login+" "+password+" "+email+" "+name+" "+surname+" "+'\n')
        f.close()
        return templates.TemplateResponse(request, "hub.html")
    else:
        return "User already exists"

@app.get("/auth", response_class=HTMLResponse)
async def handle_log(request: Request):
    return templates.TemplateResponse(request, "auth.html")

@app.post("/auth", response_class=HTMLResponse)
async def handle_login(request: Request):
    authorisation = False
    data = await request.form()
    username=data['name']
    password=data['password']
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
                current_login=parts
                print(parts)
                authorisation = True
                break
    values = {
        "name": current_login[3],
        "surname": current_login[4],
        "email": current_login[2],
        "login": current_login[0]
    }
    if not(authorisation):
        return templates.TemplateResponse(request, "main.html")
    else:
        return templates.TemplateResponse(request, "hub.html", values)

@app.get("/hub", response_class=HTMLResponse)
async def handle_log(request: Request):
    return templates.TemplateResponse(request, "hub.html")

