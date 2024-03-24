import sys
import socket
from bs4 import BeautifulSoup
import re

# Function to make an HTTP request to a URL
def make_http_request(url):
    try:
        # Parse URL to extract host and path
        host, path = parse_url(url)
        
        # Create a socket object
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to the server
        client.connect((host, 80))

        # Connection successful message
        print("Connection with the site was successful.")
        
        # Construct the HTTP request
        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        
        # Send the request
        client.send(request.encode())
        
        # Receive the response
        response = b""
        while True:
            data = client.recv(4096)
            if not data:
                break
            response += data
        
        # Close the connection
        client.close()

        return response
    
    except Exception as e:
         # Connection unsuccessful message
        print("Connection with the site was unsuccessful.")
        print(f"Error: {str(e)}")


def connect_to_site(url):

    response = make_http_request(url)

    # Decode the response bytes using ISO-8859-1 (latin-1) encoding
    try:
        decoded_response = response.decode('utf-8')
    except UnicodeDecodeError:
        decoded_response = response.decode('ISO-8859-1')  # Fallback to latin-1
        
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(decoded_response, 'html.parser')
        
    # Extract website name
    website_name = soup.title.string.strip() if soup.title else host
        
    # Extract external links and their text labels
    external_links = {}
    for link in soup.find_all('a', href=re.compile(r'^http')):
        external_links[link['href']] = link.get_text().strip()
        
    # Extract text or paragraphs
    paragraphs = [p.get_text().strip() for p in soup.find_all(['p']) if p.get_text()]
        
    # Construct and return the result dictionary
    result = {
        'website_name': website_name,
        'external_links': external_links,
        'paragraphs': paragraphs
    }
        
    return result

# Function to parse URL and extract host and path
def parse_url(url):
    parts = url.split("/", 3)
    host = parts[2]
    path = "/" + parts[3] if len(parts) == 4 else "/"

    return host, path

# Function to make a search request to a search engine
def search(search_term):
   
    url = "https://www.google.com/search?q=" + search_term
    googleClass = "DnJfK"

    response = make_http_request(url)

    # Decode the response bytes using ISO-8859-1 (latin-1) encoding
    try:
        decoded_response = response.decode('utf-8')
    except UnicodeDecodeError:
        decoded_response = response.decode('ISO-8859-1')  # Fallback to latin-1
        
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(decoded_response, 'html.parser')

    # Find the search result links
    for item in soup.find_all("div", class_=googleClass):
        print(item.find('h3').getText())
        addr = item.parent['href']

        # prefixes for links
        addr_start = addr.find("?q=")
        if(addr_start != -1):
            addr = addr[addr_start + len("?q="):]

        # suffixes for links
        addr_end = addr.find('&')
        if(addr_end != -1):
            addr = addr[:addr_end]
        print(addr)
        print()

# Function to display help
def display_help():
    print("Usage:")
    print("go2web -u <URL>")
    print("    Make an HTTP request to the specified URL and print the response")
    print("go2web -s <search-term>")
    print("    Make an HTTP request to search the term using google and print top 10 results")
    print("go2web -h")
    print("    Show this help")