# BÁO CÁO KẾT QUẢ ĐỐI CHUẨN MÔ HÌNH DỰ BÁO (MỤC 5.1 FROSTLINK)

### 1. Bảng đối chuẩn hiệu quả giữa các cấp độ mô hình

| Mô hình | MAE Sản lượng (Tấn) | Truck MAE (Xe/ngày) | Truck WAPE (%) | R² Score | Đánh giá & Vai trò trong đề án |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Baseline (Moving Avg 3d)** | 14.23 Tấn | 0.83 Xe/ngày | 25.09% | - | Phương thức thủ công HTX (trễ pha khi mưa bão, sai số cao). |
| **Hồi quy Đa biến (OLS Econometrics)** | 12.17 Tấn | 0.60 Xe/ngày | 19.35% | 0.616 | MÔ HÌNH GIẢI THÍCH (Explainable): Phân tích hệ số biên cho Giám khảo kinh tế. |
| **Random Forest (Cây quyết định)** | 10.40 Tấn | 0.53 Xe/ngày | 17.20% | 0.754 | Học máy cây ngẫu nhiên, bền bỉ, chống nhiễu phương sai tốt. |
| **XGBoost (Gradient Boosting)** | 3.98 Tấn | 0.30 Xe/ngày | 9.68% | 0.960 | MÔ HÌNH ĐỀ XUẤT CHÍNH THỨC (WAPE < 10%, bắt trọn 2 đợt bão). |

### 2. Phương trình Hồi quy Tuyến tính Đa biến (OLS)

$$\hat{Y}_t = 258.76 - 6.64 \cdot \text{Temp}_t + 0.08 \cdot \text{Rain}_t - 45.15 \cdot \text{Ripe_pct}_t + 1.00 \cdot \text{Order_ton}_t + 8.72 \cdot \text{PeakDay}_t$$

#### Ý nghĩa kinh tế của các hệ số biên (Marginal Effects):
* **Temp ($\beta = -6.644$):** Khi biến `Temp` tăng 1 đơn vị, sản lượng thu hoạch dự báo giảm 6.644 tấn.
* **Rain ($\beta = +0.080$):** Khi biến `Rain` tăng 1 đơn vị, sản lượng thu hoạch dự báo tăng 0.080 tấn.
* **Ripe_pct ($\beta = -45.151$):** Khi biến `Ripe_pct` tăng 1 đơn vị, sản lượng thu hoạch dự báo giảm 45.151 tấn.
* **Order_ton ($\beta = +0.996$):** Khi biến `Order_ton` tăng 1 đơn vị, sản lượng thu hoạch dự báo tăng 0.996 tấn.
* **PeakDay ($\beta = +8.718$):** Khi biến `PeakDay` tăng 1 đơn vị, sản lượng thu hoạch dự báo tăng 8.718 tấn.