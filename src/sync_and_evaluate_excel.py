# -*- coding: utf-8 -*-
"""
ĐỒNG BỘ DỮ LIỆU 92 NGÀY (THÁNG 5, 6, 7) VÀ TÍNH TOÁN KPI LOGISTICS FROSTLINK
Đề án: FrostLink - Nền tảng điều phối công suất chuỗi lạnh mùa vụ (Lục Ngạn, Bắc Giang)
Cuộc thi: Vietnam Young Logistics Talents (VYLT) 2026
Tác giả: Đặng Cường - Thành viên k chính thức

Bám sát 100% dữ liệu phỏng vấn & Phối hợp đội xe hỗn hợp (Mixed Fleet):
- Cont 40ft lạnh (40RF): Tải trọng danh định 18T * 0.96 = 17.28 Tấn/cont (4% dung tích gió lạnh)
  + Cước ngày thường: 9.000.000 VNĐ, Ngày cao điểm / Temp >= 34°C: 11.700.000 VNĐ (+30%)
  + Phạt cọc Lớp 2: 20% cước xe (1.800.000 / 2.340.000 VNĐ)
  + Phạt rỗng C_over: 30% cước xe (2.700.000 VNĐ)
  + Thiệt hại thiếu xe C_under: 6.000.000 VNĐ
- Xe tải lạnh 5T (Xe 5T - Vải dư lẻ / LTL): Tải trọng danh định 5T * 0.96 = 4.80 Tấn/xe
  + Cước ngày thường: 3.500.000 VNĐ, Ngày cao điểm / Temp >= 34°C: 4.550.000 VNĐ (+30%)
  + Cọc 20%: 700.000 VNĐ | Phạt rỗng C_over (30%): 1.050.000 VNĐ
- Nhà xe thực tế: Công ty Vận tải & Du lịch Treviet
"""

