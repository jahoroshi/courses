from chttp.services import catch_exception
from chttp.render import render

@catch_exception
async def home(request):
    if request.is_valid:
        if request.method == 'POST':
            print("It's method POST!")
            print("It was received:{}".format(request.body.values()))
    return await render('home.html', request)


