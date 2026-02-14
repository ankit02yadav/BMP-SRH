# ankit
import mysql.connector
from datetime import datetime
import getpass
from dataclasses import dataclass
import base64
import os
import json
# html css 
from http.server import HTTPServer,BaseHTTPRequestHandler
from urllib import parse

###########################  DATABASE  #################################

DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "bmp"

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# check admin login
def validate_credentials_admin(username_bmp: str, password_bmp: str) -> bool:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM users_bmp WHERE username_bmp=%s AND password_bmp=%s LIMIT 1",
            (username_bmp, password_bmp)
        )
        return cur.fetchone() is not None
    finally:
        conn.close()
        
# check customer login 
def validate_credentials_customer(username_bmp: str, password_bmp: str) -> bool:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM customer_bmp WHERE username_bmp=%s AND password_bmp=%s LIMIT 1",
            (username_bmp, password_bmp)
        )
        return cur.fetchone() is not None
    finally:
        conn.close()
        
# fetch full customer details 
def customer_details(username_bmp):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id_customer_bmp, full_name_bmp FROM customer_bmp WHERE username_bmp=%s LIMIT 1",
            (username_bmp,)
        )
        return cur.fetchone()
    finally:
        conn.close()

# getting heading
def get_project_name():
    conn = get_connection();
    try:
        cur = conn.cursor();
        cur.execute("SELECT heading_bmp FROM header_bmp WHERE header_id_bmp = 1 LIMIT 1");
        row = cur.fetchone();
        if row: return row[0];
        return None;
    finally:
        conn.close();
        
# chek username if its exist or not for creting new one 
def check_username(username_bmp):
    conn = get_connection();
    try:
        cur = conn.cursor();
        cur.execute(
            "SELECT 1 FROM users_bmp WHERE username_bmp = %s",
            (username_bmp,)
        )
        return cur.fetchone() is not None;
    finally:
        conn.close();
        
# chek username if its exist or not for creting new one 
def check_username_customer(username_bmp):
    conn = get_connection();
    try:
        cur = conn.cursor();
        cur.execute(
            "SELECT 1 FROM customer_bmp WHERE username_bmp = %s",
            (username_bmp,)
        )
        return cur.fetchone() is not None;
    finally:
        conn.close();
        
# gettin all admin(user) details by username
def admin_details(username_bmp):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT id_user_bmp, full_name_bmp FROM users_bmp WHERE username_bmp=%s LIMIT 1",
            (username_bmp,)
        )
        return cur.fetchone()
    finally:
        conn.close()

#  getting all menu items 
def get_menu_items():
    conn = get_connection();
    try: 
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM items_bmp"
        )
        return cur.fetchall();
    finally:
        conn.close()

# adding item in items_bmp
def add_item_db(item_name_bmp,item_price_bmp,item_quantity_bmp):
    conn = get_connection();
    try:
        cur = conn.cursor();
        cur.execute(
            """INSERT INTO items_bmp (itemname_bmp,itemprice_bmp,itemquantity_bmp)
            VALUES (%s, %s, %s)
            """,
            (item_name_bmp,item_price_bmp,item_quantity_bmp)
        )
        conn.commit()
        print(f"{item_name_bmp} is added successful")
    finally:
        conn.close()

# fetching only one item to update or remove 
def get_one_item(item_id_bmp):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM items_bmp WHERE itemid_bmp = %s LIMIT 1",
            (item_id_bmp,)
        )

        row = cur.fetchone()

        if row is None:
            print("Item Not Found")
            return None

        return row

    finally:
        conn.close()

# updating price by admin control
def update_price(item_id_bmp,new_price_bmp):
    conn = get_connection();
    try:
        cur = conn.cursor();
        cur.execute(
            """
            UPDATE items_bmp SET itemprice_bmp = %s WHERE itemid_bmp = %s;
            """,
            (new_price_bmp,item_id_bmp)
        )
        conn.commit()
        if cur.rowcount == 0:
            print("No item found with this ID")
        else:
            print("Price Updated")
    finally:
        conn.close();
    
#  updating quantity by admin control
def update_quantity(item_id_bmp,new_quantity_bmp):
    conn = get_connection();
    try:
        cur = conn.cursor();
        cur.execute(
            """
            UPDATE items_bmp SET itemquantity_bmp = %s WHERE itemid_bmp = %s;
            """,
            (new_quantity_bmp,item_id_bmp)
        )
        conn.commit()
        if cur.rowcount == 0:
            print("No item found with this ID")
        else:
            print("Quantity Updated")
    finally:
        conn.close();

# removing item by admin control
def remove_item(item_id_bmp):
    conn = get_connection();
    try:
        cur = conn.cursor();
        cur.execute(
            """
            DELETE FROM items_bmp WHERE itemid_bmp = %s; 
            """,
            (item_id_bmp,)
        )
        conn.commit()
        
        if cur.rowcount == 0:
            print("No item found with this ID")
        else:
            print("Item Removed Successfully")
    finally:
        conn.close();
        
#  change heading by admin control
def update_heading(new_heading_bmp):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE header_bmp SET heading_bmp = %s
            """,
            (new_heading_bmp,)
        )
        conn.commit()
        print("Heading Updated Successfully")
    finally:
        conn.close()
# update heading image
def update_heading_img(new_img):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE header_bmp SET headingimage_bmp = %s",
            (new_img,)
        )
        conn.commit()
        print("Image Updated Successfully")
    finally:
        conn.close()

#  getting item by name ( no binery search)
def search_item_by_name(item_name_bmp):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT *
            FROM items_bmp
            WHERE itemname_bmp LIKE %s
            """,
            (f"%{item_name_bmp}%",)
        )

        items = cur.fetchall()

        if not items:
            print("No item found with this name")
            return
        return items;

    finally:
        conn.close()
        
#  checking if the id exist for an item or not 
def check_id_item(item_id_bmp):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM items_bmp WHERE itemid_bmp = %s; 
            """,
            (item_id_bmp,)
        )

        item = cur.fetchone()
        if item is None:
            return False
        else:
            return item

    finally:
        conn.close()
        
#  appending new order after checkout 
def add_order_bmp(username_bmp,total_amount_bmp,payemnt_method_bmp):
    conn = get_connection();
    try:
        cur = conn.cursor();
        cur.execute(
            """INSERT INTO orders_bmp (customer_username_bmp, total_amount_bmp, payment_method_bmp)
            VALUES (%s, %s, %s)
            """,
            (username_bmp,total_amount_bmp,payemnt_method_bmp)
        )
        new_id = cur.lastrowid
        conn.commit()
        print(f"Order Conformed Yor ID : {new_id}");
        return new_id;
    finally:
        conn.close()
      
#  after appending new order get id of order and append all the items in a db   
def add_order_items_bmp(order_id_bmp,item_id_bmp,item_name_bmp,quantity_bmp,price_bmp,subtotal_bmp):
    conn = get_connection();
    try:
        cur = conn.cursor();
        cur.execute(
            """INSERT INTO order_items_bmp (order_id_bmp,item_id_bmp,item_name_bmp,quantity_bmp,price_bmp,subtotal_bmp)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (order_id_bmp,item_id_bmp,item_name_bmp,quantity_bmp,price_bmp,subtotal_bmp)
        )
        conn.commit()
    finally:
        conn.close()
    
# 4 admin parts

# get revenue

def get_rev():
    conn = get_connection()
    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT SUM(total_amount_bmp) 
            FROM orders_bmp
        """)

        result = cur.fetchone()[0]   # get the summed value

        return result if result is not None else 0

    finally:
        conn.close()
        
# get stock items

def get_stock():
    conn = get_connection()
    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT SUM(itemquantity_bmp) 
            FROM items_bmp
        """)

        result = cur.fetchone()[0] 

        return result if result is not None else 0

    finally:
        conn.close()
        
# get total customer

def get_tcustomer():
    conn = get_connection()
    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT COUNT(*) 
            FROM orders_bmp
        """)

        result = cur.fetchone()[0]

        return result if result is not None else 0

    finally:
        conn.close()
        
# daily orders fetch 
def get_daily_torders():
    conn = get_connection()
    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT COUNT(*)
            FROM orders_bmp
            WHERE DATE(order_date_bmp) = CURDATE()
        """)

        result = cur.fetchone()[0]

        return result if result is not None else 0

    finally:
        conn.close()
        
# get all customers

def get_all_customers():
    conn = get_connection()
    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT id_customer_bmp, username_bmp, full_name_bmp
            FROM customer_bmp
        """)

        results = cur.fetchall()

        return results if results else []

    finally:
        conn.close()
#  get project image 
def get_header_image_by_id():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT headingimage_bmp FROM header_bmp WHERE header_id_bmp = 1 LIMIT 1",
        )
        row = cur.fetchone()
        if not row:
            return None

        img_path = row[0]
        try:
            p = img_path.replace("./", "") if img_path.startswith("./") else img_path
            if os.path.exists(p):
                with open(p, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode()
                    return f"data:image/png;base64,{encoded}"
        except Exception:
            pass
        
        return img_path
    finally:
        conn.close()
        
project_logo = get_header_image_by_id();

def register_customer(form_data):
    full_name_bmp = form_data.get("fullname_bmp", "")
    username_bmp = form_data.get("username_bmp", "").strip()
    password_bmp = form_data.get("password_bmp", "")
    confirm_password_bmp = form_data.get("comform_password_bmp", "")


    if password_bmp != confirm_password_bmp:
        return Customer_reg(error="Passwords not match!")

    if check_username_customer(username_bmp):
        return Customer_reg(error="Username already exists!")
    
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO customer_bmp (full_name_bmp, username_bmp, password_bmp)
            VALUES (%s, %s, %s)
            """,
            (full_name_bmp, username_bmp, password_bmp)
        )
        conn.commit()
        return render_login_page(message="Registration successful!")
    finally:
        conn.close()
        
def register_admin(form_data):
    full_name_bmp = form_data.get("fullname_bmp", "")
    username_bmp = form_data.get("username_bmp", "").strip()
    password_bmp = form_data.get("password_bmp", "")
    confirm_password_bmp = form_data.get("comform_password_bmp", "")


    if password_bmp != confirm_password_bmp:
        return Customer_reg(error="Passwords not match!")

    if check_username(username_bmp):
        return Customer_reg(error="Username already exists!")
    
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO users_bmp (full_name_bmp, username_bmp, password_bmp)
            VALUES (%s, %s, %s)
            """,
            (full_name_bmp, username_bmp, password_bmp)
        )
        conn.commit()
        return render_admin_login_page(message="Registration successful!")
    finally:
        conn.close();
    
def get_customer_orders_with_items(username_bmp):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT order_id_bmp, order_date_bmp, total_amount_bmp, payment_method_bmp "
            "FROM orders_bmp WHERE customer_username_bmp = %s ORDER BY order_date_bmp DESC",
            (username_bmp,)
        )
        orders = cur.fetchall()

        result = []
        for order in orders:
            order_id_bmp, order_date_bmp, total_amount_bmp, payment_method_bmp = order

            cur.execute(
                "SELECT item_name_bmp, quantity_bmp, price_bmp, subtotal_bmp "
                "FROM order_items_bmp WHERE order_id_bmp = %s",
                (order_id_bmp,)
            )
            items_bmp = [
                {
                    "item_name_bmp": item[0],
                    "item_quantity_bmp": item[1],
                    "item_price_bmp": item[2],
                    "item_subtotal_bmp": item[3]
                }
                for item in cur.fetchall()
            ]

            result.append({
                "order_id_bmp": order_id_bmp,
                "order_date_bmp": order_date_bmp,
                "total_amount_bmp": total_amount_bmp,
                "payment_method_bmp": payment_method_bmp,
                "items_bmp": items_bmp
            })

        return result
    finally:
        conn.close();

def get_all_customer_orders_with_items():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT order_id_bmp, order_date_bmp, total_amount_bmp, payment_method_bmp "
            "FROM orders_bmp ORDER BY order_date_bmp DESC",
        )
        orders = cur.fetchall()

        result = []
        for order in orders:
            order_id_bmp, order_date_bmp, total_amount_bmp, payment_method_bmp = order

            cur.execute(
                "SELECT item_name_bmp, quantity_bmp, price_bmp, subtotal_bmp "
                "FROM order_items_bmp WHERE order_id_bmp = %s",
                (order_id_bmp,)
            )
            items_bmp = [
                {
                    "item_name_bmp": item[0],
                    "quantity_bmp": item[1],
                    "price_bmp": item[2],
                    "subtotal_bmp": item[3]
                }
                for item in cur.fetchall()
            ]

            result.append({
                "order_id_bmp": order_id_bmp,
                "order_date_bmp": order_date_bmp,
                "total_amount_bmp": total_amount_bmp,
                "payment_method_bmp": payment_method_bmp,
                "items_bmp": items_bmp
            })

        return result
    finally:
        conn.close();

UPLOAD_FOLDER = "images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def handle_update_heading_img(self, web_session):
    if not web_session.is_admin_logged_in:
        self.send_response(302)
        self.send_header("Location", "/admin")
        self.end_headers()
        return

    # Get headers
    content_length = int(self.headers.get("Content-Length", 0))
    content_type = self.headers.get("Content-Type", "")
    if "multipart/form-data" not in content_type:
        self.send_response(400)
        self.end_headers()
        self.wfile.write(b"Invalid Content-Type")
        return

    boundary = content_type.split("boundary=")[1].encode()
    post_data = self.rfile.read(content_length)  # KEEP AS BYTES

    # Split multipart data
    parts = post_data.split(b"--" + boundary)
    for part in parts:
        if b'Content-Disposition' in part and b'name="heading_image"' in part:
            # Extract filename
            try:
                filename_line = [line for line in part.split(b"\r\n") if b'filename=' in line][0]
                filename = filename_line.split(b'filename="')[1].split(b'"')[0].decode()
            except IndexError:
                continue  # No file selected

            if not filename:
                continue  # Skip if empty

            # Extract file content (binary)
            file_data_index = part.find(b"\r\n\r\n") + 4
            file_data = part[file_data_index:-2]  # Remove last \r\n

            # Save image
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            with open(filepath, "wb") as f:
                f.write(file_data)

            # Update database
            filename = f"./images/{filename}";
            update_heading_img(filename)

            # Update global project logo
            global project_logo
            project_logo = get_header_image_by_id();

            # Send success response
            self.send_response(302)
            self.send_header("Location", "/admin")
            self.end_headers()
            self.wfile.write(
                render_admin_dashboard(message="Image updated successfully").encode("utf-8")
            )
            return

    # If no file found
    self.send_response(400)
    self.end_headers()
    self.wfile.write(b"No file uploaded")
    
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def handle_add_item(self, web_session):
    if not web_session.is_admin_logged_in:
        self.send_response(302)
        self.send_header("Location", "/admin")
        self.end_headers()
        return

    # Read raw POST data
    content_length = int(self.headers.get("Content-Length", 0))
    content_type = self.headers.get("Content-Type", "")
    if "multipart/form-data" not in content_type:
        self.send_response(400)
        self.end_headers()
        self.wfile.write(b"Invalid Content-Type")
        return

    boundary = content_type.split("boundary=")[1].encode()
    post_data = self.rfile.read(content_length)  # bytes

    fields = {}
    for part in post_data.split(b"--" + boundary):
        if b'Content-Disposition' in part:
            # parse name
            try:
                name_line = [line for line in part.split(b"\r\n") if b'name=' in line][0]
                field_name = name_line.split(b'name="')[1].split(b'"')[0].decode()
            except IndexError:
                continue

            # parse filename if present
            if b'filename="' in name_line:
                filename = name_line.split(b'filename="')[1].split(b'"')[0].decode()
                if not filename:
                    continue
                file_data_index = part.find(b"\r\n\r\n") + 4
                file_data = part[file_data_index:-2]  # remove trailing \r\n
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                with open(file_path, "wb") as f:
                    f.write(file_data)
                fields[field_name] = f"./images/{filename}"  # store filename in DB
            else:
                # text field
                value_index = part.find(b"\r\n\r\n") + 4
                value = part[value_index:-2].decode()
                fields[field_name] = value

    # Now insert into database
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO items_bmp (itemname_bmp, itemimage_bmp, itemprice_bmp, itemquantity_bmp)
            VALUES (%s, %s, %s, %s)
        """, (fields.get("itemname_bmp"), fields.get("itemimage_bmp"), fields.get("itemprice_bmp"), fields.get("itemquantity_bmp")))
        conn.commit()
    finally:
        conn.close()

    # Respond with the same page again + success message
    self.send_response(302)
    self.send_header("Location", "/admin")
    self.end_headers()
    self.wfile.write(render_admin_dashboard(message="Item added successfully").encode("utf-8"))
        
        
