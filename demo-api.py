#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by panos on 10/15/19
# IDE: PyCharm

## add current path to system path temporary
import sys, os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


from sanic import response as Response
from sanic import Sanic
from sanic_cors import CORS
import platform
from aioVextractor.extractor.pinterest import Extractor
import aiohttp

if platform.system() in {"Linux", "Darwin"}:
    import uvloop
    uvloop.install()
else:
    pass

app = Sanic()
app.config.KEEP_ALIVE = True
app.config.KEEP_ALIVE_TIMEOUT = 500
app.config.RESPONSE_TIMEOUT = 500
CORS(app, automatic_options=True)


@app.route('/extractor', methods=['GET', 'POST'], name='extractor')
async def extractor(request):
    if request.method == 'GET':
        url = request.args.get('url')
    else:  ## request.method == 'POST'
        try:
            url = request.json.get('url')
        except:
            url = request.form.get('url')
    if url:
        print(f"url: {url}")
        with Extractor() as dinosaur:
            async with  aiohttp.ClientSession() as session:
                result = await dinosaur.entrance(webpage_url=url, session=session)
                print(f"result: {result}")
                print(f"result[0]['play_addr']: {result[0]['play_addr']}")
                return Response.text(body=result[0]['play_addr'])
    else:
        return Response.json({"code": 400,
                              "msg": "There is not enough input🤯",
                              "data": None})


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=5555,
            workers=10,
            debug=True,
            access_log=True,
            strict_slashes=False,
            )
