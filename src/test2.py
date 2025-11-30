import json
import numpy as np

# Example data to send
input_data = 1
input_data = [1, 2, 3]
input_data = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]

# Conversion to string
message_head = "COMMAND "
message_body = str(input_data).replace(' ','')
message = message_head + message_body

print(f"Message sent via UART : {message}\n")

# Reception
received_data = message.split(' ')
output_head = received_data[0]
output_body = [json.loads(x) for x in received_data[1:]]
output_body = np.squeeze(output_body).tolist()
print(f"Data extracted : {output_head} {output_body}\n")
