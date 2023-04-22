import uuid
from datetime import datetime

from fastapi import FastAPI, Request
from starlette.responses import JSONResponse, HTMLResponse, RedirectResponse
from starlette import status
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()
app.secret_key = str(uuid.uuid4())

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

reminders = []

@app.post('/delete/{index}')
async def remove_reminders(index: int):
    reminders.pop(index)
    return RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)

@app.get('/', response_class=HTMLResponse)
@app.post('/', response_class=HTMLResponse)
async def home(request: Request):
    global reminders
    if request.method == 'POST':
        form = await request.form()
        reminder_text = form['reminder']
        reminder_date = form['date']
        reminder_time = form['time']
        date_str = f'{reminder_date} {reminder_time}'
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
        reminders.append({'text': reminder_text,'time': date_obj})
        return RedirectResponse(
            url='/',
            status_code = status.HTTP_303_SEE_OTHER
        )
    now = datetime.now()
    upcoming_reminders = []
    for index, reminder in enumerate(reminders):
        if reminder['time'] > now:
            reminder['index'] = index
            upcoming_reminders.append(reminder)
    return templates.TemplateResponse('home.html', {'request':request,
                                                    'upcoming_reminders': upcoming_reminders})


