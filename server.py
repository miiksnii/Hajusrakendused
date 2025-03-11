import csv
from flask import Flask, jsonify, request
from KasparFunctions import outPutArray

app = Flask(__name__)

# Load data into memory
array = []
try:
    with open("LE.csv", "r", encoding="latin1") as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            array.append(row)
except FileNotFoundError:
    print("The file LE.csv was not found.")
    array = []

# getdata
@app.route('/getdata', methods=['GET'])
def get_data():
    # Return the data as a JSON response
    if array:
        return jsonify(array)
    else:
        return jsonify({"error": "No data found or file could not be loaded."}), 500

#search
@app.route('/getdata/search', methods=['GET'])
def search():
    # Get all query parameters (dynamic number of params)
    query_params = request.args.to_dict()

    # Prepare a list to store matching results
    results = []

    # Loop through each row in the array to perform the search
    for row in array:
        match = True  # Assume this row is a match

        # For each query parameter, check if it matches the corresponding row's field
        for param, value in query_params.items():
            # We assume the parameters correspond to columns in the row (id -> column 0, item -> column 1, etc.)
            if param == "id":
                col_index = 0  # The 'id' should be in the first column
            elif param == "item":
                col_index = 1  # The 'item' should be in the second column
            else:
                # You can extend this logic for additional parameters if needed.
                col_index = -1  # Default case for other parameters (not implemented)

            # Check if the value in the current row matches the search parameter (case-insensitive)
            if col_index != -1 and value.lower() not in row[col_index].lower():
                match = False
                break  # If any parameter doesn't match, this row is not a match

        # If the row matches all provided query parameters, add it to the results
        if match:
            results.append(row)

    # If no results were found, return a message indicating no matches
    if not results:
        return jsonify({"error": "No matching items found"}), 404

    # Get the page and per_page parameters for pagination
    page = int(request.args.get('page', 1))  # Default page is 1
    per_page = int(request.args.get('per_page', 10))  # Default per_page is 10

    # Calculate the start and end indices for pagination
    start = (page - 1) * per_page
    end = start + per_page

    # Slice the results list to return only the relevant items for the requested page
    paginated_results = results[start:end]

    # Return the paginated results as JSON
    return jsonify(paginated_results)

@app.route('/pagination', methods=['GET'])
def get_paginated_data():
    # Get the page and per_page parameters for pagination
    page = int(request.args.get('page', 1))  # Default page is 1
    per_page = int(request.args.get('per_page', 10))  # Default per_page is 10

    # If there's data in the array, apply pagination
    if array:
        # Calculate the start and end indices for pagination
        start = (page - 1) * per_page
        end = start + per_page

        # Slice the array to return only the relevant items for the requested page
        paginated_data = array[start:end]

        # Pagination metadata
        total_items = len(array)
        total_pages = (total_items // per_page) + (1 if total_items % per_page > 0 else 0)

        # Return the paginated results as JSON with pagination metadata
        return jsonify({
            'page': page,
            'per_page': per_page,
            'total_items': total_items,
            'total_pages': total_pages,
            'data': paginated_data
        })
    else:
        return jsonify({"error": "No data found or file could not be loaded."}), 500




if __name__ == '__main__':
    app.run()
