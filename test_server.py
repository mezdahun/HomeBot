import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from gpt_tools import get_GPT_application_email
from html_tools import generate_html_summary
import re

# Define the function that generates text with the given id
def generate_text_with_id(id):
    # Your implementation here
    html_summary = generate_html_summary(id)
    gptresponse, _ = get_GPT_application_email(id)
    response_text = gptresponse['choices'][0]['message']['content']
    response_text = re.sub("[\(\[].*?[\)\]]", "", response_text)
    return f"gptresponse:\n{response_text} \n\n\nhtml_data_dict:\n\n{html_summary}"
    # return f"gptresponse:\n{gptresponse['choices'][0]['text']} \n\n\nhtml_data_dict:\n\n{html_summary}"

# Define the handler that overrides the do_GET method
class GPTApplicationGenerator(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            response = "Homepage"
            self.wfile.write(response.encode())
        elif parsed_url.path == '/id':
            # can be called with http://localhost:5050/id?id=<id number of apartment>
            query_params = parse_qs(parsed_url.query)
            id = query_params.get('id', [''])[0]
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8-sig')
            self.end_headers()
            response = generate_text_with_id(id)
            self.wfile.write(response.encode('utf-8-sig'))
        else:
            super().do_GET()

# Set up the server
PORT = 5050
Handler = GPTApplicationGenerator
httpd = socketserver.TCPServer(("", PORT), Handler)

# Serve forever
print(f"Serving at http://localhost:{PORT}")
httpd.serve_forever()