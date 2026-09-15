# -*- coding: utf-8 -*-
"""
TẠO BÁO CÁO TỔNG QUAN HOÀN CHỈNH VỚI ĐỊNH DẠNG TOÁN HỌC NATIVE WORD OMML
Đề án: FrostLink - Nền tảng điều phối công suất chuỗi lạnh mùa vụ (Lục Ngạn)
Cuộc thi: Vietnam Young Logistics Talents (VYLT) 2026
"""

import sys, io
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

doc = docx.Document()

# Thiết lập lề trang chuẩn A4 (2.0 cm)
for section in doc.sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.9)
    section.right_margin = Inches(0.9)

# Màu sắc chủ đạo (Corporate Navy & Frost Blue)
COLOR_PRIMARY = RGBColor(21, 101, 192)   # Xanh dương đậm
COLOR_DARK = RGBColor(33, 33, 33)        # Đen xám than
COLOR_MUTED = RGBColor(117, 117, 117)    # Xám phụ
COLOR_ACCENT = RGBColor(211, 47, 47)     # Đỏ cảnh báo

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def add_omml_math(paragraph, omml_inner):
    """Thêm công thức toán học chuẩn Native Word OMML (như gõ Alt+= trong Word)"""
    omml_xml = (
        f'<m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
        f'<m:oMath>{omml_inner}</m:oMath>'
        f'</m:oMathPara>'
    )
    paragraph._p.append(parse_xml(omml_xml))

def add_heading_1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Segoe UI'
    run.font.size = Pt(14.5)
    run.font.bold = True
    run.font.color.rgb = COLOR_PRIMARY
    return p

def add_heading_2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Segoe UI'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGBColor(13, 71, 161)
    return p