def handle_update_item(self, web_session):
    if not web_session.is_admin_logged_in:
        self.send_response(302)
        self.send_header("Location", "/admin")
        self.end_headers()
        return

    content_length = int(self.headers.get("Content-Length", 0))
    content_type = self.headers.get("Content-Type", "")
    
    if "multipart/form-data" in content_type:
        boundary = content_type.split("boundary=")[1].encode()
        post_data = self.rfile.read(content_length)

        fields = {}
        for part in post_data.split(b"--" + boundary):
            if b'Content-Disposition' in part:
                try:
                    name_line = [line for line in part.split(b"\r\n") if b'name=' in line][0]
                    field_name = name_line.split(b'name="')[1].split(b'"')[0].decode()
                except IndexError:
                    continue

                if b'filename="' in name_line:
                    filename = name_line.split(b'filename="')[1].split(b'"')[0].decode()
                    if filename:
                        file_data_index = part.find(b"\r\n\r\n") + 4
                        file_data = part[file_data_index:-2]
                        file_path = os.path.join("images", filename)
                        with open(file_path, "wb") as f:
                            f.write(file_data)
                        fields[field_name] = f"./images/{filename}"
                else:
                    value_index = part.find(b"\r\n\r\n") + 4
                    value = part[value_index:-2].decode()
                    fields[field_name] = value

        # Update DB
        conn = get_connection()
        try:
            cur = conn.cursor()
            if "itemimage_bmp" in fields:
                cur.execute("""
                    UPDATE items_bmp
                    SET itemname_bmp=%s, itemprice_bmp=%s, itemquantity_bmp=%s, itemimage_bmp=%s
                    WHERE itemid_bmp=%s
                """, (fields["itemname_bmp"], fields["itemprice_bmp"], fields["itemquantity_bmp"], fields["itemimage_bmp"], fields["id"]))
                conn.commit()
            else:
                cur.execute("""
                    UPDATE items_bmp
                    SET itemname_bmp=%s, itemprice_bmp=%s, itemquantity_bmp=%s
                    WHERE itemid_bmp=%s
                """, (fields["itemname_bmp"], fields["itemprice_bmp"], fields["itemquantity_bmp"], fields["id"]))
                conn.commit()
        finally:
            conn.close()

    # Redirect back to /admin
    self.send_response(200)
    self.send_header("Content-Type", "text/plain")
    self.end_headers()
    self.wfile.write(b"OK")


def handle_delete_item(self, web_session):
    if not web_session.is_admin_logged_in:
        self.send_response(302)
        self.send_header("Location", "/admin")
        self.end_headers()
        return

    content_length = int(self.headers.get("Content-Length", 0))
    post_data = self.rfile.read(content_length).decode()
    from urllib import parse
    data = parse.parse_qs(post_data)
    item_id = data["id"][0]

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM items_bmp WHERE itemid_bmp=%s", (item_id,))
        conn.commit()
    finally:
        conn.close()

    # Redirect back to /admin
    self.send_response(302)
    self.send_header("Location", "/admin")
    self.end_headers()
    
    
    
@dataclass
class Session:
    is_logged_in: bool = False
    is_admin_logged_in: bool = False  
    customer_id: int | None = None
    admin_id: int | None = None
    fullname: str | None = None
    username_bmp: str | None = None
    
web_session = Session()

class SimpleHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/logout":

            # clear both roles safely
            web_session.is_logged_in = False
            web_session.is_admin_logged_in = False

            web_session.customer_id = None
            web_session.admin_id = None
            web_session.fullname = None
            web_session.username_bmp = None

            # redirect to customer login (or admin if you prefer)
            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()
            return

        # ---------- ADMIN ----------
        if self.path == "/admin":

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            if web_session.is_admin_logged_in:
                self.wfile.write(
                    render_admin_dashboard().encode("utf-8")
                )
            else:
                self.wfile.write(render_admin_login_page().encode("utf-8"))
            return


        # ---------- CUSTOMER ----------
        if self.path == "/":

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            if web_session.is_logged_in:
                self.wfile.write(
                    render_customer_section().encode("utf-8")
                )
            else:
                self.wfile.write(render_login_page().encode("utf-8"))
            return


        if self.path == "/register":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(Customer_reg().encode("utf-8"))
            return
        
        if self.path == "/admin_register":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(admin_reg().encode("utf-8"))
            return
        
        


    def do_POST(self):
        
        # ---------- ADMIN ACTION IMG ----------
        
        if self.path == "/update-heading-img":
            handle_update_heading_img(self, web_session)
            return
        
        if self.path == "/add-item":
            handle_add_item(self, web_session)
            return
        if self.path == "/update-item":
            handle_update_item(self, web_session)
            return
        if self.path == "/delete-item":
            handle_delete_item(self, web_session)
            return
        
        if self.path == "/add-order":

            length = int(self.headers["Content-Length"])
            body = self.rfile.read(length).decode()
            data = json.loads(body)

            payment = data["payment"]
            items = data["items"]

            username = web_session.username_bmp   # current logged customer

            conn = get_connection()
            cur = conn.cursor()

            try:
                # calculate total
                total = sum(i["price"] * i["qty"] for i in items)

                # create main order
                cur.execute("""
                    INSERT INTO orders_bmp 
                    (customer_username_bmp, total_amount_bmp, payment_method_bmp)
                    VALUES (%s,%s,%s)
                """,(username,total,payment))

                order_id = cur.lastrowid

                # insert each item
                for i in items:
                    subtotal = i["price"] * i["qty"]

                    cur.execute("""
                        INSERT INTO order_items_bmp
                        (order_id_bmp,item_id_bmp,item_name_bmp,quantity_bmp,price_bmp,subtotal_bmp)
                        VALUES (%s,%s,%s,%s,%s,%s)
                    """,(order_id,i["id"],i["name"],i["qty"],i["price"],subtotal))

                    # reduce stock
                    cur.execute("""
                        UPDATE Items_bmp
                        SET itemquantity_bmp = itemquantity_bmp - %s
                        WHERE itemid_bmp = %s
                    """,(i["qty"],i["id"]))

                conn.commit()

            finally:
                conn.close()

            self.send_response(200)
            self.send_header("Content-type","text/plain")
            self.end_headers()
            self.wfile.write(b"Order placed successfully!")
            return;
        
        data = parse.parse_qs(
            self.rfile.read(int(self.headers["Content-Length"])).decode()
        )
        
        
        if self.path == "/register":
            form_data = {k: v[0] for k, v in data.items()}

            page = register_customer(form_data)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(page.encode("utf-8"))
            return
        
        if self.path == "/admin_register":
            form_data = {k: v[0] for k, v in data.items()}

            page = register_admin(form_data)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(page.encode("utf-8"))
            return

        # ---------- ADMIN LOGIN ----------
        if self.path == "/admin":

            if validate_credentials_admin(
                data["username_bmp"][0],
                data["password_bmp"][0]
            ):

                web_session.is_admin_logged_in = True
                web_session.is_logged_in = False   # force customer logout

                web_session.admin_id, web_session.fullname = admin_details(
                    data["username_bmp"][0]
                )
                web_session.username_bmp = data["username_bmp"][0]

                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                self.wfile.write(
                    render_admin_dashboard(
                        message="Login successful"
                    ).encode("utf-8")
                )
            else:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(
                    render_admin_login_page(
                        error="Invalid admin credentials"
                    ).encode("utf-8")
                )
            return


        # ---------- CUSTOMER LOGIN ----------
        if self.path == "/":

            if validate_credentials_customer(
                data["username_bmp"][0],
                data["password_bmp"][0]
            ):

                web_session.is_logged_in = True
                web_session.is_admin_logged_in = False   # force admin logout

                web_session.customer_id, web_session.fullname = customer_details(
                    data["username_bmp"][0]
                )
                web_session.username_bmp = data["username_bmp"][0]

                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                self.wfile.write(
                    render_customer_section(
                        message="Login successful"
                    ).encode("utf-8")
                )
            else:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(
                    render_login_page(
                        error="Invalid username or password"
                    ).encode("utf-8")
                )
            return


        # ---------- ADMIN ACTION NAME ----------
        if self.path == "/update-heading":

            if not web_session.is_admin_logged_in:
                self.send_response(302)
                self.send_header("Location", "/admin")
                self.end_headers()
                return

            new_heading = data["heading"][0]
            update_heading(new_heading)

            self.send_response(302)
            self.send_header("Location", "/admin ")
            self.end_headers()

            self.wfile.write(
                render_admin_dashboard(
                    message="Heading updated successfully"
                ).encode("utf-8")
            )
            return
        
        

        # If POST path is unknown
        self.send_response(404)
        self.end_headers()
                
