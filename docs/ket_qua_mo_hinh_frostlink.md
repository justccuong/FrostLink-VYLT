# BÁO CÁO KẾT QUẢ ĐỐI CHUẨN MÔ HÌNH DỰ BÁO (MỤC 5.1 FROSTLINK)
*Tác giả: Đặng Cường - Thành viên k chính thức*

### 1. Bảng đối chuẩn hiệu quả giữa các cấp độ mô hình (Toàn vụ 92 ngày)

| Mô hình | MAE Sản lượng (Tấn) | Truck MAE (Xe/ngày) | Truck WAPE (%) | R² Score | Đánh giá & Vai trò trong đề án |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Baseline (Moving Avg 3d)** | 65.84 Tấn | 3.83 Xe/ngày | 24.30% | - | Phương thức thủ công HTX (bị trễ pha khi thời tiết đổi, sai số lớn). |
| **Hồi quy Đa biến (OLS Econometrics)** | 47.82 Tấn | 2.29 Xe/ngày | 14.99% | 0.929 | MÔ HÌNH GIẢI THÍCH (Explainable): Phân tích hệ số biên kinh tế lượng. |
| **Random Forest (Cây quyết định)** | 15.58 Tấn | 0.78 Xe/ngày | 5.11% | 0.991 | Học máy cây ngẫu nhiên phi tuyến, bền bỉ, chống nhiễu phương sai tốt. |
| **XGBoost (Gradient Boosting)** | 4.20 Tấn | 0.21 Xe/ngày | 1.35% | 0.999 | MÔ HÌNH ĐỀ XUẤT CHÍNH THỨC (Truck WAPE tối ưu, bắt trọn các đợt bão dông). |

### 2. Phương trình Hồi quy Tuyến tính Đa biến (OLS)

$$\hat{Y}_t = -85.32 + 4.16 \cdot \text{Temp}_t - 4.42 \cdot \text{Rain}_t + 15.12 \cdot \text{Ripe_pct}_t + 0.89 \cdot \text{Order_ton}_t - 12.16 \cdot \text{PeakDay}_t$$

#### Ý nghĩa kinh tế của các hệ số biên (Marginal Effects):
* **Temp ($\beta = +4.159$):** Khi biến `Temp` tăng 1 đơn vị, sản lượng thu hoạch dự báo tăng 4.159 tấn.
* **Rain ($\beta = -4.421$):** Khi biến `Rain` tăng 1 đơn vị, sản lượng thu hoạch dự báo giảm 4.421 tấn.
* **Ripe_pct ($\beta = +15.118$):** Khi biến `Ripe_pct` tăng 1 đơn vị, sản lượng thu hoạch dự báo tăng 15.118 tấn.
* **Order_ton ($\beta = +0.893$):** Khi biến `Order_ton` tăng 1 đơn vị, sản lượng thu hoạch dự báo tăng 0.893 tấn.
* **PeakDay ($\beta = -12.158$):** Khi biến `PeakDay` tăng 1 đơn vị, sản lượng thu hoạch dự báo giảm 12.158 tấn.