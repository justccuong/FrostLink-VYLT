# TÀI LIỆU CHUYÊN SÂU: GIẢI THÍCH TOÀN DIỆN MÔ HÌNH RANDOM FOREST & XGBOOST
**Đề án: FrostLink – Nền tảng điều phối công suất chuỗi lạnh mùa vụ (Lục Ngạn)**  
**Cuộc thi: Vietnam Young Logistics Talents (VYLT) 2026**  
*Tác giả: Đặng Cường - Thành viên k chính thức (Cẩm nang phòng vệ phản biện dành cho buổi họp và thuyết trình)*

---

## 1. TẠI SAO PHẢI DÙNG TREE-BASED (RANDOM FOREST & XGBOOST) THAY VÌ HỒI QUY ĐƠN THUẦN?

Trong kinh tế lượng truyền thống, các mô hình như OLS giả định mối quan hệ **tuyến tính (đường thẳng)** giữa các biến. Tuy nhiên, trong nông nghiệp mùa vụ (vải thiều Lục Ngạn), dữ liệu có **hiện tượng gãy khúc phi tuyến (Non-linear Threshold Effect)** rất mạnh:

* **Ví dụ thực tế:** 
  * Nếu trời mưa nhỏ ($< 15\text{mm}$), nông dân vẫn đội nón đi hái bình thường, sản lượng không đổi.
  * Nhưng hễ lượng mưa vượt ngưỡng $50\text{mm}$ (như bão ngày 16 và ngày 25), nông dân **dừng bẻ cành hoàn toàn**, sản lượng lập tức gãy đổ từ $75\text{ tấn}$ xuống thẳng $15\text{ tấn}$.
  * Mô hình đường thẳng (OLS) không thể uốn cong tức thì ở ngưỡng $50\text{mm}$, dẫn đến dự báo sai lệch lớn.
* **Giải pháp:** Các mô hình dựa trên Cây quyết định (**Decision Tree**) như **Random Forest** và **XGBoost** phân chia dữ liệu theo các câu hỏi điều kiện:
  $$\text{Nếu } Rain \ge 50\text{mm} \longrightarrow \text{Sản lượng} \approx 15 - 18\text{ Tấn (Dừng hái)}$$
  $$\text{Nếu } Rain < 50\text{mm} \text{ và } Temp \ge 34^\circ\text{C} \longrightarrow \text{Sản lượng} \approx 65 - 80\text{ Tấn (Chín rộ)}$$

---

## 2. BẢN CHẤT VÀ NGUYÊN LÝ HOẠT ĐỘNG CỦA 2 MÔ HÌNH

### 2.1. Mô hình 1: RANDOM FOREST (Rừng cây quyết định)
* **Ý tưởng cốt lõi (Trực giác bình dân):**  
  *"Một cây làm chẳng nên non, ba cây chụm lại nên hòn núi cao" (Wisdom of Crowds).*  
  Thay vì dựa vào 1 cây quyết định duy nhất (dễ bị học vẹt hoặc bị lừa bởi 1 ngày thời tiết lạ), Random Forest xây dựng một **"Hội đồng gồm 50 cây quyết định độc lập"**.
* **Cơ chế kỹ thuật (Bagging - Bootstrap Aggregating):**
  1. **Lấy mẫu có hoàn lại (Bootstrap):** Mỗi cây trong rừng được huấn luyện trên một tập dữ liệu con ngẫu nhiên.
  2. **Ngẫu nhiên hóa biến số (Feature Subsampling):** Tại mỗi bước phân nhánh, mỗi cây chỉ được nhìn thấy một số biến ngẫu nhiên (ví dụ cây này nhìn thấy Nhiệt độ & Mưa, cây kia nhìn thấy Đơn hàng & Tỷ lệ chín). Điều này giúp các cây không bị giống hệt nhau.
  3. **Biểu quyết số đông (Aggregating):** Khi có dự báo ngày mai, cả 50 cây đều đưa ra 50 con số dự báo sản lượng. Kết quả cuối cùng là **Trung bình cộng của 50 cây**:
     $$\hat{Y}_{\text{RF}} = \frac{1}{B} \sum_{b=1}^{B} T_b(X) \quad (\text{với } B = 50\text{ cây})$$
* **Ưu điểm lớn nhất:** Rất bền bỉ (Robust), triệt tiêu phương sai (Variance Reduction), không bao giờ bị phụ thuộc vào lỗi của một cây đơn lẻ.

---

### 2.2. Mô hình 2: XGBOOST (Extreme Gradient Boosting)
* **Ý tưởng cốt lõi (Trực giác bình dân):**  
  *"Cây sau sinh ra để chuộc lỗi cho cây trước" (Sequential Error Correction).*  
  Khác với Random Forest (các cây mọc độc lập, mạnh ai nấy đoán), XGBoost hoạt động theo dạng **Dây chuyền nối tiếp**:
* **Cơ chế kỹ thuật (Gradient Boosting):**
  1. **Cây số 1:** Đưa ra dự báo sơ bộ ban đầu. Chắc chắn còn nhiều ngày bị đoán sai (gọi là Phần dư - Residual $e_1 = Y - \hat{Y}_1$).
  2. **Cây số 2:** Không học lại toàn bộ dữ liệu, mà **tập trung toàn lực để dự báo phần sai số $e_1$ của Cây 1**.
  3. **Cây số 3:** Học phần sai số còn sót lại của Cây 1 + Cây 2.
  4. Cứ thế, 50 cây được huấn luyện nối đuôi nhau. Mỗi cây sau bù đắp chính xác điểm yếu của cây trước:
     $$\hat{Y}_{\text{XGB}} = \sum_{k=1}^{K} \eta \cdot f_k(X) \quad (\text{với } K = 50, \eta = 0.08)$$
* **Tại sao có chữ "Extreme" (Cực đỉnh)?:**
  * Tích hợp sẵn **Hàm phạt kiểm soát quá khớp (Regularization L1/L2)** ngay trong hàm mất mát (Loss Function), ngăn không cho các nhánh cây mọc quá sâu.
  * Sử dụng đạo hàm bậc 2 (Hessian matrix) để tối ưu bước nhảy cực kỳ chuẩn xác và tính toán song song siêu tốc trên CPU/GPU.

---

## 3. BẢNG ĐỐI ĐẦU TRỰC DIỆN: RANDOM FOREST VS XGBOOST

| Tiêu chí so sánh | Random Forest (Rừng ngẫu nhiên) | XGBoost (Gradient Boosting) |
| :--- | :--- | :--- |
| **Cơ chế xây dựng cây** | **Song song (Parallel):** Các cây độc lập với nhau. | **Nối tiếp (Sequential):** Cây sau sửa lỗi cho cây trước. |
| **Cách tổng hợp kết quả** | Lấy trung bình cộng đơn giản (Simple Average). | Tổng có trọng số của các cây kèm tốc độ học (Shrinkage). |
| **Mục tiêu tối ưu** | Giảm thiểu **Phương sai (Variance)** $\rightarrow$ Chống nhiễu dữ liệu. | Giảm thiểu **Độ chệch (Bias)** $\rightarrow$ Tăng độ chính xác tối đa. |
| **Kiểm soát quá khớp** | Nhờ cơ chế lấy mẫu ngẫu nhiên (Bagging). | Nhờ hàm phạt tham số (L1 Lasso, L2 Ridge Regularization). |
| **MAE Sản lượng** | **9.80 Tấn / ngày** | **3.98 Tấn / ngày** (Cực kỳ chính xác) |
| **Truck MAE** | **0.45 Xe / ngày** | **0.18 Xe / ngày** |
| **Truck WAPE (%)** | **3.82%** | **1.53%** (Chuẩn logistics quốc tế khắt khe) |
| **Hệ số xác định ($R^2$ ngoại suy)** | **0.924** (Giải thích 92.4% dữ liệu) | **0.962** (Giải thích 96.2% biến thiên ngoại suy) |

---

## 4. GIẢI MÃ CÁC THAM SỐ (HYPERPARAMETERS) ĐÃ DÙNG TRONG CODE

Trong file `pipeline_frostlink_ai.py`, nhóm đã cấu hình bộ tham số "vàng" phù hợp hoàn hảo với tập dữ liệu mùa vụ 92 ngày:

```python
model = xgb.XGBRegressor(
    n_estimators=70, 
    max_depth=3, 
    learning_rate=0.06, 
    reg_alpha=2.0,       # L1 Regularization chống học vẹt
    reg_lambda=5.0,      # L2 Regularization kiểm soát độ nhạy
    subsample=0.85,      # Lấy mẫu 85% hàng chống quá khớp
    colsample_bytree=0.85, # Lấy mẫu 85% cột
    random_state=42
)
```

1. **`n_estimators = 70` (Số lượng cây = 70):**  
   * Dữ liệu mùa vụ gồm 92 ngày toàn vụ (Tháng 5, 6, 7). 70 cây là con số vừa vặn nhất: đủ để học hết quy luật mưa - nắng - đơn hàng, nhưng không quá lớn (như 500 hay 1000 cây) để tránh bẫy quá khớp (Overfitting).
2. **`max_depth = 3` (Độ sâu tối đa của mỗi cây = 3 tầng):**  
   * Một cây chỉ được phân nhánh tối đa 3 câu hỏi liên tiếp (Ví dụ: Tầng 1 hỏi *Mưa $\ge 20$mm?* $\rightarrow$ Tầng 2 hỏi *Nhiệt độ $\ge 34^\circ\text{C}$?* $\rightarrow$ Tầng 3 hỏi *Có phải ngày cao điểm PeakDay?*).  
   * Giữ `max_depth = 3` giúp mô hình duy trì tính logic đơn giản, ngăn cản cây học các tiểu tiết ngoại lai.
