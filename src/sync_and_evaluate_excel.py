# -*- coding: utf-8 -*-
import sys, io
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import numpy as np
import pandas as pd
import openpyxl

wb_v = openpyxl.load_workbook('Copy of Dữ liệu (2).xlsx', data_only=True)
ws_v = wb_v['Final']
wb_f = openpyxl.load_workbook('Copy of Dữ liệu (2).xlsx', data_only=False)
ws_f = wb_f['Final']

print("[*] Đang đọc dữ liệu đầu vào và đồng bộ toàn bộ công thức...")

# Đọc các biến đầu vào cơ sở (Row 3 đến 32)
days = []
temp = []
rain = []
ripe = []
order = []
peak = []
harvest = []

for r in range(3, 33):
    days.append(ws_v.cell(r, 1).value)
    temp.append(float(ws_v.cell(r, 2).value))
    rain.append(float(ws_v.cell(r, 3).value))
    ripe.append(float(ws_v.cell(r, 4).value))
    order.append(float(ws_v.cell(r, 5).value))
    peak.append(int(ws_v.cell(r, 6).value))
    harvest.append(float(ws_v.cell(r, 7).value))

df = pd.DataFrame({
    'Day': days, 'Temp': temp, 'Rain': rain, 'Ripe': ripe, 
    'Order': order, 'Peak': peak, 'Harvest': harvest
})

# Tính toán các cột theo đúng logic chuẩn
truck_cap = 17.2
ratio = np.where(df['Peak'] == 1, 0.85, 0.80)
df['Cold_ton'] = np.round(df['Harvest'] * ratio, 2)
df['Actual_trucks'] = np.ceil(df['Cold_ton'] / truck_cap).astype(int)

# Hồi quy OLS (tương đương hàm TREND trong Excel)
from sklearn.linear_model import LinearRegression
# T+7: Order
ols_t7 = LinearRegression().fit(df[['Order']], df['Harvest'])
df['Pred_T7'] = np.round(ols_t7.predict(df[['Order']]), 1)

# T+3: Temp, Rain, Ripe, Order
ols_t3 = LinearRegression().fit(df[['Temp', 'Rain', 'Ripe', 'Order']], df['Harvest'])
df['Pred_T3'] = np.round(ols_t3.predict(df[['Temp', 'Rain', 'Ripe', 'Order']]), 1)

# T+1: Temp, Rain, Ripe, Order, Peak
ols_t1 = LinearRegression().fit(df[['Temp', 'Rain', 'Ripe', 'Order', 'Peak']], df['Harvest'])
df['Pred_T1'] = np.round(ols_t1.predict(df[['Temp', 'Rain', 'Ripe', 'Order', 'Peak']]), 1)

# Nhu cầu xe FrostLink (dựa trên T+1)
df['Demand_trucks'] = np.ceil((df['Pred_T1'] * ratio) / truck_cap).astype(int)

# 3 Lớp công suất
df['L1'] = np.round(df['Demand_trucks'] * 0.7).astype(int)
df['L2_plan'] = np.minimum(np.ceil(df['Demand_trucks'] * 0.2), np.maximum(0, df['Demand_trucks'] - df['L1'])).astype(int)
df['L2_run'] = np.where(df['Rain'] > 20, 0, df['L2_plan'])

# Giá xe và phạt cọc Lớp 2 (20% cọc)
df['Price'] = np.where((df['Temp'] >= 34) | (df['Peak'] == 1), 11_700_000, 9_000_000)
df['L2_penalty'] = np.where(df['Rain'] > 20, df['L2_plan'] * 0.2 * df['Price'], 0)

# Lớp 3 giao ngay
df['L3'] = np.maximum(0, df['Actual_trucks'] - df['L1'] - df['L2_run']).astype(int)
df['Total_run'] = df['L1'] + df['L2_run'] + df['L3']