def render_login_page(message="",error=""):
    page = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bakery Management Program | Login</title>
        <link rel="icon" type="image/png" href="{project_logo}">
        <style>
            :root {{
                --bg1: #F3E9DC; /* cream first */
                --bg2: #895737; /* coffee first */
                --bg2-light: #a67c52;
                --glass: rgba(255, 255, 255, 0.25);
                --glass-border: rgba(255, 255, 255, 0.4);
                --text: #5D4037;
            }}

            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }}

            body {{
                height: 100vh;
                background-color: var(--bg1);
                background-image: 
                    radial-gradient(at 0% 0%, rgba(137, 87, 55, 0.15) 0px, transparent 50%),
                    radial-gradient(at 100% 100%, rgba(137, 87, 55, 0.1) 0px, transparent 50%);
                display: flex;
                flex-direction: column;
                align-items: center;
                overflow: hidden;
            }}

            nav {{
                width: 100%;
                padding: 20px 50px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: var(--glass);
                backdrop-filter: blur(10px);
                border-bottom: 1px solid var(--glass-border);
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
                z-index: 10;
            }}

            nav h1 {{
                color: var(--bg2);
                font-size: 1.5rem;
                font-weight: 800;
                letter-spacing: -0.5px;
            }}

            .btn-admin {{
                padding: 10px 20px;
                border-radius: 12px;
                background: var(--bg1);
                color: var(--bg2);
                font-weight: 600;
                border: none;
                cursor: pointer;
                box-shadow: 4px 4px 10px #cfc6bb, -4px -4px 10px #ffffff;
                transition: all 0.3s ease;
            }}

            .btn-admin:hover {{
                transform: translateY(-2px);
                box-shadow: 6px 6px 15px #cfc6bb, -6px -6px 15px #ffffff;
            }}

            .content-wrapper {{
                flex: 1;
                display: flex;
                justify-content: center;
                align-items: center;
                width: 100%;
            }}

            .login-card {{
                background: var(--glass);
                backdrop-filter: blur(16px) saturate(180%);
                -webkit-backdrop-filter: blur(16px) saturate(180%);
                border-radius: 30px;
                border: 1px solid var(--glass-border);
                padding: 40px;
                width: 380px;
                box-shadow: 
                    20px 20px 60px #cfc6bb, 
                    -20px -20px 60px #ffffff;
                display: flex;
                flex-direction: column;
                gap: 25px;
            }}

            .login-card header {{
                text-align: center;
            }}

            .login-card header h2 {{
                color: var(--bg2);
                font-size: 1.6rem;
                font-weight: 700;
                margin-bottom: 5px;
            }}

            .login-card header p {{
                color: var(--text);
                font-size: 0.85rem;
                opacity: 0.7;
            }}

            .form-group {{
                display: flex;
                flex-direction: column;
                gap: 18px;
            }}

            input {{
                width: 100%;
                padding: 14px 18px;
                border-radius: 12px;
                border: 1px solid transparent;
                background: var(--bg1);
                box-shadow: inset 4px 4px 8px #cfc6bb, 
                            inset -4px -4px 8px #ffffff;
                color: var(--text);
                font-size: 0.95rem;
                outline: none;
                transition: all 0.2s ease;
            }}
            input:focus {{
                border: 1px solid var(--bg2-light);
                box-shadow: inset 2px 2px 4px #cfc6bb, 
                            inset -2px -2px 4px #ffffff,
                            0 0 0 4px rgba(137, 87, 55, 0.1);
            }}

            .actions {{
                display: flex;
                flex-direction: column;
                gap: 10px;
                margin-top: 5px;
            }}

            button.main-btn {{
                padding: 13px;
                border-radius: 12px;
                border: none;
                font-size: 0.95rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }}

            .btn-login {{
                background: var(--bg2);
                color: var(--bg1);
                box-shadow: 0 8px 16px rgba(137, 87, 55, 0.2);
            }}

            .btn-login:hover {{
                background: var(--bg2-light);
                transform: scale(1.02);
                box-shadow: 0 12px 20px rgba(137, 87, 55, 0.3);
            }}

            .btn-reg {{
                background: transparent;
                color: var(--bg2);
                border: 1px solid var(--bg2);
            }}

            .btn-reg:hover {{
                background: rgba(137, 87, 55, 0.05);
                transform: scale(1.02);
            }}

            .blob {{
                position: absolute;
                z-index: -1;
                filter: blur(80px);
                border-radius: 50%;
            }}

            .blob-1 {{
                width: 300px; height: 300px;
                background: rgba(137, 87, 55, 0.1);
                top: 10%; left: 5%;
            }}

            .blob-2 {{
                width: 250px; height: 250px;
                background: rgba(137, 87, 55, 0.05);
                bottom: 10%; right: 5%;
            }}
            
            #popup {{
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: 600;
                color: white;
                z-index: 9999;
                display: none;
            }}
        </style>
    </head>
    <body>
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
        <div id="popup"></div>
        <nav>
            <img src={project_logo} alt="BMP" style="width:60px; gap:20px border-radius:100px;">
            <h1>{get_project_name()}</h1>
            <a href="/admin"><button class="btn-admin">Admin Login</button></a>
        </nav>

        <div class="content-wrapper">
            <main class="login-card">
                <header>
                    <h2>User Login</h2>
                    <p>Enter your credentials to continue</p>
                </header>

                <form class="form-group" action="/" method="POST">
                    <input type="text" name="username_bmp" placeholder="Username_bmp" required>
                    <input type="password" name="password_bmp" placeholder="Password_bmp" required>
                    
                    <div class="actions">
                        <button type="submit" class="main-btn btn-login">Login</button>
                        <button type="button" class="main-btn btn-reg" onclick="window.location.href='/register'">Register</button>
                    </div>
                </form>
            </main>
        </div>
        <footer style=" width:100%; height:40px; display:flex; justify-content:center; align-items:center; color: #F3E9DC; background:#895737;"><p>&copy; 2026 Bakery Management Programm (BMP) Project</p></footer>
    </body>
    </html>
    <script>
    function showPopup(message, type="success") {{
        const popup = document.getElementById("popup");
        if (!popup) return;

        // Set text
        popup.textContent = message;

        // Set background color: green for success, red for error
        popup.style.background = type === "success" ? "#2e7d32" : "#c62828";

        // Show it
        popup.style.display = "block";

        // Hide after 3 seconds
        setTimeout(() => {{
            popup.style.display = "none";
        }}, 2000);
        
    }}
    const msg = "{message}";
    const err = "{error}";
    if (msg) showPopup(msg, "success");
    if (err) showPopup(err, "error");
    
    document.querySelectorAll("input").forEach(input => {{
        input.maxLength = 255;
    }});
    </script>
    """;
    return page;
    
# admin login 
def render_admin_login_page(message="",error=""):
    page = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bakery Management Program | Admin Login</title>
        <link rel="icon" type="image/png" href="{project_logo}">
        <style>
            :root {{
                --bg1: #F3E9DC; /* cream first */
                --bg2: #895737; /* coffee first */
                --bg2-light: #a67c52;
                --glass: rgba(255, 255, 255, 0.25);
                --glass-border: rgba(255, 255, 255, 0.4);
                --text: #5D4037;
            }}

            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }}

            body {{
                height: 100vh;
                background-color: var(--bg1);
                background-image: 
                    radial-gradient(at 0% 0%, rgba(137, 87, 55, 0.15) 0px, transparent 50%),
                    radial-gradient(at 100% 100%, rgba(137, 87, 55, 0.1) 0px, transparent 50%);
                display: flex;
                flex-direction: column;
                align-items: center;
                overflow: hidden;
            }}

            nav {{
                width: 100%;
                padding: 20px 50px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: var(--glass);
                backdrop-filter: blur(10px);
                border-bottom: 1px solid var(--glass-border);
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
                z-index: 10;
            }}

            nav h1 {{
                color: var(--bg2);
                font-size: 1.5rem;
                font-weight: 800;
                letter-spacing: -0.5px;
            }}

            .btn-admin {{
                padding: 10px 20px;
                border-radius: 12px;
                background: var(--bg1);
                color: var(--bg2);
                font-weight: 600;
                border: none;
                cursor: pointer;
                box-shadow: 4px 4px 10px #cfc6bb, -4px -4px 10px #ffffff;
                transition: all 0.3s ease;
            }}

            .btn-admin:hover {{
                transform: translateY(-2px);
                box-shadow: 6px 6px 15px #cfc6bb, -6px -6px 15px #ffffff;
            }}

            .content-wrapper {{
                flex: 1;
                display: flex;
                justify-content: center;
                align-items: center;
                width: 100%;
            }}

            .login-card {{
                background: var(--glass);
                backdrop-filter: blur(16px) saturate(180%);
                -webkit-backdrop-filter: blur(16px) saturate(180%);
                border-radius: 30px;
                border: 1px solid var(--glass-border);
                padding: 40px;
                width: 380px;
                box-shadow: 
                    20px 20px 60px #cfc6bb, 
                    -20px -20px 60px #ffffff;
                display: flex;
                flex-direction: column;
                gap: 25px;
            }}

            .login-card header {{
                text-align: center;
            }}

            .login-card header h2 {{
                color: var(--bg2);
                font-size: 1.6rem;
                font-weight: 700;
                margin-bottom: 5px;
            }}

            .login-card header p {{
                color: var(--text);
                font-size: 0.85rem;
                opacity: 0.7;
            }}

            .form-group {{
                display: flex;
                flex-direction: column;
                gap: 18px;
            }}

            input {{
                width: 100%;
                padding: 14px 18px;
                border-radius: 12px;
                border: 1px solid transparent;
                background: var(--bg1);
                box-shadow: inset 4px 4px 8px #cfc6bb, 
                            inset -4px -4px 8px #ffffff;
                color: var(--text);
                font-size: 0.95rem;
                outline: none;
                transition: all 0.2s ease;
            }}
            input:focus {{
                border: 1px solid var(--bg2-light);
                box-shadow: inset 2px 2px 4px #cfc6bb, 
                            inset -2px -2px 4px #ffffff,
                            0 0 0 4px rgba(137, 87, 55, 0.1);
            }}

            .actions {{
                display: flex;
                flex-direction: column;
                gap: 10px;
                margin-top: 5px;
            }}

            button.main-btn {{
                padding: 13px;
                border-radius: 12px;
                border: none;
                font-size: 0.95rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }}

            .btn-login {{
                background: var(--bg2);
                color: var(--bg1);
                box-shadow: 0 8px 16px rgba(137, 87, 55, 0.2);
            }}

            .btn-login:hover {{
                background: var(--bg2-light);
                transform: scale(1.02);
                box-shadow: 0 12px 20px rgba(137, 87, 55, 0.3);
            }}

            .btn-reg {{
                background: transparent;
                color: var(--bg2);
                border: 1px solid var(--bg2);
            }}

            .btn-reg:hover {{
                background: rgba(137, 87, 55, 0.05);
                transform: scale(1.02);
            }}

            .blob {{
                position: absolute;
                z-index: -1;
                filter: blur(80px);
                border-radius: 50%;
            }}

            .blob-1 {{
                width: 300px; height: 300px;
                background: rgba(137, 87, 55, 0.1);
                top: 10%; left: 5%;
            }}

            .blob-2 {{
                width: 250px; height: 250px;
                background: rgba(137, 87, 55, 0.05);
                bottom: 10%; right: 5%;
            }}
            
            #popup {{
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: 600;
                color: white;
                z-index: 9999;
                display: none;
            }}
        </style>
    </head>
    <body>
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
        <div id="popup"></div>
        <nav>
            <img src={project_logo} alt="BMP" style="width:60px; gap:20px border-radius:100px;">
            <h1>{get_project_name()}</h1>
        </nav>

        <div class="content-wrapper">
            <main class="login-card">
                <header>
                    <h2>Admin Login</h2>
                    <p>Enter your credentials to continue</p>
                </header>

                <form class="form-group" action="/admin" method="POST">
                    <input type="text" name="username_bmp" placeholder="Username_bmp" required>
                    <input type="password" name="password_bmp" placeholder="Password_bmp" required>
                    
                    <div class="actions">
                        <button type="submit" class="main-btn btn-login">Login</button>
                        <button type="button" class="main-btn btn-reg" onclick="window.location.href='/admin_register'">Register</button>
                    </div>
                </form>
            </main>
        </div>
        <footer style=" width:100%; height:40px; display:flex; justify-content:center; align-items:center; color: #F3E9DC; background:#895737;"><p>&copy; 2026 Bakery Management Programm (BMP) Project</p></footer>
    </body>
    </html>
    <script>
    function showPopup(message, type="success") {{
        const popup = document.getElementById("popup");
        if (!popup) return;

        // Set text
        popup.textContent = message;

        // Set background color: green for success, red for error
        popup.style.background = type === "success" ? "#2e7d32" : "#c62828";

        // Show it
        popup.style.display = "block";

        // Hide after 3 seconds
        setTimeout(() => {{
            popup.style.display = "none";
        }}, 2000);
        
    }}
    const msg = "{message}";
    const err = "{error}";
    if (msg) showPopup(msg, "success");
    if (err) showPopup(err, "error");
    
    document.querySelectorAll("input").forEach(input => {{
        input.maxLength = 255;
    }});
    </script>
    """;
    return page;