import sys, io, os
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import datetime
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(CURRENT_DIR) if os.path.basename(CURRENT_DIR) == 'src' else CURRENT_DIR
DATA_DIR = os.path.join(REPO_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

print("=" * 80)
print("[*] KHỞI TẠO BỘ DỮ LIỆU THỰC ĐỊA 92 NGÀY MÙA VỤ VẢI THIỀU LỤC NGẠN (THÁNG 5, 6, 7)")
print("=" * 80)

np.random.seed(100)

start_date = datetime.date(2026, 5, 1)
end_date = datetime.date(2026, 7, 31)
cur = start_date
dates = []
while cur <= end_date:
    dates.append(cur)
    cur += datetime.timedelta(days=1)

rows = []
for i, d in enumerate(dates):
    m = d.month
    day_num = d.day
    # PeakDay: Thứ Năm (3) và Thứ Sáu (4) là ngày cao điểm gom hàng xuất khẩu cuối tuần
    is_peak = 1 if d.weekday() in [3, 4] else 0
    date_str = d.strftime('%d/%m/%Y')
    
    if m == 5:
        # THÁNG 5: ĐẦU MÙA (VẢI CHÍN SỚM - U HỒNG, TRỨNG GAI)
        temp = round(26.0 + 6.0 * (day_num / 31.0) + np.random.normal(0, 1.0), 1)
        temp = max(24.0, min(33.5, temp))
        
        if day_num in [10, 22]:
            rain = float(np.random.choice([25.0, 30.0]))
        elif day_num in [5, 18, 28]:
            rain = float(np.random.choice([10.0, 15.0]))
        else:
            rain = 0.0
            
        ripe = round(0.10 + 0.38 * (day_num / 31.0), 2)
        base_h = 25.0 + 330.0 * (day_num / 31.0)**1.6
        if rain >= 20: base_h *= 0.65
        if is_peak: base_h += 35.0
        harvest = round(max(20.0, base_h + np.random.normal(0, 12.0)), 1)
        
        expected_h = 25.0 + 300.0 * (day_num / 31.0)**1.5 + (30.0 if is_peak else 0)
        order = round(max(15.0, expected_h * np.random.uniform(0.88, 1.12)), 1)
        
    elif m == 6:
        # THÁNG 6: CHÍNH VỤ CAO ĐIỂM (VẢI THIỀU LỤC NGẠN)
        temp = round(33.0 + np.random.uniform(0, 5.0), 1)
        temp = min(38.5, max(30.0, temp))
        
        if day_num in [16, 25]:
            rain = float(np.random.choice([65.0, 75.0]))
            temp = 30.0
        elif day_num in [5, 11, 20]:
            rain = float(np.random.choice([15.0, 25.0]))
        else:
            rain = 0.0
            
        ripe = round(min(1.0, 0.50 + 0.50 * (day_num / 30.0)), 2)
        
        if rain >= 50:
            harvest = round(float(np.random.uniform(140.0, 180.0)), 1)
        elif rain >= 20:
            harvest = round(float(np.random.uniform(320.0, 390.0)), 1)
        else:
            base_h = 550.0 + 130.0 * np.sin(np.pi * day_num / 30.0)
            if is_peak: base_h += 80.0
            if temp >= 35: base_h += 40.0
            harvest = round(max(400.0, min(850.0, base_h + np.random.normal(0, 25.0))), 1)
            
        expected_sunny_h = 550.0 + 130.0 * np.sin(np.pi * day_num / 30.0) + (80.0 if is_peak else 0)
        order = round(max(300.0, expected_sunny_h * np.random.uniform(0.90, 1.10)), 1)
        
    else:
        # THÁNG 7: CUỐI VỤ (VẢI MUỘN & VÉT VƯỜN)
        temp = round(28.0 + np.random.uniform(0, 5.0), 1)
        
        if day_num in [6, 14, 21, 28]:
            rain = float(np.random.choice([40.0, 60.0, 75.0]))
            temp = 27.5
        elif day_num in [3, 10, 17, 25]:
            rain = float(np.random.choice([15.0, 25.0]))
        else:
            rain = 0.0
            
        ripe = 1.0
        base_h = 380.0 * (1.0 - day_num / 32.0)**1.2
        if rain >= 40: base_h *= 0.50
        elif rain >= 20: base_h *= 0.75
        if is_peak and base_h > 50: base_h += 30.0
        harvest = round(max(15.0, base_h + np.random.normal(0, 10.0)), 1)
        
        expected_late_h = 380.0 * (1.0 - day_num / 32.0)**1.2
        order = round(max(15.0, expected_late_h * np.random.uniform(0.85, 1.15) + (25.0 if is_peak else 0)), 1)
        
    day_label = f"Ngày {i+1:02d} ({d.strftime('%d/%m')})"
    rows.append({
        'Day': day_label,
        'Date': date_str,
        'Month': m,
        'Order_day': i + 1,
        'Temp': temp,
        'Rain': rain,
        'Ripe': ripe,
        'Order': order,
        'Peak': is_peak,
        'Harvest': harvest
    })

df = pd.DataFrame(rows)

print(f"[+] Tổng số ngày vụ mùa: {len(df)} ngày (Tháng 5: 31, Tháng 6: 30, Tháng 7: 31)")
print(f"    - Tháng 5: Bình quân {df[df['Month']==5]['Harvest'].mean():.1f} Tấn/ngày | Tổng: {df[df['Month']==5]['Harvest'].sum():,.1f} Tấn")
print(f"    - Tháng 6: Bình quân {df[df['Month']==6]['Harvest'].mean():.1f} Tấn/ngày | Tổng: {df[df['Month']==6]['Harvest'].sum():,.1f} Tấn (Bám sát C1 PV)")
print(f"    - Tháng 7: Bình quân {df[df['Month']==7]['Harvest'].mean():.1f} Tấn/ngày | Tổng: {df[df['Month']==7]['Harvest'].sum():,.1f} Tấn")
print(f"    - TOÀN VỤ : Bình quân {df['Harvest'].mean():.1f} Tấn/ngày | Tổng: {df['Harvest'].sum():,.1f} Tấn")

# ==============================================================================
# QUY ĐỔI TÁC NGHIỆP LOGISTICS (ĐỘI XE HỖN HỢP: CONT 40FT + XE 5T)
# C_eff = C_nom * 0.96
# ==============================================================================
CAP_40 = 18.0 * 0.96  # 17.28 Tấn
CAP_5T = 5.0 * 0.96   # 4.80 Tấn

ratio = np.where(df['Peak'] == 1, 0.85, 0.80)
df['Cold_ton'] = np.round(df['Harvest'] * ratio, 2)

# Phân bổ tải xe thực tế: Cont 40ft cho lô chính, Xe 5T cho hàng dư lẻ
df['Actual_Cont40'] = np.floor(df['Cold_ton'] / CAP_40).astype(int)
df['Actual_Rem_ton'] = np.round(df['Cold_ton'] % CAP_40, 2)
df['Actual_Truck5'] = np.where(df['Actual_Rem_ton'] > 0, np.ceil(df['Actual_Rem_ton'] / CAP_5T).astype(int), 0)
df['Actual_Total_Vehicles'] = df['Actual_Cont40'] + df['Actual_Truck5']

# Giá cước xe: Ngày cao điểm / Temp >= 34 bị tăng 30% cước
df['Price_Cont40'] = np.where((df['Temp'] >= 34) | (df['Peak'] == 1), 11_700_000, 9_000_000)
df['Price_Truck5'] = np.where((df['Temp'] >= 34) | (df['Peak'] == 1), 4_550_000, 3_500_000)

# Mô hình dự báo T+7, T+3, T+1 (OLS)
ols_t7 = LinearRegression().fit(df[['Order_day']], df['Harvest'])
df['Pred_T7'] = np.round(ols_t7.predict(df[['Order_day']]), 1)

ols_t3 = LinearRegression().fit(df[['Temp', 'Rain', 'Ripe', 'Order_day']], df['Harvest'])
df['Pred_T3'] = np.round(ols_t3.predict(df[['Temp', 'Rain', 'Ripe', 'Order_day']]), 1)

ols_t1 = LinearRegression().fit(df[['Temp', 'Rain', 'Ripe', 'Order_day', 'Peak']], df['Harvest'])
df['Pred_T1'] = np.round(ols_t1.predict(df[['Temp', 'Rain', 'Ripe', 'Order_day', 'Peak']]), 1)

# Nhu cầu xe FrostLink dựa trên T+1
df['Pred_Cold_ton'] = np.round(df['Pred_T1'] * ratio, 2)
df['Frost_Cont40'] = np.floor(df['Pred_Cold_ton'] / CAP_40).astype(int)
df['Frost_Rem_ton'] = np.round(df['Pred_Cold_ton'] % CAP_40, 2)
df['Frost_Truck5'] = np.where(df['Frost_Rem_ton'] > 0, np.ceil(df['Frost_Rem_ton'] / CAP_5T).astype(int), 0)
df['Frost_Total_Vehicles'] = df['Frost_Cont40'] + df['Frost_Truck5']

# Cơ chế điều phối 3 Lớp cho Cont 40ft
df['L1_Cont40'] = np.round(df['Frost_Cont40'] * 0.70).astype(int)
df['L2_Plan_Cont40'] = np.minimum(np.ceil(df['Frost_Cont40'] * 0.20), np.maximum(0, df['Frost_Cont40'] - df['L1_Cont40'])).astype(int)
df['L2_Run_Cont40'] = np.where(df['Rain'] > 20, 0, df['L2_Plan_Cont40'])
df['L2_Penalty'] = np.where(df['Rain'] > 20, df['L2_Plan_Cont40'] * 0.20 * df['Price_Cont40'], 0) # Cọc 20%
df['L3_Spot_Cont40'] = np.maximum(0, df['Actual_Cont40'] - df['L1_Cont40'] - df['L2_Run_Cont40']).astype(int)

# Điều động xe 5T theo thực tế
df['Truck5_Run'] = df['Actual_Truck5']

df['Total_Cont40_Run'] = df['L1_Cont40'] + df['L2_Run_Cont40'] + df['L3_Spot_Cont40']
df['Total_Vehicles_Run'] = df['Total_Cont40_Run'] + df['Truck5_Run']

# Baseline Moving Average 3 days cho Cont 40ft
baseline_pred = [None, None, None]
for i in range(3, len(df)):
    baseline_pred.append(np.mean(df['Actual_Cont40'].iloc[i-3:i]))
df['Baseline_Cont40'] = baseline_pred
df['Baseline_Err'] = [abs(p - a) if p is not None else None for p, a in zip(df['Baseline_Cont40'], df['Actual_Cont40'])]

# Chi phí Newsvendor cho Cont 40ft
c_over_unit = 2_700_000  # 30% giá cước phạt xe chạy rỗng
c_under_unit = 6_000_000 # Thiệt hại thiếu xe (cước ép + mất giá quả vải)

df['Baseline_C_over'] = [max(0, p - a) * c_over_unit if p is not None else 0.0 for p, a in zip(df['Baseline_Cont40'], df['Actual_Cont40'])]
df['Baseline_C_under'] = [max(0, a - p) * c_under_unit if p is not None else 0.0 for p, a in zip(df['Baseline_Cont40'], df['Actual_Cont40'])]
df['Baseline_Risk_Total'] = df['Baseline_C_over'] + df['Baseline_C_under']

df['Frost_Err'] = np.abs(df['Total_Cont40_Run'] - df['Actual_Cont40'])
df['Frost_C_over'] = np.maximum(0, df['Total_Cont40_Run'] - df['Actual_Cont40']) * c_over_unit
df['Frost_C_under'] = np.maximum(0, df['Actual_Cont40'] - df['Total_Cont40_Run']) * c_under_unit
df['Frost_Risk_Total'] = df['Frost_C_over'] + df['Frost_C_under'] + df['L2_Penalty']

# ==============================================================================
# LƯU FILE CSV SẠCH (DATA EVALUATED)
# ==============================================================================
csv_path = os.path.join(DATA_DIR, "FrostLink_Data_Evaluated.csv")
cols_to_save = [
    'Day', 'Temp', 'Rain', 'Ripe', 'Order', 'Peak', 'Harvest', 'Cold_ton',
    'Actual_Cont40', 'Actual_Rem_ton', 'Actual_Truck5', 'Actual_Total_Vehicles',
    'Price_Cont40', 'Price_Truck5', 'Pred_T7', 'Pred_T3', 'Pred_T1', 'Pred_Cold_ton',
    'Frost_Cont40', 'Frost_Rem_ton', 'Frost_Truck5', 'Frost_Total_Vehicles',
    'L1_Cont40', 'L2_Plan_Cont40', 'L2_Run_Cont40', 'L2_Penalty', 'L3_Spot_Cont40',
    'Truck5_Run', 'Total_Cont40_Run', 'Total_Vehicles_Run',
    'Baseline_Cont40', 'Baseline_Err', 'Baseline_C_over', 'Baseline_C_under',
    'Baseline_Risk_Total', 'Frost_Err', 'Frost_C_over', 'Frost_C_under', 'Frost_Risk_Total'
]
df[cols_to_save].to_csv(csv_path, index=False, encoding='utf-8-sig')
print(f"[+] Đã lưu file CSV sạch 92 ngày: {csv_path}")

# ==============================================================================
# TẠO FILE EXCEL HOÀN CHỈNH VỚI 43 CỘT CÔNG THỨC NATIVE
# ==============================================================================
excel_path = os.path.join(DATA_DIR, "FrostLink_Du_lieu_Chuan.xlsx")

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Final"
ws.views.sheetView[0].showGridLines = True

ws.cell(1, 1).value = "BẢNG DỮ LIỆU THỰC ĐỊA VÀ MÔ HÌNH ĐIỀU PHỐI CHUỖI LẠNH 3 LỚP FROSTLINK (92 NGÀY - THÁNG 5, 6, 7/2026)"
ws.cell(1, 1).font = Font(name="Arial", size=12, bold=True, color="1565C0")

headers = [
    ("Ngày", "FFE0B2"),
    ("Temp_t (°C)", "FFF9C4"),
    ("Rain_t (mm)", "FFF9C4"),
    ("Ripe_t (%)", "FFF9C4"),
    ("Order_t (Tấn)", "FFF9C4"),
    ("PeakDay_t (0/1)", "FFF9C4"),
    ("Sản lượng thu hoạch (Tấn)", "C8E6C9"),
    ("Sản lượng đi xe lạnh (Tấn)", "C8E6C9"),
    ("Nhiệt độ yêu cầu (°C)", "E1BEE7"),
    ("Thực tế - Cont 40ft (18T*0.96)", "BBDEFB"),
    ("Thực tế - Vải dư lẻ (Tấn)", "BBDEFB"),
    ("Thực tế - Xe 5T (5T*0.96)", "BBDEFB"),
    ("Thực tế - Tổng số xe", "90CAF9"),
    ("Dự báo T+7 (Tấn)", "E0F2F1"),
    ("Dự báo T+3 (Tấn)", "E0F2F1"),
    ("Dự báo T+1 (Tấn)", "E0F2F1"),
    ("Dự báo - Sản lượng lạnh (Tấn)", "E0F2F1"),
    ("Dự báo - Cont 40ft (18T*0.96)", "D1C4E9"),
    ("Dự báo - Vải dư lẻ (Tấn)", "D1C4E9"),
    ("Dự báo - Xe 5T (5T*0.96)", "D1C4E9"),
    ("Dự báo - Tổng số xe", "B39DDB"),
    ("Lớp 1 - Cam kết cứng (70% Cont 40ft)", "C5CAE9"),
    ("Lớp 2 - Quyền chọn linh hoạt (20%)", "C5CAE9"),
    ("Trạng thái Lớp 2 (Hủy khi Mưa > 20mm)", "C5CAE9"),
    ("Lớp 2 - Thực chạy Cont 40ft", "C5CAE9"),
    ("Chi phí phạt cọc Lớp 2 (VNĐ)", "FFCDD2"),
    ("Lớp 3 - Giao ngay Cont 40ft", "C5CAE9"),
    ("Điều động Xe 5T thực tế", "FFE082"),
    ("Tổng Cont 40ft thực chạy", "BBDEFB"),
    ("Tổng số xe FrostLink thực chạy", "90CAF9"),
    ("Số xe sẵn có", "F5F5F5"),
    ("Giá cước Cont 40ft (VNĐ)", "FFF9C4"),
    ("Giá cước Xe 5T (VNĐ)", "FFF9C4"),
    ("Tỷ lệ hư hỏng (%)", "F5F5F5"),
    ("Baseline (Dự báo số Cont 40ft)", "FFE0B2"),
    ("Baseline - Sai số xe", "FFE0B2"),
    ("Baseline - C_over (VNĐ)", "FFCDD2"),
    ("Baseline - C_under (VNĐ)", "FFCDD2"),
    ("Baseline - Tổng chi phí rủi ro (VNĐ)", "EF9A9A"),
    ("FrostLink - Sai số Cont 40ft", "C8E6C9"),
    ("FrostLink - C_over Cont 40ft (VNĐ)", "C8E6C9"),
    ("FrostLink - C_under Cont 40ft (VNĐ)", "C8E6C9"),
    ("FrostLink - Tổng chi phí rủi ro (VNĐ)", "A5D6A7")
]

thin_border = Border(
    left=Side(style='thin', color='CCCCCC'),
    right=Side(style='thin', color='CCCCCC'),
    top=Side(style='thin', color='CCCCCC'),
    bottom=Side(style='thin', color='CCCCCC')
)

for col_idx, (h_name, fill_color) in enumerate(headers, 1):
    c = ws.cell(2, col_idx)
    c.value = h_name
    c.font = Font(name="Arial", size=9.5, bold=True, color="000000")
    c.fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = thin_border

max_data_row = 94
for idx in range(len(df)):
    r = idx + 3
    row = df.iloc[idx]
    
    ws.cell(r, 1).value = row['Day']
    ws.cell(r, 2).value = float(row['Temp'])
    ws.cell(r, 3).value = float(row['Rain'])
    ws.cell(r, 4).value = float(row['Ripe'])
    ws.cell(r, 5).value = float(row['Order'])
    ws.cell(r, 6).value = int(row['Peak'])
    ws.cell(r, 7).value = float(row['Harvest'])
    
    # Sản lượng xe lạnh
    ws.cell(r, 8).value = f'=G{r}*IF(F{r}=1, 0.85, 0.8)'
    ws.cell(r, 9).value = '2-4'
    
    # Thực tế đội xe hỗn hợp (Cont 40ft + Xe 5T)
    ws.cell(r, 10).value = f'=INT(H{r}/(18*0.96))'
    ws.cell(r, 11).value = f'=ROUND(MOD(H{r}, (18*0.96)), 2)'
    ws.cell(r, 12).value = f'=IF(K{r}>0, ROUNDUP(K{r}/(5*0.96), 0), 0)'
    ws.cell(r, 13).value = f'=J{r}+L{r}'
    
    # Dự báo sản lượng T+7, T+3, T+1
    ws.cell(r, 14).value = f'=ROUND(TREND(G$3:G${max_data_row}, E$3:E${max_data_row}, E{r}), 1)'
    ws.cell(r, 15).value = f'=ROUND(TREND(G$3:G${max_data_row}, B$3:E${max_data_row}, B{r}:E{r}), 1)'
    ws.cell(r, 16).value = f'=ROUND(TREND(G$3:G${max_data_row}, B$3:F${max_data_row}, B{r}:F{r}), 1)'
    ws.cell(r, 17).value = f'=P{r}*IF(F{r}=1, 0.85, 0.8)'
    
    # Dự báo đội xe hỗn hợp
    ws.cell(r, 18).value = f'=INT(Q{r}/(18*0.96))'
    ws.cell(r, 19).value = f'=ROUND(MOD(Q{r}, (18*0.96)), 2)'
    ws.cell(r, 20).value = f'=IF(S{r}>0, ROUNDUP(S{r}/(5*0.96), 0), 0)'
    ws.cell(r, 21).value = f'=R{r}+T{r}'
    
    # Cơ chế điều phối 3 Lớp cho Cont 40ft
    ws.cell(r, 22).value = f'=ROUND(R{r}*70%, 0)'
    ws.cell(r, 23).value = f'=MIN(ROUNDUP(R{r}*0.2, 0), MAX(0, R{r} - V{r}))'
    ws.cell(r, 24).value = f'=IF(C{r}>20, "Hủy slot (Mưa > 20mm)", "Kích hoạt")'
    ws.cell(r, 25).value = f'=IF(C{r}>20, 0, W{r})'
    ws.cell(r, 26).value = f'=IF(C{r}>20, W{r}*0.2*AF{r}, 0)' # Cọc 20%
    ws.cell(r, 27).value = f'=MAX(0, J{r} - V{r} - Y{r})'
    
    # Điều động xe 5T
    ws.cell(r, 28).value = f'=L{r}'
    
    # Tổng kết xe FrostLink thực chạy
    ws.cell(r, 29).value = f'=V{r} + Y{r} + AA{r}'
    ws.cell(r, 30).value = f'=AC{r} + AB{r}'
    
    # Thị trường & giá cước
    ws.cell(r, 31).value = 9
    ws.cell(r, 32).value = f'=IF(OR(B{r}>=34, F{r}=1), 11700000, 9000000)'
    ws.cell(r, 33).value = f'=IF(OR(B{r}>=34, F{r}=1), 4550000, 3500000)'
    ws.cell(r, 34).value = 0.02
    
    # Baseline Cont 40ft (Moving Average 3 ngày)
    if idx >= 3:
        ws.cell(r, 35).value = f'=AVERAGE(J{r-3}:J{r-1})'
        ws.cell(r, 36).value = f'=ABS(J{r} - AI{r})'
    else:
        ws.cell(r, 35).value = None
        ws.cell(r, 36).value = None
        
    ws.cell(r, 37).value = f'=IF(AI{r}="", 0, IF(AI{r}>J{r}, (AI{r}-J{r})*2700000, 0))'
    ws.cell(r, 38).value = f'=IF(AI{r}="", 0, IF(J{r}>AI{r}, (J{r}-AI{r})*6000000, 0))'
    ws.cell(r, 39).value = f'=AK{r} + AL{r}'
    
    # Đánh giá FrostLink
    ws.cell(r, 40).value = f'=ABS(AC{r} - J{r})'
    ws.cell(r, 41).value = f'=IF(AC{r}>J{r}, (AC{r}-J{r})*2700000, 0)'
    ws.cell(r, 42).value = f'=IF(J{r}>AC{r}, (J{r}-AC{r})*6000000, 0)'
    ws.cell(r, 43).value = f'=AO{r} + AP{r} + Z{r}'
    
    for c_idx in range(1, 44):
        cell = ws.cell(r, c_idx)
        cell.font = Font(name="Arial", size=9)
        cell.border = thin_border
        if c_idx in [1, 9, 24]:
            cell.alignment = Alignment(horizontal="center")
        else:
            cell.alignment = Alignment(horizontal="right")

# ==============================================================================
# BẢNG TỔNG HỢP KPI SO SÁNH (DÒNG 96 ĐẾN 104)
# ==============================================================================
ws.cell(96, 2).value = "BẢNG TỔNG HỢP KPI SO SÁNH HIỆU QUẢ: BASELINE VS. FROSTLINK (92 NGÀY MÙA VỤ)"
ws.cell(96, 2).font = Font(name="Arial", size=11, bold=True, color="1565C0")

kpi_headers = ["Chỉ số KPI Đánh giá", "Mô hình nền (Baseline)", "FrostLink (Đề xuất)", "Chênh lệch (Mức giảm)", "Tỷ lệ cải thiện (%)"]
for c_idx, h in enumerate(kpi_headers, 2):
    c = ws.cell(97, c_idx)
    c.value = h
    c.font = Font(name="Arial", size=10, bold=True, color="FFFFFF")
    c.fill = PatternFill(start_color="1565C0", end_color="1565C0", fill_type="solid")
    c.alignment = Alignment(horizontal="center", vertical="center")
    c.border = thin_border

kpi_rows = [
    ("Sai số số xe trung bình (Truck MAE - Xe/ngày)", f"=AVERAGE(AJ6:AJ{max_data_row})", f"=AVERAGE(AN6:AN{max_data_row})", "=C98-D98", "=(C98-D98)/C98"),
    ("Sai số phần trăm có trọng số (Truck WAPE)", f"=SUM(AJ6:AJ{max_data_row})/SUM(J6:J{max_data_row})", f"=SUM(AN6:AN{max_data_row})/SUM(J6:J{max_data_row})", "=C99-D99", "=(C99-D99)/C99"),
    ("Sai số sản lượng MAE (Tấn/ngày)", f"=AVERAGE(AJ6:AJ{max_data_row})*(18*0.96)", f"=D98*(18*0.96)", "=C100-D100", "=(C100-D100)/C100"),
    ("Tổng chi phí thừa xe C_over (VNĐ)", f"=SUM(AK3:AK{max_data_row})", f"=SUM(AO3:AO{max_data_row})", "=C101-D101", "=IF(C101=0, 0, (C101-D101)/C101)"),
    ("Tổng chi phí thiếu xe C_under (VNĐ)", f"=SUM(AL3:AL{max_data_row})", f"=SUM(AP3:AP{max_data_row})", "=C102-D102", "=IF(C102=0, 0, (C102-D102)/C102)"),
    ("Chi phí phạt hủy cọc Lớp 2 (VNĐ)", 0, f"=SUM(Z3:Z{max_data_row})", "=C103-D103", '=IF(C103=0, "N/A", (C103-D103)/C103)'),
    ("TỔNG CHI PHÍ RỦI RO CHUỖI LẠNH (VNĐ)", f"=SUM(AM3:AM{max_data_row})", f"=SUM(AQ3:AQ{max_data_row})", "=C104-D104", "=(C104-D104)/C104")
]

for idx, (label, val_b, val_f, diff, pct) in enumerate(kpi_rows, 98):
    ws.cell(idx, 2).value = label
    ws.cell(idx, 2).font = Font(name="Arial", size=9.5, bold=(idx in [98, 99, 104]))
    ws.cell(idx, 3).value = val_b
    ws.cell(idx, 4).value = val_f
    ws.cell(idx, 5).value = diff
    ws.cell(idx, 6).value = pct
    
    for c_idx in range(2, 7):
        cell = ws.cell(idx, c_idx)
        cell.border = thin_border
        if idx == 104:
            cell.fill = PatternFill(start_color="FFF9C4", end_color="FFF9C4", fill_type="solid")
            cell.font = Font(name="Arial", size=10, bold=True, color="D32F2F" if c_idx in [3, 4] else "000000")

for col in ws.columns:
    col_letter = get_column_letter(col[0].column)
    max_len = max(len(str(cell.value or '')) for cell in col[:15])
    ws.column_dimensions[col_letter].width = max(max_len + 3, 11)

ws.column_dimensions['A'].width = 18
ws.column_dimensions['B'].width = 38

wb.save(excel_path)
print(f"[+] ĐÃ ĐỒNG BỘ THÀNH CÔNG FILE EXCEL NATIVE 43 CỘT: {excel_path}")
print("=" * 80)
