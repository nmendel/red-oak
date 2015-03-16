#Request Info

class RequestInfo():
    def __init__(self, request_data):
        self.info = request_data

    def score_request(self):
        text = self.info['request_text']
        status = self.info['requester_received_pizza']
        print(text + ' ' + str(status))