# customer register page 
def Customer_reg(message ="",error=""):
    page = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bakery Management Program | Registration</title>
        <link rel="icon" type="image/png" href="{project_logo}">
        <style>
            :root {{
                --bg1: #F3E9DC; /* cream first */
                --bg2: #895737; /* coffee first */
                --bg2-light: #a67c52;
                --glass: rgba(255, 255, 255, 0.25);
                --glass-border: rgba(255, 255, 255, 0.4);
                --text: #5D4037;
            }}

            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }}

            body {{
                height: 100vh;
                background-color: var(--bg1);
                background-image: 
                    radial-gradient(at 0% 0%, rgba(137, 87, 55, 0.15) 0px, transparent 50%),
                    radial-gradient(at 100% 100%, rgba(137, 87, 55, 0.1) 0px, transparent 50%);
                display: flex;
                flex-direction: column;
                align-items: center;
                overflow: hidden;
            }}

            nav {{
                width: 100%;
                padding: 20px 50px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: var(--glass);
                backdrop-filter: blur(10px);
                border-bottom: 1px solid var(--glass-border);
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
                z-index: 10;
            }}

            nav h1 {{
                color: var(--bg2);
                font-size: 1.5rem;
                font-weight: 800;
                letter-spacing: -0.5px;
            }}

            .btn-admin {{
                padding: 10px 20px;
                border-radius: 12px;
                background: var(--bg1);
                color: var(--bg2);
                font-weight: 600;
                border: none;
                cursor: pointer;
                box-shadow: 4px 4px 10px #cfc6bb, -4px -4px 10px #ffffff;
                transition: all 0.3s ease;
            }}

            .btn-admin:hover {{
                transform: translateY(-2px);
                box-shadow: 6px 6px 15px #cfc6bb, -6px -6px 15px #ffffff;
            }}

            .content-wrapper {{
                flex: 1;
                display: flex;
                justify-content: center;
                align-items: center;
                width: 100%;
            }}

            .login-card {{
                background: var(--glass);
                backdrop-filter: blur(16px) saturate(180%);
                -webkit-backdrop-filter: blur(16px) saturate(180%);
                border-radius: 30px;
                border: 1px solid var(--glass-border);
                padding: 40px;
                width: 380px;
                box-shadow: 
                    20px 20px 60px #cfc6bb, 
                    -20px -20px 60px #ffffff;
                display: flex;
                flex-direction: column;
                gap: 25px;
            }}

            .login-card header {{
                text-align: center;
            }}

            .login-card header h2 {{
                color: var(--bg2);
                font-size: 1.6rem;
                font-weight: 700;
                margin-bottom: 5px;
            }}

            .login-card header p {{
                color: var(--text);
                font-size: 0.85rem;
                opacity: 0.7;
            }}

            .form-group {{
                display: flex;
                flex-direction: column;
                gap: 18px;
            }}

            input {{
                width: 100%;
                padding: 14px 18px;
                border-radius: 12px;
                border: 1px solid transparent;
                background: var(--bg1);
                box-shadow: inset 4px 4px 8px #cfc6bb, 
                            inset -4px -4px 8px #ffffff;
                color: var(--text);
                font-size: 0.95rem;
                outline: none;
                transition: all 0.2s ease;
            }}
            input:focus {{
                border: 1px solid var(--bg2-light);
                box-shadow: inset 2px 2px 4px #cfc6bb, 
                            inset -2px -2px 4px #ffffff,
                            0 0 0 4px rgba(137, 87, 55, 0.1);
            }}

            .actions {{
                display: flex;
                flex-direction: column;
                gap: 10px;
                margin-top: 5px;
            }}

            button.main-btn {{
                padding: 13px;
                border-radius: 12px;
                border: none;
                font-size: 0.95rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }}

            .btn-login {{
                background: var(--bg2);
                color: var(--bg1);
                box-shadow: 0 8px 16px rgba(137, 87, 55, 0.2);
            }}

            .btn-login:hover {{
                background: var(--bg2-light);
                transform: scale(1.02);
                box-shadow: 0 12px 20px rgba(137, 87, 55, 0.3);
            }}

            .btn-reg {{
                background: transparent;
                color: var(--bg2);
                border: 1px solid var(--bg2);
            }}

            .btn-reg:hover {{
                background: rgba(137, 87, 55, 0.05);
                transform: scale(1.02);
            }}

            .blob {{
                position: absolute;
                z-index: -1;
                filter: blur(80px);
                border-radius: 50%;
            }}

            .blob-1 {{
                width: 300px; height: 300px;
                background: rgba(137, 87, 55, 0.1);
                top: 10%; left: 5%;
            }}

            .blob-2 {{
                width: 250px; height: 250px;
                background: rgba(137, 87, 55, 0.05);
                bottom: 10%; right: 5%;
            }}
            
            #popup {{
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: 600;
                color: white;
                z-index: 9999;
                display: none;
            }}
        </style>
    </head>
    <body>
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
        <div id="popup"></div>
        <nav>
            <img src={project_logo} alt="BMP" style="width:60px; gap:20px border-radius:100px;">
            <h1>{get_project_name()}</h1>
        </nav>

        <div class="content-wrapper">
            <main class="login-card">
                <header>
                    <h2>Join Our Family</h2>
                    <p>Enter your Details</p>
                </header>

                <form class="form-group" action="/register" method="POST">
                    <input type="text" name="fullname_bmp" placeholder="Full_name_bmp" required>
                    <input type="text" name="username_bmp" placeholder="Username_bmp" required>
                    <input type="password" name="password_bmp" placeholder="Password_bmp" required>
                    <input type="password" name="comform_password_bmp" placeholder="Conform_Password_bmp" required>
                    
                    <div class="actions">
                        <button type="submit" class="main-btn btn-login">Register</button>
                    </div>
                </form>
            </main>
        </div>
        <footer style=" width:100%; height:40px; display:flex; justify-content:center; align-items:center; color: #F3E9DC; background:#895737;"><p>&copy; 2026 Bakery Management Programm (BMP) Project</p></footer>
    </body>
    </html>
    <script>
    function showPopup(message, type="success") {{
        const popup = document.getElementById("popup");
        if (!popup) return;

        // Set text
        popup.textContent = message;

        // Set background color: green for success, red for error
        popup.style.background = type === "success" ? "#2e7d32" : "#c62828";

        // Show it
        popup.style.display = "block";

        // Hide after 3 seconds
        setTimeout(() => {{
            popup.style.display = "none";
        }}, 2000);
        
    }}
    const msg = "{message}";
    const err = "{error}";
    if (msg) showPopup(msg, "success");
    if (err) showPopup(err, "error");
    
    document.querySelectorAll("input").forEach(input => {{
        input.maxLength = 255;
    }});
    </script>
    """;
    return page;

#  admin reg
def admin_reg(message ="",error=""):
    page = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bakery Management Program | Admin Registration</title>
        <link rel="icon" type="image/png" href="{project_logo}">
        <style>
            :root {{
                --bg1: #F3E9DC; /* cream first */
                --bg2: #895737; /* coffee first */
                --bg2-light: #a67c52;
                --glass: rgba(255, 255, 255, 0.25);
                --glass-border: rgba(255, 255, 255, 0.4);
                --text: #5D4037;
            }}

            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }}

            body {{
                height: 100vh;
                background-color: var(--bg1);
                background-image: 
                    radial-gradient(at 0% 0%, rgba(137, 87, 55, 0.15) 0px, transparent 50%),
                    radial-gradient(at 100% 100%, rgba(137, 87, 55, 0.1) 0px, transparent 50%);
                display: flex;
                flex-direction: column;
                align-items: center;
                overflow: hidden;
            }}

            nav {{
                width: 100%;
                padding: 20px 50px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: var(--glass);
                backdrop-filter: blur(10px);
                border-bottom: 1px solid var(--glass-border);
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
                z-index: 10;
            }}

            nav h1 {{
                color: var(--bg2);
                font-size: 1.5rem;
                font-weight: 800;
                letter-spacing: -0.5px;
            }}

            .btn-admin {{
                padding: 10px 20px;
                border-radius: 12px;
                background: var(--bg1);
                color: var(--bg2);
                font-weight: 600;
                border: none;
                cursor: pointer;
                box-shadow: 4px 4px 10px #cfc6bb, -4px -4px 10px #ffffff;
                transition: all 0.3s ease;
            }}

            .btn-admin:hover {{
                transform: translateY(-2px);
                box-shadow: 6px 6px 15px #cfc6bb, -6px -6px 15px #ffffff;
            }}

            .content-wrapper {{
                flex: 1;
                display: flex;
                justify-content: center;
                align-items: center;
                width: 100%;
            }}

            .login-card {{
                background: var(--glass);
                backdrop-filter: blur(16px) saturate(180%);
                -webkit-backdrop-filter: blur(16px) saturate(180%);
                border-radius: 30px;
                border: 1px solid var(--glass-border);
                padding: 40px;
                width: 380px;
                box-shadow: 
                    20px 20px 60px #cfc6bb, 
                    -20px -20px 60px #ffffff;
                display: flex;
                flex-direction: column;
                gap: 25px;
            }}

            .login-card header {{
                text-align: center;
            }}

            .login-card header h2 {{
                color: var(--bg2);
                font-size: 1.6rem;
                font-weight: 700;
                margin-bottom: 5px;
            }}

            .login-card header p {{
                color: var(--text);
                font-size: 0.85rem;
                opacity: 0.7;
            }}

            .form-group {{
                display: flex;
                flex-direction: column;
                gap: 18px;
            }}

            input {{
                width: 100%;
                padding: 14px 18px;
                border-radius: 12px;
                border: 1px solid transparent;
                background: var(--bg1);
                box-shadow: inset 4px 4px 8px #cfc6bb, 
                            inset -4px -4px 8px #ffffff;
                color: var(--text);
                font-size: 0.95rem;
                outline: none;
                transition: all 0.2s ease;
            }}
            input:focus {{
                border: 1px solid var(--bg2-light);
                box-shadow: inset 2px 2px 4px #cfc6bb, 
                            inset -2px -2px 4px #ffffff,
                            0 0 0 4px rgba(137, 87, 55, 0.1);
            }}

            .actions {{
                display: flex;
                flex-direction: column;
                gap: 10px;
                margin-top: 5px;
            }}

            button.main-btn {{
                padding: 13px;
                border-radius: 12px;
                border: none;
                font-size: 0.95rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            }}

            .btn-login {{
                background: var(--bg2);
                color: var(--bg1);
                box-shadow: 0 8px 16px rgba(137, 87, 55, 0.2);
            }}

            .btn-login:hover {{
                background: var(--bg2-light);
                transform: scale(1.02);
                box-shadow: 0 12px 20px rgba(137, 87, 55, 0.3);
            }}

            .btn-reg {{
                background: transparent;
                color: var(--bg2);
                border: 1px solid var(--bg2);
            }}

            .btn-reg:hover {{
                background: rgba(137, 87, 55, 0.05);
                transform: scale(1.02);
            }}

            .blob {{
                position: absolute;
                z-index: -1;
                filter: blur(80px);
                border-radius: 50%;
            }}

            .blob-1 {{
                width: 300px; height: 300px;
                background: rgba(137, 87, 55, 0.1);
                top: 10%; left: 5%;
            }}

            .blob-2 {{
                width: 250px; height: 250px;
                background: rgba(137, 87, 55, 0.05);
                bottom: 10%; right: 5%;
            }}
            
            #popup {{
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: 600;
                color: white;
                z-index: 9999;
                display: none;
            }}
            
        </style>
    </head>
    <body>
        <div class="blob blob-1"></div>
        <div class="blob blob-2"></div>
        <div id="popup"></div>
        <nav>
            <img src={project_logo} alt="BMP" style="width:60px; gap:20px border-radius:100px;">
            <h1>{get_project_name()}</h1>
        </nav>

        <div class="content-wrapper">
            <main class="login-card">
                <header>
                    <h2>Add New Owner</h2>
                    <p>Enter your Details</p>
                </header>

                <form class="form-group" action="/admin_register" method="POST">
                    <input type="text" name="fullname_bmp" placeholder="Full_name_bmp" required>
                    <input type="text" name="username_bmp" placeholder="Username_bmp" required>
                    <input type="password" name="password_bmp" placeholder="Password_bmp" required>
                    <input type="password" name="comform_password_bmp" placeholder="Conform_Password_bmp" required>
                    
                    <div class="actions">
                        <button type="submit" class="main-btn btn-login">Register</button>
                    </div>
                </form>
            </main>
        </div>
        <footer style=" width:100%; height:40px; display:flex; justify-content:center; align-items:center; color: #F3E9DC; background:#895737;"><p>&copy; 2026 Bakery Management Programm (BMP) Project</p></footer>
    </body>
    </html>
    <script>
    function showPopup(message, type="success") {{
        const popup = document.getElementById("popup");
        if (!popup) return;

        // Set text
        popup.textContent = message;

        // Set background color: green for success, red for error
        popup.style.background = type === "success" ? "#2e7d32" : "#c62828";

        // Show it
        popup.style.display = "block";

        // Hide after 3 seconds
        setTimeout(() => {{
            popup.style.display = "none";
        }}, 2000);
        
    }}
    const msg = "{message}";
    const err = "{error}";
    if (msg) showPopup(msg, "success");
    if (err) showPopup(err, "error");
    
    document.querySelectorAll("input").forEach(input => {{
        input.maxLength = 255;
    }});
    </script>
    """;
    return page;

