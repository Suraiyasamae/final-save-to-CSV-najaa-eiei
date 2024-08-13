import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# อ่านไฟล์ CSV
data = pd.read_csv('thermal_data.csv', header=None)

# ฟังก์ชันในการกำหนดสีตามช่วงอุณหภูมิ
def temperature_to_color(t):
    if t < 27.99:
        return (235/255, 131/255, 52/255)  # สีส้ม
    elif t < 28.51:
        return (235/255, 195/255, 52/255)  # สีเหลืองอ่อน
    elif t < 28.99:
        return (228/255, 235/255, 52/255)  # สีเขียวอ่อน
    elif t < 29.51:
        return (187/255, 235/255, 52/255)  # สีเขียวเข้ม
    elif t < 29.99:
        return (177/255, 235/255, 52/255)  # สีเขียวอ่อนมาก
    elif t < 30.51:
        return (52/255, 235/255, 110/255)  # สีเขียว
    elif t < 30.99:
        return (52/255, 235/255, 191/255)  # สีน้ำเงินเขียว
    elif t < 31.55:
        return (52/255, 235/255, 235/255)  # สีฟ้าอ่อน
    elif t < 31.99:
        return (83/255, 213/255, 83/255)  # สีเขียว
    elif t < 32.55:
        return (52/255, 177/255, 235/255)  # สีน้ำเงินอ่อน
    elif t < 32.99:
        return (52/255, 142/255, 235/255)  # สีน้ำเงิน
    elif t < 33.55:
        return (52/255, 112/255, 235/255)  # สีน้ำเงินเข้ม
    elif t < 34.00:
        return (52/255, 83/255, 235/255)  # สีน้ำเงินเข้มมาก
    elif t < 34.55:
        return (29/255, 63/255, 231/255)  # สีน้ำเงินเข้มที่สุด
    elif t < 34.99:
        return (0/255, 0/255, 255/255)  # สีน้ำเงิน
    elif t < 35.00:
        return (217/255, 39/255, 39/255)  # สีแดง
    else:
        return (2/255, 2/255, 196/255)  # สีน้ำเงินเข้มมาก

# ฟังก์ชันในการพล็อตภาพความร้อน
def plot_thermal_image(row_data, timestamp):
    # แปลงข้อมูลแถวเป็นตัวเลข โดยข้ามเวลา
    row_data_numeric = pd.to_numeric(row_data[1:], errors='coerce')
    if row_data_numeric.isnull().any():
        print("ข้อผิดพลาด: ข้อมูลที่ไม่ใช่ตัวเลขถูกพบ.")
        return

    # แปลงข้อมูลเป็นอาร์เรย์ขนาด 24x32 (ข้ามเวลา)
    thermal_data = np.array(row_data_numeric).reshape(24, 32)

    # สร้างฟังก์ชันในการแมพสีตามค่าอุณหภูมิ
    cmap = mcolors.LinearSegmentedColormap.from_list('custom_cmap', [temperature_to_color(t) for t in np.linspace(27.99, 35.00, 256)], N=256)

    # สร้างรูปภาพและแกน
    fig, ax = plt.subplots()

    # พล็อตภาพความร้อน
    im = ax.imshow(thermal_data, cmap=cmap, interpolation='nearest')

    # เพิ่มแถบสี
    cbar = plt.colorbar(im)
    cbar.set_label('Temperature (°C)')

    # เปลี่ยนชื่อเรื่องด้วยเวลาที่บันทึก
    safe_timestamp = timestamp.replace(':', '-')  # แทนที่ ':' ด้วย '-' เพื่อให้เป็นชื่อไฟล์ที่ถูกต้อง
    plt.title(f'Thermal Image at {timestamp}')

    # บันทึกภาพ
    plt.savefig(f"thermal_image_{safe_timestamp}.png")
    plt.close()

# พล็อตข้อมูลแต่ละแถว
for index, row in data.iterrows():
    timestamp = row[0]
    plot_thermal_image(row, timestamp)
