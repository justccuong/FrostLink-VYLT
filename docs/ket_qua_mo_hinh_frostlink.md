# BÁO CÁO KẾT QUẢ ĐỐI CHUẨN MÔ HÌNH DỰ BÁO (MỤC 5.1 FROSTLINK)
*Tác giả: Đặng Cường - Lead AI Engineer*

### 1. Bảng đối chuẩn hiệu quả giữa các cấp độ mô hình (Toàn vụ 92 ngày)

| Mô hình | MAE Sản lượng (Tấn) | Truck MAE (Xe/ngày) | Truck WAPE (%) | R² Score | Đánh giá & Vai trò trong đề án |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Baseline (Moving Avg 3d)** | 65.07 Tấn | 3.81 Xe/ngày | 25.66% | — | Phương thức thủ công HTX (bị trễ pha khi có bão, sai số lớn). |
| **Hồi quy Đa biến (OLS Econometrics)** | 47.82 Tấn | 2.24 Xe/ngày | 15.57% | 0.929 | Mô hình giải thích (Explainable): Phân tích hệ số biên kinh tế lượng. |
| **Random Forest (Cây quyết định)** | 15.58 Tấn | 0.74 Xe/ngày | 5.14% | 0.991 | Học máy phi tuyến, bền bỉ, chống quá khớp (overfitting) và phương sai tốt. |
| **XGBoost (Gradient Boosting)** | 4.20 Tấn | 0.18 Xe/ngày | 1.28% | 0.999 | Mô hình tối ưu chính thức: Bắt trọn 2 đợt bão dông, WAPE tối thiểu. |

### 2. Phương trình Hồi quy Tuyến tính Đa biến (OLS)

$$\hat{Y}_t = -85.32 + 4.16 \cdot \text{Temp}_t - 4.42 \cdot \text{Rain}_t + 15.12 \cdot \text{Ripe}_t + 0.89 \cdot \text{Order}_t - 12.16 \cdot \text{Peak}_t$$

#### Ý nghĩa kinh tế của các hệ số biên (Marginal Effects):
* **Temp ($\beta = +4.159$):** Khi biến `Temp` tăng 1 đơn vị, sản lượng thu hoạch dự báo tăng 4.159 tấn.
* **Rain ($\beta = -4.421$):** Khi biến `Rain` tăng 1 đơn vị, sản lượng thu hoạch dự báo giảm 4.421 tấn.
* **Ripe ($\beta = +15.118$):** Khi biến `Ripe` tăng 1 đơn vị, sản lượng thu hoạch dự báo tăng 15.118 tấn.
* **Order ($\beta = +0.893$):** Khi biến `Order` tăng 1 đơn vị, sản lượng thu hoạch dự báo tăng 0.893 tấn.
* **Peak ($\beta = -12.158$):** Khi biến `Peak` tăng 1 đơn vị, sản lượng thu hoạch dự báo giảm 12.158 tấn.