# customer page
def render_customer_section(message="", error="", search="", sort=""):
    items = get_menu_items()
    each_item_html = "";
    for item in items:
        img_src = item[2]
        try:
            p = item[2].replace("./", "") if item[2].startswith("./") else item[2]
            if os.path.exists(p):
                with open(p, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode()
                    img_src = f"data:image/png;base64,{encoded}"
        except Exception:
            pass

        each_item_html += f"""
        <div class="product-card"
            data-id="{item[0]}"
            data-name="{item[1].lower()}"
            data-price="{item[3]}"
            data-quantity="{item[4]}">

            <div class="product-img">
                <img src="{img_src}" alt="{item[1]}">
            </div>

            <h3>itemname_bmp: {item[1]}</h3>
            <span class="price-tag">Price_bmp: {item[3]}</span>
            <hr>
            <span class="price-tag">Quantity_bmp: {item[4]}</span>
            
            <div class="cart-controls">
                <button class="btn-add-cart" data-stock="{item[4]}">Add to Cart</button>
            </div>
        </div>
        """
        
    
    all_orders = get_customer_orders_with_items(web_session.username_bmp)

    all_orders_html = ""

    for order in all_orders:
        items_list = ", ".join([f"{item['item_quantity_bmp']}x {item['item_name_bmp']}" for item in order['items_bmp']])
        
        all_orders_html += f"""
        <tr>
            <td>{order['order_id_bmp']}</td>
            <td>{order['order_date_bmp'].strftime('%b %d, %Y')}</td>
            <td>{items_list}</td>
            <td>${order['total_amount_bmp']:.2f}</td>
            <td>{order['payment_method_bmp']}</td>
        </tr>
        """


    page = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Customer Dashboard | Bakery Management System</title>
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <link rel="icon" type="image/png" href="{project_logo}">
        <style>
            :root {{
                --primary: #895737;
                --primary-light: #A67C52;
                --accent: #E6CCB2;
                --bg: #F3E9DC;
                --glass: rgba(255, 255, 255, 0.35);
                --glass-border: rgba(255, 255, 255, 0.5);
                --text: #5D4037;
                --shadow-light: #ffffff;
                --shadow-dark: #cfc6bb;
            }}

            * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Poppins', sans-serif; }}
            body {{ background-color: var(--bg); display: flex; height: 100vh; overflow: hidden; }}
            /* Sidebar */
            .sidebar {{
                width: 280px; background: var(--glass); backdrop-filter: blur(20px);
                border-right: 1px solid var(--glass-border); padding: 40px 20px;
                display: flex; flex-direction: column; gap: 30px;
            }}
            .navbar-heading{{
                height: 70px;
                display: flex;
                top: 0;
                justify-content: center;
                align-items: center;
                margin: 0;
                padding: 0;
                width: 100%;
            }}
            .navbar-heading .head{{
                font-size: 2.3rem;
                font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
                font-weight: 700;
                color: #895737;
            }}
            .sidebar-logo {{
                font-family: 'Playfair Display', serif; font-size: 1.5rem;
                color: var(--primary); display: flex; align-items: center; gap: 10px;
                margin-bottom: 20px; padding-left: 10px; cursor: pointer;
            }}

            .nav-menu {{ list-style: none; display: flex; flex-direction: column; gap: 10px; }}           
            .nav-item {{
                padding: 15px 20px; border-radius: 15px; cursor: pointer;
                display: flex; align-items: center; gap: 15px; color: var(--text);
                font-weight: 500; transition: 0.3s;
            }}
            .nav-item:hover, .nav-item.active {{
                background: var(--bg); box-shadow: 4px 4px 8px var(--shadow-dark), -4px -4px 8px var(--shadow-light);
                color: var(--primary);
            }}

            /* Main Content */
            .main-content {{ flex: 1; padding: 40px; overflow-y: auto; background-image: radial-gradient(at top right, rgba(137,87,55,0.05), transparent); }}
            .section-title {{ font-family: 'Playfair Display', serif; color: var(--primary); font-size: 2.2rem; margin-bottom: 30px; }}
            .product-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 30px; }}
            .product-card {{
                background: var(--glass); backdrop-filter: blur(10px);
                border-radius: 25px; border: 1px solid var(--glass-border);
                padding: 20px; text-align: center; transition: 0.3s;
                box-shadow: 10px 10px 20px var(--shadow-dark), -5px -5px 15px var(--shadow-light);
            }}
            .product-card:hover {{ transform: translateY(-10px); }}

            .product-img {{
                width: 100%; height: 150px; background: var(--bg); border-radius: 20px;
                margin-bottom: 15px; display: flex; align-items: center; justify-content: center;
                font-size: 3rem; color: var(--primary-light);
                box-shadow: 5px 5px 10px var(--shadow-dark), -5px -5px 10px var(--shadow-light);
            }}
            .product-img img {{
                width: 100%;
                height: 100%;
                border-radius: 20px;
                object-fit: cover;
                display: block;
            }}

            .price-tag {{ font-weight: 700; color: var(--primary); font-size: 1.2rem; display: block; margin-bottom: 5px; }}
            .btn-add-cart {{
                width: 100%; padding: 10px; border-radius: 12px; border: none;
                background: var(--primary); color: white; cursor: pointer;
                transition: 0.3s; font-weight: 600;
            }}


            /* Orders Table */
            .order-history {{
                background: var(--glass); border-radius: 30px; padding: 30px;
                border: 1px solid var(--glass-border);
                box-shadow: 15px 15px 35px var(--shadow-dark);
            }}
            table {{ width: 100%; border-collapse: collapse; }}
            th {{ text-align: left; padding: 15px; color: var(--primary); border-bottom: 2px solid var(--accent); }}
            td {{padding: 15px; border-bottom: 1px solid var(--accent); color: var(--text); }}
            
            /* Simple Modal Simulation */
            
            #popup {{
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: 600;
                color: white;
                z-index: 9999;
                display: none;
            }}
            /* Search + Sort Bar */

            .filter-bar{{
                display:flex;
                gap:20px;
                margin-bottom:30px;
                background: var(--glass);
                backdrop-filter: blur(12px);
                border:1px solid var(--glass-border);
                padding:15px 20px;
                border-radius:20px;
                box-shadow: 6px 6px 15px var(--shadow-dark), -4px -4px 12px var(--shadow-light);
            }}

            .search-box{{
                flex:1;
                position:relative;
            }}

            .search-box input{{
                width:100%;
                padding:12px 40px 12px 15px;
                border-radius:15px;
                border:none;
                outline:none;
                background: var(--bg);
                color: var(--text);
                font-weight:500;
                box-shadow: inset 4px 4px 8px var(--shadow-dark), inset -4px -4px 8px var(--shadow-light);
            }}

            .search-box i{{
                position:absolute;
                right:15px;
                top:50%;
                transform:translateY(-50%);
                color:var(--primary);
            }}

            .sort-box select{{
                padding:12px 15px;
                border-radius:15px;
                border:none;
                outline:none;
                background: var(--bg);
                color: var(--text);
                font-weight:600;
                cursor:pointer;
                box-shadow: inset 4px 4px 8px var(--shadow-dark), inset -4px -4px 8px var(--shadow-light);
            }}
            
            
            .btn-minus, .btn-plus {{
                width: 35px;
                height: 35px;
                border-radius: 50%;
                border: none;
                background: var(--primary);
                color: white;
                font-size: 1.2rem;
                font-weight: bold;
                cursor: pointer;
                transition: 0.2s;
                box-shadow: 3px 3px 8px var(--shadow-dark), -2px -2px 5px var(--shadow-light);
            }}

            .btn-minus:hover, .btn-plus:hover {{
                background: var(--primary-light);
                transform: scale(1.1);
            }}

            .qty {{
                display: inline-block;
                width: 25px;
                text-align: center;
                font-weight: 600;
                font-size: 1.1rem;
                color: var(--text);
            }}
            #floating-cart {{
                position: fixed;
                bottom: 25px;
                right: 25px;
                background: var(--primary);
                color: white;
                width: 65px;
                height: 65px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 26px;
                cursor: pointer;
                box-shadow: 0 10px 25px rgba(0,0,0,0.25);
                transition: 0.3s ease;
                z-index: 9999;
            }}

            #floating-cart:hover {{
                transform: scale(1.12);
                background: var(--primary-light);
            }}
            
            
            #cart-popup {{
                position: fixed;
                bottom: 110px;
                right: 25px;
                width: 320px;
                background: var(--bg);
                border-radius: 18px;
                padding: 18px;
                box-shadow: 0 15px 35px rgb(0,0,0);
                display: none;
                z-index: 9999;
            }}

            #cart-popup h3 {{
                color: var(--primary);
                margin-bottom: 12px;
            }}

            .cart-row {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 8px;
                font-size: 0.9rem;
            }}

            #cart-total {{
                margin-top: 12px;
                font-weight: bold;
                color: var(--primary);
            }}

            .btn {{
                margin-top: 12px;
                width: 100%;
                background: var(--primary);
                color: white;
                border: none;
                padding: 10px;
                border-radius: 10px;
                cursor: pointer;
            }}
            .btn-cart{{
                margin-top: 12px;
                background: var(--primary-light);
                color: white;
                display:inline;
                border: none;
                padding: 10px;
                border-radius: 10px;
                cursor: pointer;
            }}
            nav {{
                width: 100%;
                padding: 20px 50px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: var(--glass);
                backdrop-filter: blur(10px);
                border-bottom: 1px solid var(--glass-border);
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
                z-index: 10;
            }}

            nav h1 {{
                color: var(--bg2);
                font-size: 1.5rem;
                font-weight: 800;
                letter-spacing: -0.5px;
            }}
            
            /* responsive */
            /* ======================= Customer view ======================= */
            @media (max-width: 1300px) {{

                /* Navbar heading */
                .customer-navbar .navbar-heading {{
                    flex-direction: column;
                    align-items: flex-start;
                    gap: 15px;
                }}
                .customer-navbar .navbar-heading .head {{
                    font-size: 1.8rem;
                }}
                .customer-navbar .navbar-heading img {{
                    width: 60px;
                }}

                /* Product grid */
                .customer-main .product-grid {{
                    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
                    gap: 20px;
                }}
                .customer-main .product-card {{
                    padding: 15px;
                }}
                .customer-main .product-img {{
                    height: 120px;
                }}
                .customer-main .btn-add-cart, .btn {{
                    padding: 8px;
                    font-size: 0.9rem;
                }}

                /* Search + filter */
                .customer-main .filter-bar {{
                    flex-direction: column;
                    gap: 15px;
                }}
                .customer-main .search-box input,
                .customer-main .sort-box select {{
                    width: 100%;
                    padding: 10px 35px 10px 12px;
                    font-size: 0.9rem;
                }}
            }}

            /* Smaller devices for customer */
            @media (max-width: 900px) {{
                *{{
                    font-size:12px;
                }}
                .sidebar{{
                    width:150px;
                }}
                .nav-item{{
                    font-size:12px;
                }}
                .navbar-heading .head {{
                    font-size: 20px;
                }}
                .customer-main .product-grid {{
                    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
                }}
                .customer-main .product-img {{
                    height: 100px;
                }}
                .customer-main .btn-add-cart {{
                    /*font-size: 0.85rem;*/
                    padding: 6px;
                }}
            }}
            /* Mobile devices */
            @media (max-width: 500px) {{
                .customer-navbar .navbar-heading .head {{
                    font-size: 20px;
                }}
                .customer-navbar .navbar-heading img {{
                    width: 50px;
                }}
                .customer-main .product-grid {{
                    grid-template-columns: 1fr;
                    gap: 10px;
                }}
                .customer-main .product-img {{
                    height: 90px;
                }}
                .customer-main .btn-add-cart {{
                    font-size: 0.8rem;
                    padding: 5px;
                }}
            }}
        </style>
    </head>
    <body>
        <div id="popup"></div>
        <!--  -->
        
        <aside class="sidebar">
            <div class="sidebar-logo" onclick="window.location.href='index.html'">
                <!-- <i class="fas fa-bread-slice"></i> -->
                <span></span>
            </div>
            <ul class="nav-menu">
                <li class="nav-item active" onclick="showSection('shop')"><i class="fas fa-store"></i> Items_bmp</li>
                <li class="nav-item" onclick="showSection('orders')"><i class="fas fa-history"></i> Orders_bmp</li>
                <li class="nav-item" onclick="window.location.href='/logout'"><i class="fas fa-sign-out-alt"></i> Logout</li>
            </ul>
            <footer style="position:absolute; bottom:0px; left :0px; width:100%; height:40px; display:flex; justify-content:center; align-items:center; color: #F3E9DC; background:#895737;"><p>&copy; 2026 Bakery Management Programm (BMP) Project</p></footer>
        </aside>

        <!-- Main Content -->
        <main class="main-content">
            <!-- Shop Section -->
            <section id="shop-section">
                <div class="navbar-heading" style="gap:20px" margin:0px 0px 20px 0px;>
                    <img src={project_logo} alt="BMP" style="width:80px; gap:20px border-radius:100px;">
                    
                    <h1 class="head">{get_project_name()}</h1>
                </div>
                <form class="filter-bar" method="POST" action="/" style="margin:40px 0px 0px 0px;">
                    <div class="search-box">
                        <input 
                            type="text" 
                            name="search"
                            placeholder="Search bakery items..."
                            value="{search}">
                        <i class="fas fa-search"></i>
                    </div>

                    <div class="sort-box">
                        <select>
                            <option value="">Sort Items</option>
                            <option value="name_asc">Name (A → Z)</option>
                            <option value="name_desc">Name (Z → A)</option>
                            <option value="price_asc">Price (Low → High)</option>
                            <option value="price_desc">Price (High → Low)</option>
                        </select>
                    </div>

                    <button style="display:none"></button>
                </form>
                <div class="product-grid" style="margin:40px 0px 0px 0px;">
                    {each_item_html}
                </div>
            </section>

            <section id="orders-section" style="display: none; gap:20px;">
                <div class="navbar-heading" style="gap:20px margin:0px 0px 20px 0px;">
                    <img src={project_logo} alt="BMP" style="width:80px; margin:0px 20px 0px 0px;">
                    
                    <h1 class="head">{get_project_name()}</h1>
                </div>
                <div class="order-history" style="margin:20px 0px 0px 0px;">
                    <table>
                        <thead>
                            <tr><th>Order_id_bmp</th><th>order_date_bmp</th><th>order_items_bmp</th><th>total_amount_bmp</th><th>order_method_bmp</th></tr>
                        </thead>
                        <tbody>
                            {all_orders_html}
                        </tbody>
                    </table>
                </div>
            </section>
            <div id="floating-cart">
                <i class="fas fa-shopping-cart"></i>
            </div>
        </main>
        <div id="cart-popup" style="display:none; position:fixed; bottom:20px; right:20px; padding:20px; border-radius:15px; border:1px solid var(--glass-border); z-index:10000;">
            <h3>Cart</h3>
            <div id="cart-items"></div>
            <div id="cart-total" style="margin-top:10px;"></div>
            <div style="display:flex; gap:10px; margin-top:10px;">
                <button id="checkout-cash" class="btn">Pay Cash</button>
                <button id="checkout-card" class="btn">Pay Card</button>
                <button id="close-cart" class="btn">Close</button>
            </div>
        </div>
        <script>
            /* ===================== POPUP MESSAGE ===================== */
            function showPopup(message, type="success") {{
                const popup = document.getElementById("popup");
                if (!popup) return;

                popup.textContent = message;
                popup.style.background = type === "success" ? "#2e7d32" : "#c62828";
                popup.style.display = "block";

                setTimeout(() => {{
                    popup.style.display = "none";
                }}, 2000);
            }}

            /* ===================== SECTION SWITCH ===================== */
            function showSection(section) {{
                document.getElementById('shop-section').style.display = section === 'shop' ? 'block' : 'none';
                document.getElementById('orders-section').style.display = section === 'orders' ? 'block' : 'none';
            }}

            /* ===================== CART SYSTEM ===================== */
            let cart = JSON.parse(localStorage.getItem("bmp_cart") || "{{}}");

            function saveCart() {{
                localStorage.setItem("bmp_cart", JSON.stringify(cart));
            }}

            const cartPopup = document.getElementById("cart-popup");
            const cartItemsBox = document.getElementById("cart-items");
            const cartTotalBox = document.getElementById("cart-total");

            document.getElementById("close-cart").onclick = () => {{
                cartPopup.style.display = "none";
            }};
            document.getElementById("checkout-cash").onclick = () => sendOrder("Cash");
            document.getElementById("checkout-card").onclick = () => sendOrder("Card");

            const floatingCart = document.getElementById("floating-cart");
            if(floatingCart){{
                floatingCart.onclick = () => {{
                    cartPopup.style.display = cartPopup.style.display === "block" ? "none" : "block";
                    renderCart();
                }};
            }}

            /* ===================== INIT PRODUCTS ===================== */
            document.querySelectorAll(".product-card").forEach(card => {{
                const name = card.dataset.name;
                if (cart[name]) {{
                    renderControls(card);
                }} else {{
                    const controls = card.querySelector(".cart-controls");
                    let addBtn = controls.querySelector(".btn-add-cart");
                    if(!addBtn) return;

                    const price = parseFloat(card.dataset.price);
                    const stock = parseInt(card.dataset.quantity);

                    addBtn.onclick = () => {{
                        cart[name] = {{
                            id: card.dataset.id,
                            qty: 1,
                            price: price,
                            stock: stock
                        }};
                        saveCart();
                        renderControls(card);
                        renderCart();
                        cartPopup.style.display = "block";
                    }};
                }}
            }});

            /* ===================== RENDER +/- CONTROLS ===================== */
            function renderControls(card){{
                const name = card.dataset.name;
                const item = cart[name];
                const controls = card.querySelector(".cart-controls");

                controls.innerHTML = `
                    <button class="btn-minus">-</button>
                    <span class="qty">${{item.qty}}</span>
                    <button class="btn-plus">+</button>
                `;

                controls.querySelector(".btn-minus").onclick = () => {{
                    item.qty--;
                    if(item.qty <= 0){{
                        delete cart[name];
                        controls.innerHTML = `<button class="btn-add-cart">Add to Cart</button>`;
                        controls.querySelector(".btn-add-cart").onclick = () => {{
                            cart[name] = {{
                                id: card.dataset.id,
                                qty: 1,
                                price: item.price,
                                stock: item.stock
                            }};
                            renderControls(card);
                            renderCart();
                        }};
                    }} else {{
                        renderControls(card);
                    }}
                    renderCart();
                }};

                controls.querySelector(".btn-plus").onclick = () => {{
                    if(item.qty >= item.stock){{
                        alert("Stock limit reached!");
                        return;
                    }}
                    item.qty++;
                    renderControls(card);
                    renderCart();
                }};
            }}

            /* ===================== RENDER CART ===================== */
            function renderCart(){{
                cartItemsBox.innerHTML = "";
                let total = 0;

                for(let name in cart){{
                    const item = cart[name];
                    const lineTotal = item.qty * item.price;
                    total += lineTotal;

                    const row = document.createElement("div");
                    row.className = "cart-row";
                    row.innerHTML = `<span>${{name}} x ${{item.qty}}</span><span>€${{lineTotal.toFixed(2)}}</span>`;
                    cartItemsBox.appendChild(row);
                }}

                cartTotalBox.textContent = "Total: €" + total.toFixed(2);
            }}

            /* ===================== SEND ORDER ===================== */
            async function sendOrder(method){{
                if(Object.keys(cart).length === 0){{
                    showPopup("Cart is empty", "error");
                    return;
                }}

                const items = Object.keys(cart).map(name => {{
                    return {{
                        id: cart[name].id,
                        name: name,
                        price: cart[name].price,
                        qty: cart[name].qty
                    }};
                }});

                const res = await fetch("/add-order", {{
                    method: "POST",
                    headers: {{ "Content-Type": "application/json" }},
                    body: JSON.stringify({{ payment: method, items: items }})
                }});

                const msg = await res.text();
                showPopup(msg, "success");

                cart = {{}};
                renderCart();
                cartPopup.style.display = "none";

                // Reset all product card controls to "Add to Cart"
                document.querySelectorAll(".product-card").forEach(card => {{
                    const controls = card.querySelector(".cart-controls");
                    if(controls.querySelector(".btn-minus")) {{
                        const name = card.dataset.name;
                        controls.innerHTML = `<button class="btn-add-cart">Add to Cart</button>`;
                        controls.querySelector(".btn-add-cart").onclick = () => {{
                            const price = parseFloat(card.dataset.price);
                            const stock = parseInt(card.dataset.quantity);
                            cart[name] = {{
                                id: card.dataset.id,
                                qty: 1,
                                price: price,
                                stock: stock
                            }};
                            renderControls(card);
                            renderCart();
                            cartPopup.style.display = "block";
                        }};
                    }}
                }});
            }}

            /* ===================== INPUT LIMIT ===================== */
            document.querySelectorAll("input").forEach(input => {{
                input.maxLength = 255;
            }});

            /* ===================== SEARCH & SORT ===================== */
            const searchInput = document.querySelector('.search-box input');
            const sortSelect = document.querySelector('.sort-box select');
            const grid = document.querySelector('.product-grid');

            let cards = Array.from(document.querySelectorAll('.product-card'));

            function renderCards(list){{
                grid.innerHTML = "";
                list.forEach(card => grid.appendChild(card));
            }}

            searchInput.addEventListener("input", () => {{
                const value = searchInput.value.toLowerCase();

                const filtered = cards.filter(card =>
                    card.dataset.name.includes(value)
                );

                renderCards(filtered);
            }});

            sortSelect.addEventListener("change", () => {{
                let sorted = [...cards];

                if(sortSelect.value === "name_asc"){{
                    sorted.sort((a,b)=> a.dataset.name.localeCompare(b.dataset.name));
                }}
                else if(sortSelect.value === "name_desc"){{
                    sorted.sort((a,b)=> b.dataset.name.localeCompare(a.dataset.name));
                }}
                else if(sortSelect.value === "price_asc"){{
                    sorted.sort((a,b)=> parseFloat(a.dataset.price) - parseFloat(b.dataset.price));
                }}
                else if(sortSelect.value === "price_desc"){{
                    sorted.sort((a,b)=> parseFloat(b.dataset.price) - parseFloat(a.dataset.price));
                }}

                renderCards(sorted);
            }});

        </script>
    </body>
    </html>

    """
    return page;

# admin dashboard 
def render_admin_dashboard(message="",error="",search="",sort=""):
    
    cus_list = get_all_customers()
    all_customers = ""

    for user in cus_list:
        all_customers += f"""
        <tr>
            <td>{user[0]}</td>
            <td>{user[1]}</td>
            <td>{user[2]}</td>
        </tr>
        """
    
    all_orders = get_all_customer_orders_with_items();

    all_orders_html = ""

    for order in all_orders:
        items_list = ", ".join([f"{item['quantity_bmp']}x {item['item_name_bmp']}" for item in order['items_bmp']])
        
        all_orders_html += f"""
        <tr>
            <td>{order['order_id_bmp']}</td>
            <td>{order['order_date_bmp'].strftime('%b %d, %Y')}</td>
            <td>{items_list}</td>
            <td>${order['total_amount_bmp']:.2f}</td>
            <td>{order['payment_method_bmp']}</td>
        </tr>
        """
        
        
    items = get_menu_items()
    each_item_html = "";
    for item in items:
        img_src = item[2]
        try:
            p = item[2].replace("./", "") if item[2].startswith("./") else item[2]
            if os.path.exists(p):
                with open(p, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode()
                    img_src = f"data:image/png;base64,{encoded}"
        except Exception:
            pass

        each_item_html += f"""
        <div class="product-card"
            data-id="{item[0]}"
            data-name="{item[1].lower()}"
            data-price="{item[3]}"
            data-quantity="{item[4]}">

            <div class="product-img">
                <img src="{img_src}" alt="{item[1]}">
            </div>

            <input type="file" class="item-image"
                accept="image/png, image/jpeg, image/jpg, image/webp"
                style="margin-bottom:10px;">

            <h3>
                <input type="text" class="item-name price-tag" value="{item[1]}">
            </h3>

            <span class="price-tag">
                item_price_bmp:
                <input type="number" class="item-price price-tag" value="{item[3]}">
            </span>

            <hr>

            <span class="price-tag">
                item_quantity_bmp:
                <input type="number" class="item-quantity price-tag" value="{item[4]}">
            </span>

            <div class="cart-controls" style="display:flex; gap:20px;">
                <button class="btn update-btn">Update</button>
                <button class="btn dlt delete-btn" data-id="{item[0]}">Delete</button>
            </div>
        </div>
        """
    
    page = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Admin Dashboard | Bakery Management System</title>
                <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
                <link rel="icon" type="image/png" href="{project_logo}">
                <style>
                    :root {{
                        --primary: #5D4037;
                        --primary-light: #895737;
                        /*above before (below after)*/
                        --primary: #895737;
                        --primary-light: #A67C52;
                        --bg: #F3E9DC;
                        --glass: rgba(255, 255, 255, 0.25);
                        --glass-border: rgba(255, 255, 255, 0.4);
                        --text: #3E2723;
                        --shadow-light: #ffffff;
                        --shadow-dark: #cfc6bb;
                        --danger: #d32f2f;
                        --success: #388e3c;
                    }}

                    * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Poppins', sans-serif; }}

                    body {{ background-color: var(--bg); display: flex; height: 100vh; overflow: hidden; }}

                    /* Sidebar Admin */
                    .sidebar {{
                        width: 260px; background: var(--primary); color: white;
                        padding: 40px 20px; display: flex; flex-direction: column; gap: 35px;
                    }}

                    .sidebar-logo {{ font-family: 'Playfair Display', serif; font-size: 1.4rem; display: flex; align-items: center; gap: 10px; color: var(--bg); }}
                    .section-title {{ font-family: 'Playfair Display', serif; color: var(--primary); font-size: 2.2rem; margin-bottom: 30px; }}
                    .admin-nav {{ list-style: none; display: flex; flex-direction: column; gap: 8px; }}
                    .admin-nav-item {{
                        padding: 14px 18px; border-radius: 12px; cursor: pointer;
                        display: flex; align-items: center; gap: 12px; transition: 0.3s;
                        color: rgba(255,255,255,0.7); font-weight: 500;
                    }}
                    .admin-nav-item:hover, .admin-nav-item.active {{
                        background: rgba(255,255,255,0.1); color: white;
                    }}
                    /* Main Section */
                    .main {{ flex: 1; padding: 35px; overflow-y: auto; background-image: linear-gradient(to bottom right, transparent, rgba(93,64,55,0.05));}}

                    .top-stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 25px; margin-bottom: 40px; }}
                    .stat-card {{
                        background: var(--glass); backdrop-filter: blur(10px);
                        border-radius: 20px; border: 1px solid var(--glass-border);
                        padding: 25px; box-shadow: 10px 10px 20px var(--shadow-dark), -10px -10px 20px var(--shadow-light);
                        display: flex; align-items: center; gap: 20px;
                    }}
                    .stat-icon {{ width: 50px; height: 50px; border-radius: 15px; background: var(--primary); color: white; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; }}
                    .stat-info h4 {{ font-size: 0.8rem; color: var(--primary-light); text-transform: uppercase; letter-spacing: 1px; }}
                    .stat-info p {{ font-size: 1.5rem; font-weight: 700; color: var(--primary); }}

                    /* Sections Grid */
                    .admin-grid {{ display: grid; grid-template-columns: 1.5fr 1fr; gap: 30px; }}
                    .admin-panel {{
                        background: var(--glass); backdrop-filter: blur(20px);
                        border-radius: 30px; border: 1px solid var(--glass-border);
                        padding: 30px; box-shadow: 15px 15px 35px var(--shadow-dark), -15px -15px 35px var(--shadow-light);
                    }}
                    .admin-panel h3 {{ font-family: 'Playfair Display', serif; color: var(--primary); margin-bottom: 25px; font-size: 1.5rem; display: flex; align-items: center; gap: 10px; }}

                    /* Forms */
                    .form-row {{ display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 20px; margin-bottom: 20px; }}
                    .form-group {{ display: flex; flex-direction: column; gap: 8px; }}
                    .form-group label {{ font-size: 0.85rem; font-weight: 600; color: var(--primary); }}
                    
                    input, select {{
                        padding: 12px; border-radius: 10px; border: none; background: var(--bg);
                        box-shadow: inset 3px 3px 6px var(--shadow-dark), inset -3px -3px 6px var(--shadow-light);
                        outline: none;
                    }}

                    .btn-action {{
                        padding: 12px 25px; border-radius: 10px; border: none; background: var(--primary);
                        color: white; font-weight: 600; cursor: pointer; transition: 0.3s;
                    }}
                    .btn-action:hover {{ background: var(--primary-light); transform: translateY(-2px); }}

                    /* Table Styling */
                    table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                    th {{ text-align: left; font-size: 0.85rem; color: var(--primary-light); padding: 12px 5px; border-bottom: 2px solid var(--accent); }}
                    td {{ padding: 15px 5px; border-bottom: 1px solid var(--accent); font-size: 0.9rem; color: var(--text); }}
                    
                    .badge {{ padding: 4px 10px; border-radius: 8px; font-size: 0.75rem; font-weight: 600; }}
                    .badge-stock {{ background: #e8f5e9; color: var(--success); }}
                    .badge-low {{ background: #ffebee; color: var(--danger); }}
                    .form-group img {{ width:100px; height:100px; display:flex;}}
                    .action-btns {{ display: flex; gap: 10px; }}
                    .btn-icon {{ width: 32px; height: 32px; border-radius: 8px; border: none; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: 0.2s; }}
                    .btn-edit {{ background: var(--accent); color: var(--primary); }}
                    .btn-del {{ background: #ffebee; color: var(--danger); }}
                    #popup {{
                        position: fixed;
                        top: 20px;
                        right: 20px;
                        padding: 12px 20px;
                        border-radius: 8px;
                        font-weight: 600;
                        color: white;
                        z-index: 9999;
                        display: none;
                    }}
                    #inventory-section{{
                        display:none;
                    }}
                    
                    
                    #users-section {{
                        display: none;
                        padding: 20px;
                        background: var(--glass);
                        border-radius: 20px;
                    }}

                    #users-section h2 {{
                        font-family: 'Playfair Display', serif;
                        color: var(--primary);
                        margin-bottom: 20px;
                        font-size: 1.8rem;
                    }}

                    #users-section table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 15px;
                        background: var(--bg);
                        border-radius: 12px;
                        overflow: hidden;
                    }}

                    #users-section th, #users-section td {{
                        padding: 12px 10px;
                        text-align: left;
                        font-size: 0.9rem;
                        color: var(--text);
                    }}

                    #users-section th {{
                        background: var(--primary);
                        color: white;
                        font-weight: 600;
                    }}

                    #users-section tr:nth-child(even) {{
                        background: rgba(93,64,55,0.05);
                    }}

                    #users-section tr:hover {{
                        background: rgba(93,64,55,0.1);
                    }}

                    #users-section .action-btns {{
                        display: flex;
                        gap: 8px;
                    }}

                    #users-section .btn-icon {{
                        width: 28px;
                        height: 28px;
                        border-radius: 6px;
                        border: none;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        cursor: pointer;
                        transition: 0.2s;
                    }}

                    #users-section .btn-edit {{
                        background: var(--success);
                        color: white;
                    }}

                    #users-section .btn-del {{
                        background: var(--danger);
                        color: white;
                    }}

                    #users-section .btn-icon:hover {{
                        transform: scale(1.1);
                    }}
                    
                    .order-history {{
                        background: rgba(255, 255, 255, 0.35); border-radius: 30px; padding: 30px;
                        border: 1px solid rgba(255, 255, 255, 0.5);
                        box-shadow: 15px 15px 35px #cfc6bb;
                    }}
                    table {{ width: 100%; border-collapse: collapse; }}
                    th {{ text-align: left; padding: 15px; color: #895737; border-bottom: 2px solid #E6CCB2; }}
                    td {{padding: 15px; border-bottom: 1px solid #E6CCB2; color: #5D4037; }}
                     .main-content {{ flex: 1; padding: 40px; overflow-y: auto; background-image: radial-gradient(at top right, rgba(137,87,55,0.05), transparent); }}
                    .section-title {{ font-family: 'Playfair Display', serif; color: var(--primary); font-size: 2.2rem; margin-bottom: 30px; }}
                    .product-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 30px; }}
                    
                    .product-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 30px; }}
                    .product-card {{
                        background: var(--glass); backdrop-filter: blur(10px);
                        border-radius: 25px; border: 1px solid var(--glass-border);
                        padding: 20px; text-align: center; transition: 0.3s;
                        box-shadow: 10px 10px 20px var(--shadow-dark), -5px -5px 15px var(--shadow-light);
                    }}
                    .product-card:hover {{ transform: translateY(-10px); }}
                    .product-card input{{width:100%;}}
                    .product-img {{
                        width: 100%; height: 150px; background: var(--bg); border-radius: 20px;
                        margin-bottom: 15px; display: flex; align-items: center; justify-content: center;
                        font-size: 3rem; color: var(--primary-light);
                        box-shadow: 5px 5px 10px var(--shadow-dark), -5px -5px 10px var(--shadow-light);
                    }}
                    .product-img img {{
                        width: 100%;
                        height: 100%;
                        border-radius: 20px;
                        object-fit: cover;
                        display: block;
                    }}

                    .price-tag {{ font-weight: 700; color: var(--primary); font-size: 1.2rem; display: block; margin-bottom: 5px; }}
                    .btn {{
                        width: 100%; padding: 10px; border-radius: 12px; border: none;
                        background: var(--primary); color: white; cursor: pointer;
                        transition: 0.3s; font-weight: 600;
                        background:var(--primary-light);
                        margin-top:10px;
                    }}
                    .dlt{{
                        background:var(--primary);
                    }}
                    .filter-bar{{
                        display:flex;
                        margin-top:10px;
                        gap:20px;
                        margin-bottom:30px;
                        background: var(--glass);
                        backdrop-filter: blur(12px);
                        border:1px solid var(--glass-border);
                        padding:15px 20px;
                        border-radius:20px;
                        box-shadow: 6px 6px 15px var(--shadow-dark), -4px -4px 12px var(--shadow-light);
                    }}

                    .search-box{{
                        flex:1;
                        position:relative;
                    }}

                    .search-box input{{
                        width:100%;
                        padding:12px 40px 12px 15px;
                        border-radius:15px;
                        border:none;
                        outline:none;
                        background: var(--bg);
                        color: var(--text);
                        font-weight:500;
                        box-shadow: inset 4px 4px 8px var(--shadow-dark), inset -4px -4px 8px var(--shadow-light);
                    }}

                    .search-box i{{
                        position:absolute;
                        right:15px;
                        top:50%;
                        transform:translateY(-50%);
                        color:var(--primary);
                    }}

                    .sort-box select{{
                        padding:12px 15px;
                        border-radius:15px;
                        border:none;
                        outline:none;
                        background: var(--bg);
                        color: var(--text);
                        font-weight:600;
                        cursor:pointer;
                        box-shadow: inset 4px 4px 8px var(--shadow-dark), inset -4px -4px 8px var(--shadow-light);
                    }}
                    
                    .navbar-heading{{
                        height: 70px;
                        display: flex;
                        top: 0;
                        justify-content: center;
                        align-items: center;
                        margin: 0px 0px 30px 0px;
                        padding: 0;
                        width: 100%;
                    }}
                    .navbar-heading .head{{
                        font-size: 2.3rem;
                        font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
                        font-weight: 700;
                        color: #895737;
                    }}
                    /* ======================= Admin view ======================= */
                    @media (max-width: 1300px) {{

                        /* Admin Navbar */
                        .admin-navbar .navbar-heading {{
                            flex-direction: column;
                            align-items: flex-start;
                            gap: 10px;
                        }}
                        .admin-navbar .navbar-heading .head {{
                            font-size: 1.6rem;
                        }}
                        .admin-navbar .navbar-heading img {{
                            width: 55px;
                        }}

                        /* Admin main content */
                        .admin-main {{
                            padding: 20px;
                        }}

                        /* Tables */
                        .admin-main table {{
                            width: 100%;
                            font-size: 0.9rem;
                        }}
                        .admin-main table th, .admin-main table td {{
                            padding: 10px;
                        }}
                        .top-stats{{
                            grid-template-columns: repeat(2, 1fr);
                            gap: 15px;
                        }}
                        .admin-grid{{
                            grid-template-columns: repeat(2, 1fr);
                            gap: 15px;
                        }}

                        /* Inputs and buttons */
                        .admin-main input[type="text"],
                        .admin-main input[type="number"],
                        .admin-main select,
                        .admin-main .btn {{
                            width: 100%;
                            font-size: 0.9rem;
                            padding: 8px 12px;
                        }}
                        .form-row {{
                            grid-template-columns: repeat(2, 1fr);
                            gap: 10px;
                        }}
                    }}

                    /* Tablets */
                    @media (max-width: 900px) {{
                        *{{
                            font-size:12px;
                        }}
                        .navbar-heading .head  {{
                            font-size: 20px;
                        }}
                        .top-stats{{
                            grid-template-columns: 1fr;
                            gap: 10px;
                        }}
                        .form-row {{
                            grid-template-columns: 1fr;
                            gap: 10px;
                        }}
                        .admin-grid{{
                            grid-template-columns: 1fr;
                            gap: 10px;
                        }}
                        .admin-main table th, .admin-main table td {{
                            font-size: 0.8rem;
                            padding: 8px;
                        }}
                    }}

                    /* Mobile */
                    @media (max-width: 500px) {{
                        .admin-navbar .navbar-heading .head {{
                            font-size: 1.1rem;
                        }}
                        .admin-navbar .navbar-heading img {{
                            width: 45px;
                        }}
                        .admin-main table th, .admin-main table td {{
                            font-size: 0.7rem;
                            padding: 6px;
                        }}
                        .admin-main input[type="text"],
                        .admin-main input[type="number"],
                        .admin-main select,
                        .admin-main .btn {{
                            font-size: 0.8rem;
                            padding: 6px 10px;
                        }}
                    }}
                </style>
            </head>
            <body>
                <aside class="sidebar">
                    <div class="sidebar-logo">
                        <i class="fas fa-crown"></i>
                        <span>Staff Console</span>
                    </div>
                    <ul class="admin-nav">
                        <li class="admin-nav-item active"><i class="fas fa-chart-line"></i> Dashboard</li>
                        <li class="admin-nav-item"><i class="fas fa-cookie-bite"></i> Items_bmp</li>
                        <li class="admin-nav-item"><i class="fas fa-receipt"></i> Orders_bmp</li>
                        <li class="admin-nav-item"><i class="fas fa-users-cog"></i> Customer_bmp</li>
                        <li class="admin-nav-item" onclick="window.location.href='/logout'" style="margin-top: 50px; color: var(--accent);"><i class="fas fa-power-off"></i> Logout</li>
                        <footer style="position:absolute; bottom:0px; left :0px; width:100%; height:40px; display:flex; justify-content:center; z-index:10; align-items:center; color: #F3E9DC; background:#895737;"><p>&copy; 2026 Bakery Management Programm (BMP) Project</p></footer>
                    </ul>
                    
                </aside>

                <main class="main" id="dashboard-section">
                    <div class="navbar-heading" style="gap:20px margin:0px 0px 20px 0px;">
                        <img src={project_logo} alt="BMP" style="width:80px; margin:0px 20px 0px 0px;">
                        
                        <h1 class="head">{get_project_name()}</h1>
                    </div>
                    <div class="top-stats">
                        <div class="stat-card">
                            <div class="stat-icon"><i class="fas fa-shopping-bag"></i></div>
                            <div class="stat-info"><h4>Daily Orders</h4><p>{get_daily_torders()}</p></div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-icon"><i class="fas fa-dollar-sign"></i></div>
                            <div class="stat-info"><h4>Revenue</h4><p>€{get_rev()}</p></div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-icon"><i class="fas fa-box"></i></div>
                            <div class="stat-info"><h4>Stock Items</h4><p>{get_stock()}</p></div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-icon"><i class="fas fa-user-friends"></i></div>
                            <div class="stat-info"><h4>Customers</h4><p>{get_tcustomer()}</p></div>
                        </div>
                    </div>

                    <div class="admin-grid">
                        <!-- Inventory Management -->
                        <section class="admin-panel">
                            <h3><i class="fas fa-tools"></i> Update Logo</h3>
                            <form method="POST" action="/update-heading-img" enctype="multipart/form-data">
                                <div class="form-group" style="margin-bottom: 25px;">
                                    <img src="{project_logo}" alt="Logo">
                                    <label>headingimage_bmp</label>
                                    <input type="file" name="heading_image" value="{project_logo}">
                                </div>

                                <button class="btn-action" type="submit">Update Image</button>
                            </form>
                        </section>

                        <!-- System Configuration -->
                        <section class="admin-panel">
                            <h3><i class="fas fa-tools"></i> Update Name</h3>
                            <form method="POST" action="/update-heading">
                                <div class="form-group" style="margin-bottom: 25px;">
                                    <label>heading_bmp</label>
                                    <input type="text" name="heading" value="{get_project_name()}">
                                </div>

                                <button class="btn-action" type="submit">Update Heading</button>
                            </form>
                        </section>
                        <div id="popup"></div>
                    </div>
                </main>
                
                <main id="inventory-section" class="main">
                    <div class="navbar-heading" style="gap:20px margin:0px 0px 20px 0px;">
                        <img src={project_logo} alt="BMP" style="width:80px; margin:0px 20px 0px 0px;">
                        <h1 class="head">{get_project_name()}</h1>
                    </div>
                    <div class="admin-content">
                        <section class="admin-panel">
                            <h3><i class="fas fa-boxes"></i> Inventory Control</h3>
                            <form method="POST" action="/add-item" enctype="multipart/form-data">
                                <div class="form-row">
                                    <div class="form-group">
                                        <label>itemname_bmp</label>
                                        <input type="text" name="itemname_bmp" placeholder="Cake" required>
                                    </div>
                                    <div class="form-group">
                                        <label>itemimage_bmp</label>
                                        <input type="file" name="itemimage_bmp" required>
                                    </div>
                                    <div class="form-group">
                                        <label>itemprice_bmp</label>
                                        <input type="number" step="0.01" name="itemprice_bmp" placeholder="0.00" required>
                                    </div>
                                    <div class="form-group">
                                        <label>itemquantity_bmp</label>
                                        <input type="number" name="itemquantity_bmp" placeholder="0" required>
                                    </div>
                                </div>
                                <button class="btn-action" type="submit">Add Item to Store</button>
                            </form>
                        </section>
                        <section id="shop-section" style="margin:20px 0px 0px 0px;">
                            <form class="filter-bar" method="POST" action="/">
                                <div class="search-box">
                                    <input 
                                        type="text" 
                                        name="search"
                                        placeholder="Search bakery items by ID..."
                                        value="{search}">
                                    <i class="fas fa-search"></i>
                                </div>

                                <div class="sort-box">
                                    <select>
                                        <option value="">Sort Items</option>
                                        <option value="quantity_asc">Quantity (Low → High)</option>
                                        <option value="quantity_desc">Quantity (High → Low)</option>
                                    </select>
                                </div>

                                <button style="display:none"></button>
                            </form>
                            <div class="product-grid" style="margin:20px 0px 0px 0px;">
                                {each_item_html}
                            </div>
                        </section>
                    </div>
                </main>
                <main id="orders-section" class="main">
                    <div class="navbar-heading" style="gap:20px margin:0px 0px 20px 0px;">
                        <img src={project_logo} alt="BMP" style="width:80px; margin:0px 20px 0px 0px;">
                        <h1 class="head">{get_project_name()}</h1>
                    </div>
                    <div class="order-history">
                        <table>
                            <thead>
                                <tr><th>Order_id_bmp</th><th>order_date_bmp</th><th>Items_bmp</th><th>Total_amount_bmp</th><th>order_Method_bmp</th></tr>
                            </thead>
                            <tbody>
                                {all_orders_html}
                            </tbody>
                        </table>
                    </div>
                </main>
                <main id="users-section" class="main" style="display:none;">
                    <div class="navbar-heading" style="gap:20px margin:0px 0px 20px 0px;">
                        <img src={project_logo} alt="BMP" style="width:80px; margin:0px 20px 0px 0px;">
                        <h1 class="head">{get_project_name()}</h1>
                    </div>
                    <table>
                        <thead>
                            <tr>
                                <th>id_customer_bmp</th>
                                <th>username_bmp</th>
                                <th>full_name_bmp</th>
                            </tr>
                        </thead>
                        <tbody>
                            {all_customers}
                        </tbody>
                    </table>
                </main>
            </body>
            
            <script>
                function showPopup(message, type="success") {{
                    const popup = document.getElementById("popup");
                    if (!popup) return;

                    // Set text
                    popup.textContent = message;

                    // Set background color: green for success, red for error
                    popup.style.background = type === "success" ? "#2e7d32" : "#c62828";

                    // Show it
                    popup.style.display = "block";

                    // Hide after 3 seconds
                    setTimeout(() => {{
                        popup.style.display = "none";
                    }}, 2000);
                    
                }}
                const msg = "{message}";
                const err = "{error}";
                if (msg) showPopup(msg, "success");
                if (err) showPopup(err, "error");
                
                const navItems = document.querySelectorAll('.admin-nav-item');
                const dashboardSection = document.getElementById('dashboard-section');
                const inventorySection = document.getElementById('inventory-section');
                const ordersSection = document.getElementById('orders-section');
                const usersSection = document.getElementById('users-section');
                
                navItems.forEach(item => {{
                    item.addEventListener('click', (e) => {{
                        navItems.forEach(i => i.classList.remove('active'));
                        e.currentTarget.classList.add('active');

                        const text = e.currentTarget.textContent.trim();

                        // Toggle visibility
                        dashboardSection.style.display = text === 'Dashboard' ? 'block' : 'none';
                        inventorySection.style.display = text === 'Items_bmp' ? 'block' : 'none';
                        ordersSection.style.display = text === 'Orders_bmp' ? 'block' : 'none';
                        usersSection.style.display = text === 'Customer_bmp' ? 'block' : 'none';
                    }});
                }});
                dashboardSection.style.display = 'block';
                inventorySection.style.display = 'none';
                ordersSection.style.display = 'none';
                usersSection.style.display = 'none';
                
                
                const grid = document.querySelector(".product-grid");
                const cards = Array.from(document.querySelectorAll(".product-card"));

                const searchInput = document.querySelector(".search-box input");
                const sortSelect = document.querySelector(".sort-box select");

                function renderCards(list){{
                    grid.innerHTML = "";
                    list.forEach(card => grid.appendChild(card));
                }}

                searchInput.addEventListener("input", () => {{
                const value = searchInput.value.trim();

                if (!value) {{
                    renderCards(cards); 
                    return;
                }}

                const filtered = cards.filter(card =>
                    card.dataset.id === value
                );

                renderCards(filtered);
            }});

                sortSelect.addEventListener("change", () => {{
                    let sorted = [...cards];

                    if(sortSelect.value === "quantity_asc"){{
                        sorted.sort((a,b)=> parseFloat(a.dataset.quantity) - parseFloat(b.dataset.quantity));
                    }}
                    else if(sortSelect.value === "quantity_desc"){{
                        sorted.sort((a,b)=> parseFloat(b.dataset.quantity) - parseFloat(a.dataset.quantity));
                    }}

                    renderCards(sorted);
                }});
                
                document.querySelectorAll(".update-btn").forEach(btn => {{
                    btn.addEventListener("click", async (e) => {{
                        e.preventDefault();

                        const card = btn.closest(".product-card");
                        const id = card.dataset.id;

                        const formData = new FormData();
                        formData.append("id", id);
                        formData.append("itemname_bmp", card.querySelector(".item-name").value);
                        formData.append("itemprice_bmp", card.querySelector(".item-price").value);
                        formData.append("itemquantity_bmp", card.querySelector(".item-quantity").value);

                        const imageFile = card.querySelector(".item-image").files[0];
                        if (imageFile) {{
                            formData.append("itemimage_bmp", imageFile);
                        }}

                        const response = await fetch("/update-item", {{
                            method: "POST",
                            body: formData
                        }});
                        alert("Item updated")
                        location.reload();
                    }});
                }});

                document.querySelectorAll(".delete-btn").forEach(btn => {{
                    btn.addEventListener("click", async (e) => {{
                        e.preventDefault();
                        const id = e.target.dataset.id;
                        const response = await fetch("/delete-item", {{
                        method: "POST",
                        headers: {{ "Content-Type": "application/x-www-form-urlencoded" }},
                        body: `id=${{id}}`
                        }});
                        const text = await response.text();
                        alert("Item Deleted")
                        location.reload();
                    }});
                }});
                
            </script>
        </html>
    """
    return page;

