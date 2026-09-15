# TỔNG KẾT TOÀN DIỆN CÔNG VIỆC ĐÃ HOÀN THÀNH (AI & LOGISTICS MODEL 5.1)
**Đề án: FrostLink – Nền tảng điều phối công suất chuỗi lạnh mùa vụ (Lục Ngạn, Bắc Giang)**  
*Dành cho: Đặng Cường (Lead AI Engineer) báo cáo trong buổi họp nhóm 10h tối*

---

## 1. BỐI CẢNH VÀ BẢN CHẤT VAI TRÒ CỦA AI ENGINEER
* **Bối cảnh đề tài:** Tham dự cuộc thi *Vietnam Young Logistics Talents (VYLT)*.
* **Định hướng từ Giám khảo (Báo cáo nhận xét):**
  * Cấm làm "Sàn Grab mở hai chiều" (sinh viên không đủ lực quản lý thanh khoản và giao dịch chui).
  * Chuyển trọng tâm sang **Dự án thí điểm (Pilot) B2B**: Dự báo nhu cầu ngắn hạn và đặt trước công suất lạnh cho một mắt xích cụ thể (Vải thiều Lục Ngạn đi cửa khẩu Lạng Sơn).
* **Nhiệm vụ của AI Engineer:** 
  * Không trình diễn công nghệ phức tạp (Deep Learning/LSTM) trên tập dữ liệu nhỏ ($N=30$ ngày).
  * Xây dựng pipeline chuẩn mực: **Kiểm định dữ liệu $\rightarrow$ Trực quan hóa (EDA) $\rightarrow$ Mô hình giải thích được (Explainable Econometrics OLS / Tree) $\rightarrow$ Quy đổi tác nghiệp sang số xe Container $\rightarrow$ Lượng hóa rủi ro tài chính (Newsvendor Model)**.

---

## 2. NGUỒN GỐC DỮ LIỆU & BẰNG CHỨNG THỰC ĐỊA (FIELDWORK DATA)
Toàn bộ số liệu trong mô hình được "neo" 100% vào **Biên bản phỏng vấn thực tế với Doanh nghiệp thu mua & Đơn vị vận tải**:

1. **Đơn vị vận tải đối tác nòng cốt:** Công ty Vận tải và Du lịch Treviet.
2. **Tuyến vận chuyển chính:** Lục Ngạn $\rightarrow$ Cửa khẩu Hữu Nghị, Chi Ma, Hà Khẩu (Lạng Sơn).
3. **Phương tiện chuyên dụng:** Container lạnh 40 feet (Cont 40ft - 40RF).
   * Tải trọng hàng thực tế khi chở vải thiều: **18 tấn** (do giới hạn thể tích thùng xốp chèn đá và quy định trạm cân đường bộ 40 tấn).
   * Tải trọng hữu dụng kỹ thuật ($C_{\text{eff}}$): **17.2 tấn/cont** (chừa 4.5% dung tích cho luồng gió lạnh tuần hoàn).
4. **Giá cước vận tải:**
   * Ngày thường: **9.000.000 VNĐ / chuyến**.
   * Ngày cao điểm (cháy xe, nhiệt độ $\ge 34^\circ\text{C}$ hoặc cuối tuần): **Tăng 30% = 11.700.000 VNĐ / chuyến**.
5. **Quy mô mùa vụ thí điểm:** Tổng sản lượng thu hoạch 30 ngày chính vụ (tháng 6/2026) là **1.647 tấn vải** (tương đương nhu cầu **93 chuyến Cont 40ft**), đại diện cho Cụm liên minh gồm 1 Doanh nghiệp đầu mối và 2-3 Hợp tác xã vệ tinh.

---

## 3. BỘ THAM SỐ TÀI CHÍNH ĐÃ CHUẨN HÓA (ĐƯỢC KHÁNH LY THỐNG NHẤT)

Nhóm đã giải quyết triệt để "hạt sạn" kinh tế (tránh nghịch lý cọc đắt hơn xe chạy rỗng) với bộ 3 tham số:

