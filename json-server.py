#FIRST: copy over the nss_handler 
import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status
#SECOND: create the views
from views import list_metals, list_sizes, list_styles, list_orders, retrieve_style, retrieve_size, retrieve_metal, retrieve_orders, delete_order, insert_order, expand_order_by_id, expand_order

#THIRD: Build out the json-server
#FOURTH: expand orders 
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
# the function below needs to change. I want:
# When a customer searches orders, for all of them to come
# When a customer searches for a specific order, for it to come
# When a customer wants to expands all orders, it comes
# When a customer wants to expand a specific order, it happens
# How do I write the cleanest conditionals for that to happen?
        elif url["requested_resource"] == "orders":
            if url["pk"] != 0:
                if "_expand" in url["query_params"]:
                    response_body = expand_order_by_id(url, url["pk"])
                    return self.response(response_body, status.HTTP_200_SUCCESS.value)
                response_body = retrieve_orders(url["pk"])
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            if url["pk"] == 0:
                if "_expand" in url["query_params"]:
                    response_body = expand_order(url)
                    return self.response(response_body, status.HTTP_200_SUCCESS.value)
                response_body = list_orders()
                return self.response(response_body, status.HTTP_200_SUCCESS.value)
        else:
            return self.response("RESOURCE NOT FOUND", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
        
    def do_PUT(self):
        """Handle PUT requests from a client"""
        return self.response("METHOD NOT ALLOWED", status.HTTP_405_METHOD_NOT_ALLOWED.value)
    
    def do_DELETE(self):
        """Handle DELETE requests from a client"""

        url = self.parse_url(self.path)
        pk = url["pk"]

        if url["requested_resource"] == "orders":
            if pk != 0:
                successfully_deleted = delete_order(pk)
                if successfully_deleted:
                    return self.response('', status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value)

                return self.response("Requested resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)

        else:
            return self.response("METHOD NOT ALLOWED", status.HTTP_405_METHOD_NOT_ALLOWED.value)
        
    def do_POST(self):
        """Handle POST requests from a client"""

        url = self.parse_url(self.path)

        # Get the request body JSON for the new data
        content_len = int(self.headers.get('content-length', 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "orders":
            response_body = insert_order(request_body)
            return self.response(response_body, status.HTTP_201_SUCCESS_CREATED.value)

        else:
            return self.response("METHOD NOT ALLOWED", status.HTTP_405_METHOD_NOT_ALLOWED.value)




def main():
    host = ''
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()

if __name__ == "__main__":
    main()

## still need to expand everything on orders