#  this function check if its int or not 
def input_int(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Invalid input please enter a number")

#################################### AUTH ################################################

# store all the login logout activity in app.log
def log_event(message: str, logfile: str = "app.log") -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(logfile, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {message}\n")

#  login function (customers)

def login(session, validate_function):
    if session.is_logged_in:
        print(f"Already logged in as {session.username_bmp}.")
        return session
    
    username_bmp = input("Username: ").strip()
    password_bmp = getpass.getpass("Password: ").strip()
    
    if validate_function(username_bmp, password_bmp):
        session.is_logged_in = True
        session.username_bmp = username_bmp
        session.customer_id,session.fullname = customer_details(username_bmp);
        print(f"Login successful. Welcome, {username_bmp}!")
        print(f"Your ID : {session.customer_id} , Name : {session.fullname}")
        log_event(f"LOGIN success user={username_bmp}")
    else:
        print(f"Invalid credentials.")
        log_event(f"LOGIN failed user={username_bmp}")
    return session

#  logout function for both customer and admin 
def logout(session):
    if not session.is_logged_in:
        print("Please Log in");
        return session
    user_bmp = session.username_bmp
    session.is_logged_in = False
    session.username_bmp = None
    session.customer_id = None
    session.fullname = None
    print("Logged out.")
    log_event(f"LOGOUT user={user_bmp}")
    return session

#  register function for customer
def register():
    username_bmp = input("Enter a unique username : ").strip();
    

    if check_username_customer(username_bmp):
        print("Username already exist try again");
        return;

    password_bmp = input("Create a Password: ").strip()
    password_bmp2 = input("Confirm Password: ").strip()

    if password_bmp != password_bmp2:
        print("Password doesn't match")
        return

    full_name_bmp = input("Enter your full name: ")

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO customer_bmp (username_bmp, password_bmp, full_name_bmp)
            VALUES (%s, %s, %s)
            """,
            (username_bmp, password_bmp, full_name_bmp)
        )
        conn.commit()
        print("Registration successful")
    finally:
        conn.close()
        
# new admin registration by admin control only 
def admin_register():
    username_bmp = input("Enter a unique username : ").strip();
    

    if check_username(username_bmp):
        print("Username already exist try again");
        return;

    password_bmp = input("Create a Password: ").strip()
    password_bmp2 = input("Confirm Password: ").strip()

    if password_bmp != password_bmp2:
        print("Password doesn't match")
        return

    full_name_bmp = input("Enter your full name: ")

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO users_bmp (username_bmp, password_bmp, full_name_bmp)
            VALUES (%s, %s, %s)
            """,
            (username_bmp, password_bmp, full_name_bmp)
        )
        conn.commit()
        print("New Admin Registration successful")
    finally:
        conn.close()

#  admin login 
def admin_login(session, validate_function):
    if session.is_logged_in:
        print(f"Already logged in as {session.username_bmp}.")
        return session
    
    username_bmp = input("Username: ").strip()
    password_bmp = getpass.getpass("Password: ").strip()
    
    if validate_function(username_bmp, password_bmp):
        session.is_logged_in = True
        session.username_bmp = username_bmp
        session.admin_id,session.fullname = admin_details(username_bmp);
        print(f"Login successful. Welcome, {username_bmp}!")
        print(f"Your ID : {session.admin_id} , Name : {session.fullname}")
        log_event(f"LOGIN success user={username_bmp}")
    else:
        print(f"Invalid credentials.")
        log_event(f"LOGIN failed user={username_bmp}")
    return session

# abin 
################################ ADMIN ###############################################
#  viewing all items items_bmp

def view_items():
    print("-" * 46)
    print(f"{'ID'.ljust(3)} | "f"{'Name'.ljust(20)} | "f"{'Price'.ljust(6)} | "f"{'Quantity'.ljust(10)}")
    print("-" * 46)

    for item in get_menu_items():
        print(f"{str(item[0]).ljust(3)} | "f"{str(item[1])[:20].ljust(20)} | "f"{str(item[2]).ljust(6)} | "f"{str(item[3]).ljust(10)}")

    print("-" * 46)

# bubble sort on quantity for admin 
def bubble_sort_by_quantity(menu_list):
    n = len(menu_list)

    for i in range(n - 1):
        for j in range(n - 1 - i):
            if menu_list[j][3] > menu_list[j + 1][3]:
                menu_list[j], menu_list[j + 1] = menu_list[j + 1], menu_list[j]

    return menu_list

# printing only one item by id calling it places like when we remove an item 
def print_one_item(item_id): # cli part 
    item = get_one_item(item_id);
    if(item):
        print("-" * 46)
        print(f"{'ID'.ljust(3)} | "f"{'Name'.ljust(20)} | "f"{'Price'.ljust(6)} | "f"{'Quantity'.ljust(10)}")
        print("-" * 46)
        print(f"{str(item[0]).ljust(3)} | "f"{str(item[1])[:20].ljust(20)} | "f"{str(item[2]).ljust(6)} | "f"{str(item[3]).ljust(10)}")
        print("-" * 46)
        return True;
    return False;

# mohammad azhaf alam 

def manage_items(session):
    print("-"*20);
    print("1. View Menu")
    print("2. Add Item")
    print("3. Update Item price")
    print("4. Update Item Quantity")
    print("5. remove Item")
    print("6. Exit")
    choice = input("Enter Your Choice : ")
    if (choice == "1"):
        view_items();
        return manage_items(session)
    elif choice == "2":
        item_name = input("Enter Item name : ");
        item_price = input_int("Enter Item Price : ");
        item_quantity = input_int("Enter Item Quantity : ");
        add_item_db(item_name,item_price,item_quantity)
        return manage_items(session)
    elif choice == "3":
        item_id = input_int("Enter Item ID : ");
        if not print_one_item(item_id):
            return manage_items(session)
        new_price = input_int("Enter new Price : ");
        update_price(item_id,new_price);
        return manage_items(session)
    elif choice == "4":
        item_id = input_int("Enter Item ID : ");
        if not print_one_item(item_id):
            return manage_items(session)
        new_quantity = input_int("Enter new Quantity : ");
        update_quantity(item_id,new_quantity);
        return manage_items(session)
    elif choice == "5":
        item_id = input_int("Enter Item ID to Remove : ");
        print_one_item(item_id)
        remove_item(item_id)
        return manage_items(session)
    elif choice == "6":
        return ; 
    else: return;

# search item using binary search
def search_item_bs(item_id):
    items = get_menu_items()

    low = 0
    high = len(items) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_id = items[mid][0] 

        if mid_id == item_id:
            print_one_item(item_id)
            return
        elif item_id < mid_id:
            high = mid - 1
        else:
            low = mid + 1

    print("Item not found with the ID : ",item_id)
    
def admin_menu(session):
    print("\n==============================")
    print("          Admin Menu          ")
    print("==============================")
    print("1. View all items");
    print("2. Sort Items by Quantity");
    print("3. Search Items by id");
    print("4. Manage Items");
    print("5. Modify Header");
    print("6. Add Admin");
    print("7. Exit");
    choice = input("Enter Your Choice : ");
    match choice:
        case "1":
            view_items();
            return admin_menu(session);
        case "2":
            menu_list = get_menu_items()
            bubble_sort_by_quantity(menu_list);
            
            print("-" * 46)
            print(f"{'ID'.ljust(3)} | "f"{'Name'.ljust(20)} | "f"{'Price'.ljust(6)} | "f"{'Quantity'.ljust(10)}")
            print("-" * 46)

            for item in menu_list:
                print(f"{str(item[0]).ljust(3)} | "f"{str(item[1])[:20].ljust(20)} | "f"{str(item[2]).ljust(6)} | "f"{str(item[3]).ljust(10)}")

            print("-" * 46)
            
            return admin_menu(session);
        case "3":
            item_id = input_int("Enter Item Id to search : ");
            search_item_bs(item_id);
            return admin_menu(session);
        case "4":
            manage_items(session);
            return admin_menu(session);
        case "5":
            print(f"The previous heading is : {get_project_name()}")
            new_heading_bmp = input("Enter New Heading : ")
            update_heading(new_heading_bmp);
            return admin_menu(session);
        case "6":
            admin_register();
            return admin_menu(session)
        case "7":
            print("bye!");
            return;
        case _:
            return;
# ishika nath
############################## CUSTOMER ######################################
#  this one print menu by list we gave it not all not few just the list we gave it 
def print_menu_order(menu_list):
    print("-" * 46)
    print(f"{'ID'.ljust(3)} | "f"{'Name'.ljust(20)} | "f"{'Price'.ljust(6)} | "f"{'Quantity'.ljust(10)}")
    print("-" * 46)
    for item in menu_list:
        print(f"{str(item[0]).ljust(3)} | "f"{str(item[1])[:20].ljust(20)} | "f"{str(item[2]).ljust(6)} | "f"{str(item[3]).ljust(10)}")
    print("-" * 46)
  
#  bubble sort on price for customers
def bubble_sort_by_price(menu_list):
    n = len(menu_list)

    for i in range(n - 1):
        for j in range(n - 1 - i):
            if menu_list[j][2] > menu_list[j + 1][2]:
                menu_list[j], menu_list[j + 1] = menu_list[j + 1], menu_list[j]

    return menu_list  

# bubble sort by name casue python read char by ASCII value simple
def bubble_sort_by_name(menu_list):
    n = len(menu_list)

    for i in range(n - 1):
        for j in range(n - 1 - i):
            if menu_list[j][1].lower() > menu_list[j + 1][1].lower():
                menu_list[j], menu_list[j + 1] = menu_list[j + 1], menu_list[j]
    return menu_list;
    
def sort_items_menu(session):
    print("1. Acc Price");
    print("2. Dec Price");
    print("3. A -> Z");
    print("4. Z -> A");
    print("5. Exit");
    choice = input("Enter your choice : ")
    if choice == "1":
        menu_list = get_menu_items()
        bubble_sort_by_price(menu_list);
        print_menu_order(menu_list)
        return sort_items_menu(session)
    elif choice == "2":
        menu_list = get_menu_items()
        bubble_sort_by_price(menu_list)
        print_menu_order(menu_list[::-1])
        return sort_items_menu(session)
    elif choice == "3":
        menu_list = get_menu_items();
        bubble_sort_by_name(menu_list)
        print_menu_order(menu_list)
        return sort_items_menu(session)
    elif choice == "4":
        menu_list = get_menu_items();
        bubble_sort_by_name(menu_list)
        print_menu_order(menu_list[::-1])
        return sort_items_menu(session)
    elif choice == "5":
        print("Back");
        return;
    else:
        print("Invalid Choice!");
        return;
    
# ankit
# cart 
class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, item_id_bmp, itemname_bmp, itemprice_bmp, itemquantity_bmp):
        self.items.append([item_id_bmp, itemname_bmp, itemprice_bmp, itemquantity_bmp])

    def view(self):
        if not self.items:
            print("Cart is empty")
            return
        else:
            print("-" * 46)
            print(f"{'ID'.ljust(3)} | "f"{'Name'.ljust(20)} | "f"{'Price'.ljust(6)} | "f"{'Quantity'.ljust(10)}")
            print("-" * 46)

            for item in self.items:
                print(f"{str(item[0]).ljust(3)} | "f"{str(item[1])[:20].ljust(20)} | "f"{str(item[2]).ljust(6)} | "f"{str(item[3]).ljust(10)}")
                
            print("-" * 46)
    def remove_item(self, item_id_bmp):
        for item in self.items:
            if item[0] == item_id_bmp:
                self.items.remove(item)
                print("Item removed from cart")
                return
        print("Item not found in cart")
            
    def update_item(self, item_id_bmp, new_quantity):
        for item in self.items:
            if item[0] == item_id_bmp:
                item[3] = new_quantity
                print(f"Quantity updated to {new_quantity}")
                return
        print("Item not found in cart")
    
    def clear(self):
        self.items.clear()
        print("Cart cleared")
    
    def total_amount(self):
        tp = 0;
        for item in self.items:
            tp += item[2]*item[3];
        return tp;
    
