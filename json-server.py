#FIRST: copy over the nss_handler 
import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status
#SECOND: create the views
from views import list_metals, list_sizes, list_styles, retrieve_style, retrieve_size, retrieve_metal

#THIRD: Build out the json-server
class JSONServer(HandleRequests):
    """Server class to handle incoming HTTP requests for shipping ships"""

    def do_GET(self):
        """Handle GET requests from a client"""

        response_body = ""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "metals":
            if url["pk"] != 0:
                response_body = retrieve_metal(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            response_body = list_metals()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "sizes":
            if url["pk"] != 0:
                response_body = retrieve_size(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            response_body = list_sizes()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        elif url["requested_resource"] == "styles":
            if url["pk"] != 0:
                response_body = retrieve_style(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            response_body = list_styles()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        else:
            return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
        
    # def PUT(self):

# #FOURTH: expand
def main():
    host = ''
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()

if __name__ == "__main__":
    main()