# Baseline Moving Average 3 days
baseline_pred = [None, None, None]
for i in range(3, len(df)):
    baseline_pred.append(np.mean(df['Actual_trucks'].iloc[i-3:i]))
df['Baseline_pred'] = baseline_pred
df['Baseline_err'] = [abs(p - a) if p is not None else None for p, a in zip(df['Baseline_pred'], df['Actual_trucks'])]

# Chi phí rủi ro chuẩn hóa
c_over_unit = 2_700_000
c_under_unit = 6_000_000

df['Baseline_C_over'] = [max(0, p - a) * c_over_unit if p is not None else 0 for p, a in zip(df['Baseline_pred'], df['Actual_trucks'])]
df['Baseline_C_under'] = [max(0, a - p) * c_under_unit if p is not None else 0 for p, a in zip(df['Baseline_pred'], df['Actual_trucks'])]
df['Baseline_Risk_Total'] = df['Baseline_C_over'] + df['Baseline_C_under']

df['Frost_err'] = np.abs(df['Total_run'] - df['Actual_trucks'])
df['Frost_C_over'] = np.maximum(0, df['Total_run'] - df['Actual_trucks']) * c_over_unit
df['Frost_C_under'] = np.maximum(0, df['Actual_trucks'] - df['Total_run']) * c_under_unit
df['Frost_Risk_Total'] = df['Frost_C_over'] + df['Frost_C_under'] + df['L2_penalty']

print("[+] Đã tính toán xong bảng dữ liệu 30 ngày:")
print(f"    - Tổng sản lượng thu hoạch: {df['Harvest'].sum():,.1f} Tấn")
print(f"    - Tổng số cont yêu cầu    : {df['Actual_trucks'].sum()} Cont")
print(f"    - Tổng xe FrostLink chạy  : {df['Total_run'].sum()} Cont")
print(f"    - Tổng cọc phạt hủy Lớp 2 : {df['L2_penalty'].sum():,.0f} VNĐ")

# Ghi vào file Excel chuẩn FrostLink_Du_lieu_Chuan.xlsx
# Giữ nguyên công thức trong cell, nhưng lưu giá trị vào
wb_out = openpyxl.load_workbook('Copy of Dữ liệu (2).xlsx', data_only=False)
ws = wb_out['Final']

for idx, r in enumerate(range(3, 33)):
    row_data = df.iloc[idx]
    # Cập nhật công thức và cấu trúc
    ws.cell(r, 8).value = f'=G{r}*IF(F{r}=1, 0.85, 0.8)'
    ws.cell(r, 10).value = f'=ROUNDUP(H{r}/17.2, 0)'
    ws.cell(r, 11).value = f'=ROUND(TREND(G$3:G$32, E$3:E$32, E{r}), 1)'
    ws.cell(r, 12).value = f'=ROUND(TREND(G$3:G$32, B$3:E$32, B{r}:E{r}), 1)'
    ws.cell(r, 13).value = f'=ROUND(TREND(G$3:G$32, B$3:F$32, B{r}:F{r}), 1)'
    ws.cell(r, 14).value = f'=ROUNDUP(M{r}*IF(F{r}=1, 0.85, 0.8)/17.2, 0)'
    ws.cell(r, 15).value = f'=ROUND(N{r}*70%, 0)'
    ws.cell(r, 16).value = f'=MIN(ROUNDUP(N{r}*0.2, 0), MAX(0, N{r} - O{r}))'
    ws.cell(r, 17).value = f'=IF(C{r}>20, "Hủy slot (Mưa > 20mm)", "Kích hoạt")'
    ws.cell(r, 18).value = f'=IF(C{r}>20, 0, P{r})'
    ws.cell(r, 19).value = f'=IF(C{r}>20, P{r}*0.2*Y{r}, 0)'
    ws.cell(r, 20).value = f'=MAX(0, J{r} - O{r} - R{r})'
    ws.cell(r, 21).value = f'=O{r} + R{r} + T{r}'
    ws.cell(r, 25).value = f'=IF(OR(B{r}>=34, F{r}=1), 11700000, 9000000)'
    
    if idx >= 3:
        ws.cell(r, 27).value = f'=AVERAGE(J{r-3}:J{r-1})'
        ws.cell(r, 28).value = f'=ABS(J{r} - AA{r})'
    else:
        ws.cell(r, 27).value = None
        ws.cell(r, 28).value = None
        
    ws.cell(r, 30).value = f'=IF(AA{r}="", 0, IF(AA{r}>J{r}, (AA{r}-J{r})*2700000, 0))'
    ws.cell(r, 31).value = f'=IF(AA{r}="", 0, IF(J{r}>AA{r}, (J{r}-AA{r})*6000000, 0))'
    ws.cell(r, 32).value = f'=AD{r} + AE{r}'
    
    ws.cell(r, 33).value = f'=ABS(U{r} - J{r})'
    ws.cell(r, 34).value = f'=IF(U{r}>J{r}, (U{r}-J{r})*2700000, 0)'
    ws.cell(r, 35).value = f'=IF(J{r}>U{r}, (J{r}-U{r})*6000000, 0)'
    ws.cell(r, 36).value = f'=AH{r} + AI{r} + S{r}'

