from socket import *
import os
import time
import threading
import socket
from threading import Thread


MAX_AGE = 30

status_msg = {
    200: "OK",
    403: "Forbidden",
    404: "Not Found",
}

url_map = {
    '/'+filename: filename
    for filename in os.listdir()
}

url_map.update({
    '/': 'index.html',
    '/secret': 'secret.html',
    '/cookie': 'cookie.html'
})

cookie_lock = threading.Lock()

cookies = {
}

def write_cookie_expire(id):
    with cookie_lock:
        cookies[id] = time.time()

def get_left_seconds(id):
    return int(MAX_AGE - (time.time()- cookies.get(id)))

# print("url map:", url_map)


def get_dict_from_list_by_sep(arr, sep):
    """
    ["a=1","b=2"] => {"a":"1","b":"2"}
    """
    return {
        element.split(sep)[0].strip(): element.split(sep)[1].strip() if len(element.split(sep)) == 2 else '' #빈값 처리
        for element in arr
    }


def parse_request(request):
    header, body = request.split("\r\n\r\n", 1)
    request_line, *header_list = header.split("\r\n")
    method, url, http_version = request_line.split(" ")
    path, *params = url.split("?",1)

    if params:
        params = get_dict_from_list_by_sep(params[0].split("&"), "=")
    else:
        params = {}
    
    header_dict = get_dict_from_list_by_sep(header_list, ":")

    cookie_dict = {}
    if header_dict.get('Cookie'):
        cookie_dict = get_dict_from_list_by_sep(header_dict.get('Cookie').split(';'), '=')

    path = url_map.get(path, False)
    
    return (method, url, path, cookie_dict, header_dict, params)


def controller(request):
    method, url, path, cookie_dict, header_dict, params = parse_request(request)
    headers = {}
    # Cookie Check 
    cookie_name = "sy_session_id"
    # print(url, path, cookie_dict, params)

    if path == "index.html":
        if cookie_dict.get(cookie_name):
            headers = {
                "Location": "/secret.html"
            }
            return (200, 'secret.html', headers, {})
        return (200, path, headers, {})

    elif path == "secret.html" and (params.get('id') and params.get('pw')):
        headers = {
            "Set-Cookie": "{}={}; Max-Age={}".format(cookie_name, params.get('id'), MAX_AGE)
        }
        write_cookie_expire(params.get('id'))
        return (200, path, headers, {})

    elif not cookie_dict.get(cookie_name):
        return (403, '403.html', headers, {})

    elif path == "cookie.html":
        _id = cookie_dict.get(cookie_name)
        left_seconds = get_left_seconds(_id)
        return (200, path, headers, {"username": _id, "left_seconds": left_seconds})

    elif path and cookie_dict.get(cookie_name):
        return (200, path, headers, {})
    
    return (404, '404.html', headers, {})

def read_content(path):
    with open(path, "rb") as f:
        content = f.read()
    return content


def make_response(status_code, _headers, content):
    http_stauts = 'HTTP/1.1 {} {}\r\n'.format(status_code, status_msg.get(status_code))

    headers = {
        "Date": time.strftime('%a, %d %b %Y %H:%M:%S GMT'),
        'Connection': 'keep-alive',
        "Content-Length": len(content),
        "Content-Type": "text/html; charset=utf-8",
        "Keep-Alive:": "timeout=5, max=10"
    }

    headers.update(_headers)

    headers_string = "\r\n".join([
        "{}: {}".format(header_name.lower(), header_value) 
        for header_name, header_value in headers.items()
    ])

    response = http_stauts+ headers_string + '\r\n\r\n' 
    return response.encode('utf-8') + content


def parse_content_type(content_path):
    """
    image or html
    """
    filetype = content_path.split('.')[-1]
    if filetype == 'html':
        return "text/html; charset=utf-8"
    return "image/" + filetype


def handle_connection(conn, addr):
    max_count = 100
    conn.settimeout(10)
    while max_count:
        # print("wait", max_count)
        try:
            request_bytes = conn.recv(2048)
            status_code, path, headers, render_info = controller(request_bytes.decode("utf-8"))
            
            content = read_content(path)
            if path.split('.')[-1]== 'html':
                content = content.decode('utf-8').format(**render_info).encode('utf-8')
            
            headers.update({
                "Content-Type": parse_content_type(path),
                "Keep-Alive": "timeout=10, max={}".format(max_count)
            })

            response = make_response(status_code, headers, content)

            totalsent = 0
            MSGLEN = len(response)
            while totalsent < MSGLEN:
                sent = conn.send(response[totalsent:])
                if sent == 0:
                    raise RuntimeError("socket connection broken")
                totalsent += sent
                # print(int(totalsent/MSGLEN*100), sent)

            max_count -= 1
        except Exception as e:
            # print(e)
            break
    conn.close()
            


if __name__ == "__main__":
    port = 10080

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', port))
        sock.listen(5)
        print("listen")
        while True:
            conn, addr = sock.accept()
            # print("Accept", conn, addr)
            Thread(target=handle_connection, args=(conn, addr)).start()
            # print("Thread Start")
        # print("loop end")


