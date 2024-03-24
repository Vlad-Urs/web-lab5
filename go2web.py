from requests_lib import *


# Check for the correct number of arguments
if len(sys.argv) < 2:
    print("Error: Not enough arguments")
    display_help()
    
# Parse command line arguments
option = sys.argv[1]
if option == "-h":
    display_help()
elif option == "-u" and len(sys.argv) == 3:
    url = sys.argv[2]
    response = connect_to_site(url)

    print(response["website_name"])
    print()

    for key in response["external_links"]:
        print(response["external_links"][key])
        print(key)
        print()
        
    for paragraph in response["paragraphs"]:
        print(paragraph)
        print()

elif option == "-s" and len(sys.argv) >= 3:
    search_term = sys.argv[2:]

    query_str = ""
    for word in search_term:
        query_str += word + '+'

    results = search(query_str)
    print(results)
        
else:
    print("Error: Invalid arguments")
    display_help()
