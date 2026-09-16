# TỔNG KẾT TOÀN DIỆN CÔNG VIỆC ĐÃ HOÀN THÀNH (AI & LOGISTICS MODEL 5.1)
**Đề án: FrostLink – Nền tảng điều phối công suất chuỗi lạnh mùa vụ (Lục Ngạn, Bắc Giang)**  
*Tác giả / Báo cáo: Đặng Cường - Thành viên k chính thức (Buổi họp nhóm 10h tối)*

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
2. **Nguồn gốc dữ liệu & Đội xe hỗn hợp (Mixed Fleet):**
   - **Container lạnh 40 feet (Cont 40ft - 40RF):** Tải trọng danh định 18T, tải trọng hữu dụng thực tế $C_{\text{eff, 40}} = 18 \times 0.96 = 17.28\text{ tấn/cont}$ (chừa 4% dung tích khí lạnh tuần hoàn). Toàn vụ phát sinh 1.308 chuyến cont 40ft chở các lô xuất khẩu chính ngạch lớn.
   - **Xe tải lạnh 5 tấn (Xe 5T):** Tải trọng danh định 5T, tải trọng hữu dụng thực tế $C_{\text{eff, 5}} = 5 \times 0.96 = 4.80\text{ tấn/xe}$ (cước 3.5 triệu/chuyến thay vì 9.0 triệu/chuyến của Cont 40ft). Toàn vụ điều động 219 chuyến xe 5T gom sạch vải dư lẻ (LTL).
   - Tổng cộng: **1.527 chuyến xe lạnh** thực tế toàn vụ ($28.742,2\text{ tấn}$ thu hoạch, $23.415,8\text{ tấn}$ đi chuỗi lạnh).
   - Giá cước: Cont 40ft (9M thường / 11.7M cao điểm), Xe 5T (3.5M thường / 4.55M cao điểm).

---

## 3. BỘ THAM SỐ TÀI CHÍNH ĐÃ CHUẨN HÓA THEO BIÊN BẢN PHỎNG VẤN

Nhóm đã giải quyết triệt để bài toán kinh tế với bộ tham số chuẩn từ nhà xe Treviet:

| Hạng mục chi phí | Tỷ lệ quy định | Số tiền đưa vào mô hình | Căn cứ nghiệp vụ giải trình |
| :--- | :---: | :---: | :--- |
| **1. Cọc giữ chỗ Lớp 2 (Hủy trước 24h)** | **20% giá cước** | **1.800.000 - 2.340.000 VNĐ** | Báo hủy trước 24h khi có bão mưa $> 20\text{mm}$, xe **chưa lăn bánh đến bãi**, mất cọc 20% bảo hiểm. |
| **2. Phạt xe chạy rỗng ($C_{over}$)** | **30% giá cước** | **2.700.000 VNĐ / cont** | Xe **đã lăn bánh đến bãi** nhưng không có hàng bốc lên $\rightarrow$ Xe chạy rỗng về bãi. Bồi thường tiền dầu. |
| **3. Thiệt hại thiếu xe ($C_{under}$)** | **Cước ép + Vải mất giá** | **6.000.000 VNĐ / cont** | Gồm: 2.7 triệu (bị ép cước cao điểm +30%) + 3.3 triệu (tiền vải chờ xe mất 25% giá trị xuất khẩu). |

👉 **Thang bậc logic:** $\text{Cọc hủy (1.8tr - 2.34tr)} < \text{Xe chạy rỗng (2.7tr) + Vải thâm hỏng} \; (>8.7\text{tr})$.  
Đúng chuẩn kinh tế: *Chủ động hủy slot bảo hiểm rủi ro thời tiết luôn tiết kiệm tiền hơn để xe chạy rỗng và hàng bị đọng!*

---

## 4. 4 KỊCH BẢN VẬN HÀNH THỰC TẾ TRÊN NỀN TẢNG FROSTLINK

Để trình bày với nhóm và ban giám khảo, bạn sử dụng 4 kịch bản sau:

### Kịch bản 1: Ngày bình thường (Normal Day - Đúng dự báo)
* AI dự báo cần 4 cont và 1 xe 5T $\rightarrow$ Tự động phân bổ: 3 cont Lớp 1 (giá cố định 9tr), 1 cont Lớp 2 (cọc 20%), 1 xe 5T gom hàng lẻ.
* Thực tế thu hoạch đúng kế hoạch $\rightarrow$ Xe chạy đủ hàng, cước rẻ, không thừa không thiếu.

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

### 5.1. Bảng so sánh giữa Baseline và FrostLink toàn vụ 92 ngày (Dòng 96-104 trong Excel)

| Chỉ số KPI | Mô hình nền (Baseline HTX) | Mô hình FrostLink (Đề xuất) | Mức cải thiện | Ý nghĩa kinh tế |
| :--- | :---: | :---: | :---: | :--- |
| **Truck MAE (Sai số số xe)** | **3.78 xe/ngày** | **1.11 xe/ngày** | **Giảm 70.6%** | Sai số chỉ còn lệch 1 cont mỗi ngày. |
| **Truck WAPE (Sai số % có trọng số)** | **25.80%** | **7.59%** | **Giảm 70.6%** | Chuẩn sai số logistics quốc tế (<8%). |
| **Sản lượng MAE** | 65.37 Tấn/ngày | 19.18 Tấn/ngày | Giảm 70.6% | Dự báo sát thực tế thu hoạch từng ngày. |
| **Tổng chi phí thừa xe ($C_{over}$)** | 455.400.000 VNĐ | 283.500.000 VNĐ | Giảm 171.900.000 VNĐ (37.7%) | Giảm tối đa xe chạy rỗng. |
| **Tổng chi phí thiếu xe ($C_{under}$)** | 1.008.000.000 VNĐ | **0 VNĐ** | **Giảm 100%** | Nhờ Lớp 3 bù xe, triệt tiêu 100% rủi ro thiếu xe làm hỏng vải. |
| **Chi phí phạt cọc Lớp 2** | 0 VNĐ | 57.420.000 VNĐ | +(57.42 triệu) | Chi phí bảo hiểm rủi ro thời tiết (cọc 20% cho các ngày bão mưa > 20mm). |
| **TỔNG CHI PHÍ RỦI RO CHUỖI LẠNH** | **1.463.400.000 VNĐ** | **340.920.000 VNĐ** | **TIẾT KIỆM 1.122.480.000 VNĐ (GIẢM 76.7%)** | Cắt giảm hơn 1.12 tỷ đồng tổn thất cho toàn liên minh! |

### 5.2. Phương trình hồi quy kinh tế lượng OLS (92 ngày)
$$\hat{Y}_t = -85.32 + 4.16 \cdot \text{Temp}_t - 4.42 \cdot \text{Rain}_t + 15.12 \cdot \text{Ripe\_pct}_t + 0.89 \cdot \text{Order\_ton}_t - 12.16 \cdot \text{PeakDay}_t$$

* $R^2 = 0.929$ (Giải thích được 92.9% biến động sản lượng hàng ngày).
* Cứ thêm 1 tấn đơn hàng chốt trước, hệ thống kích hoạt thu hoạch thêm **0.89 tấn** vải ($\beta = +0.893$).
* Mỗi độ C nhiệt độ tăng thúc đẩy sản lượng thu hoạch tăng **4.16 tấn** do vải chín nhanh.
* Mỗi mm mưa làm giảm sản lượng thu hoạch **4.42 tấn** do nông dân tạm dừng bẻ cành khi trời mưa.

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
