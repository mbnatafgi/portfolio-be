import sys
import os
import yaml
import json
import asyncio
from io import StringIO
from websockets import serve
from . import cli


def get_cli_output(message):

    stdout, stderr = sys.stdout, sys.stderr
    output, error = StringIO(), StringIO()
    sys.stdout, sys.stderr = output, error
    sys.argv[0] = sys.argv[0].replace(os.path.basename(sys.argv[0]), 'mbnatafgi')

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


def main():
    start_server = serve(connect, '0.0.0.0', 8001)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
