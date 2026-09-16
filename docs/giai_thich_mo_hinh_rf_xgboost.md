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
| **MAE Sản lượng** | **10.40 Tấn / ngày** | **3.98 Tấn / ngày** (Cực kỳ chính xác) |
| **Truck MAE** | **0.53 Xe / ngày** | **0.30 Xe / ngày** |
| **Truck WAPE (%)** | **17.20%** | **9.68%** (Đạt chuẩn Logistics quốc tế $< 10\%$) |
| **Hệ số xác định ($R^2$)** | **0.754** (Giải thích 75.4% dữ liệu) | **0.960** (Giải thích 96.0% dữ liệu) |

---

## 4. GIẢI MÃ CÁC THAM SỐ (HYPERPARAMETERS) ĐÃ DÙNG TRONG CODE

Trong file `pipeline_frostlink_ai.py`, nhóm đã cấu hình bộ tham số "vàng" phù hợp hoàn hảo với tập dữ liệu mùa vụ:

```python
model = xgb.XGBRegressor(
    n_estimators=50, 
    max_depth=3, 
    learning_rate=0.08, 
    random_state=42
)
```

1. **`n_estimators = 50` (Số lượng cây = 50):**  
   * Dữ liệu mùa vụ gồm 30 ngày. 50 cây là con số vừa vặn nhất: đủ để học hết quy luật mưa - nắng - đơn hàng, nhưng không quá lớn (như 500 hay 1000 cây) để tránh bẫy quá khớp (Overfitting).
2. **`max_depth = 3` (Độ sâu tối đa của mỗi cây = 3 tầng):**  
   * Một cây chỉ được phân nhánh tối đa 3 câu hỏi liên tiếp (Ví dụ: Tầng 1 hỏi *Mưa $\ge 50$mm?* $\rightarrow$ Tầng 2 hỏi *Nhiệt độ $\ge 34^\circ\text{C}$?* $\rightarrow$ Tầng 3 hỏi *Có phải ngày cuối tuần?*).  
   * Giữ `max_depth = 3` giúp mô hình duy trì tính logic đơn giản, ngăn cản cây học các tiểu tiết vụn vặt.
3. **`learning_rate = 0.08` (Tốc độ học $\eta$):**  
   * Mỗi cây sau chỉ được đóng góp $8\%$ vào kết quả chung. Việc đi từng bước nhỏ giúp mô hình hội tụ êm ái, tránh bị sốc khi gặp các điểm ngoại lai.
4. **`random_state = 42`:**  
   * Cố định hạt giống ngẫu nhiên, đảm bảo kết quả luôn tái lập $100\%$ chính xác giữa máy của bạn, máy của ban giám khảo và máy của nhóm.

---

## 5. BỘ KỊCH BẢN PHÒNG VỆ PHẢN BIỆN (DEFENSE Q&A SCRIPT)

### ❓ Câu hỏi 1: "Tập dữ liệu mùa vụ chỉ có 30 ngày ($N=30$), chạy Random Forest và XGBoost có bị Overfitting (học vẹt) không?"
* **Trả lời chuẩn:**  
  *"Dạ thưa Thầy/Cô, nhóm đã lường trước nguy cơ này ngay từ khâu thiết kế thuật toán nên đã áp dụng 3 cơ chế phòng vệ chống Overfitting cực kỳ nghiêm ngặt:  
  1. **Khống chế độ sâu cây (Pruning):** Nhóm cố định `max_depth = 3`. Cây chỉ được phép hỏi tối đa 3 câu điều kiện thực tế (Mưa, Nhiệt độ, Ngày cao điểm), loại bỏ hoàn toàn khả năng chia nhánh phức tạp để học vẹt dữ liệu.  
  2. **Thu hẹp tốc độ học (Shrinkage):** Cài đặt `learning_rate = 0.08` rất nhỏ, mỗi cây chỉ hiệu chỉnh một phần sai số nhỏ chứ không ghi nhớ điểm dữ liệu.  
  3. **Quy đổi tác nghiệp theo hàm trần/sàn (Discretization) & Đội xe hỗn hợp:** Dự báo sản lượng sau đó được nén qua định mức tải trọng hữu dụng Cont 40ft ($18 \times 0.95 = 17.1\text{ tấn}$) và Xe 5T ($5 \times 0.95 = 4.75\text{ tấn}$) cùng rổ phân bổ 3 Lớp công suất. Điều này triệt tiêu mọi dao động nhỏ của thuật toán trước khi biến thành quyết định điều xe thực tế."*

### ❓ Câu hỏi 2: "Tại sao nhóm chọn XGBoost và Random Forest mà không dùng Deep Learning hay LSTM?"
* **Trả lời chuẩn:**  
  *"Thưa Thầy/Cô, với dữ liệu dạng bảng (Tabular Data) và quy mô mùa vụ nông sản ngắn hạn, các nghiên cứu khoa học uy tín trên thế giới (như bài báo nổi tiếng NeurIPS 'Why do tree-based models still outperform deep learning on tabular data?') đều khẳng định các mô hình Tree-based (XGBoost/RF) luôn vượt trội Deep Learning về cả độ chính xác, tốc độ huấn luyện lẫn khả năng chống nhiễu. Deep Learning chỉ phát huy tác dụng khi có hàng triệu ảnh hoặc chuỗi thời gian nhiều năm; nếu áp dụng vào 30 ngày mùa vải sẽ chắc chắn thất bại vì thiếu dữ liệu."*

### ❓ Câu hỏi 3: "Giữa Random Forest và XGBoost, mô hình nào là phương án đề xuất chính thức của FrostLink?"
* **Trả lời chuẩn:**  
  *"XGBoost là mô hình dự báo sản lượng chính thức vì đạt độ chính xác vượt trội (Truck WAPE chỉ $9.68\%$ so với $17.20\%$ của Random Forest). Nhờ cơ chế sửa sai nối tiếp, XGBoost bắt trọn được điểm rơi sản lượng của 2 ngày mưa bão lịch sử (ngày 16 và 25), giúp hệ thống kích hoạt lệnh hủy cọc Lớp 2 chuẩn xác $100\%$, mang lại mức tiết kiệm chi phí rủi ro $71.4\%$ cho toàn bộ vụ mùa."*
