This is a Python-based GUI application designed for managing salon services and products, including customer memberships, billing, and payment processing. The application is built using Tkinter for the user interface and MySQL for database integration, and it uses Pillow for image handling.

Features

Product and Service Management: Allows customers to view and select from a range of hair and skin products, as well as salon services.
Membership Discounts: Implements multiple membership tiers (Silver, Gold, and Premium) with varying discount rates (10%, 15%, 20%) on total services and products.
Customer Management: Supports adding new customers or retrieving details of existing customers from a MySQL database.
Billing and Payment: Automatically calculates total cost based on selected products, services, and membership discounts. Offers multiple payment options (cash and internet banking).
Image Integration: Displays images of products and services in the GUI.
Receipt Generation: Generates and saves a receipt for customer purchases.

Project Structure

Main Window: The main interface of the application, allowing navigation to the service, product, and billing windows.
Service Window: Displays available salon services (hair and skin) with associated prices and images.
Product Window: Displays available hair and skin products, allowing customers to select quantities.
Billing Window: Calculates the total cost, applies discounts based on the selected membership, and processes payments.
Payment Window: Handles cash and internet banking payment methods, including receipt generation.

Technologies Used

Python: The core programming language used for the application logic.
Tkinter: Used for creating the graphical user interface.
MySQL: Database management for storing and retrieving customer details.
Pillow: A Python imaging library used for handling and displaying images in the GUI.

SQL Script

CREATE DATABASE salon;
USE salon;

CREATE TABLE customer (
  id INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(255),
  `Phone Number` VARCHAR(15) UNIQUE,
  Address VARCHAR(255),
  `Membership Type` VARCHAR(50)
);

How to Use

Main Window: Choose between services, products, or billing.
Service/Product Selection: Select the desired services and products. Quantities can be adjusted for products.
Billing: View the total cost, apply membership discounts, and proceed to payment.
Payment: Choose between cash or internet banking and complete the payment process. The application generates a receipt at the end.

Future Improvements

Enhance user authentication for secure access.
Add more robust error handling and validation for better user experience.
Implement a reporting feature to track sales and customer activity.