| Hạng mục chi phí | Tỷ lệ quy định | Số tiền đưa vào mô hình | Căn cứ nghiệp vụ giải trình |
| :--- | :---: | :---: | :--- |
| **1. Cọc giữ chỗ Lớp 2 (Hủy trước 24h)** | **20% giá cước** | **1.800.000 VNĐ / cont** | Báo hủy trước 24h khi có bão, xe **chưa lăn bánh đến bãi**, nhà xe nhận trọn 20% cọc và nhận chuyến khác. HTX chỉ mất 1.8 triệu. |
| **2. Phạt xe chạy rỗng ($C_{over}$)** | **30% giá cước** | **2.700.000 VNĐ / cont** | Xe **đã lăn bánh đến bãi** nhưng không có hàng bốc lên $\rightarrow$ Xe chạy không về bãi. Bồi thường tiền dầu và công nhật tài xế. |
| **3. Thiệt hại thiếu xe ($C_{under}$)** | **Cước ép + Vải mất giá** | **6.000.000 VNĐ / cont** | Gồm: 2.7 triệu (bị ép cước cao điểm +30%) + 3.3 triệu (tiền 1 tấn vải chờ xe mất 25% giá trị xuất khẩu). |

👉 **Thang bậc logic:** $\text{Cọc hủy (1.8tr)} < \text{Xe chạy rỗng (2.7tr)} < \text{Thiếu xe (6.0tr)}$.  
Đúng chuẩn kinh tế: *Hủy trước luôn tiết kiệm tiền hơn để xe chạy rỗng!*

---

## 4. 4 KỊCH BẢN VẬN HÀNH THỰC TẾ TRÊN NỀN TẢNG FROSTLINK

Để trình bày với nhóm và ban giám khảo, bạn sử dụng 4 kịch bản sau:

### Kịch bản 1: Ngày bình thường (Normal Day - Đúng dự báo)
* AI dự báo cần 4 cont $\rightarrow$ Tự động phân bổ: 3 cont Lớp 1 (giá cố định 9tr), 1 cont Lớp 2 (cọc 20%), 0 cont Lớp 3.
* Thực tế thu hoạch đúng 4 cont $\rightarrow$ Cả 4 cont chạy đủ hàng, cước rẻ, không thừa không thiếu.

### Kịch bản 2: Ngày mưa bão bất ngờ (Rainy Day - Kích hoạt bảo hiểm thời tiết)
* Dự báo cần 4 cont (3 cont Lớp 1 + 1 cont Lớp 2).
* Trước 24h, API thời tiết báo mưa to bão gió ($Rain > 20\text{mm}$) $\rightarrow$ Nông dân giảm hái, chỉ cắt lượng tối thiểu để trả đơn hợp đồng (thực tế chỉ cần 3 cont).
* **Hệ thống FrostLink tự động gửi lệnh HỦY SLOT LỚP 2**. HTX chỉ mất 1.8 triệu tiền cọc.
* **Kết quả:** 3 cont Lớp 1 vẫn chở đầy hàng. **Không bị chiếc xe nào chạy rỗng**, tránh được việc phải đền 2.7 triệu / xe chạy rỗng.

### Kịch bản 3: Ngày nắng rộ / Đơn hàng tăng vọt (Peak Day - Vượt dự báo)
* Thời tiết nắng nóng $38^\circ\text{C}$, vải chín rực, đơn xuất khẩu tăng gấp $\rightarrow$ Nhu cầu thực tế vọt lên 6 cont.
* 3 cont Lớp 1 + 1 cont Lớp 2 chạy hết công suất.
* **2 cont thiếu hụt:** Hệ thống tự động kích hoạt **Lớp 3 (Giao ngay - Spot Pool)**, quét xe chạy rỗng chiều về hoặc xe trống khung giờ từ mạng lưới đối tác của Treviet bù vào ngay trong ngày. Không có quả vải nào bị hỏng.

### Kịch bản 4: HTX cảm tính không nghe khuyến nghị AI (Human Bias Override - Ý tưởng của Khánh Ly)
* App cảnh báo mưa to và đề xuất chỉ đặt 3 cont.
* HTX không nghe, vẫn nghĩ mình hái kịp nên tự ý đặt thêm cont thứ 4.
* Mưa ập xuống, không đủ hàng bốc lên $\rightarrow$ Cont thứ 4 phải quay đầu chạy rỗng về bãi.
* HTX phải móc tiền túi đền **2.700.000 VNĐ** tiền xe chạy rỗng.  
$\Rightarrow$ *Đây là minh chứng rõ nhất vì sao phải có FrostLink để triệt tiêu thiên kiến cảm tính!*

---

## 5. KẾT QUẢ ĐỐI CHUẨN MÔ HÌNH VÀ BỘ SỐ LIỆU ĐỊNH LƯỢNG

### 5.1. Bảng so sánh giữa Baseline và FrostLink (Dòng 35-42 trong Excel)