#  print the last slip for customer to print 
def print_slip(session,cart):
    print("-" * 46);
    print(f"{'Name: ' + session.fullname:<28}{'Customer ID: ' + str(session.customer_id):>14}")
    print(f"{'Username: ' + session.username_bmp:<28}{'Date: ' + datetime.now().strftime('%Y-%m-%d'):>14}")
    print("-" * 46);
    print(f"{'ID'.ljust(3)} | "f"{'Name'.ljust(20)} | "f"{'Price'.ljust(6)} | "f"{'Quantity'.ljust(10)}")
    print("-" * 46);
    for item in cart.items:
        print(f"{str(item[0]).ljust(3)} | "f"{str(item[1])[:20].ljust(20)} | "f"{str(item[2]).ljust(6)} | "f"{str(item[3]).ljust(10)}")
    print("-" * 46)
    print(f"{'Total:':>33}{cart.total_amount():>9}")
    

def chekout(session,cart):
    print('-'*20);
    method = input("Press 1 for card payment for cash press anything: ")
    method = "Card" if method == "1" else "Cash"
    print(f"Payment method : {method}")
    total_amount = cart.total_amount();
    if not cart.items:
        print("No items in your cart")
        return manage_cart(session, cart)
    else:
        order_id_bmp = add_order_bmp(session.username_bmp,total_amount,method);
        for item in cart.items:
            add_order_items_bmp(order_id_bmp,item[0],item[1],item[3],item[2],item[3]*item[2]);
        print_slip(session,cart);
        return logout(session);    
        

