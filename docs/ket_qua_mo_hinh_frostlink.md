# BÁO CÁO KẾT QUẢ ĐỐI CHUẨN MÔ HÌNH DỰ BÁO (MỤC 5.1 FROSTLINK)
*Tác giả: Đặng Cường - Lead AI Engineer*

### 1. Bảng đối chuẩn hiệu quả giữa các cấp độ mô hình (Toàn vụ 92 ngày)

| Mô hình | MAE Sản lượng (Tấn) | Truck MAE (Xe/ngày) | Truck WAPE (%) | R² Score | Đánh giá & Vai trò trong đề án |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Baseline (Moving Avg 3d)** | 37.41 Tấn | 2.16 Xe/ngày | 17.92% | — | Phương thức thủ công HTX (bị trễ pha khi có bão, sai số lớn). |
| **Hồi quy Đa biến (OLS Econometrics)** | 17.29 Tấn | 0.82 Xe/ngày | 6.94% | 0.983 | Mô hình giải thích (Explainable): Phân tích hệ số biên kinh tế lượng. |
| **Random Forest (Cây quyết định)** | 7.15 Tấn | 0.26 Xe/ngày | 2.22% | 0.997 | Học máy phi tuyến, bền bỉ, chống quá khớp (overfitting) và phương sai tốt. |
| **XGBoost (Gradient Boosting)** | 2.39 Tấn | 0.07 Xe/ngày | 0.56% | 1.000 | Mô hình tối ưu chính thức: Bắt trọn 2 đợt bão dông, WAPE tối thiểu. |

### 2. Phương trình Hồi quy Tuyến tính Đa biến (OLS)

$$\hat{Y}_t = -22.05 + 1.60 \cdot \text{Temp}_t - 2.84 \cdot \text{Rain}_t + 45.80 \cdot \text{Ripe}_t + 0.85 \cdot \text{Order}_t + 10.76 \cdot \text{Peak}_t$$

#### Ý nghĩa kinh tế của các hệ số biên (Marginal Effects):
* **Temp ($\beta = +1.604$):** Khi biến `Temp` tăng 1 đơn vị, sản lượng thu hoạch dự báo tăng 1.604 tấn.
* **Rain ($\beta = -2.835$):** Khi biến `Rain` tăng 1 đơn vị, sản lượng thu hoạch dự báo giảm 2.835 tấn.
* **Ripe ($\beta = +45.797$):** Khi biến `Ripe` tăng 1 đơn vị, sản lượng thu hoạch dự báo tăng 45.797 tấn.
* **Order ($\beta = +0.848$):** Khi biến `Order` tăng 1 đơn vị, sản lượng thu hoạch dự báo tăng 0.848 tấn.
* **Peak ($\beta = +10.761$):** Khi biến `Peak` tăng 1 đơn vị, sản lượng thu hoạch dự báo tăng 10.761 tấn.