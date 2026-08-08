from fastapi import FastAPI ,Request ,Form
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
import json
import datetime
import random
#8 9 10 11 12 13 14 15 16 17 18 19 20
admin_pass="admin"
app = FastAPI()
templates = Jinja2Templates(directory="templates")
user=[""]*5
room_list=list()
with open("rooms.txt",'r') as f:
    splt=f.read().split('\n')
    for i in splt:
        room_list.append(i.split()[1])
values={}
success=False
week_days=["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse(request, "main.html")

@app.get("/reg", response_class=HTMLResponse)
async def reg(request: Request):
    return templates.TemplateResponse(request, "reg.html")

@app.post("/reg", response_class=HTMLResponse)
async def reg(request: Request,
               login: str=Form(...),
               password: str=Form(...),
               email: str=Form(...),
               name: str=Form(...),
               surname: str=Form(...)):
    global user
    global success
    success=False
    data = await request.form()
    # login = data['login']
    # password = data['password']
    # email = data['email']
    # name = data['name']
    # surname = data['surname']
    f=open("profiles.txt",'r+')
    a=f.read()
    if login not in a:
        user=[login,password,email,name,surname]
        #print(a.split()[0])
        print(login)
        f.write(login+" "+password+" "+email+" "+name+" "+surname+" "+'\n')
        f.close()
        values = {
            "reply": None,
            "result": "hub.html"
        }
        success=True
        return templates.TemplateResponse(request, "hub.html",values)
    else:
        success=False
        values={
            "reply" : "Пользователь с таким логином уже есть, попробуйте авторизацию",
            "result": "reg.html"
        }
        return templates.TemplateResponse(request, "main.html",values)


@app.post("/auth", response_class=HTMLResponse)
async def auth1(request: Request,
                login: str=Form(...),
                password: str=Form(...)):
    global user
    authorisation = False
    data = await request.form()
    # login=data['login']
    # password=data['password']
    with open("profiles.txt", "r", encoding="utf-8") as file:
        for line in file:
            cleaned_line = line.strip()
            parts = cleaned_line.split()
            file_login = parts[0]
            file_password = parts[1]
            file_email = parts[2]
            print(login,password)
            print(parts)
            print(file_login == login)
            print(file_password == password)
            if (file_login == login or file_email==login) and file_password == password:
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
    print(user)
    if not(authorisation):
        values = {
            "reply": "Неправильный пароль / Пользователя с таким логином не сущевствует"
        }
        return templates.TemplateResponse(request, "main.html",values)
    else:
        return templates.TemplateResponse(request, "hub.html", values)

@app.get("/auth", response_class=HTMLResponse)
async def auth(request: Request):
    return templates.TemplateResponse(request, "auth.html",values)

@app.post("/hub", response_class=HTMLResponse)
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
    print(values)
    return templates.TemplateResponse(request, "profile.html",values)

@app.post("/profile", response_class=HTMLResponse)
async def profile1(request: Request):
    global user
    values = {
        "name":user[3],
        "surname": user[4],
        "email": user[2],
        "login": user[0],
    }
    print(values)
    print(user)
    return templates.TemplateResponse(request, "profile.html",values)
@app.get("/clear_bookings", response_class=HTMLResponse)
async def clear_bookings(request: Request):
    return templates.TemplateResponse(request, "clear.html")


@app.post("/clear_bookings", response_class=HTMLResponse)
async def clear_bookings1(request: Request,
                         pasw: str=Form(...)):
    global admin_pass
    global room_list
    global week_days
    if admin_pass==pasw:
        room_list = list()
        with open("rooms.txt", 'r') as f:
            splt = f.read().split('\n')
            for i in splt:
                room_list.append(i.split()[1])
        print(room_list)
        for i in room_list:
            for j in week_days:
                with open(f"bookings\\{j}\\{i}.txt",'w+') as f:
                    print("empty empty empty empty empty empty empty empty empty empty empty empty empty",end='',file=f)

@app.get("/all_bookings", response_class=HTMLResponse)
async def all_bookings(request: Request):
    global room_list
    global week_days
    values={}
    for i in week_days:
        for j in room_list:
            for time in range(8,21):
                with open(f"bookings\\{i}\\{j}.txt",'r') as f:
                    values[f"{i}_{j}_{time}"]=f.read().strip().split()[time-8]
    a=""
    for i in values.items():
        a=a+str(i)+'\n'
    return a

@app.get("/booking", response_class=HTMLResponse)
async def booking(request: Request):
    return templates.TemplateResponse(request, "create_booking.html")

@app.post("/booking", response_class=HTMLResponse)
async def booking1(request: Request,
        time_start: int = Form(...),
        time_end: int = Form(...),
        number: int = Form(...),
        week_day: str = Form(...)):
    if time_start > time_end :
        values={
            "response":"Err_Time"
        }
        return templates.TemplateResponse(request, "hub.html",values)
    global room_list
    global week_days
    global user
    free=True
    room_id=room_list[number-1]
    with open(f"bookings\\{week_day}\\{room_id}.txt",'r') as f:
        books=f.read().strip().split()
        for i in range(time_start-8,time_end-7):
            if books[i]!="empty":
                free=False
            else:
                books[i]=user[3]+"_"+user[4]
    with open(f"bookings\\{week_day}\\{room_id}.txt", 'w') as f:
        print(*books,file=f,end='')
        if free:
            values={
                "response":"OK"
            }
            return templates.TemplateResponse(request, "hub.html",values)
        else:
            values = {
                "response": "Err_Not_Free"
            }
            return templates.TemplateResponse(request, "hub.html",values)