# Cập nhật Bảng KPI dòng 35-42
ws.cell(36, 3).value = '=AVERAGE(AB6:AB32)'
ws.cell(36, 4).value = '=AVERAGE(AG6:AG32)'
ws.cell(36, 5).value = '=C36 - D36'
ws.cell(36, 6).value = '=(C36 - D36) / C36'

ws.cell(37, 3).value = '=SUM(AB6:AB32) / SUM(J6:J32)'
ws.cell(37, 4).value = '=SUM(AG6:AG32) / SUM(J6:J32)'
ws.cell(37, 5).value = '=C37 - D37'
ws.cell(37, 6).value = '=(C37 - D37) / C37'

ws.cell(38, 3).value = '=AVERAGE(AB6:AB32) * 17.2'
ws.cell(38, 4).value = '=D36 * 17.2'
ws.cell(38, 5).value = '=C38 - D38'
ws.cell(38, 6).value = '=(C38 - D38) / C38'

ws.cell(39, 3).value = '=SUM(AD3:AD32)'
ws.cell(39, 4).value = '=SUM(AH3:AH32)'
ws.cell(39, 5).value = '=C39 - D39'
ws.cell(39, 6).value = '=IF(C39=0, 0, (C39 - D39) / C39)'

ws.cell(40, 3).value = '=SUM(AE3:AE32)'
ws.cell(40, 4).value = '=SUM(AI3:AI32)'
ws.cell(40, 5).value = '=C40 - D40'
ws.cell(40, 6).value = '=IF(C40=0, 0, (C40 - D40) / C40)'

ws.cell(41, 3).value = 0
ws.cell(41, 4).value = '=SUM(S3:S32)'
ws.cell(41, 5).value = '=C41 - D41'
ws.cell(41, 6).value = '=IF(C41=0, "N/A", (C41-D41)/C41)'

ws.cell(42, 3).value = '=SUM(AF3:AF32)'
ws.cell(42, 4).value = '=SUM(AJ3:AJ32)'
ws.cell(42, 5).value = '=C42 - D42'
ws.cell(42, 6).value = '=(C42 - D42) / C42'

wb_out.save('FrostLink_Du_lieu_Chuan.xlsx')
print("[+] Đã lưu thành công file hoàn chỉnh: FrostLink_Du_lieu_Chuan.xlsx")

# Lưu thêm 1 bản dạng CSV sạch để các script Python đọc siêu tốc
df.to_csv('FrostLink_Data_Evaluated.csv', index=False, encoding='utf-8-sig')
print("[+] Đã lưu bản dữ liệu tính sẵn: FrostLink_Data_Evaluated.csv")
