# -*- coding: utf-8 -*-
"""
TẠO BÁO CÁO TỔNG QUAN HOÀN CHỈNH VỚI ĐỊNH DẠNG TOÁN HỌC NATIVE WORD OMML (92 NGÀY)
Đề án: FrostLink - Nền tảng điều phối công suất chuỗi lạnh mùa vụ (Lục Ngạn)
Cuộc thi: Vietnam Young Logistics Talents (VYLT) 2026
Tác giả: Đặng Cường - Lead AI Engineer
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

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(CURRENT_DIR) if os.path.basename(CURRENT_DIR) == 'src' else CURRENT_DIR
DOCS_DIR = os.path.join(REPO_ROOT, "docs")
FIGURES_DIR = os.path.join(REPO_ROOT, "figures")

doc = docx.Document()
doc.core_properties.author = "Đặng Cường - Lead AI Engineer"

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

# ==============================================================================
# TRANG TIÊU ĐỀ BÁO CÁO (COVER HEADER)
# ==============================================================================
p_banner = doc.add_paragraph()
p_banner.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p_banner.paragraph_format.space_after = Pt(2)
r_banner = p_banner.add_run("VIETNAM YOUNG LOGISTICS TALENTS (VYLT) 2026")
r_banner.font.name = 'Segoe UI'
r_banner.font.size = Pt(9)
r_banner.font.bold = True
r_banner.font.color.rgb = COLOR_MUTED

p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
p_title.paragraph_format.space_after = Pt(4)
r_title = p_title.add_run("BÁO CÁO KỸ THUẬT & TOÁN HỌC ĐỀ ÁN FROSTLINK (MỤC 5.1)")
r_title.font.name = 'Segoe UI'
r_title.font.size = Pt(18)
r_title.font.bold = True
r_title.font.color.rgb = COLOR_PRIMARY

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.LEFT
p_sub.paragraph_format.space_after = Pt(14)
r_sub = p_sub.add_run("Mô hình Dự báo Nhu cầu Nông sản và Tối ưu hóa Điều phối Đội xe Lạnh Hỗn hợp 3 Lớp (Toàn vụ 92 ngày)")
r_sub.font.name = 'Segoe UI'
r_sub.font.size = Pt(11.5)
r_sub.font.italic = True
r_sub.font.color.rgb = COLOR_MUTED

p_meta = doc.add_paragraph()
p_meta.paragraph_format.space_after = Pt(12)
r_meta = p_meta.add_run("Người thực hiện: Đặng Cường (Lead AI Engineer)  |  Địa bàn khảo sát: Huyện Lục Ngạn, Bắc Giang  |  Phiên bản: 5.1 Final")
r_meta.font.name = 'Segoe UI'
r_meta.font.size = Pt(9.5)
r_meta.font.bold = True
r_meta.font.color.rgb = COLOR_PRIMARY

# Đường kẻ phân cách
p_line = doc.add_paragraph()
p_line.paragraph_format.space_after = Pt(10)
p_line_border = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:space="1" w:color="1565C0"/></w:pBdr>')
p_line._p.get_or_add_pPr().append(p_line_border)

# ==============================================================================
# PHẦN 1: CĂN CỨ THỰC TẾ & THAM SỐ KHẢO SÁT
# ==============================================================================
add_heading_1("1. CĂN CỨ THỰC TIỄN & BỘ THAM SỐ KHẢO SÁT THỰC ĐỊA")
add_paragraph("Để khắc phục triệt để nhận xét của Giám khảo về việc 'đề án thiếu dữ liệu thực tế và phạm vi quá rộng', nhóm đã phỏng vấn sâu doanh nghiệp thu mua đầu mối và đơn vị vận chuyển tại Lục Ngạn. Toàn bộ tham số trong mô hình được neo 100% vào số liệu thực địa:")

tbl_survey = doc.add_table(rows=7, cols=3)
tbl_survey.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_survey.autofit = False

survey_data = [
    ["Hạng mục khảo sát", "Kết quả phỏng vấn thực tế", "Quy chuẩn đưa vào Mô hình FrostLink"],
    ["Sản lượng thu hoạch chính vụ", "Tháng 6 bình quân đạt 600 tấn vải tươi/ngày (Câu 1 PV).", "Tháng 6 bình quân 615.5 Tấn/ngày (dao động 150 - 850T tùy mưa/nắng). Toàn vụ 92 ngày đạt 28,742 Tấn."],
    ["Đối tác & Tuyến vận tải", "Cty Vận tải & Du lịch Treviet; chạy tuyến Lục Ngạn đi Cửa khẩu Hữu Nghị, Chi Ma, Hà Khẩu (Lạng Sơn).", "Mô phỏng chính xác tuyến gom hàng Lục Ngạn ra các cửa khẩu xuất khẩu phía Bắc."],
    ["Phương tiện & Đội xe hỗn hợp", "Cont 40ft (18T danh định) chở lô xuất khẩu chính. Vải dư lẻ (LTL) cần xe tải lạnh nhỏ 5T để giải tỏa gom hàng kịp thời.", "Định mức hữu dụng: Tải trọng danh định × 0.96 (chừa 4% gió lạnh tuần hoàn). Cont 40ft = 17.28T (1,308 chuyến); Xe 5T = 4.80T (219 chuyến gom hàng lẻ)."],
    ["Giá cước vận tải", "Cont 40ft: ngày thường 9.000.000 VNĐ; cao điểm cháy xe tăng 30% = 11.700.000 VNĐ. Xe 5T: thường 3.500.000 VNĐ, cao điểm 4.550.000 VNĐ.", "Áp dụng giá cước phân tầng theo điều kiện thời tiết (Temp >= 34°C) hoặc ngày cao điểm gom hàng (PeakDay = 1)."],
    ["Tỷ lệ cọc & Hủy chuyến", "Đặt trước phải cọc giữ chỗ 20% giá cước. Nếu xe đến bãi mà không có hàng thì bồi thường xe chạy rỗng 30% tiền dầu.", "Cọc giữ chỗ Lớp 2: 20% (1.8tr thường, 2.34tr cao điểm). Phạt rỗng tại bãi (C_over): 30% cước Cont 40ft (2.7 triệu VNĐ)."],
    ["Tần suất thiếu xe", "Khoảng 50% thời điểm cao điểm gặp khó khăn trong tìm xe do phụ thuộc kích thước thùng.", "FrostLink thiết lập Lớp 3 (Spot buffer) bù xe giao ngay, triệt tiêu 100% tình trạng thiếu xe (C_under = 0 VNĐ)."]
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

add_paragraph("Phương trình Hồi quy OLS thực nghiệm huấn luyện trên bộ dữ liệu toàn vụ 92 ngày:")

omml_ols_emp = (
    '<m:sSub><m:e><m:acc><m:accPr><m:chr m:val="^"/></m:accPr><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>Y</m:t></m:r></m:e></m:acc></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t> = -85.32 + 4.16·</m:t></m:r><m:sSub><m:e><m:r><m:t>Temp</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t> - 4.42·</m:t></m:r><m:sSub><m:e><m:r><m:t>Rain</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t> + 15.12·</m:t></m:r><m:sSub><m:e><m:r><m:t>Ripe</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t> + 0.89·</m:t></m:r><m:sSub><m:e><m:r><m:t>Order</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t> - 12.16·</m:t></m:r><m:sSub><m:e><m:r><m:t>PeakDay</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t>   (</m:t></m:r><m:sSup><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>R</m:t></m:r></m:e><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSup><m:r><m:t> = 0.929)</m:t></m:r>'
)
p_ols_emp = doc.add_paragraph()
p_ols_emp.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_ols_emp.paragraph_format.space_before = Pt(4)
p_ols_emp.paragraph_format.space_after = Pt(8)
add_omml_math(p_ols_emp, omml_ols_emp)

add_heading_2("2.2. Quy đổi Tác nghiệp Đội xe Hỗn hợp: Cont 40ft & Xe 5T (C_eff = C_nom × 0.96)")
add_paragraph(
    "Thay vì ép toàn bộ sản lượng vào container 40ft dẫn đến lãng phí diện tích và đội chi phí cước khi chỉ thừa vài tấn vải lẻ, "
    "FrostLink xây dựng cơ chế điều phối đội xe hỗn hợp (Mixed Fleet). Định mức tải trọng hữu dụng tuân thủ tiêu chuẩn kỹ thuật hàng lạnh: "
    "Tải trọng hữu dụng = Tải trọng danh định × 0.96 (chừa 4% dung tích tuần hoàn khí lạnh theo khảo sát Treviet):"
)

# Công thức Cont 40ft và Xe 5T OMML
omml_mixed_fleet = (
    '<m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>N</m:t></m:r></m:e><m:sub><m:r><m:t>cont40,t</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t> = </m:t></m:r>'
    '<m:d><m:dPr><m:begChr m:val="⌊"/><m:endChr m:val="⌋"/></m:dPr>'
    '<m:e><m:f><m:num><m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>Y</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub><m:r><m:t> × </m:t></m:r><m:sSub><m:e><m:r><m:t>α</m:t></m:r></m:e><m:sub><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>t</m:t></m:r></m:sub></m:sSub></m:num>'
    '<m:den><m:r><m:t>18 × 0.96</m:t></m:r></m:den></m:f></m:e></m:d>'
    '<m:r><m:t>       |       </m:t></m:r>'
    '<m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>N</m:t></m:r></m:e><m:sub><m:r><m:t>truck5,t</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t> = </m:t></m:r>'
    '<m:d><m:dPr><m:begChr m:val="⌈"/><m:endChr m:val="⌉"/></m:dPr>'
    '<m:e><m:f><m:num><m:sSub><m:e><m:r><m:rPr><m:sty m:val="i"/></m:rPr><m:t>Y</m:t></m:r></m:e><m:sub><m:r><m:t>rem,t</m:t></m:r></m:sub></m:sSub></m:num>'
    '<m:den><m:r><m:t>5 × 0.96</m:t></m:r></m:den></m:f></m:e></m:d>'
)
p_mixed = doc.add_paragraph()
p_mixed.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_mixed.paragraph_format.space_before = Pt(4)
p_mixed.paragraph_format.space_after = Pt(8)
add_omml_math(p_mixed, omml_mixed_fleet)

add_paragraph(
    "Trong đó:\n"
    "• α_t là tỷ lệ vải đạt tiêu chuẩn xuất khẩu đi chuỗi lạnh (80% ngày thường, 85% ngày cao điểm).\n"
    "• C_eff,40 = 18 × 0.96 = 17.28 Tấn/cont: Tải trọng hữu dụng của Container 40 feet (chứa trọn lô xuất khẩu lớn).\n"
    "• Y_rem,t = (Y_t × α_t) mod 17.28 (Tấn): Lượng vải dư lẻ cuối ngày sau khi đã đóng kín các container 40ft.\n"
    "• C_eff,5 = 5 × 0.96 = 4.80 Tấn/xe: Tải trọng hữu dụng xe tải lạnh 5T (chuyên chở gom vét hàng lẻ LTL với cước phí chỉ 3.5tr so với 9tr của Cont 40ft, tiết kiệm hàng trăm triệu đồng cho HTX)."
)

add_heading_2("2.3. Công thức Phân bổ 3 Lớp Công suất (3-Tier Capacity Booking)")
add_paragraph("Thuật toán tự động phân bổ rổ công suất cho các container 40ft:")

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
    "• Cọc giữ chỗ Lớp 2 (Hủy trước 24h khi có bão mưa > 20mm): 20% giá cước (1.800.000 VNĐ ngày thường, 2.340.000 VNĐ ngày cao điểm).\n"
    "• Chi phí thừa xe chạy rỗng (C_over): 2.700.000 VNĐ / cont (Xe đã đến bãi nhưng không có hàng, bồi thường 30% tiền dầu theo thỏa thuận).\n"
    "• Chi phí thiếu xe (C_under): 6.000.000 VNĐ / cont (Gồm cước ép giờ cao điểm 2.7tr + mất giá quả vải 3.3tr do phơi nắng chờ xe).\n"
    "⇒ Nguyên lý kinh tế cốt lõi: Cọc hủy (1.8tr - 2.34tr) < Phạt xe rỗng + tổn thất thâm vỏ vải (>8.7tr). Cơ chế chủ động hủy slot bảo hiểm rủi ro thời tiết giúp tiết kiệm hàng tỷ đồng cho toàn liên minh HTX.",
    bold_prefix="Thang bậc rủi ro chi phí: "
)

# ==============================================================================
# PHẦN 4: KẾT QUẢ ĐỐI CHUẨN KPI & ĐO LƯỜNG SAI SỐ (TOÀN VỤ 92 NGÀY)
# ==============================================================================
add_heading_1("4. KẾT QUẢ ĐỐI CHUẨN ĐỊNH LƯỢNG TOÀN VỤ (BENCHMARK 92 NGÀY)")

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

tbl_kpi = doc.add_table(rows=8, cols=5)
tbl_kpi.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_kpi.autofit = False

kpi_data = [
    ["Chỉ số KPI Đánh giá", "Mô hình nền (Baseline)", "FrostLink (Đề xuất)", "Mức giảm", "Tỷ lệ cải thiện"],
    ["Sai số số xe trung bình (Truck MAE)", "3.78 Xe/ngày", "1.11 Xe/ngày", "2.67 Xe/ngày", "Giảm 70.6%"],
    ["Sai số phần trăm có trọng số (Truck WAPE)", "25.80%", "7.59%", "18.21%", "Cải thiện 70.6%"],
    ["Sai số sản lượng trung bình (MAE)", "65.37 Tấn/ngày", "19.18 Tấn/ngày", "46.19 Tấn/ngày", "Giảm 70.6%"],
    ["Tổng chi phí thừa xe C_over (VNĐ)", "455.400.000 VNĐ", "283.500.000 VNĐ", "171.900.000 VNĐ", "Giảm 37.7%"],
    ["Tổng chi phí thiếu xe C_under (VNĐ)", "1.008.000.000 VNĐ", "0 VNĐ", "1.008.000.000 VNĐ", "Triệt tiêu 100%"],
    ["Chi phí phạt hủy cọc Lớp 2 (VNĐ)", "0 VNĐ", "57.420.000 VNĐ", "+(57.420.000 VNĐ)", "Phí bảo hiểm rủi ro"],
    ["TỔNG CHI PHÍ RỦI RO CHUỖI LẠNH", "1.463.400.000 VNĐ", "340.920.000 VNĐ", "1.122.480.000 VNĐ", "TIẾT KIỆM 76.7%"]
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
        elif r_idx == 7:
            set_cell_background(cell, "E8F5E9")
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
add_paragraph("Dưới đây là 4 biểu đồ kể chuyện dữ liệu (Storytelling Data Visualization) phục vụ báo cáo và thuyết trình trên toàn vụ 92 ngày:")

images_info = [
    ("eda_01_weather_yield_impact.png", "Hình 1: Tương quan giữa lượng mưa và sản lượng thu hoạch vải thiều qua 3 tháng mùa vụ (Lục Ngạn)"),
    ("eda_02_three_tier_dispatch.png", "Hình 2: Cơ chế điều phối công suất đội xe hỗn hợp (Cont 40ft & Xe 5T) và tính năng hủy slot Lớp 2 khi có bão"),
    ("eda_03_forecast_benchmark.png", "Hình 3: Đối chuẩn đường dự báo số lượng xe cont giữa Baseline truyền thống và FrostLink"),
    ("eda_04_economic_risk_cost.png", "Hình 4: Lượng hóa giá trị kinh tế theo bài toán Newsvendor (Tiết kiệm hơn 1.12 tỷ VNĐ chi phí rủi ro)")
]

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
    "1. Tính khả thi cao: Mô hình bám sát 100% dữ liệu phỏng vấn nhà xe Treviet và định mức tải trọng kỹ thuật đội xe hỗn hợp "
    "(Cont 40ft: 17.28 tấn/cont; Xe 5T: 4.80 tấn/xe), đáp ứng trọn vẹn 1,527 chuyến xe xuất khẩu toàn vụ.\n"
    "2. Hiệu quả tài chính vượt trội: Giúp Cụm liên minh HTX và Doanh nghiệp đầu mối tiết kiệm hơn 1.12 tỷ đồng (76.7%) chi phí rủi ro "
    "trong suốt 3 tháng mùa vụ, giảm 70.6% sai số điều xe và triệt tiêu hoàn toàn tổn thất do cháy xe thiếu phương tiện.\n"
    "3. Khả năng mở rộng: Thuật toán có thể đóng gói thành API nhẹ nhàng tích hợp vào hệ thống TMS hoặc Web portal điều hành mùa vụ của chính quyền địa phương.",
    bold_prefix="Khẳng định giá trị của Đề án: "
)

output_path = os.path.join(DOCS_DIR, "Bao_cao_tong_quan_mo_hinh_FrostLink_5.1.docx")
doc.save(output_path)
root_output_path = os.path.join(REPO_ROOT, "Bao_cao_tong_quan_mo_hinh_FrostLink_5.1.docx")
doc.save(root_output_path)
doc.save(os.path.join(DOCS_DIR, "Mo_hinh_du_bao_kinh_te_5.1_FrostLink.docx"))
print(f"[+] ĐÃ TẠO THÀNH CÔNG BÁO CÁO WORD TỔNG QUAN NATIVE OMML 92 NGÀY: {output_path} và {root_output_path}")
