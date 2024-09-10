import os
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import Toplevel, Label, Button, Checkbutton, IntVar
from tkinter import messagebox
from abc import ABC, abstractmethod
from PIL import Image, ImageTk

import mysql.connector 

class Service:
    def __init__(self, root):
        self.root = root
        self.create_service_window()

    def create_service_window(self):
        self.service_window = Toplevel(self.root)
        self.service_window.title("Service Window")
        self.service_window.geometry("800x600+0+0")

        canvas_frame = Frame(self.service_window)
        canvas_frame.pack(expand=True, fill='both')

        canvas = Canvas(canvas_frame)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(canvas_frame, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        frame = Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor='nw')

        self.add_service_images(frame)

        frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        canvas.bind_all("<MouseWheel>", lambda event: self._on_mousewheel(event, canvas))

    def add_service_images(self, frame):
        # Hair Products Heading
        hair_products_label = Label(frame, text="Hair Services", font=("Arial", 18, "bold"))
        hair_products_label.grid(row=0, column=0, columnspan=4, pady=20)

        hair_images = [
            ("haircolor.jpeg", "Hair colour - $150", 1, 0, 1),
            ("hcandhw.jpeg", "Hair wash \n  & \n hair cut - $100", 1, 2, 3),
            ("haircut.jpeg", "Hair cut - $60", 2, 0, 1),
        ]

        for img_path, label_text, row, img_col, lbl_col in hair_images:
            image = Image.open(img_path)
            resized_image = image.resize((200, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(resized_image)

            img_label = Label(frame, image=photo)
            img_label.image = photo
            img_label.grid(row=row, column=img_col, padx=10, pady=10)

            label = Label(frame, text=label_text, font=("Arial", 14))
            label.grid(row=row, column=lbl_col, pady=10)

        # Skin Products Heading
        skin_products_label = Label(frame, text="Skin Services", font=("Arial", 18, "bold"))
        skin_products_label.grid(row=3, column=0, columnspan=4, pady=20)

        skin_images = [
            ("facial.jpeg", "Facial - $100", 4, 0, 1),
            ("waxing.jpeg", "Waxing - $110", 4, 2, 3)
        ]

        for img_path, label_text, row, img_col, lbl_col in skin_images:
            image = Image.open(img_path)
            resized_image = image.resize((200, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(resized_image)

            img_label = Label(frame, image=photo)
            img_label.image = photo
            img_label.grid(row=row, column=img_col, padx=10, pady=10)

            label = Label(frame, text=label_text, font=("Arial", 14))
            label.grid(row=row, column=lbl_col, pady=10)

    def _on_mousewheel(self, event, canvas):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

class BaseWindow:
    def __init__(self, root, title):
        self._root = root
        self._window = tk.Toplevel(root)
        self._window.title(title)
        self._window.geometry("800x600+0+0")

class Membership(ABC):
    def __init__(self, discount_rate):
        self.discount_rate = discount_rate

    @abstractmethod
    def apply_discount(self, total_cost):
        pass

class SilverMembership(Membership):
    def __init__(self):
        super().__init__(0.10)
    
    def apply_discount(self, total_cost):
        return total_cost * (1 - self.discount_rate)
    
    def description(self):
        return "Silver Membership: 10% discount"

class GoldMembership(Membership):
    def __init__(self):
        super().__init__(0.15)
    
    def apply_discount(self, total_cost):
        return total_cost * (1 - self.discount_rate)
    
    def description(self):
        return "Gold Membership: 15% discount"

class PremiumMembership(Membership):
    def __init__(self):
        super().__init__(0.20)
    
    def apply_discount(self, total_cost):
        return total_cost * (1 - self.discount_rate)
    
    def description(self):
        return "Premium Membership: 20% discount"

class NoMembership(Membership):
    def __init__(self):
        super().__init__(0.0)
    
    def apply_discount(self, total_cost):
        return total_cost
    
    def description(self):
        return "No Membership: No discount"

class Billing(BaseWindow):
    def __init__(self, root, hair_vars, skin_vars, products):
        self._hair_vars = hair_vars
        self._skin_vars = skin_vars
        self._products = products
        self._servicebox = None
        self._gift_voucher_label = None
        self._service_vars = {}
        super().__init__(root, "Billing Window")
        self._create_billing_window()

    def _create_billing_window(self):
        self._name_var = tk.StringVar()
        self._membership_var = tk.StringVar()
        self._address_var = tk.StringVar()
        self._ph_var = tk.StringVar()
        self._customer_type_var = tk.IntVar()  # 1 for existing, 2 for new

        # Main Frame with Scrollbar
        self._main_frame = Frame(self._window)
        self._main_frame.pack(fill=tk.BOTH, expand=True)

        self._canvas = tk.Canvas(self._main_frame)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._scrollbar = ttk.Scrollbar(self._main_frame, orient="vertical", command=self._canvas.yview)
        self._scrollbar.pack(side=tk.RIGHT, fill="y")

        self._canvas.configure(yscrollcommand=self._scrollbar.set)
        self._canvas.bind('<Configure>', lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")))

        self._window_frame = Frame(self._canvas)
        self._canvas.create_window((0, 0), window=self._window_frame, anchor="nw")

        # Configure window frame to resize with canvas
        self._window_frame.bind("<Configure>", lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")))
        
        self._canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Customer Information Frame
        self._customer_frame = Frame(self._window_frame, bd=2, relief="solid", padx=10, pady=10)
        self._customer_frame.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        label = Label(self._customer_frame, text="Customer Information", font=("Arial", 20, "bold"), fg="navy")
        label.grid(row=0, column=0, columnspan=3, pady=5)

        self._add_customer_details(self._customer_frame)

        # Total Cost Frame
        cost_frame = Frame(self._window_frame, bd=2, relief="solid", padx=10, pady=10)
        cost_frame.grid(row=1, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        label_total = Label(cost_frame, text="Total Cost:", font=("Arial", 14, "bold"), fg="darkgreen")
        label_total.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)

        self._text_price = Text(cost_frame, height=1, width=20, font=("Arial", 14))
        self._text_price.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)

        # Button Frame
        button_frame = Frame(self._window_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        button_calculate = Button(button_frame, text="Calculate Total Cost", font=("Arial", 12), width=16, command=self._submit_order, bg="#F0F0F0", fg="Black")
        button_calculate.grid(row=0, column=0, padx=10)

        button_DB = Button(button_frame, text="Save to DB", font=("Arial", 12), command=self._connect_database, bg="#F0F0F0", fg="Black")
        button_DB.grid(row=0, column=1, padx=10)

        button_payment = Button(button_frame, text="Make Payment", font=("Arial", 12), command=self.payment, bg="#F0F0F0", fg="Black")
        button_payment.grid(row=0, column=2, padx=10)

    def _on_mousewheel(self, event):
        self._canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def _add_customer_details(self, parent):
        label_name = Label(parent, text="Customer Name", font=("Arial", 12))
        label_name.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

        self._name_entry = Entry(parent, font=("Arial", 12), textvariable=self._name_var)
        self._name_entry.grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)

        label_address = Label(parent, text="Address", font=("Arial", 12))
        label_address.grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)

        self._address_entry = Entry(parent, font=("Arial", 12), textvariable=self._address_var)
        self._address_entry.grid(row=3, column=1, sticky=tk.W, padx=10, pady=5)

        label_ph = Label(parent, text="Phone Number", font=("Arial", 12))
        label_ph.grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)

        self._phone_entry = Entry(parent, font=("Arial", 12), textvariable=self._ph_var)
        self._phone_entry.grid(row=4, column=1, sticky=tk.W, padx=10, pady=5)
        self._ph_var.trace_add("write", self._fetch_customer_details_by_phone)

        Radiobutton(parent, text="Existing Customer", variable=self._customer_type_var, value=1, command=self._toggle_membership, font=("Arial", 12)).grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        Radiobutton(parent, text="New Customer", variable=self._customer_type_var, value=2, command=self._new_customer_message, font=("Arial", 12)).grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)

        self._label_membership = Label(parent, text="Membership Type:", font=("Arial", 12))
        self._label_membership.grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)

        membership_types = ['Null', 'Silver', 'Gold', 'Premium']
        self._membership_combobox = ttk.Combobox(parent, values=membership_types, font=("Arial", 12), state="readonly", width=18, textvariable=self._membership_var)
        self._membership_combobox.grid(row=5, column=1, sticky=tk.W, padx=10, pady=5)
        self._membership_combobox.current(0)
        self._membership_combobox.bind("<<ComboboxSelected>>", self._update_membership_description)

        self._membership_description_label = Label(parent, text="", font=("Arial", 12, "italic"))
        self._membership_description_label.grid(row=6, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)

        # Added Membership Description Label
        self._membership_description_label = Label(parent, text="", font=("Arial", 12, "italic"))
        self._membership_description_label.grid(row=6, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)

        self._gift_voucher_label = Label(parent, text="", font=("Arial", 12), fg="green")
        self._gift_voucher_label.grid(row=7, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)

        label_service = Label(parent, text="Service", font=("Arial", 12))
        label_service.grid(row=8, column=0, sticky=tk.W, padx=10, pady=5)

        button_yes = Button(parent, font=("Arial", 12), text="Yes", command=self._show_services, bg="#F0F0F0", fg="Black")
        button_yes.grid(row=8, column=1, pady=10, sticky=tk.W, padx=10)

        button_no = Button(parent, font=("Arial", 12), text="No", command=self._no_services, bg="#F0F0F0", fg="black")
        button_no.grid(row=8, column=2, pady=10, sticky=tk.W, padx=10)

        self._toggle_membership()


    def _fetch_customer_details_by_phone(self, *args):
        phone_number = self._ph_var.get().strip()
        if self._customer_type_var.get() == 1 and len(phone_number) == 10:
            self._fetch_customer_details(phone_number)
    def _fetch_customer_details(self, phone_number):
        try:
            conn = mysql.connector.connect(
                host='localhost',
                database='salon',
                user='root',
                password='Jatin@2004'
            )
            cursor = conn.cursor()
            query = "SELECT Name, Address, `Phone Number`, `Membership Type` FROM customer WHERE `Phone Number` = %s"
            cursor.execute(query, (phone_number,))
            result = cursor.fetchone()
            if result:
                name, address, phone_number, membership = result
                self._name_var.set(name)
                self._address_var.set(address)
                self._ph_var.set(phone_number)
                self._membership_var.set(membership)
            else:
                messagebox.showerror("Error", "Phone number not found.")
            cursor.close()
            conn.close()
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Failed to fetch customer details: {error}")
            print(f"Error: {error}")

    def _toggle_membership(self):
        if self._customer_type_var.get() == 1:
            self._label_membership.grid()
            self._membership_combobox.grid()
            self._gift_voucher_label.config(text="")
        else:
            self._label_membership.grid_remove()
            self._membership_combobox.grid_remove()

    def _new_customer_message(self):
        if self._customer_type_var.get() == 2:
            self._gift_voucher_label.config(text="New customers should be given a $20 gift voucher")
        self._toggle_membership()

    def _show_services(self):
        self._service_prices = {
            "Hair Colour": 150,
            "Haircut": 60,
            "Hairwash and Haircut": 100,
            "Facial": 100,
            "Waxing": 110
        }
                   

        if self._servicebox:
            self._servicebox.grid_forget()

        self._servicebox = Frame(self._customer_frame, bd=2, relief="solid", padx=10, pady=10)
        self._servicebox.grid(row=8, column=0, columnspan=3, sticky="nsew")

        Label(self._servicebox, text="Select Service", font=("Arial", 12, "bold"), fg="darkred").grid(row=0, column=0, columnspan=2, pady=5)

        for index, (service, price) in enumerate(self._service_prices.items(), start=1):
            service_var = tk.BooleanVar()
            self._service_vars[service] = service_var
            Checkbutton(self._servicebox, text=f"{service} - ${price}", font=("Arial", 12), variable=service_var).grid(row=index, column=0, sticky=tk.W, padx=10, pady=5)

        self._toggle_membership()

    def _no_services(self):
        if self._servicebox:
            self._servicebox.grid_forget()

        self._service_vars = {}
        self._calculate_total()
   
     
    def _calculate_total(self):
        total = 0
        for service, var in self._service_vars.items():
            if var.get() == 1:
                total += self._service_prices[service]
        
        return total 

    def _validate_name(self):
        customer_name = self._name_var.get()
        if not customer_name.isalpha():
            messagebox.showerror("Invalid Input", "Customer name must contain only alphabetic characters. Please enter a valid name.")
            self._name_var.set("")
            self._window.update()
            # Set focus back to the name entry field
            self._name_entry.focus_set()  # Use the actual variable name for the name entry widget
            return False
        return True

    def _validate_phone(self):
        phone_number = self._ph_var.get()
        if not phone_number.isdigit() or len(phone_number) != 10:
            messagebox.showerror("Invalid Input", "Phone number must be a 10-digit numeric value.")
            self._ph_var.set("")
            self._window.update()
            # Set focus back to the phone entry field
            self._phone_entry.focus_set()  # Use the actual variable name for the phone entry widget
            return False
        return True

    def _validate_address(self):
        address = self._address_var.get()
        if not address:
            messagebox.showerror("Invalid Input", "Address cannot be empty.")
            self._address_var.set("")
            self._window.update()  # Force the window to update to clear the invalid input
            self._address_entry.focus_set()  # Use the actual variable name for the address entry widget
            return False
        return True

    def _validate_total_cost(self):
        try:
            total_cost_text = self._text_price.get('1.0', tk.END).strip()
            if not total_cost_text:
                messagebox.showerror("Invalid Total Cost", "Total cost is not displayed.")
                return False
            total_cost = float(total_cost_text)
            if total_cost <= 0:
                messagebox.showerror("Invalid Total Cost", "Total cost must be greater than zero before making a payment.")
                return False
            return True
        except ValueError:
            messagebox.showerror("Invalid Total Cost", "Total cost must be a valid number before making a payment.")
            return False
    
    def _submit_order(self):
        # Ensure the order does not proceed if any validation fails
        if not self._validate_name():
            return
        if not self._validate_phone():
            return
        if not self._validate_address():
            return

        total_cost = 0
        for product, var in self._hair_vars.items():
            quantity = var.get()
            if quantity > 0:
                total_cost += self._products[product] * quantity

        for product, var in self._skin_vars.items():
            quantity = var.get()
            if quantity > 0:
                total_cost += self._products[product] * quantity

        total_cost += self._calculate_total()

        membership_type = self._membership_var.get()
        membership = None

        if membership_type == 'Silver':
            membership = SilverMembership()
        elif membership_type == 'Gold':
            membership = GoldMembership()
        elif membership_type == 'Premium':
            membership = PremiumMembership()
        else:
            membership = NoMembership()

        description = membership.description()
        self._membership_description_label.config(text=description)

        total_cost = membership.apply_discount(total_cost)

        total_cost_rounded = f"{total_cost:.2f}"
    
        self._text_price.delete('1.0', tk.END)
        self._text_price.insert(tk.END, total_cost_rounded)



    def _create_membership_instance(self, membership_type):
        memberships = {
            "Null": Membership,
            "Silver": SilverMembership,
            "Gold": GoldMembership,
            "Premium": PremiumMembership
        }
        return memberships.get(membership_type, Membership)()

    def _connect_database(self):
        customer_name = self._name_var.get()
        customer_address = self._address_var.get()
        customer_phone = self._ph_var.get()
        customer_membership = self._membership_var.get()

        if not all([customer_name, customer_address, customer_phone]):
            messagebox.showerror("Error", "All customer details must be provided.")
            return

        try:
            conn = mysql.connector.connect(
                host='localhost',
                database='salon',
                user='root',
                password='Jatin@2004'
            )
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO customer (Name, Address, `Phone Number`, `Membership Type`)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE Name=%s, Address=%s, `Phone Number`=%s, `Membership Type`=%s
            """, (customer_name, customer_address, customer_phone, customer_membership,
                  customer_name, customer_address, customer_phone, customer_membership))

            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Customer details saved successfully.")
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Failed to save customer details: {error}")
     
    def payment(self):
        if not self._validate_total_cost():
            return

        self.payment_window = tk.Toplevel(self._window)
        self.payment_window.title("Payment Window")
        self.payment_window.geometry("800x600+0+0")
        
        label = Label(self.payment_window, text="Choose a payment method", font=("Arial", 14))
        label.grid(row=1, column=1, columnspan=2, pady=20)

        style = ttk.Style()
        style.configure("TRadiobutton", font=("Arial", 12))

        payment_var = IntVar()

        cash_radio = ttk.Radiobutton(self.payment_window, text="Cash", variable=payment_var, value=1, style="TRadiobutton",
                                    command=lambda: self._handle_payment_selection(payment_var.get()))
        cash_radio.grid(row=2, column=1, padx=20, pady=10)

        card_radio = ttk.Radiobutton(self.payment_window, text="Internet Banking", variable=payment_var, value=2, style="TRadiobutton",
                                    command=lambda: self._handle_payment_selection(payment_var.get()))
        card_radio.grid(row=2, column=2, padx=20, pady=10)
 
    def _handle_payment_selection(self, value):
        for widget in self.payment_window.winfo_children():
            if widget.winfo_y() > 30:  # Removes all widgets below the payment options
                widget.destroy()

        if value == 1:  # Cash selected
            cash_var = tk.DoubleVar()
            tk.Label(self.payment_window, text="Enter your cash amount:", font=("Arial", 12)).grid(row=3, column=1, pady=10)
            cash_entry = tk.Entry(self.payment_window, font=("Arial", 12), textvariable=cash_var)
            cash_entry.grid(row=3, column=2, pady=10)

            tk.Label(self.payment_window, text="Change:", font=("Arial", 12)).grid(row=4, column=1, pady=10)
            change_entry = tk.Entry(self.payment_window, font=("Arial", 12))
            change_entry.grid(row=4, column=2, pady=10)

            def calculate_change():
                try:
                    amount_given = float(cash_var.get())
                    amount_due = float(self._text_price.get("1.0", tk.END).strip().replace('$', ''))
                    if amount_given < amount_due:
                        messagebox.showerror("Insufficient Amount", "The cash amount entered is less than the total cost.")
                        cash_entry.focus_set()
                        return
                    
                    change = amount_given - amount_due
                    change_entry.delete(0, tk.END)
                    change_entry.insert(0, f"${change:.2f}")
                except ValueError:
                    messagebox.showerror("Invalid input", "Please enter a valid amount")
                    cash_entry.focus_set()

            tk.Button(self.payment_window, text="Calculate Change", command=calculate_change, font=("Arial", 12)).grid(row=6, column=0, columnspan=2, pady=10)

        elif value == 2:  # Internet Banking selected
            tk.Label(self.payment_window, text="Account Holder Name:", font=("Arial", 12)).grid(row=3, column=0, pady=10, padx=10)
            holder_name_entry = tk.Entry(self.payment_window, font=("Arial", 12))
            holder_name_entry.grid(row=3, column=1, pady=10, padx=10)

            tk.Label(self.payment_window, text="Account Number:", font=("Arial", 12)).grid(row=4, column=0, pady=10, padx=10)
            account_number_entry = tk.Entry(self.payment_window, font=("Arial", 12))
            account_number_entry.grid(row=4, column=1, pady=10, padx=10)

            tk.Label(self.payment_window, text="Reference:", font=("Arial", 12)).grid(row=5, column=0, pady=10, padx=10)
            reference_entry = tk.Entry(self.payment_window, font=("Arial", 12))
            reference_entry.grid(row=5, column=1, pady=10, padx=10)

            def process_internet_banking_payment():
                holder_name = holder_name_entry.get().strip()
                account_number = account_number_entry.get().strip()
                reference = reference_entry.get().strip()

                # Basic validation checks
                if not holder_name.isalpha():
                    messagebox.showerror("Invalid Input", "Please enter the account holder's name.")
                    holder_name_entry.focus_set()
                    return

                if not account_number.isdigit() or len(account_number) < 8:
                    messagebox.showerror("Invalid Input", "Please enter a valid account number (at least 8 digits).")
                    account_number_entry.focus_set()
                    return

                if not reference:
                    messagebox.showerror("Invalid Input", "Please enter a reference.")
                    reference_entry.focus_set()
                    return

                # Placeholder for internet banking payment processing
                if self._validate_bank_details(holder_name, account_number, reference):
                    messagebox.showinfo("Payment Success", "Internet banking payment processed successfully.")
                    self.print_receipt()
                else:
                    messagebox.showerror("Payment Failed", "Internet banking payment failed. Please check your details.")
                    account_number_entry.focus_set()

            tk.Button(self.payment_window, text="Process Payment", command=process_internet_banking_payment, font=("Arial", 12)).grid(row=6, column=0, columnspan=2, pady=20)
        # Add Close button for both payment methods
        tk.Button(self.payment_window, text="Print Receipt", command=self.print_receipt, font=("Arial", 12)).grid(row=7, column=0, columnspan=2, pady=20)
        tk.Button(self.payment_window, text="Close", command=self.close_payment_window,font=("Arial", 12)).grid(row=7, column=2, columnspan=2, pady=10)

    def close_payment_window(self):
        if self.payment_window:
            self.payment_window.destroy()
            self.payment_window = None
    def _validate_bank_details(self, holder_name, account_number, reference):
        # Placeholder for actual validation logic
        # In a real-world application, this would involve calling a backend API or service to validate and process payment
        return True

    def print_receipt(self):
        # Gather selected hair products
        hair_products = []
        for product, var in self._hair_vars.items():
            quantity = var.get()
            if quantity > 0:
                hair_products.append(f"{product} (x{quantity}) - ${self._products[product] * quantity}")

        # Gather selected skin products
        skin_products = []
        for product, var in self._skin_vars.items():
            quantity = var.get()
            if quantity > 0:
                skin_products.append(f"{product} (x{quantity}) - ${self._products[product] * quantity}")

        # Gather selected services
        selected_services = []
        for service, var in self._service_vars.items():
            if var.get():
                selected_services.append(f"{service} - ${self._service_prices[service]}")

        # Create receipt text
        receipt_text = f"""
        Receipt:
        
        Name: {self._name_var.get()}
        Address: {self._address_var.get()}
        Phone Number: {self._ph_var.get()}
        Membership Type: {self._membership_var.get()}
        
        Hair Products:
        {'\n'.join(hair_products) if hair_products else 'None'}
        
        Skin Products:
        {'\n'.join(skin_products) if skin_products else 'None'}
        
        Services:
        {'\n'.join(selected_services) if selected_services else 'None'}
        
        Total Cost: {self._text_price.get("1.0", tk.END).strip()}
        """

        file_path = "receipt1.txt"

        # Write the receipt text to the file
        with open(file_path, "a") as file:
            file.write(receipt_text)

        # Notify the user
        messagebox.showinfo("Receipt", f"Receipt has been saved to {file_path}")

    @property
    def get_hair_vars(self):
        return self._hair_vars

    @property
    def get_skin_vars(self):
        return self._skin_vars

    @property
    def get_products(self):
        return self._products

    @property
    def get_service_vars(self):
        return self._service_vars

    @property

    def get_customer_info(self):
        return {
            "name": self._name_var.get(),
            "membership": self._membership_var.get(),
            "address": self._address_var.get(),
            "phone_number": self._ph_var.get(),
            "total_cost": self._text_price.get("1.0", tk.END).strip()
        }

    def _update_membership_description(self, event=None):
        membership_type = self._membership_var.get()
        description = ""

        if membership_type == 'Silver':
            description = SilverMembership().description()
        elif membership_type == 'Gold':
            description = GoldMembership().description()
        elif membership_type == 'Premium':
            description = PremiumMembership().description()
        else:
            description = NoMembership().description()

        self._membership_description_label.config(text=description)


class Products(BaseWindow):
    def __init__(self, root, products):
        self.__products = products
        self.__hair_vars = {product: IntVar() for product in self.__products if "Hair" in product}
        self.__skin_vars = {product: IntVar() for product in self.__products if "Skin" in product}
        super().__init__(root, "Product Selection")
        self.__create_products_window()

    def __create_products_window(self):
        label = Label(self._window, text="Products List", font=("Arial", 20))
        label.grid(row=0, column=0, columnspan=2, pady=10)

        hair_label = Label(self._window, text="Hair Products", font=("Arial", 16))
        hair_label.grid(row=1, column=0, sticky=W)

        skin_label = Label(self._window, text="Skin Products", font=("Arial", 16))
        skin_label.grid(row=1, column=1, sticky=W)

        hair_frame = Frame(self._window)
        hair_frame.grid(row=2, column=0, sticky=W)

        skin_frame = Frame(self._window)
        skin_frame.grid(row=2, column=1, sticky=W)

        row = 0
        for product, price in self.__products.items():
            if "Hair" in product:
                Checkbutton(hair_frame, text=f"{product} (${price})", variable=self.__hair_vars[product], font=("Arial", 12)).grid(row=row, column=0, sticky=W)
            elif "Skin" in product:
                Checkbutton(skin_frame, text=f"{product} (${price})", variable=self.__skin_vars[product], font=("Arial", 12)).grid(row=row, column=0, sticky=W)
            row += 1

        button_billing = Button(self._window, text="Proceed to Billing", font=("Arial", 12), command=self.__open_billing_window)
        button_billing.grid(row=3, column=0, columnspan=2, pady=10, sticky=W)

    @property
    def get_products(self):
        return self.__products

    @property
    def get_hair_vars(self):
        return self.__hair_vars

    @property
    def get_skin_vars(self):
        return self.__skin_vars

    @property
    # If you need to access the state of checkbuttons or other elements, you can add more methods
    def get_selected_hair_products(self):
        return {product: var.get() for product, var in self.__hair_vars.items() if var.get() == 1}

    @property
    # If you need to access the state of checkbuttons or other elements, you can add more methods
    def get_selected_skin_products(self):
        return {product: var.get() for product, var in self.__skin_vars.items() if var.get() == 1}

    def __open_billing_window(self):
        Billing(self._root, self.__hair_vars, self.__skin_vars, self.__products)  


class OrderWindow:
    def __init__(self, root):
        self.root = root
        self.products = {
            'Shampoo': 10.99,
            'Conditioner': 12.99,
            'Hair Serum': 15.99,
            'Hair Protector': 20.99,
            'Hair Spray': 8.99,
            'Face Wash': 7.99,
            'Face Cream': 18.99,
            'Serum': 22.99,
            'Toner': 12.99,
            'SPF': 14.99
        }
        self.create_order_window()

    def create_order_window(self):
        self.order_window = Toplevel(self.root)
        self.order_window.title("Buy Products Window")
        self.order_window.geometry("800x600+0+0")

        canvas_frame = Frame(self.order_window)
        canvas_frame.pack(expand=True, fill='both')

        canvas = Canvas(canvas_frame)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(canvas_frame, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        frame = Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor='nw')

        self.product_vars = {}
        self.add_products(frame)

        button_order = Button(frame, text="Proceed to Billing", font=("Arial", 16),
                              command=self.open_billing_window)
        button_order.grid(row=len(self.product_vars) + 3, column=0, columnspan=2, pady=10, sticky=W)

        cancel_button = Button(frame, text="Cancel", font=("Arial", 14), width=10, command=self.order_window.destroy)
        cancel_button.grid(row=len(self.product_vars) + 3, column=1, pady=10, sticky='e')

        frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    def add_products(self, frame):
        hair_products = ['Shampoo', 'Conditioner', 'Hair Serum', 'Hair Protector', 'Hair Spray']
        skin_products = ['Face Wash', 'Face Cream', 'Serum', 'Toner', 'SPF']

        # Hair Products Section
        hair_heading = Label(frame, text="Hair Products", font=("Arial", 18, "bold"))
        hair_heading.grid(row=0, column=0, pady=(0, 10))

        image_path_hair = "hair.jpeg"
        image_hair = Image.open(image_path_hair)
        resized_image_hair = image_hair.resize((250, 250), Image.LANCZOS)
        photo_hair = ImageTk.PhotoImage(resized_image_hair)

        hair_label = Label(frame, image=photo_hair)
        hair_label.image = photo_hair
        hair_label.grid(row=1, column=0, padx=10, pady=10)

        for i, product in enumerate(hair_products, start=1):
            var = IntVar(value=0)
            self.product_vars[product] = var

            Label(frame, text=f"{product} - ${self.products[product]:.2f}", font=("Arial", 14)).grid(row=i + 1, column=0, sticky='w')

            quantity_frame = Frame(frame)
            quantity_frame.grid(row=i + 1, column=1, sticky='w')

            minus_button = Button(quantity_frame, text="-", command=lambda p=product: self.adjust_quantity(p, -1))
            minus_button.pack(side=LEFT)

            quantity_label = Label(quantity_frame, textvariable=var, width=5)
            quantity_label.pack(side=LEFT)

            plus_button = Button(quantity_frame, text="+", command=lambda p=product: self.adjust_quantity(p, 1))
            plus_button.pack(side=LEFT)

        # Skin Products Section
        skin_heading = Label(frame, text="Skin Products", font=("Arial", 18, "bold"))
        skin_heading.grid(row=0, column=2, pady=(0, 10))

        image_path_skin = "skin.jpeg"
        image_skin = Image.open(image_path_skin)
        resized_image_skin = image_skin.resize((250, 250), Image.LANCZOS)
        photo_skin = ImageTk.PhotoImage(resized_image_skin)

        skin_label = Label(frame, image=photo_skin)
        skin_label.image = photo_skin
        skin_label.grid(row=1, column=2, padx=10, pady=10)

        for i, product in enumerate(skin_products, start=1):
            var = IntVar(value=0)
            self.product_vars[product] = var

            Label(frame, text=f"{product} - ${self.products[product]:.2f}", font=("Arial", 14)).grid(row=i + 1, column=2, sticky='w')

            quantity_frame = Frame(frame)
            quantity_frame.grid(row=i + 1, column=3, sticky='w')

            minus_button = Button(quantity_frame, text="-", command=lambda p=product: self.adjust_quantity(p, -1))
            minus_button.pack(side=LEFT)

            quantity_label = Label(quantity_frame, textvariable=var, width=5)
            quantity_label.pack(side=LEFT)

            plus_button = Button(quantity_frame, text="+", command=lambda p=product: self.adjust_quantity(p, 1))
            plus_button.pack(side=LEFT)

    def adjust_quantity(self, product, change):
        current_quantity = self.product_vars[product].get()
        new_quantity = max(0, current_quantity + change)
        self.product_vars[product].set(new_quantity)

    def open_billing_window(self):
        # Pass actual data to Billing window
        hair_vars = {product: var for product, var in self.product_vars.items() if product in [
            'Shampoo', 'Conditioner', 'Hair Serum', 'Hair Protector', 'Hair Spray']}
        skin_vars = {product: var for product, var in self.product_vars.items() if product in [
            'Face Wash', 'Face Cream', 'Serum', 'Toner', 'SPF']}
        Billing(self.root, hair_vars, skin_vars, self.products)

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Femina")
        self.root.geometry("800x600+0+0")
        self.root.configure(bg="#f2f2f2")
        self.create_main_window()

    def create_main_window(self):
        # Load main image (logo)
        try:
            image_path = "logo.jpeg"
            pil_image = Image.open(image_path)
            resized_image = pil_image.resize((800, 280), Image.LANCZOS)
            tk_image = ImageTk.PhotoImage(resized_image)
        except FileNotFoundError:
            print("Image file not found")
            tk_image = None

        canvas = tk.Canvas(self.root, width=800, height=250, bg="#f2f2f2", highlightthickness=0)
        canvas.pack(fill="both", expand=True, pady=(10, 0))
        if tk_image:
            canvas.create_image(0, 0, image=tk_image, anchor="nw")

        frame = tk.Frame(self.root, bg="#f2f2f2")
        frame.pack(expand=True, fill="both", pady=(0, 20))

        frame.columnconfigure((0, 1, 2, 3), weight=1)
        frame.rowconfigure((0, 1, 2), weight=1)

        self.add_buttons(frame)

        # Retain image references
        canvas.image = tk_image

        self.root.mainloop()
    
    def add_buttons(self, frame):
        button_style = {
            "font": ("Arial", 14, "bold"),
            "width": 12,
            "height": 1,
            "bd": 2,
            "bg": "#F0F0F0",
            "fg": "#333333",
            "activebackground": "green",
            "activeforeground": "#ffffff",
        }

        # Product button and image
        order_image_path = "product.jpeg"
        order_tk_image = self.load_image(order_image_path, (200, 150))

        order_image_label = Label(frame, image=order_tk_image, bg="grey")
        order_image_label.grid(row=0, column=2, padx=10, pady=5)

        order_button = Button(frame, text="Product", **button_style, command=lambda: OrderWindow(self.root))
        order_button.grid(row=1, column=2, padx=10, pady=5)

        # Service button and image
        service_image_path = "service.jpeg"
        service_tk_image = self.load_image(service_image_path, (200, 150))

        service_image_label = Label(frame, image=service_tk_image, bg="grey")
        service_image_label.grid(row=0, column=0, padx=10, pady=5)

        service_button = Button(frame, text="Service", **button_style, command=lambda: Service(self.root))
        service_button.grid(row=1, column=0, padx=10, pady=5)

        # Billing button and image
        billing_image_path = "billing0.jpeg"
        billing_tk_image = self.load_image(billing_image_path, (200, 150))

        billing_image_label = Label(frame, image=billing_tk_image, bg="grey")
        billing_image_label.grid(row=0, column=1, padx=10, pady=5)

        billing_button = Button(frame, text="Billing", **button_style, command=lambda: Billing(self.root, {}, {}, {}))
        billing_button.grid(row=1, column=1, padx=10, pady=5)

        # Membership button and image
        membership_image_path = "membership0.jpeg"
        membership_tk_image = self.load_image(membership_image_path, (180, 150))

        membership_image_label = Label(frame, image=membership_tk_image, bg="grey")
        membership_image_label.grid(row=0, column=3, padx=10, pady=5)

        self.add_member_button  = Button(frame, text="Add a Member", font=("Arial", 14, "bold"), command=self.show_membership_form, bg="#F0F0F0", fg="#333333")
        self.add_member_button.grid(row=1, column=3, padx=10, pady=5)

        # Retain image references
        order_image_label.image = order_tk_image
        service_image_label.image = service_tk_image
        billing_image_label.image = billing_tk_image
        membership_image_label.image = membership_tk_image

    def show_membership_form(self):
        self.add_member_button.grid_forget()  # Hide the "Add a Member" button

        # Create a form frame with a border and increased padding
        self.form_frame = Frame(self.root, bg="#ffffff", borderwidth=2, relief="solid")
        self.form_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=300)  # Adjust size as needed

        # Title
        Label(self.form_frame, text="Become a Member", font=("Arial", 18, "bold"), bg="#ffffff").grid(row=0, column=0, columnspan=2, pady=15)

        # Customer ID
        Label(self.form_frame, text="Customer ID:", font=("Arial", 12), bg="#ffffff").grid(row=1, column=0, sticky=tk.W, padx=10)
        self.customer_id_var = StringVar()
        Entry(self.form_frame, textvariable=self.customer_id_var, font=("Arial", 12)).grid(row=1, column=1, pady=5, padx=10, sticky=tk.W)

        # Name
        Label(self.form_frame, text="Name:", font=("Arial", 12), bg="#ffffff").grid(row=2, column=0, sticky=tk.W, padx=10)
        self.name_var = StringVar()
        Entry(self.form_frame, textvariable=self.name_var, font=("Arial", 12)).grid(row=2, column=1, pady=5, padx=10, sticky=tk.W)

        # Phone Number
        Label(self.form_frame, text="Phone Number:", font=("Arial", 12), bg="#ffffff").grid(row=3, column=0, sticky=tk.W, padx=10)
        self.phone_var = StringVar()
        Entry(self.form_frame, textvariable=self.phone_var, font=("Arial", 12)).grid(row=3, column=1, pady=5, padx=10, sticky=tk.W)

        # Address
        Label(self.form_frame, text="Address:", font=("Arial", 12), bg="#ffffff").grid(row=4, column=0, sticky=tk.W, padx=10)
        self.address_var = StringVar()
        Entry(self.form_frame, textvariable=self.address_var, font=("Arial", 12)).grid(row=4, column=1, pady=5, padx=10, sticky=tk.W)

        # Membership Type
        Label(self.form_frame, text="Membership Type:", font=("Arial", 12), bg="#ffffff").grid(row=5, column=0, sticky=tk.W, padx=10)
        self.membership_var = StringVar()
        membership_types = ['null', 'Silver', 'Gold', 'Premium']
        self.membership_combobox = ttk.Combobox(self.form_frame, values=membership_types, font=("Arial", 12), state="readonly", textvariable=self.membership_var)
        self.membership_combobox.grid(row=5, column=1, pady=5, padx=10, sticky=tk.W)
        self.membership_combobox.current(0)  # Default to 'null'

        # Save and Close buttons
        Button(self.form_frame, text="Save", font=("Arial", 12), command=self.save_membership, bg="#28a745", fg="white").grid(row=6, column=0, pady=15, padx=10)
        Button(self.form_frame, text="Close", font=("Arial", 12), command=self.hide_membership_form, bg="#dc3545", fg="white").grid(row=6, column=1, pady=15, padx=10)

    def hide_membership_form(self):
        self.form_frame.destroy()  # Remove the membership form
        self.add_member_button.grid(row=1, column=3, padx=10, pady=5)  # Show the "Add a Member" button again

    def save_membership(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        address = self.address_var.get().strip()
        membership = self.membership_var.get().strip()

        if membership == 'null':
            membership = ''  # Set membership to empty string if 'null' is selected

        if not name or not phone or not address or not membership:
            messagebox.showerror("Invalid Input", "All fields are required.")
            return

        try:
            conn = mysql.connector.connect(
                host='localhost',
                database='salon',
                user='root',
                password='Jatin@2004'
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO customer (Name, `Phone Number`, Address, `Membership Type`) VALUES (%s, %s, %s, %s)",
                           (name, phone, address, membership))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Membership saved successfully.")
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Failed to save membership: {error}")

    def load_image(self, path, size):
        try:
            pil_image = Image.open(path)
            resized_image = pil_image.resize(size, Image.LANCZOS)
            tk_image = ImageTk.PhotoImage(resized_image)
            return tk_image
        except FileNotFoundError:
            print(f"Image file '{path}' not found")
            return None

if __name__ == "__main__":
    MainWindow()