| Chỉ số KPI | Mô hình nền (Baseline HTX) | Mô hình FrostLink (Đề xuất) | Mức cải thiện | Ý nghĩa kinh tế |
| :--- | :---: | :---: | :---: | :--- |
| **Truck MAE (Sai số số xe)** | **0.83 xe/ngày** | **0.26 xe/ngày** | **Giảm 68.7%** | Sai số chỉ còn lệch 1/4 cont mỗi ngày. |
| **Truck WAPE (Sai số % có trọng số)** | **25.09%** | **7.87%** | **Giảm 68.7%** | Chuẩn sai số logistics đẳng cấp quốc tế (<10%). |
| **Sản lượng MAE** | 14.23 Tấn/ngày | 4.46 Tấn/ngày | Giảm 68.7% | Dự báo sát thực tế thu hoạch. |
| **Tổng chi phí thừa xe ($C_{over}$)** | 29.700.000 VNĐ | 24.300.000 VNĐ | Giảm 5.400.000 VNĐ | Giảm tối đa xe chạy rỗng. |
| **Tổng chi phí thiếu xe ($C_{under}$)** | 68.000.000 VNĐ | **0 VNĐ** | **Giảm 100%** | Nhờ Lớp 3 bù xe, không bao giờ bị thiếu xe làm hỏng vải. |
| **Chi phí phạt cọc Lớp 2** | 0 VNĐ | 3.600.000 VNĐ | +(3.6 triệu) | Chi phí bảo hiểm rủi ro thời tiết (2 ngày mưa). |
| **TỔNG CHI PHÍ RỦI RO CHUỖI LẠNH** | **97.700.000 VNĐ** | **27.900.000 VNĐ** | **TIẾT KIỆM 69.800.000 VNĐ (GIẢM 71.4%)** | Giúp cụm HTX tiết kiệm gần 70 triệu đồng trong 1 tháng! |

### 5.2. Phương trình hồi quy kinh tế lượng OLS
$$\hat{Y}_t = 258.76 - 6.64 \cdot \text{Temp}_t + 0.08 \cdot \text{Rain}_t - 45.15 \cdot \text{Ripe\_pct}_t + 1.00 \cdot \text{Order\_ton}_t + 8.72 \cdot \text{PeakDay}_t$$

* $R^2 = 0.616$ (Giải thích được hơn 61.6% biến động sản lượng hàng ngày).
* Cứ thêm 1 tấn đơn hàng chốt trước, hệ thống kích hoạt thu hoạch thêm đúng **1.0 tấn** vải ($\beta = +0.996$).
* Ngày cao điểm cuối tuần thúc đẩy tăng thêm **8.72 tấn** để kịp lịch thông quan cửa khẩu.

---

## 6. DANH MỤC CÁC FILE ĐÃ TẠO VÀ SẴN SÀNG BÀN GIAO

1. **File Excel chuẩn hóa:** [`FrostLink_Du_lieu_Chuan.xlsx`](file:///e:/_FPT_UNI_/Ki_4/jup/FrostLink_Du_lieu_Chuan.xlsx) (Toàn bộ công thức chuẩn, không lỗi `#REF`, bảng KPI tự động).
2. **File CSV tính sẵn:** [`FrostLink_Data_Evaluated.csv`](file:///e:/_FPT_UNI_/Ki_4/jup/FrostLink_Data_Evaluated.csv).
3. **Script AI Pipeline:** [`pipeline_frostlink_ai.py`](file:///e:/_FPT_UNI_/Ki_4/jup/pipeline_frostlink_ai.py).
4. **Bộ 4 biểu đồ 300 DPI xuất sắc:**
   * [`eda_01_weather_yield_impact.png`](file:///e:/_FPT_UNI_/Ki_4/jup/eda_01_weather_yield_impact.png)
   * [`eda_02_three_tier_dispatch.png`](file:///e:/_FPT_UNI_/Ki_4/jup/eda_02_three_tier_dispatch.png)
   * [`eda_03_forecast_benchmark.png`](file:///e:/_FPT_UNI_/Ki_4/jup/eda_03_forecast_benchmark.png)
   * [`eda_04_economic_risk_cost.png`](file:///e:/_FPT_UNI_/Ki_4/jup/eda_04_economic_risk_cost.png)
5. **Báo cáo Word tổng quan hoàn chỉnh:** `Bao_cao_tong_quan_mo_hinh_FrostLink_5.1.docx`.
