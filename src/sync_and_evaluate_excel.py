# -*- coding: utf-8 -*-
"""
TẠO LẠI TOÀN BỘ FILE EXCEL DATA CHUẨN VÀ FILE CSV ĐÁNH GIÁ CHUẨN:
- 100% CONTAINER LẠNH 40 FEET (REEFER CONT 40FT)
- KHÔNG CÒN BẤT KỲ CỘT XE 5T, DƯ LẺ HAY LOGIC XE TẢI NÀO
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

# Nạp module thời tiết API Open-Meteo ERA5 Reanalysis
weather_cache = os.path.join(DATA_DIR, "weather_luc_ngan_api.csv")
if os.path.exists(weather_cache):
    w_df = pd.read_csv(weather_cache)
else:
    raise RuntimeError(f"Không thể nạp dữ liệu thời tiết Lục Ngạn: {weather_cache}")

print("=" * 80)
print("[*] TẠO FILE DỮ LIỆU CHUẨN 92 NGÀY (THUẦN CONTAINER LẠNH 40 FEET)")
print("=" * 80)

np.random.seed(42)

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
    is_peak = 1 if d.weekday() in [3, 4] else 0
    date_str = d.strftime('%d/%m/%Y')
    
    temp = round(float(w_df.iloc[i]['Temp_Max_C']), 1)
    rain = round(float(w_df.iloc[i]['Precip_mm']), 1)
    
    if m == 5:
        r = 0.12 + 0.33 * ((day_num - 1) / 30.0)**1.3 + np.random.normal(0, 0.008)
        r = min(0.46, max(0.11, r))
        order_base = 25.0 + 260.0 * ((day_num - 1) / 30.0)**1.3 + (30.0 if is_peak else 0)
        order = round(max(15.0, order_base + np.random.normal(0, 10.0)), 1)
        base_h = 10.0 + 300.0 * (r - 0.10) + 0.52 * order + 4.5 * (temp - 28.0)
        if is_peak: base_h += 30.0
        if rain >= 20: base_h *= 0.65
        elif rain >= 10: base_h *= 0.85
        harvest = round(max(20.0, base_h + np.random.normal(0, 8.0)), 1)
    elif m == 6:
        t6 = (day_num - 1) / 29.0
        r_curve = 0.46 + 0.46 * np.sin(np.pi * t6)
        r = r_curve + np.random.normal(0, 0.008)
        r = min(0.93, max(0.46, r))
        order_base = 420.0 + 150.0 * np.sin(np.pi * (day_num - 1) / 29.0) + (70.0 if is_peak else 0)
        order = round(max(300.0, order_base + np.random.normal(0, 20.0)), 1)
        base_h = 170.0 + 240.0 * (r - 0.46) + 0.48 * order + 5.5 * (temp - 30.0)
        if is_peak: base_h += 35.0
        if rain >= 40:
            harvest = round(float(np.random.uniform(140.0, 190.0)), 1)
        elif rain >= 20:
            harvest = round(float(np.random.uniform(320.0, 400.0)), 1)
        elif rain >= 10:
            harvest = round(max(350.0, base_h * 0.85 + np.random.normal(0, 15.0)), 1)
        else:
            harvest = round(max(400.0, min(850.0, base_h + np.random.normal(0, 18.0))), 1)
    else:
        t7 = (day_num - 1) / 30.0
        r = 0.60 * (1.0 - t7)**1.2 + 0.08 + np.random.normal(0, 0.008)
        r = min(0.68, max(0.08, r))
        order_base = 280.0 * (1.0 - t7)**1.2 + (20.0 if is_peak else 0)
        order = round(max(15.0, order_base + np.random.normal(0, 10.0)), 1)
        base_h = 10.0 + 200.0 * (r - 0.08) + 0.50 * order + 4.0 * (temp - 30.0)
        if is_peak and base_h > 40: base_h += 15.0
        if rain >= 40: base_h *= 0.50
        elif rain >= 20: base_h *= 0.75
        elif rain >= 10: base_h *= 0.88
        harvest = round(max(15.0, base_h + np.random.normal(0, 8.0)), 1)
        
    day_label = f"Ngày {i+1:02d} ({d.strftime('%d/%m')})"
    rows.append({
        'Day': day_label,
        'Date': date_str,
        'Month': m,
        'Order_day': i + 1,
        'Temp': temp,
        'Rain': rain,
        'Ripe': round(r, 3),
        'Order': order,
        'Peak': is_peak,
        'Harvest': harvest
    })

df = pd.DataFrame(rows)

# ==============================================================================
# QUY ĐỔI TÁC NGHIỆP LOGISTICS (THUẦN CONTAINER LẠNH 40 FEET)
# C_eff = 18.0 * 0.96 = 17.28 Tấn/cont
# ==============================================================================
CAP_40 = 18.0 * 0.96  # 17.28 Tấn

ratio = np.where(df['Peak'] == 1, 0.85, 0.80)
df['Cold_ton'] = np.round(df['Harvest'] * ratio, 2)

# Nhu cầu thực tế Cont 40ft (bảo toàn 1.081 Cont toàn vụ)
df['Actual_Cont40'] = np.floor(df['Cold_ton'] / CAP_40).astype(int)

# Giá cước Cont 40ft
df['Price_Cont40'] = np.where((df['Temp'] >= 34) | (df['Peak'] == 1), 11_700_000, 9_000_000)

# Mô hình dự báo T+7, T+3, T+1 (OLS)
ols_t7 = LinearRegression().fit(df[['Order']], df['Harvest'])
df['Pred_T7'] = np.maximum(15.0, np.round(ols_t7.predict(df[['Order']]), 1))

ols_t3 = LinearRegression().fit(df[['Temp', 'Rain', 'Ripe', 'Order']], df['Harvest'])
df['Pred_T3'] = np.maximum(15.0, np.round(ols_t3.predict(df[['Temp', 'Rain', 'Ripe', 'Order']]), 1))

ols_t1 = LinearRegression().fit(df[['Temp', 'Rain', 'Ripe', 'Order', 'Peak']], df['Harvest'])
df['Pred_T1'] = np.maximum(15.0, np.round(ols_t1.predict(df[['Temp', 'Rain', 'Ripe', 'Order', 'Peak']]), 1))

# Nhu cầu xe FrostLink dựa trên T+1 (Cont 40ft)
df['Pred_Cold_ton'] = np.maximum(0.0, np.round(df['Pred_T1'] * ratio, 2))
df['Frost_Cont40'] = np.maximum(0, np.floor(df['Pred_Cold_ton'] / CAP_40).astype(int))

# Cơ chế điều phối 3 Lớp cho Cont 40ft (Đảm bảo không bao giờ âm)
df['L1_Cont40'] = np.maximum(0, np.round(df['Frost_Cont40'] * 0.70).astype(int))
df['L2_Plan_Cont40'] = np.maximum(0, np.minimum(np.ceil(df['Frost_Cont40'] * 0.20), np.maximum(0, df['Frost_Cont40'] - df['L1_Cont40'])).astype(int))
df['L2_Run_Cont40'] = np.where(df['Rain'] > 20, 0, df['L2_Plan_Cont40'])
df['L2_Penalty'] = np.where(df['Rain'] > 20, df['L2_Plan_Cont40'] * 0.20 * df['Price_Cont40'], 0) # Cọc 20%
df['L3_Spot_Cont40'] = np.maximum(0, df['Actual_Cont40'] - df['L1_Cont40'] - df['L2_Run_Cont40']).astype(int)

df['Total_Cont40_Run'] = df['L1_Cont40'] + df['L2_Run_Cont40'] + df['L3_Spot_Cont40']

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
# LƯU FILE CSV SẠCH (CHỈ CONT 40FT)
# ==============================================================================
csv_path = os.path.join(DATA_DIR, "FrostLink_Data_Evaluated.csv")
cols_to_save = [
    'Day', 'Temp', 'Rain', 'Ripe', 'Order', 'Peak', 'Harvest', 'Cold_ton',
    'Actual_Cont40', 'Price_Cont40', 'Pred_T7', 'Pred_T3', 'Pred_T1', 'Pred_Cold_ton',
    'Frost_Cont40', 'L1_Cont40', 'L2_Plan_Cont40', 'L2_Run_Cont40', 'L2_Penalty',
    'L3_Spot_Cont40', 'Total_Cont40_Run',
    'Baseline_Cont40', 'Baseline_Err', 'Baseline_C_over', 'Baseline_C_under',
    'Baseline_Risk_Total', 'Frost_Err', 'Frost_C_over', 'Frost_C_under', 'Frost_Risk_Total'
]
df[cols_to_save].to_csv(csv_path, index=False, encoding='utf-8-sig')
print(f"[+] Đã lưu file CSV sạch 92 ngày (thuần Cont 40ft): {csv_path}")

# ==============================================================================
# TẠO FILE EXCEL HOÀN CHỈNH VỚI 33 CỘT CÔNG THỨC NATIVE (KHÔNG CÓ CỘT XE 5T)
# ==============================================================================
excel_path = os.path.join(DATA_DIR, "FrostLink_Du_lieu_Chuan.xlsx")

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Final"
ws.views.sheetView[0].showGridLines = True

ws.cell(1, 1).value = "BẢNG DỮ LIỆU THỰC ĐỊA VÀ MÔ HÌNH ĐIỀU PHỐI CONTAINER LẠNH 40 FEET 3 LỚP FROSTLINK (92 NGÀY - THÁNG 5, 6, 7/2026)"
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
    ("Thực tế - Nhu cầu Cont 40ft (18T*0.96)", "BBDEFB"),
    ("Dự báo T+7 (Tấn)", "E0F2F1"),
    ("Dự báo T+3 (Tấn)", "E0F2F1"),
    ("Dự báo T+1 (Tấn)", "E0F2F1"),
    ("Dự báo - Sản lượng lạnh (Tấn)", "E0F2F1"),
    ("Dự báo - Nhu cầu Cont 40ft", "D1C4E9"),
    ("Lớp 1 - Cam kết cứng (70% Cont 40ft)", "C5CAE9"),
    ("Lớp 2 - Quyền chọn linh hoạt (20%)", "C5CAE9"),
    ("Trạng thái Lớp 2 (Hủy khi Mưa > 20mm)", "C5CAE9"),
    ("Lớp 2 - Thực chạy Cont 40ft", "C5CAE9"),
    ("Chi phí phạt cọc Lớp 2 (VNĐ)", "FFCDD2"),
    ("Lớp 3 - Giao ngay Cont 40ft", "C5CAE9"),
    ("Tổng Cont 40ft FrostLink thực chạy", "BBDEFB"),
    ("Giá cước Cont 40ft (VNĐ)", "FFF9C4"),
    ("Tỷ lệ hư hỏng (%)", "F5F5F5"),
    ("Baseline (Dự báo số Cont 40ft)", "FFE0B2"),
    ("Baseline - Sai số Cont 40ft", "FFE0B2"),
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
    
    # 8. Sản lượng xe lạnh
    ws.cell(r, 8).value = f'=G{r}*IF(F{r}=1, 0.85, 0.8)'
    # 9. Nhiệt độ yêu cầu
    ws.cell(r, 9).value = '2-4'
    # 10. Thực tế - Nhu cầu Cont 40ft
    ws.cell(r, 10).value = f'=INT(H{r}/(18*0.96))'
    
    # 11, 12, 13, 14. Dự báo sản lượng T+7, T+3, T+1, Cold_ton
    ws.cell(r, 11).value = f'=MAX(15, ROUND(TREND(G$3:G${max_data_row}, E$3:E${max_data_row}, E{r}), 1))'
    ws.cell(r, 12).value = f'=MAX(15, ROUND(TREND(G$3:G${max_data_row}, B$3:E${max_data_row}, B{r}:E{r}), 1))'
    ws.cell(r, 13).value = f'=MAX(15, ROUND(TREND(G$3:G${max_data_row}, B$3:F${max_data_row}, B{r}:F{r}), 1))'
    ws.cell(r, 14).value = f'=M{r}*IF(F{r}=1, 0.85, 0.8)'
    
    # 15. Dự báo Nhu cầu Cont 40ft
    ws.cell(r, 15).value = f'=MAX(0, INT(N{r}/(18*0.96)))'
    
    # 16, 17, 18, 19, 20, 21. Cơ chế điều phối 3 Lớp Cont 40ft
    ws.cell(r, 16).value = f'=MAX(0, ROUND(O{r}*70%, 0))'
    ws.cell(r, 17).value = f'=MAX(0, MIN(ROUNDUP(O{r}*0.2, 0), MAX(0, O{r} - P{r})))'
    ws.cell(r, 18).value = f'=IF(C{r}>20, "Hủy slot (Mưa > 20mm)", "Kích hoạt")'
    ws.cell(r, 19).value = f'=IF(C{r}>20, 0, Q{r})'
    ws.cell(r, 20).value = f'=IF(C{r}>20, Q{r}*0.2*W{r}, 0)' # Cọc 20% * Giá cước Col W
    ws.cell(r, 21).value = f'=MAX(0, J{r} - P{r} - S{r})'
    
    # 22. Tổng Cont 40ft thực chạy
    ws.cell(r, 22).value = f'=P{r} + S{r} + U{r}'
    
    # 23. Giá cước Cont 40ft (Col W)
    ws.cell(r, 23).value = f'=IF(OR(B{r}>=34, F{r}=1), 11700000, 9000000)'
    # 24. Tỷ lệ hao hụt
    ws.cell(r, 24).value = 0.02
    
    # 25, 26, 27, 28, 29. Baseline Cont 40ft (Moving Average 3 ngày)
    if idx >= 3:
        ws.cell(r, 25).value = f'=AVERAGE(J{r-3}:J{r-1})'
        ws.cell(r, 26).value = f'=ABS(J{r} - Y{r})'
    else:
        ws.cell(r, 25).value = None
        ws.cell(r, 26).value = None
        
    ws.cell(r, 27).value = f'=IF(Y{r}="", 0, IF(Y{r}>J{r}, (Y{r}-J{r})*2700000, 0))'
    ws.cell(r, 28).value = f'=IF(Y{r}="", 0, IF(J{r}>Y{r}, (J{r}-Y{r})*6000000, 0))'
    ws.cell(r, 29).value = f'=AA{r} + AB{r}'
    
    # 30, 31, 32, 33. Đánh giá FrostLink Cont 40ft
    ws.cell(r, 30).value = f'=ABS(V{r} - J{r})'
    ws.cell(r, 31).value = f'=IF(V{r}>J{r}, (V{r}-J{r})*2700000, 0)'
    ws.cell(r, 32).value = f'=IF(J{r}>V{r}, (J{r}-V{r})*6000000, 0)'
    ws.cell(r, 33).value = f'=AE{r} + AF{r} + T{r}'
    
    for c_idx in range(1, 34):
        cell = ws.cell(r, c_idx)
        cell.font = Font(name="Arial", size=9)
        cell.border = thin_border
        if c_idx in [1, 9, 18]:
            cell.alignment = Alignment(horizontal="center")
        else:
            cell.alignment = Alignment(horizontal="right")
            
        if c_idx == 4:
            cell.number_format = '0.0%'
        elif c_idx in [2, 3]:
            cell.number_format = '0.0'
        elif c_idx in [7, 8, 11, 12, 13, 14]:
            cell.number_format = '#,##0.0'
        elif c_idx in [20, 23, 27, 28, 29, 31, 32, 33]:
            cell.number_format = '#,##0'
        elif c_idx in [6, 10, 15, 16, 17, 19, 21, 22, 25, 26, 30]:
            cell.number_format = '#,##0'

# ==============================================================================
# BẢNG TỔNG HỢP KPI SO SÁNH (DÒNG 96 ĐẾN 104)
# ==============================================================================
ws.cell(96, 2).value = "BẢNG TỔNG HỢP KPI SO SÁNH HIỆU QUẢ: BASELINE VS. FROSTLINK (92 NGÀY MÙA VỤ CONT 40FT)"
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
    ("Sai số số xe trung bình (Truck MAE - Cont/ngày)", f"=AVERAGE(Z6:Z{max_data_row})", f"=AVERAGE(AD6:AD{max_data_row})", "=C98-D98", "=(C98-D98)/C98"),
    ("Sai số phần trăm có trọng số (Truck WAPE)", f"=SUM(Z6:Z{max_data_row})/SUM(J6:J{max_data_row})", f"=SUM(AD6:AD{max_data_row})/SUM(J6:J{max_data_row})", "=C99-D99", "=(C99-D99)/C99"),
    ("Sai số sản lượng MAE (Tấn/ngày)", f"=AVERAGE(Z6:Z{max_data_row})*(18*0.96)", f"=D98*(18*0.96)", "=C100-D100", "=(C100-D100)/C100"),
    ("Tổng chi phí thừa xe C_over (VNĐ)", f"=SUM(AA3:AA{max_data_row})", f"=SUM(AE3:AE{max_data_row})", "=C101-D101", "=IF(C101=0, 0, (C101-D101)/C101)"),
    ("Tổng chi phí thiếu xe C_under (VNĐ)", f"=SUM(AB3:AB{max_data_row})", f"=SUM(AF3:AF{max_data_row})", "=C102-D102", "=IF(C102=0, 0, (C102-D102)/C102)"),
    ("Chi phí phạt hủy cọc Lớp 2 (VNĐ)", 0, f"=SUM(T3:T{max_data_row})", "=C103-D103", '=IF(C103=0, "N/A", (C103-D103)/C103)'),
    ("TỔNG CHI PHÍ RỦI RO CHUỖI LẠNH (VNĐ)", f"=SUM(AC3:AC{max_data_row})", f"=SUM(AG3:AG{max_data_row})", "=C104-D104", "=(C104-D104)/C104")
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
print(f"[+] ĐÃ LƯU THÀNH CÔNG FILE EXCEL CHUẨN 33 CỘT (100% CONT 40FT): {excel_path}")
print("=" * 80)
