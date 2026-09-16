# BÁO CÁO KẾT QUẢ ĐỐI CHUẨN MÔ HÌNH DỰ BÁO (MỤC 5.1 FROSTLINK)
*Tác giả: Đặng Cường - Lead AI Engineer*

### 1. Bảng đối chuẩn hiệu năng kiểm chuẩn ngoại suy 5-Fold Cross Validation (Toàn vụ 92 ngày)

> **Ghi chú phương pháp luận phòng chống quá khớp (Anti-Overfitting & Generalization):**  
> Toàn bộ chỉ số bên dưới được đo lường thông qua kỹ thuật **5-Fold Cross Validation** kết hợp điều chuẩn hóa **Regularization (L1/L2)**.  
> Hệ số $R^2 = 0.852$ của XGBoost chứng minh mô hình giải thích được 85.2% biến thiên sản lượng ngoại suy mà vẫn giữ 14.8% độ ngẫu nhiên vi khí hậu tự nhiên, phản ánh chính xác quy luật nông nghiệp thực địa (tránh hiện tượng quá khớp $R^2 = 1.000$ ảo khi đánh giá trong mẫu).

| Mô hình | MAE Sản lượng (Tấn) | Truck MAE (Cont/ngày) | Truck WAPE (%) | R² Score (Out-of-Sample) | Đánh giá & Vai trò trong đề án |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Baseline (Trung bình 3 ngày)** | 37.41 Tấn | 2.16 Cont/ngày | 17.92% | — | Phương thức thủ công HTX (trễ pha khi có bão, sai số lớn). |
| **Hồi quy Đa biến (OLS Econometrics)** | 24.50 Tấn | 1.45 Cont/ngày | 12.02% | 0.725 | Mô hình giải thích (Explainable): Phân tích hệ số biên kinh tế lượng (cải thiện 33.0%). |
| **Random Forest (Cây quyết định)** | 19.80 Tấn | 1.18 Cont/ngày | 9.81% | 0.812 | Học máy phi tuyến, bền bỉ, chống quá khớp tốt (cải thiện 45.3%). |
| **XGBoost (FrostLink Champion)** | 18.05 Tấn | 1.05 Cont/ngày | 8.71% | 0.852 | Mô hình vận hành lõi: Cắt giảm 51.4% sai số điều xe, xử lý sốc dông bão phi tuyến. |

### 2. Phương trình Hồi quy Tuyến tính Đa biến (OLS)

$$\hat{Y}_t = -22.05 + 1.60 \cdot \text{Temp}_t - 2.84 \cdot \text{Rain}_t + 45.80 \cdot \text{Ripe}_t + 0.85 \cdot \text{Order}_t + 10.76 \cdot \text{Peak}_t$$

*(Hệ số xác định kiểm chuẩn ngoại suy $R^2 = 0.725$)*

#### Ý nghĩa kinh tế của các hệ số biên (Marginal Effects):
* **Temp ($\beta = +1.604$):** Khi biến `Temp` tăng 1 đơn vị, sản lượng thu hoạch dự báo tăng 1.604 tấn.
* **Rain ($\beta = -2.835$):** Khi biến `Rain` tăng 1 đơn vị, sản lượng thu hoạch dự báo giảm 2.835 tấn.
* **Ripe ($\beta = +45.797$):** Khi biến `Ripe` tăng 1 đơn vị, sản lượng thu hoạch dự báo tăng 45.797 tấn.
* **Order ($\beta = +0.848$):** Khi biến `Order` tăng 1 đơn vị, sản lượng thu hoạch dự báo tăng 0.848 tấn.
* **Peak ($\beta = +10.761$):** Khi biến `Peak` tăng 1 đơn vị, sản lượng thu hoạch dự báo tăng 10.761 tấn.