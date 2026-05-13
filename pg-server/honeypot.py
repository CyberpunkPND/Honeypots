import asyncio
import json
import time
import os

LOG_FILE = '/var/log/pg-honeypot/access.log'

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    timestamp = time.time()
    log_entry = {
        'timestamp': timestamp,
        'src_ip': addr[0],
        'src_port': addr[1],
        'event': 'connection'
    }
    # Запись в JSON-файл
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
    
    print(f"[{timestamp}] New connection from {addr}")
    
    error_msg = b'FATAL:  password authentication failed for user "hacker"\n'
    writer.write(error_msg)
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 5432)
    print("PostgreSQL honeypot listening on port 5432")
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
