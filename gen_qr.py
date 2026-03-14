import qrcode
import os

# Laptop ka IP Address (Jo aapke phone mein chalta hai)
# Ise wahi rakhein jo aapne app.py mein dekha tha
IP_ADDRESS = "172.20.10.2" 
PORT = "5000"

def generate_table_qrs(num_tables):
    # static folder ke andar qrcodes naam ka folder banana
    if not os.path.exists('static/qrcodes'):
        os.makedirs('static/qrcodes')
        print("📁 'static/qrcodes' folder ban gaya hai.")

    for i in range(1, num_tables + 1):
        # QR Code ka link: isme table number auto-add hoga
        url = f"http://{IP_ADDRESS}:{PORT}/?table={i}"
        
        # QR Code design settings
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Image banana
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Image save karna
        file_path = f"static/qrcodes/table_{i}.png"
        img.save(file_path)
        print(f"✅ Table {i} ka QR Code taiyaar: {file_path}")

if __name__ == "__main__":
    # Jitni tables aapke cafe mein hain, utne QR ban jayenge
    # Abhi ke liye 5 tables set hain
    generate_table_qrs(5)
    print("\n🎉 Saare QR Codes 'static/qrcodes' folder mein mil jayenge!")