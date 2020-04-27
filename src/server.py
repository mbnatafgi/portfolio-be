import asyncio
import sys
import cli
import yaml
import json
from io import StringIO
from websockets import serve


def get_cli_output(message):

    stdout, stderr = sys.stdout, sys.stderr
    output, error = StringIO(), StringIO()
    sys.stdout, sys.stderr = output, error
    sys.argv[0] = sys.argv[0].replace('server.py', 'mbnatafgi')

    try:
        command = [x.strip() for i, x in enumerate(message.split(' ')) if x != 'mbnatafgi' and i != 0]
        cli.mbnatafgi(command)
    except SystemExit as e:
        try:
            if e.code or '--help' in command:
                raise Exception()
            return json.dumps(yaml.safe_load(output.getvalue() or error.getvalue()), )
        except Exception as e:
            return output.getvalue() or error.getvalue()
    except Exception as e:
        return 'Something went wrong :('
    finally:
        sys.stdout, sys.stderr = stdout, stderr


async def connect(websocket, path):

    async for message in websocket:

        output = get_cli_output(message)

        await websocket.send(output)


start_server = serve(connect, '0.0.0.0', 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
