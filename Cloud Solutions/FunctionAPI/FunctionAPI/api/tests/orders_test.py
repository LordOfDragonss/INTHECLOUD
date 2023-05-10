import unittest
import json
import azure.functions as func
from function_app import get_orders, get_order, delete_order

class TestFunction(unittest.TestCase):
    def test_get_orders_should_return_all_orders(self):
        request = func.HttpRequest(
            method="GET",
            body=None,
            url="/api/orders")

        funcCall = get_orders.build().get_user_function()
        response = funcCall(request)

        ordersFromFile = []
        with open("orders.json", "r") as ordersFile:
            ordersFromFile = json.load(ordersFile)
        
        self.assertEqual(
            len(json.loads(response.get_body())),
            len(ordersFromFile))
        
    def test_get_order_should_return_correct_order(self):
        orderNumber = "70001"
        request = func.HttpRequest(
            method="GET",
            body=None,
            url="api/orders/",
            route_params={"orderNumber":orderNumber})

        funcCall = get_order.build().get_user_function()
        response = funcCall(request)
        response = json.loads(response.get_body())
        self.assertEqual(
            response["orderNr"],
            int(orderNumber))

    def test_get_order_with_invalid_number_returns_error(self):
        orderNumber = "no_number"
        request = func.HttpRequest(
            method="GET",
            body=None,
            url="api/orders/",
            route_params={"orderNumber":"no_number"})    
        
        funcCall = get_order.build().get_user_function()
        response = funcCall(request)
        response = json.loads(response.get_body())
        self.assertEqual(
            response["message"],
            f"Order number: {orderNumber} is not a number, only numbers are allowed.")
        
    def test_order_with_not_existing_order_number_should_return_error(self):
        orderNumber = "1"
        request = func.HttpRequest(
            method="GET",
            body=None,
            url="api/orders/",
            route_params={"orderNumber":orderNumber})

        funcCall = get_order.build().get_user_function()
        response = funcCall(request)
        response = json.loads(response.get_body())

        self.assertEqual(
            response["message"],
            f"Order with order number: {orderNumber}, could not be found."
        )  
   
class TestFunctionDelete(unittest.TestCase):
    def test_delete_order_should_delete_order(self):
        orderNumber = "70001"
        request = func.HttpRequest(
            method="DELETE",
            body=None,
            url="api/orders/",
            route_params={"orderNumber":orderNumber})  
        
        funcCall = delete_order.build().get_user_function()
        response = funcCall(request)
        response = json.loads(response.get_body())
        print(response)
        self.assertEqual(
            response["orderNr"],
            int(orderNumber))

