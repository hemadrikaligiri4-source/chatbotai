import json
try:
    with open('api_output.txt', 'rb') as f:
        data = f.read().decode('utf-16le', errors='ignore')
    
    # Extract JSON part
    start_index = data.find('{')
    if start_index != -1:
        json_data = data[start_index:]
        with open('api_error_log.txt', 'w', encoding='utf-8') as f:
            f.write(json_data)
        print("Error log saved to api_error_log.txt")
    else:
        print("No JSON found in log.")
except Exception as e:
    print(f"Failed to convert log: {e}")
