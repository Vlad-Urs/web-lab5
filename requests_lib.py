import socket

def fetch_html(url):
    # Parse URL to get host and path
    host = url.split("//")[-1].split("/")[0]
    path = "/" + "/".join(url.split("//")[-1].split("/")[1:])
    
    # Establish connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, 80))
    
    # Send HTTP GET request
    sock.send(f"GET {path} HTTP/1.1\r\nHost: {host}\r\n\r\n".encode())
    
    # Receive response
    response = b""
    while True:
        data = sock.recv(4096)
        if not data:
            break
        response += data
    
    # Close socket connection
    sock.close()
    
    return response.decode()

def parse_html(html_content):
    # Basic HTML parser to extract text content
    lines = html_content.split("\r\n")
    start_index = None
    end_index = None
    for i, line in enumerate(lines):
        if "<html" in line.lower():
            start_index = i
        if "</html" in line.lower():
            end_index = i
            break
    if start_index is not None and end_index is not None:
        html_content = "\n".join(lines[start_index:end_index+1])
    
    return html_content

# Example usage
if __name__ == "__main__":
    url = "http://www.google.com"
    html_content = fetch_html(url)
    parsed_html = parse_html(html_content)
    print(parsed_html)