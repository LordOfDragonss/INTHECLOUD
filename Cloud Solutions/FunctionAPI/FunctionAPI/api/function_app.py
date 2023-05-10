import azure.functions as func
import logging
import json

app = func.FunctionApp()

orders = []

with open("orders.json", "r") as ordersFile:
    orders = json.load(ordersFile)

def calculate_total(items:object):
    """
    Calculating the total price of all items in the items list from an order.

    Parameters:
    -------
    Items: all items from an order.

    Returns:
    -------
    The total amount of all items.
    """
    total = 0
    for item in items:
        total+=int(item["price"])

    return total

for order in orders:
    order["total"] = calculate_total(order["items"])

def create_error_response(message: str, statusCode: int):
    """
    Create a http error response with a status code and message.

    Parameters:
    -------
    Message: Error message you want to return with the reponse.
    Status code: Http status code.
    
    Returns:
    -------
    HTTP response with a custom message and status code.
    """
    error = {
        "message": message,
        "status": statusCode
    }

    return func.HttpResponse(
        json.dumps(error),
        mimetype="application/json",
        status_code=statusCode)

def create_json_response(item: object):
    """
    Creates a http repsonse with the given object in a json format.

    Parameters:
    -------
    item: The item you want to add to the response.

    Returns:
    -------
    HTTP response with an json object.
    """
    return func.HttpResponse(
        json.dumps(item),
        mimetype="application/json")

def get_orders_by_status(fulfilled: str):
    """
    Creates an array of all orders with the matching fulfilled status (True or False).

    Parameters:
    -------
    fulfilled: status of the fulfilled value in an order.

    Returns:
    -------
    List with the matching fulfilled status.
    """
    fulfilled = fulfilled.capitalize()
    if fulfilled != "True" and fulfilled != "False":
        return create_error_response(
            f"Invallid fulfilled param: {fulfilled}, only True and False allowed.", 
            400)

    fulfilled = bool(fulfilled == "True")
    mathingOrders = []
    for order in orders:
        if order["fulfilled"] == fulfilled:
            mathingOrders.append(order)

    return create_json_response(
        mathingOrders)

def validateNumber(number, type: str):
    """
    Validating a given string to make sure its a number.

    Parameters:
    -------
    Number: the 'number' to validate.
    Type: the type of the number like order number or customer ID

    Returns:
    -------
    True if the number is valid, otherwise a http error.
    """
    if number.isdigit() == False:
        return create_error_response(
           f"{type}: {number} is not a number, only numbers are allowed.",
           400)
    else:
        return True

@app.function_name(name="get_orders")
@app.route(route="orders", methods=["GET"])
def get_orders(req: func.HttpRequest) -> func.HttpResponse:
    """
    Getting all made orders.
        
    Response:
    -------
    All made orders.
    """
    param = req.params.get("fulfilled")
    if param != None:
       return get_orders_by_status(param)
    else:
        return create_json_response(orders)

@app.function_name("post_order")
@app.route(route="orders", methods=["POST"])
def post_order(req: func.HttpRequest) -> func.HttpResponse:
    """
    Posting a new order and adding it to the in memory order array.
    
    Response:
    -------
    The created order.
    """
    order = req.get_json()
    order["total"] = calculate_total(order["items"])
    orders.append(order)

    return create_json_response(order)

@app.function_name("get_order")
@app.route(route="orders/{orderNumber}", methods=["GET"])
def get_order(req: func.HttpRequest) -> func.HttpResponse:
    """
    Retrieving an order from the orders list with the matching order number.
    
    Returns:
    -------
    The order with the matching order number.
    """
    orderNumber = req.route_params.get("orderNumber")
    validNumber = validateNumber(orderNumber, "Order number")
    
    if validNumber != True:
        return validNumber

    for order in orders:
        if order["orderNr"] == int(orderNumber):
            return create_json_response(order)

    return create_error_response(
        f"Order with order number: {orderNumber}, could not be found.",
        404)

@app.function_name("delete_order")
@app.route(route="orders/{orderNumber}", methods=["DELETE"])
def delete_order(req: func.HttpRequest) -> func.HttpResponse:
    """
    Deleting an order from the orders list with the matching order number.

    Returns:
    -------
    The deleted order.
    """
    orderNumber = req.route_params.get("orderNumber")
    validNumber = validateNumber(orderNumber, "Order number")
    if validNumber != True:
        return validNumber

    for order in orders:
        if order["orderNr"] == int(orderNumber):
            orders.remove(order)
            return create_json_response(order)

    return create_error_response(
        f"Order with order number: {orderNumber}, could not be found.", 
        404)

@app.function_name("get_orders_by_customer")
@app.route(route="customers/{customerId}", methods=["GET"])
def get_orders_by_customer(req: func.HttpRequest) -> func.HttpResponse:
    """
    Getting all orders from a customer with the matching customer ID
    
    Returns:
    -------
    List with all the ordrs from the customer.
    """
    customerId = req.route_params.get("customerId")

    validNumber = validateNumber(customerId, "Customer ID")
    if validNumber != True:
        return validNumber

    ordersFromCustomer = []

    for order in orders:
        if order["customerId"] == int(customerId):
            ordersFromCustomer.append(order)

    if len(ordersFromCustomer) == 0:
        return create_error_response(
            f"Customer with ID: {customerId}, does not have any orders.", 
            404)   

    return create_json_response(
        ordersFromCustomer)