# FrostLink AI Engine: Short-Term Cold Chain Demand Forecasting & 3-Tier Capacity Reservation

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![XGBoost](https://img.shields.io/badge/Model-XGBoost%20%7C%20Random%20Forest-orange.svg)](https://xgboost.readthedocs.io/)
[![Competition](https://img.shields.io/badge/VYLT-2026-green.svg)](https://vietnamyounglogisticstalents.vn/)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

> **Đề án:** FrostLink – Nền tảng điều phối công suất chuỗi lạnh mùa vụ (Lục Ngạn, Bắc Giang)  
> **Hạng mục:** Mô-đun 5.1 – Dự báo nhu cầu ngắn hạn và Đặt trước công suất vận tải lạnh 3 lớp  
> **Cuộc thi:** Vietnam Young Logistics Talents (VYLT) 2026  
> **Tác giả:** Đặng Cường THÀNH VIÊN K CHÍNH THỨC

---

## 📌 1. Giới thiệu Đề tài (Project Overview)

Mùa vụ thu hoạch vải thiều tại huyện Lục Ngạn (Bắc Giang) diễn ra tập trung trong vỏn vẹn 3–4 tuần (tháng 6), đòi hỏi quy chuẩn chuỗi lạnh nghiêm ngặt ($2^\circ\text{C} - 4^\circ\text{C}$) để xuất khẩu sang Trung Quốc qua các cửa khẩu Lạng Sơn (Hữu Nghị, Chi Ma, Tân Thanh).

Hệ thống logistics truyền thống hiện nay gặp thất bại thị trường nghiêm trọng do **tính bị động (gọi xe gấp khi đã bẻ cành)**:
- **Ngày nắng rộ:** Cháy xe, cước chợ đen bị đẩy tăng 30%–50%, thiếu xe khiến quả vải phơi nắng mất 25%–40% giá trị.
- **Ngày mưa to ($Rain \ge 50\text{mm}$):** Nông dân ngừng thu hoạch đột ngột, xe lạnh đã đặt chạy rỗng đến bãi nằm chờ, HTX chịu tiền phạt rỗng.

**FrostLink AI Engine** giải quyết triệt để bài toán này bằng cách:
1. **Dự báo nhu cầu ngắn hạn (1, 3, 7 ngày):** Kết hợp các mô hình Machine Learning phi tuyến (**Random Forest** và **XGBoost**) với dữ liệu thời tiết ngoại sinh và đơn hàng xuất khẩu.
2. **Quy đổi tác nghiệp sang Container lạnh 40 feet (40RF):** Dựa trên tải trọng hữu dụng thực tế $C_{\text{eff}} = 17.2\text{ tấn/cont}$ (860 thùng xốp ướp đá).
3. **Cơ chế Đặt xe 3 Lớp (3-Tier Capacity Booking):** Tự động phân bổ $70\%$ Cam kết cứng (Lớp 1), $20\%$ Quyền chọn linh hoạt (Lớp 2 có cọc), và $10\%$ Giao ngay (Lớp 3), tích hợp tính năng **hủy slot Lớp 2 trước 24h khi có bão**.

---

## 📊 2. Kết quả Đối chuẩn Mô hình (Model Benchmark)

Thử nghiệm đối chuẩn trên tập dữ liệu 30 ngày chính vụ Lục Ngạn ($1.647\text{ tấn}$ vải, $93\text{ chuyến}$ Container 40RF):

| Mô hình | MAE Sản lượng (Tấn) | Truck MAE (Xe/ngày) | Truck WAPE (%) | $R^2$ Score | Đánh giá & Vai trò trong đề án |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Baseline (Trung bình 3 ngày)** | 14.23 Tấn | 0.83 Xe/ngày | 25.09% | — | Phương thức thủ công hiện tại của HTX (bị trễ pha khi mưa bão). |
| **Hồi quy Đa biến (OLS Econometrics)** | 12.17 Tấn | 0.60 Xe/ngày | 19.35% | 0.616 | **Mô hình giải thích (Explainable):** Phân tích hệ số tác động biên ($\beta$) cho Giám khảo kinh tế. |
| **Random Forest (Cây quyết định)** | 10.40 Tấn | 0.53 Xe/ngày | 17.20% | 0.754 | Học máy phi tuyến, bền bỉ, chống nhiễu phương sai tốt. |
| **XGBoost (Gradient Boosting)** | **3.98 Tấn** | **0.30 Xe/ngày** | **9.68%** | **0.960** | **Mô hình tối ưu:** Đưa WAPE xuống $<10\%$ (chuẩn khắt khe logistics quốc tế). |
| **FrostLink (Tích hợp Cơ chế 3 Lớp)** | **—** | **0.26 Xe/ngày** | **7.87%** | **—** | **Quy đổi tác nghiệp:** Tiết kiệm **71.4% chi phí rủi ro** vụ mùa. |

### 💰 Lượng hóa Kinh tế theo Bài toán Newsvendor:
- **Chi phí phạt xe rỗng ($C_{\text{over}}$):** Giảm từ $29.7\text{ triệu}$ xuống $24.3\text{ triệu VNĐ}$.
- **Thiệt hại thiếu xe ($C_{\text{under}}$):** Giảm từ $68.0\text{ triệu}$ xuống **$0\text{ VNĐ}$ (Triệt tiêu hoàn toàn 100%)**.
- **Phí hủy cọc bảo hiểm Lớp 2:** $3.6\text{ triệu VNĐ}$ (cho 2 ngày bão lớn $Rain \ge 50\text{mm}$).
- **TỔNG CHI PHÍ RỦI RO:** Giảm từ **$97.7\text{ triệu}$ xuống $27.9\text{ triệu VNĐ}$**, **tiết kiệm $69.8\text{ triệu VNĐ (71.4%)}$**.

---

## 📁 3. Cấu trúc Thư mục Repository (Directory Structure)

```text
frostlink-ai/
├── data/                                 # Dữ liệu phục vụ mô hình
│   ├── FrostLink_Du_lieu_Chuan.xlsx      # Dữ liệu chuẩn hóa 30 ngày có công thức Excel
│   ├── FrostLink_Data_Evaluated.csv      # File CSV trung gian phục vụ huấn luyện
│   └── raw/                              # Dữ liệu khảo sát thực địa ban đầu
├── src/                                  # Mã nguồn chương trình
│   ├── pipeline_frostlink_ai.py          # Pipeline huấn luyện RF, XGBoost & xuất 4 EDA
│   ├── generate_final_report_docx.py     # Script xuất báo cáo Word với công thức OMML
│   └── sync_and_evaluate_excel.py        # Script tính toán KPI Newsvendor
├── figures/                              # Bộ biểu đồ trực quan hóa độ nét cao (300 DPI)
│   ├── eda_01_weather_yield_impact.png   # Tương quan thời tiết - sản lượng (2 đợt bão)
│   ├── eda_02_three_tier_dispatch.png    # Cơ chế điều phối công suất 3 lớp
│   ├── eda_03_forecast_benchmark.png     # Đối chuẩn đường dự báo số xe
│   ├── eda_04_economic_risk_cost.png     # Đối chuẩn tổn thất chi phí Newsvendor
│   └── so_do_kien_truc_5.1.png           # Sơ đồ kiến trúc 4 tầng giải pháp
├── docs/                                 # Tài liệu giải trình & báo cáo đề án
│   ├── giai_thich_mo_hinh_rf_xgboost.md  # Cẩm nang chuyên sâu giải thích RF & XGBoost
│   ├── Bao_cao_tong_quan_mo_hinh_FrostLink_5.1.docx # Báo cáo Word hoàn chỉnh chuẩn nộp
│   ├── ke_hoach_nhung_gi_da_lam.md       # Báo cáo tóm tắt & kịch bản vận hành thực tế
│   ├── ket_qua_mo_hinh_frostlink.md      # Kết quả định lượng chi tiết
│   ├── latex.txt                         # Toàn bộ mã nguồn công thức LaTeX
│   └── De_xuat_chi_tiet_de_tai_FROSTLINK.docx # Bản đề xuất chi tiết hoàn chỉnh
├── .gitignore                            # Bỏ qua file rác, file tạm Office (~$*.xlsx)
├── requirements.txt                      # Danh sách thư viện phụ thuộc
└── README.md                             # Hướng dẫn tổng quan dự án
```

---

## 🚀 4. Hướng dẫn Cài đặt & Chạy (Quick Start)

### Yêu cầu môi trường:
- Python 3.10 trở lên
- Git

### Các bước thực hiện:
```bash
# 1. Clone repository
git clone https://github.com/<your-username>/frostlink-ai.git
cd frostlink-ai

# 2. Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# 3. Chạy pipeline huấn luyện mô hình và xuất biểu đồ EDA
python src/pipeline_frostlink_ai.py

# 4. Tạo báo cáo Word chuẩn Native OMML
python src/generate_final_report_docx.py
```

---

## 🧠 5. Công nghệ & Thư viện Sử dụng (Tech Stack)

- **Machine Learning:** `scikit-learn` (RandomForestRegressor), `xgboost` (XGBRegressor).
- **Data Manipulation:** `pandas`, `numpy`, `openpyxl`.
- **Visualization:** `matplotlib` (Publication-grade 300 DPI, Segoe UI Vietnamese font).
- **Document Processing:** `python-docx`, `lxml` (Office Math Markup Language - OMML native equations).

---

## 📜 6. Giấy phép (License)
Dự án được phát triển phục vụ cuộc thi Vietnam Young Logistics Talents 2026. Bản quyền thuộc về Đội thi FrostLink.
