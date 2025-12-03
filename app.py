import streamlit as st
import pandas as pd
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="Product Stock & Billing System",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for animations and responsiveness
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Animated header */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animated-header {
        animation: fadeInDown 0.8s ease-out;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Card animations */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Metric cards */
    .css-1xarl3l {
        animation: slideIn 0.6s ease-out;
    }
    
    /* Responsive table */
    .dataframe {
        width: 100%;
        overflow-x: auto;
    }
    
    /* Success message animation */
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .success-message {
        animation: bounce 0.6s ease;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Input fields */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main {
            padding: 0.5rem;
        }
        .animated-header {
            font-size: 1.2rem;
            padding: 0.8rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Helper function to format currency
def format_currency(amount):
    """Format amount as Rs with Indian numbering system"""
    return f"Rs {amount:,.2f}"

# Initialize session state
if 'products' not in st.session_state:
    st.session_state.products = {
        1: {"name": "Soap", "price": 150, "quantity": 50, "expiry_date": "2025-05-10", "category": "Cosmetics"},
        2: {"name": "Oil", "price": 200, "quantity": 40, "expiry_date": "2026-05-10", "category": "Grocery"},
        3: {"name": "Shampoo", "price": 300, "quantity": 78, "expiry_date": "2027-09-10", "category": "Cosmetics"},
        4: {"name": "Biscuit", "price": 40, "quantity": 69, "expiry_date": "2027-09-10", "category": "Grocery"}
    }

if 'categories' not in st.session_state:
    st.session_state.categories = {"Cosmetics", "Grocery"}

if 'sales_history' not in st.session_state:
    st.session_state.sales_history = []

if 'cart' not in st.session_state:
    st.session_state.cart = []

if 'next_product_id' not in st.session_state:
    st.session_state.next_product_id = max(st.session_state.products.keys()) + 1 if st.session_state.products else 1

# Header
st.markdown('<div class="animated-header"><h1>🛒 Product Stock & Billing System</h1></div>', unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("### 📋 Navigation")
    page = st.radio(
        "Select Option:",
        ["🏠 Dashboard", "📦 Display Products", "➕ Add Product", "🔄 Update Stock", "💳 Generate Bill", "📊 Categories", "📈 Sales History"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    total_products = len(st.session_state.products)
    total_stock = sum(p["quantity"] for p in st.session_state.products.values())
    st.metric("Total Products", total_products)
    st.metric("Total Stock", total_stock)

# Dashboard Page
if page == "🏠 Dashboard":
    st.markdown("## 📊 Dashboard Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Products",
            value=len(st.session_state.products),
            delta="Active"
        )
    
    with col2:
        total_value = sum(p["price"] * p["quantity"] for p in st.session_state.products.values())
        st.metric(
            label="Total Inventory Value",
            value=format_currency(total_value)
        )
    
    with col3:
        st.metric(
            label="Total Stock",
            value=sum(p["quantity"] for p in st.session_state.products.values())
        )
    
    with col4:
        st.metric(
            label="Categories",
            value=len(st.session_state.categories)
        )
    
    st.markdown("---")
    
    # Product overview chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📦 Stock Levels")
        if st.session_state.products:
            chart_data = pd.DataFrame([
                {"Product": p["name"], "Quantity": p["quantity"]}
                for p in st.session_state.products.values()
            ])
            st.bar_chart(chart_data, x="Product", y="Quantity", use_container_width=True)
        else:
            st.info("No products to display")
    
    with col2:
        st.markdown("### 💰 Product Prices")
        if st.session_state.products:
            chart_data_price = pd.DataFrame([
                {"Product": p["name"], "Price": p["price"]}
                for p in st.session_state.products.values()
            ])
            st.bar_chart(chart_data_price, x="Product", y="Price", use_container_width=True)
        else:
            st.info("No products to display")

# Display Products Page
elif page == "📦 Display Products":
    st.markdown("## 📦 Available Products")
    
    # Search and filter options
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        search_term = st.text_input("🔍 Search Products", placeholder="Enter product name...")
    with col2:
        category_filter = st.selectbox("Filter by Category", ["All"] + sorted(list(st.session_state.categories)))
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    if st.session_state.products:
        # Filter products
        filtered_products = {}
        for key, value in st.session_state.products.items():
            # Search filter
            if search_term and search_term.lower() not in value["name"].lower():
                continue
            # Category filter
            if category_filter != "All" and value.get("category", "") != category_filter:
                continue
            filtered_products[key] = value
        
        if filtered_products:
            df = pd.DataFrame([
                {
                    "ID": key,
                    "Name": value["name"],
                    "Price": format_currency(value["price"]),
                    "Quantity": value["quantity"],
                    "Category": value.get("category", "N/A"),
                    "Expiry Date": value["expiry_date"]
                }
                for key, value in filtered_products.items()
            ])
            
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Product cards
            st.markdown("### Product Cards")
            cols = st.columns(3)
            for idx, (key, product) in enumerate(filtered_products.items()):
                with cols[idx % 3]:
                    with st.container():
                        stock_color = "#28a745" if product['quantity'] > 20 else "#ffc107" if product['quantity'] > 5 else "#dc3545"
                        st.markdown(f"""
                        <div style='padding: 1rem; border-radius: 10px; background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%); margin-bottom: 1rem;'>
                            <h3>🏷️ {product['name']}</h3>
                            <p><strong>Price:</strong> {format_currency(product['price'])}</p>
                            <p><strong>Stock:</strong> <span style='color: {stock_color}; font-weight: bold;'>{product['quantity']} units</span></p>
                            <p><strong>Category:</strong> {product.get('category', 'N/A')}</p>
                            <p><strong>Expiry:</strong> {product['expiry_date']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Delete button
                        if st.button(f"🗑️ Delete", key=f"del_{key}", use_container_width=True):
                            del st.session_state.products[key]
                            st.success(f"Deleted {product['name']}!")
                            time.sleep(0.5)
                            st.rerun()
        else:
            st.warning("No products match your search criteria!")
    else:
        st.info("No products available. Add some products to get started!")

# Add Product Page
elif page == "➕ Add Product":
    st.markdown("## ➕ Add New Product")
    
    # Auto-generate next ID
    st.info(f"💡 Next available Product ID: {st.session_state.next_product_id}")
    
    with st.form("add_product_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            use_auto_id = st.checkbox("Use Auto-Generated ID", value=True)
            if use_auto_id:
                key = st.session_state.next_product_id
                st.markdown(f"**Product ID:** {key}")
            else:
                key = st.number_input("Product ID", min_value=1, step=1, value=st.session_state.next_product_id)
            
            name = st.text_input("Product Name *", placeholder="e.g., Soap")
            price = st.number_input("Price (Rs) *", min_value=0.0, step=0.50, format="%.2f")
        
        with col2:
            quantity = st.number_input("Quantity *", min_value=0, step=1, value=10)
            expiry_date = st.date_input("Expiry Date *")
            
            # Category dropdown with option to add new
            existing_categories = ["-- Select or Add New --"] + sorted(list(st.session_state.categories))
            selected_category = st.selectbox("Category", existing_categories)
            
            if selected_category == "-- Select or Add New --":
                category = st.text_input("New Category Name")
            else:
                category = selected_category
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("✅ Add Product", use_container_width=True)
        with col2:
            reset = st.form_submit_button("🔄 Reset Form", use_container_width=True)
        
        if submitted:
            if key in st.session_state.products:
                st.error("❌ Product ID already exists! Uncheck 'Use Auto-Generated ID' to choose different ID.")
            elif not name:
                st.error("❌ Please enter product name!")
            elif price <= 0:
                st.error("❌ Price must be greater than 0!")
            elif not category or category == "-- Select or Add New --":
                st.error("❌ Please select or enter a category!")
            else:
                st.session_state.products[key] = {
                    "name": name,
                    "price": price,
                    "quantity": quantity,
                    "expiry_date": str(expiry_date),
                    "category": category
                }
                if category:
                    st.session_state.categories.add(category)
                
                # Update next product ID
                st.session_state.next_product_id = max(st.session_state.products.keys()) + 1
                
                st.success(f"✅ Product '{name}' added successfully with ID {key}!")
                st.balloons()
                time.sleep(1)
                st.rerun()

# Update Stock Page
elif page == "🔄 Update Stock":
    st.markdown("## 🔄 Update Product Stock")
    
    if st.session_state.products:
        product_names = {key: f"{key} - {value['name']}" for key, value in st.session_state.products.items()}
        
        selected = st.selectbox("Select Product", options=list(product_names.keys()), format_func=lambda x: product_names[x])
        
        if selected:
            current_qty = st.session_state.products[selected]["quantity"]
            st.info(f"Current Stock: {current_qty} units")
            
            col1, col2 = st.columns(2)
            
            with col1:
                add_qty = st.number_input("Quantity to Add", min_value=0, step=1)
                if st.button("➕ Add Stock", use_container_width=True):
                    st.session_state.products[selected]["quantity"] += add_qty
                    st.success(f"✅ Added {add_qty} units!")
                    time.sleep(1)
                    st.rerun()
            
            with col2:
                remove_qty = st.number_input("Quantity to Remove", min_value=0, step=1)
                if st.button("➖ Remove Stock", use_container_width=True):
                    if remove_qty <= st.session_state.products[selected]["quantity"]:
                        st.session_state.products[selected]["quantity"] -= remove_qty
                        st.success(f"✅ Removed {remove_qty} units!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Not enough stock!")
    else:
        st.info("No products available!")

# Generate Bill Page
elif page == "💳 Generate Bill":
    st.markdown("## 💳 Generate Bill")
    
    customer_name = st.text_input("Customer Name")
    
    st.markdown("### 🛒 Add Items to Cart")
    
    col1, col2, col3 = st.columns([3, 2, 1])
    
    with col1:
        if st.session_state.products:
            product_names = {key: f"{value['name']} ({format_currency(value['price'])}) - Stock: {value['quantity']}" 
                           for key, value in st.session_state.products.items()}
            selected_product = st.selectbox("Select Product", options=list(product_names.keys()), 
                                          format_func=lambda x: product_names[x])
    
    with col2:
        quantity = st.number_input("Quantity", min_value=1, step=1, value=1)
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Add to Cart", use_container_width=True):
            if selected_product in st.session_state.products:
                if quantity <= st.session_state.products[selected_product]["quantity"]:
                    st.session_state.cart.append({
                        "key": selected_product,
                        "name": st.session_state.products[selected_product]["name"],
                        "price": st.session_state.products[selected_product]["price"],
                        "quantity": quantity,
                        "total": st.session_state.products[selected_product]["price"] * quantity
                    })
                    st.success("✅ Added to cart!")
                else:
                    st.error("❌ Not enough stock!")
    
    # Display cart
    if st.session_state.cart:
        st.markdown("### 🛒 Current Cart")
        
        cart_df = pd.DataFrame(st.session_state.cart)
        st.dataframe(cart_df, use_container_width=True, hide_index=True)
        
        total_amount = sum(item["total"] for item in st.session_state.cart)
        
        # Discount and tax options
        col1, col2 = st.columns(2)
        with col1:
            discount_percent = st.number_input("Discount (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.5)
        with col2:
            tax_percent = st.number_input("Tax/GST (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.5)
        
        discount_amount = (total_amount * discount_percent) / 100
        subtotal = total_amount - discount_amount
        tax_amount = (subtotal * tax_percent) / 100
        final_total = subtotal + tax_amount
        
        # Display calculation
        st.markdown("### 💰 Bill Summary")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Subtotal:** {format_currency(total_amount)}")
            st.markdown(f"**Discount ({discount_percent}%):** -{format_currency(discount_amount)}")
            st.markdown(f"**Tax/GST ({tax_percent}%):** +{format_currency(tax_amount)}")
        with col2:
            st.markdown(f"### **Grand Total:** {format_currency(final_total)}")
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([2, 2, 2])
        
        with col2:
            if st.button("🗑️ Clear Cart", use_container_width=True):
                st.session_state.cart = []
                st.rerun()
        
        with col3:
            if st.button("✅ Generate Bill", use_container_width=True):
                if customer_name:
                    # Update stock
                    for item in st.session_state.cart:
                        st.session_state.products[item["key"]]["quantity"] -= item["quantity"]
                    
                    # Save to history
                    st.session_state.sales_history.append({
                        "customer": customer_name,
                        "items": st.session_state.cart.copy(),
                        "subtotal": total_amount,
                        "discount": discount_amount,
                        "tax": tax_amount,
                        "total": final_total,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                    # Show bill
                    st.markdown("---")
                    st.markdown("## 🧾 Bill Receipt")
                    st.markdown(f"""
                    <div style='padding: 2rem; border-radius: 10px; background: white; border: 2px solid #667eea;'>
                        <h2 style='text-align: center; color: #667eea;'>📋 INVOICE</h2>
                        <hr>
                        <p><strong>Customer:</strong> {customer_name}</p>
                        <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                        <hr>
                    """, unsafe_allow_html=True)
                    
                    for item in st.session_state.cart:
                        st.markdown(f"**{item['name']}** x {item['quantity']} = {format_currency(item['total'])}")
                    
                    st.markdown(f"""
                        <hr>
                        <p><strong>Subtotal:</strong> {format_currency(total_amount)}</p>
                        <p><strong>Discount ({discount_percent}%):</strong> -{format_currency(discount_amount)}</p>
                        <p><strong>Tax/GST ({tax_percent}%):</strong> +{format_currency(tax_amount)}</p>
                        <hr>
                        <h3 style='color: #667eea;'>Grand Total: {format_currency(final_total)}</h3>
                        <p style='text-align: center; margin-top: 2rem;'>Thank you for your business! 🙏</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.balloons()
                    st.session_state.cart = []
                else:
                    st.error("❌ Please enter customer name!")

# Categories Page
elif page == "📊 Categories":
    st.markdown("## 📊 Product Categories")
    
    if st.session_state.categories:
        cols = st.columns(3)
        for idx, category in enumerate(st.session_state.categories):
            with cols[idx % 3]:
                st.markdown(f"""
                <div style='padding: 1.5rem; border-radius: 10px; background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%); 
                text-align: center; margin-bottom: 1rem;'>
                    <h3>📁 {category}</h3>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ➕ Add New Category")
    new_category = st.text_input("Category Name")
    if st.button("Add Category", use_container_width=True):
        if new_category:
            st.session_state.categories.add(new_category)
            st.success("✅ Category added!")
            time.sleep(1)
            st.rerun()

# Sales History Page
elif page == "📈 Sales History":
    st.markdown("## 📈 Sales History")
    
    if st.session_state.sales_history:
        # Summary metrics
        total_sales = sum(sale['total'] for sale in st.session_state.sales_history)
        total_transactions = len(st.session_state.sales_history)
        avg_sale = total_sales / total_transactions if total_transactions > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Sales", format_currency(total_sales))
        with col2:
            st.metric("Total Transactions", total_transactions)
        with col3:
            st.metric("Average Sale", format_currency(avg_sale))
        
        st.markdown("---")
        
        # Search and filter
        col1, col2 = st.columns(2)
        with col1:
            search_customer = st.text_input("🔍 Search by Customer Name")
        with col2:
            sort_order = st.selectbox("Sort by", ["Newest First", "Oldest First", "Highest Amount", "Lowest Amount"])
        
        # Filter and sort
        filtered_sales = st.session_state.sales_history.copy()
        if search_customer:
            filtered_sales = [s for s in filtered_sales if search_customer.lower() in s['customer'].lower()]
        
        if sort_order == "Newest First":
            filtered_sales = list(reversed(filtered_sales))
        elif sort_order == "Highest Amount":
            filtered_sales = sorted(filtered_sales, key=lambda x: x['total'], reverse=True)
        elif sort_order == "Lowest Amount":
            filtered_sales = sorted(filtered_sales, key=lambda x: x['total'])
        
        st.markdown(f"### Showing {len(filtered_sales)} transaction(s)")
        
        for idx, sale in enumerate(filtered_sales):
            sale_num = st.session_state.sales_history.index(sale) + 1
            with st.expander(f"🧾 Sale #{sale_num} - {sale['customer']} - {format_currency(sale['total'])} - {sale['date']}"):
                st.markdown(f"**Date:** {sale['date']}")
                st.markdown(f"**Customer:** {sale['customer']}")
                st.markdown("**Items:**")
                for item in sale['items']:
                    st.markdown(f"- {item['name']} x {item['quantity']} = {format_currency(item['total'])}")
                
                st.markdown("---")
                st.markdown(f"**Subtotal:** {format_currency(sale.get('subtotal', sale['total']))}")
                if 'discount' in sale and sale['discount'] > 0:
                    st.markdown(f"**Discount:** -{format_currency(sale['discount'])}")
                if 'tax' in sale and sale['tax'] > 0:
                    st.markdown(f"**Tax/GST:** +{format_currency(sale['tax'])}")
                st.markdown(f"### **Total: {format_currency(sale['total'])}**")
        
        # Export option
        st.markdown("---")
        if st.button("📥 Export Sales Data (CSV)", use_container_width=True):
            sales_data = []
            for idx, sale in enumerate(st.session_state.sales_history):
                for item in sale['items']:
                    sales_data.append({
                        "Sale #": idx + 1,
                        "Date": sale['date'],
                        "Customer": sale['customer'],
                        "Product": item['name'],
                        "Quantity": item['quantity'],
                        "Price": item['price'],
                        "Item Total": item['total'],
                        "Bill Total": sale['total']
                    })
            
            df_export = pd.DataFrame(sales_data)
            csv = df_export.to_csv(index=False)
            st.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name=f"sales_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.info("No sales history available yet!")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>Made with ❤️ using Streamlit</div>",
    unsafe_allow_html=True
)