def add_paragraph(text, bold_prefix="", italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Segoe UI'
        r_pre.font.size = Pt(10.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_DARK
    r_body = p.add_run(text)
    r_body.font.name = 'Segoe UI'
    r_body.font.size = Pt(10.5)
    r_body.font.italic = italic
    r_body.font.color.rgb = COLOR_DARK
    return p

def add_callout(text, title="ĐIỂM MẤU CHỐT:"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "E3F2FD") # Light blue
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    cell.width = Inches(6.7)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    r_t = p.add_run(title + " ")
    r_t.font.name = 'Segoe UI'
    r_t.font.size = Pt(10.5)
    r_t.font.bold = True
    r_t.font.color.rgb = COLOR_PRIMARY
    
    r_c = p.add_run(text)
    r_c.font.name = 'Segoe UI'
    r_c.font.size = Pt(10)
    r_c.font.color.rgb = COLOR_DARK
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

# ==============================================================================
# TRANG BÌA / HEADER TIÊU ĐỀ
# ==============================================================================
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_before = Pt(10)
p_title.paragraph_format.space_after = Pt(4)
r_t1 = p_title.add_run("BÁO CÁO KẾT QUẢ ĐẶC TẢ VÀ THỰC NGHIỆM MÔ HÌNH (MỤC 5.1)\n")
r_t1.font.name = 'Segoe UI'
r_t1.font.size = Pt(17)
r_t1.font.bold = True
r_t1.font.color.rgb = COLOR_PRIMARY

r_t2 = p_title.add_run("HỆ THỐNG DỰ BÁO NGẮN HẠN VÀ ĐẶT TRƯỚC CÔNG SUẤT VẬN TẢI LẠNH 3 LỚP\n")
r_t2.font.name = 'Segoe UI'
r_t2.font.size = Pt(12.5)
r_t2.font.bold = True
r_t2.font.color.rgb = RGBColor(38, 50, 56)

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_after = Pt(16)
r_sub = p_sub.add_run("Đề án: FrostLink – Nền tảng điều phối chuỗi lạnh nông sản mùa vụ (Lục Ngạn)\nCuộc thi: Vietnam Young Logistics Talents (VYLT) 2026")
r_sub.font.name = 'Segoe UI'
r_sub.font.size = Pt(10)
r_sub.font.italic = True
r_sub.font.color.rgb = COLOR_MUTED

add_callout(
    "Báo cáo này giải trình toàn diện phương pháp luận định lượng, bằng chứng khảo sát thực tế (nhà xe Treviet, container 40ft), "
    "công thức toán học chuẩn Native Word OMML, kết quả đối chuẩn giữa mô hình nền Baseline và FrostLink, cùng bộ 4 biểu đồ 300 DPI.",
    title="TÓM TẮT ĐIỀU HÀNH (EXECUTIVE SUMMARY):"
)

# ==============================================================================
# PHẦN 1: BẰNG CHỨNG THỰC ĐỊA & CƠ SỞ DỮ LIỆU PHỎNG VẤN
# ==============================================================================
add_heading_1("1. BẰNG CHỨNG THỰC ĐỊA & NGUỒN GỐC SỐ LIỆU PHỎNG VẤN")
add_paragraph("Để khắc phục triệt để nhận xét của Giám khảo về việc 'đề án thiếu dữ liệu thực tế và phạm vi quá rộng', nhóm đã phỏng vấn sâu doanh nghiệp thu mua đầu mối và đơn vị vận chuyển tại Lục Ngạn. Toàn bộ tham số trong mô hình được neo 100% vào số liệu thực địa:")

# Bảng khảo sát
tbl_survey = doc.add_table(rows=6, cols=3)
tbl_survey.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_survey.autofit = False

survey_data = [
    ["Hạng mục khảo sát", "Kết quả phỏng vấn thực tế", "Quy chuẩn đưa vào Mô hình FrostLink"],
    ["Đối tác & Tuyến vận tải", "Cty Vận tải & Du lịch Treviet; chạy tuyến Lục Ngạn đi Cửa khẩu Hữu Nghị, Chi Ma, Hà Khẩu (Lạng Sơn).", "Mô phỏng chính xác tuyến gom hàng Lục Ngạn ra cửa khẩu xuất khẩu (150 km)."],
    ["Phương tiện & Tải trọng", "Container lạnh 40 feet (Cont 40ft - 40RF). Đóng thực tế khoảng 18 tấn vải do thùng xốp chèn đá.", "Định mức tải trọng hữu dụng: C_eff = 17.2 Tấn/cont (trừ 4.5% dung tích tuần hoàn khí lạnh)."],
    ["Giá cước vận tải", "Ngày thường 9.000.000 VNĐ/chuyến; ngày cao điểm cháy xe giá bị đẩy tăng 30%.", "Giá thường: 9.000.000 VNĐ; Giá cao điểm (Temp >= 34°C hoặc cuối tuần): 11.700.000 VNĐ."],
    ["Tỷ lệ cọc & Hủy chuyến", "Đặt trước phải cọc từ 20% - 40% giá cước. Nếu xe đến bãi mà không có hàng thì phạt tiền chạy rỗng.", "Cọc hủy trước 24h (Lớp 2): 20% (1.8 triệu); Phạt xe rỗng tại bãi (C_over): 30% cước (2.7 triệu)."],
    ["Tần suất thiếu xe", "Khoảng 50% thời gian cao điểm gặp khó khăn trong tìm xe do phụ thuộc kích thước thùng.", "FrostLink thiết lập Lớp 3 (Spot buffer) bù xe giao ngay, giải quyết triệt để tình trạng thiếu xe."]
]

for r_idx, row in enumerate(survey_data):
    for c_idx, val in enumerate(row):
        cell = tbl_survey.cell(r_idx, c_idx)
        cell.text = val
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(2)
        if r_idx == 0:
            set_cell_background(cell, "1565C0")
            p.runs[0].font.name = 'Segoe UI'
            p.runs[0].font.bold = True
            p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
            p.runs[0].font.size = Pt(9.5)
        else:
            set_cell_background(cell, "F5F5F5" if r_idx % 2 == 1 else "FFFFFF")
            p.runs[0].font.name = 'Segoe UI'
            p.runs[0].font.size = Pt(9)
            p.runs[0].font.color.rgb = COLOR_DARK
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)

tbl_survey.columns[0].width = Inches(1.8)
tbl_survey.columns[1].width = Inches(2.7)
tbl_survey.columns[2].width = Inches(2.2)

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# ==============================================================================
# PHẦN 2: CƠ CHẾ TOÁN HỌC & CÔNG THỨC CHUYỂN ĐỔI TÁC NGHIỆP
# ==============================================================================
add_heading_1("2. CƠ CHẾ TOÁN HỌC & CÔNG THỨC CHUYỂN ĐỔI TÁC NGHIỆP")

add_heading_2("2.1. Hàm Kinh tế lượng Dự báo Sản lượng thu hoạch (Y_t)")
add_paragraph("Phương pháp tiếp cận dựa trên mô hình hồi quy kinh tế lượng đa biến có thể giải thích được hệ số tác động biên (Marginal Effects):")

# Công thức OLS lý thuyết OMML
omml_ols_theory = (
    '<m:sSub><m:e><m:acc><m:accPr><m:chr m:val="^"/></m:accPr><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>Y</m:t></m:r></m:e></m:acc></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t> = </m:t></m:r>'
    '<m:sSub><m:e><m:r><m:t>β</m:t></m:r></m:e><m:sub><m:r><m:t>0</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t> + </m:t></m:r>'
    '<m:sSub><m:e><m:r><m:t>β</m:t></m:r></m:e><m:sub><m:r><m:t>1</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t>·</m:t></m:r><m:sSub><m:e><m:r><m:t>Temp</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t> - </m:t></m:r>'
    '<m:sSub><m:e><m:r><m:t>β</m:t></m:r></m:e><m:sub><m:r><m:t>2</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t>·</m:t></m:r><m:sSub><m:e><m:r><m:t>Rain</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t> + </m:t></m:r>'
    '<m:sSub><m:e><m:r><m:t>β</m:t></m:r></m:e><m:sub><m:r><m:t>3</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t>·</m:t></m:r><m:sSub><m:e><m:r><m:t>Ripe</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t> + </m:t></m:r>'
    '<m:sSub><m:e><m:r><m:t>β</m:t></m:r></m:e><m:sub><m:r><m:t>4</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t>·</m:t></m:r><m:sSub><m:e><m:r><m:t>Order</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t> + </m:t></m:r>'
    '<m:sSub><m:e><m:r><m:t>β</m:t></m:r></m:e><m:sub><m:r><m:t>5</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t>·</m:t></m:r><m:sSub><m:e><m:r><m:t>PeakDay</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t> + </m:t></m:r>'
    '<m:sSub><m:e><m:r><m:t>ε</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub>'
)
p_ols_th = doc.add_paragraph()
p_ols_th.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_ols_th.paragraph_format.space_before = Pt(4)
p_ols_th.paragraph_format.space_after = Pt(6)
add_omml_math(p_ols_th, omml_ols_theory)

add_paragraph("Phương trình Hồi quy OLS thực nghiệm huấn luyện trên bộ dữ liệu vụ mùa:")

# Công thức OLS thực nghiệm OMML
omml_ols_emp = (
    '<m:sSub><m:e><m:acc><m:accPr><m:chr m:val="^"/></m:accPr><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>Y</m:t></m:r></m:e></m:acc></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t> = 258.76 - 6.64·</m:t></m:r><m:sSub><m:e><m:r><m:t>Temp</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t> + 0.08·</m:t></m:r><m:sSub><m:e><m:r><m:t>Rain</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t> - 45.15·</m:t></m:r><m:sSub><m:e><m:r><m:t>Ripe</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t> + 1.00·</m:t></m:r><m:sSub><m:e><m:r><m:t>Order</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t> + 8.72·</m:t></m:r><m:sSub><m:e><m:r><m:t>PeakDay</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t>   (</m:t></m:r><m:sSup><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>R</m:t></m:r></m:e><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSup><m:r><m:t> = 0.616)</m:t></m:r>'
)
p_ols_emp = doc.add_paragraph()
p_ols_emp.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_ols_emp.paragraph_format.space_before = Pt(4)
p_ols_emp.paragraph_format.space_after = Pt(8)
add_omml_math(p_ols_emp, omml_ols_emp)

add_heading_2("2.2. Công thức Quy đổi Tác nghiệp sang Số Cont 40ft (N_t)")
add_paragraph("Sản lượng thu hoạch dự báo được quy đổi thành số lượng phương tiện thực tế theo công thức hàm trần (Ceiling function):")

omml_truck = (
    '<m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>N</m:t></m:r></m:e><m:sub><m:r><m:t>trucks,t</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t> = </m:t></m:r>'
    '<m:d><m:dPr><m:begChr m:val="⌈"/><m:endChr m:val="⌉"/></m:dPr>'
    '<m:e><m:f><m:num>'
    '<m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>Y</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t> × </m:t></m:r>'
    '<m:sSub><m:e><m:r><m:t>α</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub>'
    '</m:num><m:den>'
    '<m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>C</m:t></m:r></m:e><m:sub><m:r><m:t>eff</m:t></m:r></m:sub></m:sSub>'
    '</m:den></m:f></m:e></m:d>'
)
p_truck = doc.add_paragraph()
p_truck.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_truck.paragraph_format.space_before = Pt(4)
p_truck.paragraph_format.space_after = Pt(8)
add_omml_math(p_truck, omml_truck)

add_paragraph(
    "Trong đó: α_t là tỷ lệ hàng tiêu chuẩn xuất khẩu bắt buộc đi chuỗi lạnh (α = 80% - 85%); "
    "C_eff = 17.2 Tấn/cont là tải trọng hữu dụng thực tế của Container 40 feet lạnh (chừa 4.5% dung tích tuần hoàn khí lạnh)."
)

add_heading_2("2.3. Công thức Phân bổ 3 Lớp Công suất (3-Tier Capacity Booking)")
add_paragraph("Thuật toán tự động phân bổ rổ công suất cho từng ngày:")

omml_tiers = (
    '<m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>N</m:t></m:r></m:e><m:sub><m:r><m:t>1,t</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t> = round(</m:t></m:r><m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>N</m:t></m:r></m:e><m:sub><m:r><m:t>pred,t</m:t></m:r></m:sub></m:sSub><m:r><m:t> × 70%),   </m:t></m:r>'
    '<m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>N</m:t></m:r></m:e><m:sub><m:r><m:t>2,t</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t> = min(⌈</m:t></m:r><m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>N</m:t></m:r></m:e><m:sub><m:r><m:t>pred,t</m:t></m:r></m:sub></m:sSub><m:r><m:t> × 20%⌉, max(0, </m:t></m:r><m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>N</m:t></m:r></m:e><m:sub><m:r><m:t>pred,t</m:t></m:r></m:sub></m:sSub><m:r><m:t> - </m:t></m:r><m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>N</m:t></m:r></m:e><m:sub><m:r><m:t>1,t</m:t></m:r></m:sub></m:sSub><m:r><m:t>))</m:t></m:r>'
)
p_tiers = doc.add_paragraph()
p_tiers.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_tiers.paragraph_format.space_before = Pt(4)
p_tiers.paragraph_format.space_after = Pt(8)
add_omml_math(p_tiers, omml_tiers)

# ==============================================================================
# PHẦN 3: BỘ THAM SỐ TÀI CHÍNH & NGUYÊN LÝ NEWSVENDOR
# ==============================================================================
add_heading_1("3. NGUYÊN LÝ QUẢN TRỊ RỦI RO NEWSVENDOR & BỘ THAM SỐ TÀI CHÍNH")
add_paragraph("Mô hình lượng hóa tổn thất dựa trên lý thuyết Bài toán người bán báo (Newsvendor Model):")

omml_cost = (
    '<m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>Total_Cost</m:t></m:r><m:r><m:t> = </m:t></m:r>'
    '<m:nary><m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/></m:naryPr><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r><m:r><m:t>=1</m:t></m:r></m:sub><m:sup><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>n</m:t></m:r></m:sup><m:e>'
    '<m:r><m:t>[</m:t></m:r>'
    '<m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>C</m:t></m:r></m:e><m:sub><m:r><m:t>over</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t>·max(0, </m:t></m:r><m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>U</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub><m:r><m:t> - </m:t></m:r><m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>J</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub><m:r><m:t>) + </m:t></m:r>'
    '<m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>C</m:t></m:r></m:e><m:sub><m:r><m:t>under</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t>·max(0, </m:t></m:r><m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>J</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub><m:r><m:t> - </m:t></m:r><m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>U</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub><m:r><m:t>) + </m:t></m:r>'
    '<m:sSub><m:e><m:r><m:t>Penalty</m:t></m:r></m:e><m:sub><m:r><m:t>L2,t</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t>]</m:t></m:r>'
    '</m:e></m:nary>'
)
p_cost = doc.add_paragraph()
p_cost.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_cost.paragraph_format.space_before = Pt(4)
p_cost.paragraph_format.space_after = Pt(8)
add_omml_math(p_cost, omml_cost)

add_paragraph(
    "• Cọc Lớp 2 (Hủy trước 24h): 1.800.000 VNĐ / cont (Xe chưa lăn bánh đến bãi, nhà xe nhận trọn 20% cọc và nhận chuyến khác).\n"
    "• Chi phí thừa xe chạy rỗng (C_over): 2.700.000 VNĐ / cont (Xe đã đến bãi nhưng không có hàng, bồi thường 30% tiền dầu).\n"
    "• Chi phí thiếu xe (C_under): 6.000.000 VNĐ / cont (Gồm 2.7 triệu cước ép giờ cao điểm + 3.3 triệu do 1 tấn vải chờ xe mất 25% giá trị xuất khẩu).\n"
    "⇒ Nguyên lý kinh tế cốt lõi: Cọc hủy (1.8tr) < Phạt xe rỗng (2.7tr) < Thiếu xe (6.0tr). Cơ chế luôn tạo động lực tiết kiệm chi phí cho HTX.",
    bold_prefix="Thang bậc rủi ro chi phí: "
)

# ==============================================================================
# PHẦN 4: KẾT QUẢ ĐỐI CHUẨN KPI & ĐO LƯỜNG SAI SỐ
# ==============================================================================
add_heading_1("4. KẾT QUẢ ĐỐI CHUẨN ĐỊNH LƯỢNG (BENCHMARK RESULTS)")

# Công thức MAE và WAPE OMML
omml_metrics = (
    '<m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>Truck_MAE</m:t></m:r><m:r><m:t> = </m:t></m:r>'
    '<m:f><m:num><m:r><m:t>1</m:t></m:r></m:num><m:den><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>n</m:t></m:r></m:den></m:f>'
    '<m:nary><m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/></m:naryPr><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r><m:r><m:t>=1</m:t></m:r></m:sub><m:sup><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>n</m:t></m:r></m:sup><m:e>'
    '<m:d><m:dPr><m:begChr m:val="|"/><m:endChr m:val="|"/></m:dPr><m:e>'
    '<m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>N</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub><m:r><m:t> - </m:t></m:r>'
    '<m:sSub><m:e><m:acc><m:accPr><m:chr m:val="^"/></m:accPr><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>N</m:t></m:r></m:e></m:acc></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub>'
    '</m:e></m:d></m:e></m:nary>'
    '<m:r><m:t>       |       </m:t></m:r>'
    '<m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>Truck_WAPE</m:t></m:r><m:r><m:t> = </m:t></m:r>'
    '<m:f><m:num><m:nary><m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/></m:naryPr><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r><m:r><m:t>=1</m:t></m:r></m:sub><m:sup><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>n</m:t></m:r></m:sup><m:e>'
    '<m:d><m:dPr><m:begChr m:val="|"/><m:endChr m:val="|"/></m:dPr><m:e>'
    '<m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>N</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub><m:r><m:t> - </m:t></m:r>'
    '<m:sSub><m:e><m:acc><m:accPr><m:chr m:val="^"/></m:accPr><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>N</m:t></m:r></m:e></m:acc></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub>'
    '</m:e></m:d></m:e></m:nary></m:num>'
    '<m:den><m:nary><m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/></m:naryPr><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r><m:r><m:t>=1</m:t></m:r></m:sub><m:sup><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>n</m:t></m:r></m:sup><m:e>'
    '<m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>N</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub></m:e></m:nary></m:den></m:f>'
    '<m:r><m:t> × 100%</m:t></m:r>'
)
p_metrics = doc.add_paragraph()
p_metrics.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_metrics.paragraph_format.space_before = Pt(4)
p_metrics.paragraph_format.space_after = Pt(8)
add_omml_math(p_metrics, omml_metrics)

# Bảng KPI
tbl_kpi = doc.add_table(rows=8, cols=5)
tbl_kpi.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_kpi.autofit = False

kpi_data = [
    ["Chỉ số KPI Đánh giá", "Mô hình nền (Baseline)", "FrostLink (Đề xuất)", "Mức giảm", "Tỷ lệ cải thiện"],
    ["Sai số số xe trung bình (Truck MAE)", "0.83 Xe/ngày", "0.26 Xe/ngày", "0.57 Xe/ngày", "Giảm 68.7%"],
    ["Sai số phần trăm có trọng số (Truck WAPE)", "25.09%", "7.87%", "17.22%", "Cải thiện 68.7%"],
    ["Sai số sản lượng trung bình (MAE)", "14.23 Tấn/ngày", "4.46 Tấn/ngày", "9.77 Tấn/ngày", "Giảm 68.7%"],
    ["Tổng chi phí thừa xe C_over (VNĐ)", "29.700.000 VNĐ", "24.300.000 VNĐ", "5.400.000 VNĐ", "Giảm 18.2%"],
    ["Tổng chi phí thiếu xe C_under (VNĐ)", "68.000.000 VNĐ", "0 VNĐ", "68.000.000 VNĐ", "Triệt tiêu 100%"],
    ["Chi phí phạt hủy cọc Lớp 2 (VNĐ)", "0 VNĐ", "3.600.000 VNĐ", "+(3.600.000 VNĐ)", "Phí bảo hiểm rủi ro"],
    ["TỔNG CHI PHÍ RỦI RO CHUỖI LẠNH", "97.700.000 VNĐ", "27.900.000 VNĐ", "69.800.000 VNĐ", "TIẾT KIỆM 71.4%"]
]

for r_idx, row in enumerate(kpi_data):
    for c_idx, val in enumerate(row):
        cell = tbl_kpi.cell(r_idx, c_idx)
        cell.text = val
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(2)
        if r_idx == 0:
            set_cell_background(cell, "1565C0")
            p.runs[0].font.name = 'Segoe UI'
            p.runs[0].font.bold = True
            p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
            p.runs[0].font.size = Pt(9.5)
        elif r_idx == 7: # Dòng tổng
            set_cell_background(cell, "E8F5E9") # Light green
            p.runs[0].font.name = 'Segoe UI'
            p.runs[0].font.bold = True
            p.runs[0].font.color.rgb = RGBColor(46, 125, 50)
            p.runs[0].font.size = Pt(9.5)
        else:
            set_cell_background(cell, "F5F5F5" if r_idx % 2 == 1 else "FFFFFF")
            p.runs[0].font.name = 'Segoe UI'
            p.runs[0].font.size = Pt(9)
            p.runs[0].font.color.rgb = COLOR_DARK
        set_cell_margins(cell, top=70, bottom=70, left=90, right=90)

tbl_kpi.columns[0].width = Inches(2.4)
tbl_kpi.columns[1].width = Inches(1.3)
tbl_kpi.columns[2].width = Inches(1.3)
tbl_kpi.columns[3].width = Inches(1.0)
tbl_kpi.columns[4].width = Inches(1.0)

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# ==============================================================================
# PHẦN 5: CHÈN BỘ 4 BIỂU ĐỒ TRỰC QUAN HÓA (300 DPI)
# ==============================================================================
add_heading_1("5. BỘ BIỂU ĐỒ TRỰC QUAN HÓA DỮ LIỆU ĐỘ NÉT CAO (300 DPI)")
add_paragraph("Dưới đây là 4 biểu đồ kể chuyện dữ liệu (Storytelling Data Visualization) phục vụ báo cáo và thuyết trình:")

images_info = [
    ("eda_01_weather_yield_impact.png", "Hình 1: Tương quan giữa lượng mưa, nhiệt độ và sản lượng thu hoạch vải thiều (Lục Ngạn)"),
    ("eda_02_three_tier_dispatch.png", "Hình 2: Cơ chế điều phối công suất 3 lớp tự động và tính năng hủy slot Lớp 2 khi có bão"),
    ("eda_03_forecast_benchmark.png", "Hình 3: Đối chuẩn đường dự báo số lượng xe cont giữa Baseline truyền thống và FrostLink"),
    ("eda_04_economic_risk_cost.png", "Hình 4: Lượng hóa giá trị kinh tế theo bài toán Newsvendor (Tiết kiệm 71.4% chi phí rủi ro)")
]

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(CURRENT_DIR) if os.path.basename(CURRENT_DIR) == 'src' else CURRENT_DIR
FIGURES_DIR = os.path.join(REPO_ROOT, "figures")
DOCS_DIR = os.path.join(REPO_ROOT, "docs")

for img_name, caption in images_info:
    img_path = os.path.join(FIGURES_DIR, img_name) if os.path.exists(os.path.join(FIGURES_DIR, img_name)) else img_name
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(6.5))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(12)
        r_cap = p_cap.add_run(caption)
        r_cap.font.name = 'Segoe UI'
        r_cap.font.size = Pt(9.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = COLOR_MUTED

# ==============================================================================
# PHẦN 6: KẾT LUẬN & KHUYẾN NGHỊ VẬN HÀNH
# ==============================================================================
add_heading_1("6. KẾT LUẬN & GIÁ TRỊ THƯƠNG MẠI")
add_paragraph(
    "1. Tính khả thi cao: Mô hình bám sát hoàn toàn hợp đồng thực tế của nhà xe Treviet và tải trọng Cont 40ft (17.2 tấn).\n"
    "2. Hiệu quả tài chính vượt trội: Giúp cụm liên minh HTX tiết kiệm gần 70 triệu đồng trong 1 tháng cao điểm vụ vải, giảm 68.7% sai số điều xe và triệt tiêu hoàn toàn rủi ro thiếu xe làm hư hỏng nông sản xuất khẩu.\n"
    "3. Khả năng mở rộng: Thuật toán có thể đóng gói thành API nhẹ nhàng tích hợp vào hệ thống TMS hoặc Web portal điều hành mùa vụ của chính quyền địa phương.",
    bold_prefix="Khẳng định giá trị của Đề án: "
)

output_path = os.path.join(DOCS_DIR, "Bao_cao_tong_quan_mo_hinh_FrostLink_5.1.docx")
doc.save(output_path)
print(f"[+] ĐÃ TẠO THÀNH CÔNG BÁO CÁO WORD TỔNG QUAN NATIVE OMML: {output_path}")