3. **`reg_alpha = 2.0` và `reg_lambda = 5.0` (Điều chuẩn hóa L1/L2):**  
   * Phạt độ lớn trọng số của các lá cây, ngăn mô hình gán trọng số cực đoan vào các ngày cá biệt.
4. **`learning_rate = 0.06` (Tốc độ học $\eta$):**  
   * Mỗi cây sau chỉ được đóng góp $6\%$ vào kết quả chung. Việc đi từng bước nhỏ giúp mô hình hội tụ êm ái, tránh bị sốc khi gặp các điểm biến động thời tiết cực đoan.

---

## 5. BỘ KỊCH BẢN PHÒNG VỆ PHẢN BIỆN (DEFENSE Q&A SCRIPT)

### ❓ Câu hỏi 1: "Tại sao ban đầu chạy mô hình XGBoost ra $R^2 = 1.000$? Đó có phải là học vẹt (Overfitting) không?"
* **Trả lời chuẩn đập tan phản biện:**  
  *"Dạ thưa Thầy/Cô, nhận định của Thầy/Cô hoàn toàn chính xác về mặt nguyên lý học máy! Ban đầu nếu ta huấn luyện mô hình trên toàn bộ 92 ngày rồi đo lường ngay trên chính tập dữ liệu đó (đánh giá trong mẫu - In-Sample Resubstitution), thuật toán XGBoost với dung lượng mạnh sẽ ghi nhớ từng điểm dữ liệu khiến $R^2 \approx 0.9997$ làm tròn thành $1.000$.  
  Nhận thức sâu sắc nguy cơ học vẹt này, nhóm nghiên cứu đã **triệt tiêu hoàn toàn đánh giá trong mẫu** và chuyển toàn bộ sang phương pháp luận kiểm chuẩn khoa học nghiêm ngặt:  
  1. **Kiểm chuẩn chéo 5-Fold Cross Validation:** Chia dữ liệu thành 5 phần độc lập; mô hình chỉ được dự báo trên tập dữ liệu kiểm thử mà nó **hoàn toàn chưa từng được nhìn thấy** trong lúc học.  
  2. **Điều chuẩn hóa Regularization ($L_1 = 2.0, L_2 = 5.0$):** Bắt buộc hàm mục tiêu phải tối giản hóa trọng số, triệt tiêu khả năng vẽ đường cong quá khớp.  
  3. **Khống chế độ sâu `max_depth = 3`:** Giới hạn cây chỉ phân nhánh 3 tầng điều kiện tự nhiên.  
  Kết quả kiểm chuẩn ngoại suy độc lập cho thấy mô hình đạt **$R^2 = 0.962$** và **Truck WAPE = 1.53%**. Con số $R^2 = 0.962$ giải thích được 96.2% biến thiên sản lượng ngoại suy mà vẫn giữ 3.8% độ biến thiên vi khí hậu tự nhiên, chứng minh tính vững chắc và khả năng khái quát hóa (Generalization) vượt trội khi ứng dụng thực địa."*

### ❓ Câu hỏi 2: "Tại sao nhóm chọn XGBoost và Random Forest mà không dùng Deep Learning hay LSTM?"
* **Trả lời chuẩn:**  
  *"Thưa Thầy/Cô, với dữ liệu dạng bảng (Tabular Data) và quy mô mùa vụ nông sản 92 ngày, các nghiên cứu khoa học uy tín trên thế giới (như bài báo NeurIPS 'Why do tree-based models still outperform deep learning on tabular data?') đều khẳng định các mô hình Tree-based (XGBoost/RF) luôn vượt trội Deep Learning về cả độ chính xác, tốc độ huấn luyện lẫn khả năng chống nhiễu. Deep Learning chỉ phát huy tác dụng khi có hàng trăm nghìn mẫu dữ liệu; nếu áp dụng vào 92 ngày mùa vải sẽ chắc chắn thất bại vì thiếu dữ liệu và bẫy quá khớp nặng."*

### ❓ Câu hỏi 3: "Giữa Random Forest và XGBoost, mô hình nào là phương án đề xuất chính thức của FrostLink?"
* **Trả lời chuẩn:**  
  *"XGBoost là mô hình dự báo sản lượng chính thức (Champion Engine) vì đạt độ chính xác kiểm chuẩn ngoại suy vượt trội (Truck WAPE chỉ $1.53\%$ so với $3.82\%$ của Random Forest và $6.94\%$ của OLS). Nhờ cơ chế sửa sai nối tiếp, XGBoost bắt trọn được điểm rơi sản lượng của các đợt mưa dông bất thường, giúp hệ thống kích hoạt lệnh hủy cọc Lớp 2 chuẩn xác, kết hợp với điều phối Đội xe hỗn hợp mang lại mức tiết kiệm chi phí rủi ro $91.9\%$ cho toàn bộ vụ mùa."*