def manage_cart(session,cart):
    print("-"*30);
    print("1. View Cart");
    print("2. Add item to cart");
    print("3. update quantity of yor items");
    print("4. Remove item from cart");
    print("5. Delete my cart");
    print("6. Checkout");
    print("7. Exit");
    choice = input("Enetr Your Choice : ");
    if choice == "1":
        cart.view();
        return manage_cart(session,cart);
    elif choice == "2":
        view_items();
        print("Which Item do you want to add")
        cus_id_bmp = input_int("Enter Item Id: ");
        item = check_id_item(cus_id_bmp)
        if item:
            cus_quantity_bmp = input_int("Enter Quantity: ");
            if(cus_quantity_bmp <= item[3]):
                cart.add_item(item[0],item[1],item[3],cus_quantity_bmp)
                return manage_cart(session,cart)
            print("Your Required Quantity is not available rn")
        print("There no item with this id") 
        return manage_cart(session,cart)
    
    elif choice == "3":
        cart.view()
        item_id_bmp = input_int("Enter the ID you your Item: ");

        found = False
        for item in cart.items:
            if item[0] == item_id_bmp:
                found = True
                new_quantity = input_int(f"Enter quantity for {item[1]}: ")
                cart.update_item(item_id_bmp, new_quantity)
                break
        
        if not found:
            print("Item not found in cart")
        
        return manage_cart(session, cart)
        
    elif choice == "4":
        cart.view();
        item_id_bmp = input_int("Enter ID of item you want to remove : ");
        cart.remove_item(item_id_bmp);
        return manage_cart(session,cart);
    elif choice == "5":
        cart.clear();
        return manage_cart(session,cart);
    elif choice == "6":
        chekout(session,cart);
        return ;
    elif choice == "7":
        print("Back");
        return;
    else:
        return;
################################ MAIN ##############################################
def show_menu(session):
    print("\n==============================")
    print(get_project_name())
    print("==============================")
    if session.is_logged_in:
        print(f"Logged in as: {session.username_bmp}")
        print("1. View Menu")
        print("2. Sort Items")
        print("3. Search Item")
        print("4. Manage Cart")
        print("5. Logout")
        print("6. Exit")
    else:
        print("Not logged in")
        print("1. Login")
        print("2. Register")
        print("3. Admin Login")
        print("4. Exit")

def main_loop(session):
    show_menu(session);
    choice = input("Enter Your Choice : ");
    if not session.is_logged_in:
        if choice == "1":
            session = login(session, validate_credentials_customer);
            return main_loop(session)
        elif choice == "2":
            register();
            return main_loop(session)
        elif choice == "3":
            session = admin_login(session, validate_credentials_admin)
            if session.is_logged_in :
                admin_menu(session);
            logout(session);
            return main_loop(session)
        elif choice == "4":
            print("Bye!")
            return
        else:
            print("Invalid option.")
            return main_loop(session)
    else:
        if choice == "1":
            view_items();
            return main_loop(session)
        elif choice == "2":
            sort_items_menu(session);
            return main_loop(session)
        elif choice == "3":
            name_bmp = input("Enter Item name : ")
            items_list = search_item_by_name(name_bmp);
            if items_list:
                print_menu_order(items_list)
            return main_loop(session)
        elif choice == "4":
            cart = Cart()
            manage_cart(session,cart);
            return main_loop(session)
        elif choice == "5":
            session = logout(session)
            return main_loop(session)
        elif choice == "6":
            print("Bye!")
            return
        else:
            print("Invalid option.")
            return main_loop(session)

if __name__ == "__main__":
    # session = Session();
    # main_loop(session);
    server = HTTPServer(("", 7000), SimpleHandler);
    print("Server is running at http://localhost:7000");
    server.serve_forever();