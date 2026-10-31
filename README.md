# Hệ Thống Dự Báo Nguy Cơ Lỗi Quy Trình Sản Xuất Bán Dẫn (UCI SECOM)

> **Phân biệt phiên bản (2026-10-26):** **Version 2 đã chạy xong:** dự báo tương lai bao phủ 9/16 Fail (56,25%) với workload 133/297 (44,78%); phân luồng QC Recall 5/17 (29,41%) với workload 86/314 (27,39%). Cả hai chưa đạt mục tiêu; `PRODUCTION_READY = FALSE`. Xem [báo cáo V2](<Version 2/README.md>) và [nhật ký](PROCESS.md). Phần báo cáo bên dưới lưu kết quả **Version 1**; bốn notebook V1 và artifact gốc được giữ nguyên, đã kiểm tra mã băm.

> **Thông báo trạng thái thực nghiệm & Nghiệm thu kỹ thuật (2026-10-24 ~08:56 Asia/Saigon):**  
> Dự án đã hoàn tất toàn bộ chu trình thực thi và đối soát độc lập qua 4 notebook (`01_EDA.ipynb` $\to$ `02_Preprocessing.ipynb` $\to$ `03_Train.ipynb` $\to$ `04_Metrics.ipynb`).  
> **Kết luận chính thức:** **KHÔNG ĐẠT TIÊU CHÍ NGHIỆM THU VẬN HÀNH (NOT OPERATIONAL READY / PRODUCTION_READY = FALSE)**.  
> Mô hình được chọn đóng băng (`lr_history_c01` tại nominal budget 0.20) đạt tỷ lệ bao phủ Fail **50.0% (8/16 Fail)** với mức Workload thực tế **37.71% (112/297 quan sát)** trên khung đánh giá cố định Holdout. **Cả hai chỉ số mục tiêu đều thất bại** (mục tiêu bao phủ Fail $\ge 70\%$ không đạt; trần Workload mong muốn $\le 30\%$ bị vi phạm). Nhánh nghiên cứu dự báo rủi ro tương lai theo khung thời gian này chính thức được đề xuất dừng lại để chuyển hướng nghiệp vụ phù hợp hơn.

---

## 1. Kết quả đánh giá cuối theo thời gian với giao thức đã chốt

Dưới đây là bảng tổng hợp kết quả đối chiếu giữa mô hình chiến thắng được chọn đóng băng (`lr_history_c01`, nominal budget 0.20) và các chính sách so chuẩn (Baselines) trên khung thời gian đánh giá cố định $[2008\text{-}10\text{-}03\ 06:00:00, 2008\text{-}10\text{-}17\ 06:00:00)$ (gồm 297 quan sát, 16 ca Fail thực tế, 53 forecast origins):

| Mô hình / Chính sách | Ngân sách danh định | Tỷ lệ bao phủ Fail (Coverage) | Khối lượng kiểm tra (Workload) | Thời gian chịu cảnh báo (Time under alert) | Số Fail bao phủ / Tổng Fail | Số mẫu kiểm tra / Tổng mẫu | Trạng thái đạt mục tiêu ($\ge 70\%$ Fail & $\le 30\%$ WL) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`lr_history_c01` (FROZEN SELECTED)** | **0.20** | **50.00%** | **37.71%** | **26.79%** | **8 / 16** | **112 / 297** | **KHÔNG ĐẠT (Trượt cả 2 mục tiêu)** |
| `lr_history_c01` *(tham khảo mô tả)* | 0.25 / 0.30 | 75.00% | 40.74% | 28.57% | 12 / 16 | 121 / 297 | Không chọn (Vi phạm trần WL 30%) |
| Baseline Rate 24h | 0.20 | 25.00% | 26.26% | 21.43% | 4 / 16 | 78 / 297 | Không đạt mục tiêu bao phủ |
| Baseline Rate 72h | 0.20 | 93.75% | 59.60% | 46.43% | 15 / 16 | 177 / 297 | Vi phạm nghiêm trọng trần WL |
| Baseline Rate 168h | 0.20 | 87.50% | 58.25% | 44.64% | 14 / 16 | 173 / 297 | Vi phạm nghiêm trọng trần WL |

### Các chỉ số chi tiết bổ sung của mô hình chính thức (`lr_history_c01`, budget 0.20):

Bao phủ Fail = số Fail duy nhất thuộc hợp các khoảng được cảnh báo **Nguy cơ cao** / toàn bộ Fail trong khung đánh giá cố định. Workload = số quan sát duy nhất trong cùng hợp đó / toàn bộ quan sát trong cùng khung. Các cửa sổ chồng nhau không làm một quan sát được đếm nhiều lần; khoảng thưa mẫu vẫn đóng góp các Fail vào mẫu số. Khung không có Fail báo coverage là N/A, không phải 0% hay 100%.

- **Quan sát lành (Pass) bị bao phủ:** 104 / 281 quan sát lành rơi vào diện cảnh báo.
- **Độ chính xác cấp thực thể (Unique Fail Precision):** $8 / 112 = 7.14\%$ (tỷ lệ Fail thực tế trong số các thực thể bị gắn cảnh báo; lưu ý: Workload không phải là tỷ lệ cảnh báo sai).
- **Thống kê cấp cảnh báo (Origin Alerts):** Có 8 / 53 origins phát mức "Nguy cơ cao". Trong đó có 7 origins là "False High-event" (tỷ lệ Fail tương lai thực tế $< 10\%$, dù vậy các khung này vẫn có thể chứa một số ca Fail lẻ tẻ) và 0 origins bị thiếu mẫu (undefined).
- **Độ chính xác và độ nhạy cấp cửa sổ (Window Metrics):** Window Precision đạt $12.50\%$, Window Recall đạt $9.09\%$.
- **Khoảng tin cậy Block Bootstrap 2 ngày (1000 lượt mô phỏng, 7 blocks lịch):**
  - Tỷ lệ bao phủ Fail (Coverage 95% CI): $[14.29\%, 58.33\%]$.
  - Tỷ lệ khối lượng kiểm tra (Workload 95% CI): $[6.97\%, 63.11\%]$.
  - *Lưu ý:* Phép bootstrap này mang tính khám phá có điều kiện trên một chuỗi thời gian ngắn và phụ thuộc; đây không phải là khoảng tin cậy bảo đảm chính thức cho toàn bộ quá trình lựa chọn mô hình.

---

## 2. Giới thiệu & Bản chất bài toán nghiệp vụ

### 2.1 Bản chất bài toán
Mục tiêu cốt lõi của nghiên cứu là **dự báo nguy cơ một khoảng thời gian trong tương lai có tỷ lệ quan sát lỗi (Fail rate) tăng cao**, chỉ dựa trên những thông tin thực tế đã sẵn có tại thời điểm đưa ra dự báo $t$.
- **Đối tượng hỗ trợ:** Kỹ sư quản lý chất lượng (Quality Engineer), giúp chủ động phân bổ nguồn lực và ưu tiên thực hiện các đợt kiểm tra quy trình hoặc đo kiểm bổ sung (QC inspection triage) trong các khung thời gian có rủi ro cao.
- **Ranh giới bài toán nghiêm ngặt:**
  - **KHÔNG PHẢI** là bài toán phân loại nhị phân truyền thống trên từng dòng dữ liệu riêng lẻ ($X_i \to y_i$ trên cùng một quan sát).
  - **KHÔNG PHẢI** là hệ thống bảo trì dự đoán thiết bị (Predictive Maintenance), không phát hiện hỏng hóc cơ khí máy móc hay thời gian ngừng máy (downtime).
  - Tỷ lệ lấy mẫu quan sát trong dữ liệu không bảo đảm đại diện cho toàn bộ sản lượng thực tế của nhà máy.

### 2.2 Các mốc thời gian và tham số bài toán đã đóng băng
- **Thời điểm dự báo ($t$):** Thời điểm mô hình thu thập dữ liệu đã sẵn có để đưa ra quyết định cảnh báo.
- **Thời gian báo trước tối thiểu ($L = 6\text{h}$):** Khoảng thời gian từ lúc phát cảnh báo đến khi khoảng thời gian rủi ro bắt đầu.
- **Độ dài cửa sổ dự báo tương lai ($H = 24\text{h}$):** Khoảng thời gian mục tiêu $[t+L, t+L+H)$, nửa mở $[t+6\text{h}, t+30\text{h})$.
- **Chu kỳ phát dự báo (Forecast cadence $= 6\text{h}$):** Cứ mỗi 6 giờ hệ thống thu thập dữ liệu và đưa ra một quyết định mới.
- **Độ dài lịch sử quan sát ($W = 168\text{h}$ / 7 ngày):** Khoảng thời gian thu thập dữ liệu quá khứ $[t-168\text{h}, t)$ dùng để tính toán các đặc trưng thống kê trượt nhân quả (causal rolling features).
- **Độ trễ báo cáo nhãn kiểm định ($D = 6\text{h}$ - GIẢ ĐỊNH):** Do dữ liệu gốc không ghi nhận thời gian trả kết quả đo kiểm, độ trễ $D=6\text{h}$ được **giả định kỹ thuật** (assumed, not measured). Nhạy độ của tham số $D, L, q$ chưa được kiểm chứng đầy đủ trong nghiên cứu này.
- **Tiêu chí tỷ lệ lỗi cao ($q = 10\%$):** Khoảng tương lai có tỷ lệ Fail $\ge 10\%$ được gán nhãn sự kiện thực tế dương tính (high-Fail-rate event).
- **Hỗ trợ mẫu tối thiểu ($= 5$ mẫu):** Chỉ gán nhãn sự kiện tỷ lệ Fail cao khi khoảng tương lai có ít nhất 5 quan sát. Tỷ lệ Fail vẫn tính được khi có từ 1 mẫu, nhưng biến động lớn; không có mẫu thì tỷ lệ không xác định. Các mô hình hồi quy dùng tỷ lệ ở các khoảng có mẫu. Quyết định cảnh báo không dùng số mẫu tương lai, và các Fail trong khoảng thưa vẫn thuộc mẫu số đánh giá chính.
- **Chính sách ngưỡng quyết định thích ứng (Past-only Adaptive Capacity Policy):** Ngưỡng $\tau$ được tính động dựa trên 21 phân vị điểm số trong 14 ngày quá khứ gần nhất ($[t-14\text{d}, t)$), bảo đảm không nhìn trước tương lai.

Chính sách chỉ dùng các cửa sổ quá khứ đã kết thúc và có kết quả sẵn sàng tại thời điểm dự báo. Ngân sách 20/25/30% là tham số thiết kế theo lịch sử, không bảo đảm workload tương lai giữ dưới mức đó. Ngưỡng điểm số cảnh báo $\tau$ khác ngưỡng $q$ định nghĩa nhãn sự kiện thực tế.

---

## 3. Phạm vi dữ liệu & Giới hạn kỹ thuật (UCI SECOM)

### 3.1 Nguồn dữ liệu & Bản sao cục bộ
- **Nguồn dữ liệu:** UCI Machine Learning Repository - SECOM Dataset ([UCI SECOM](https://archive.ics.uci.edu/dataset/179/secom)).
- **Trích dẫn chuẩn:** McCann, M. & Johnston, A. (2008). SECOM [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C54305
- **Bản sao dữ liệu thô:** Bản sao hợp lệ đã được lưu trữ sẵn sàng tại thư mục nội bộ `data/secom/` (`secom.data`, `secom_labels.data`, `secom.names`). Bản gốc tại `D:\AI_Bussiness_Huflit\Đồ án\Industry_4_AI\data\secom` được giữ ở chế độ chỉ đọc.
- **Quy mô toàn bộ:** 1567 quan sát sản xuất, 590 phép đo cảm biến dạng số, 104 quan sát lỗi (Fail).
- **Nhãn:** Nhãn gốc `-1 = Pass`, `+1 = Fail`; mô hình dùng `0 = Pass`, `1 = Fail`. Một dòng là một quan sát tại điểm đo kiểm, không phải mã lô hay mã máy đã được xác nhận.
- **Dấu thời gian (Timestamps):** Dấu thời gian trong dữ liệu không xác định múi giờ (timezone-naive); hệ thống giữ nguyên dạng naive, không tự ý bản địa hóa sang múi giờ Asia/Saigon.

### 3.2 Kế toán phân chia tập dữ liệu & Lộ thông tin Holdout
- **Tập phát triển (Development Set):** Gồm 1253 quan sát (87 Fail), kết thúc tại điểm cutoff `2008-10-02 20:54:00`. Có 269 forecast origins hợp lệ (72 sự kiện rủi ro cao, 157 sự kiện bình thường, 40 khoảng thưa mẫu).
- **Tập thẩm định Walk-Forward (3 outer spans cố định):** 879 quan sát (35 Fail) trải qua 3 giai đoạn: `2008-08-21 18:00` $\to$ `09-04 18:00` $\to$ `09-18 18:00` $\to$ `10-02 18:00`.
- **Tập Holdout (314 quan sát cuối / 17 Fail):**
  - **Minh bạch tiền sử lộ thông tin:** 314 quan sát này đã từng hiển thị kết quả trong workspace cũ trước đây; tuyệt đối **không được coi là tập dữ liệu mù mới (never call newly blind)**.
  - **Phân định ranh giới lịch đã công bố trước:**
    - Khung đánh giá cố định (Frozen Planned Span): $[2008\text{-}10\text{-}03\ 06:00:00, 2008\text{-}10\text{-}17\ 06:00:00)$ gồm **297 quan sát và 16 ca Fail**.
    - Giai đoạn warm-up trước span: 15 quan sát (1 ca Fail).
    - Giai đoạn sau span: 2 quan sát (0 ca Fail).
    - Toàn bộ 17 ca Fail đều được kế toán minh bạch; 1 ca Fail biên bị loại trừ thuần túy do nằm ngoài ranh giới lịch đã đóng băng trước khi đánh giá, không phải do chọn lọc kết quả.

---

## 4. Hệ thống hiển thị 3 mức rủi ro & Hành động kiểm định QC

Hệ thống mô phỏng 3 trạng thái quyết định gửi đến kỹ sư quản lý chất lượng (không phải trạng thái sức khỏe máy móc vật lý):
1. **Bình thường:** Điểm rủi ro nằm dưới ngưỡng theo dõi; tiếp tục theo dõi quy trình thông thường.
2. **Cần theo dõi:** Điểm rủi ro vượt ngưỡng theo dõi; tăng cường giám sát dữ liệu cảm biến trực tuyến.
3. **Nguy cơ cao:** Điểm rủi ro đạt hoặc vượt ngưỡng cảnh báo cao; kích hoạt kiểm tra chất lượng tăng cường (QC inspection triage) cho các sản phẩm trong khung thời gian tương lai. **Chỉ có mức Nguy cơ cao mới cấu thành cảnh báo hợp lệ tính vào tỷ lệ bao phủ Fail.**

Điểm phân loại chưa được hiệu chuẩn thành xác suất; điểm hồi quy là ước lượng tỷ lệ Fail. Ba mức hiển thị là quyết định mô phỏng về ưu tiên QC, không phải nhãn sức khỏe máy móc. “Bình thường” chỉ có nghĩa điểm dưới ngưỡng theo dõi, không bảo đảm sản phẩm hoặc quy trình không có lỗi. Không suy ra lợi ích bảo trì hay tiết kiệm chi phí từ mô phỏng này.

---

## 5. Bản đồ cấu trúc tệp (File Map)

Hệ thống tuân thủ cấu trúc tối giản và kỷ luật nghiêm ngặt:
- **Notebooks (đúng 4 notebook, thực thi tuần tự):**
  - [01_EDA.ipynb](01_EDA.ipynb): Khám phá dữ liệu thời gian và cảm biến trên tập phát triển, xác lập cutoff `2008-10-02 20:54`.
  - [02_Preprocessing.ipynb](02_Preprocessing.ipynb): Tạo đặc trưng và nhãn tương lai, kiểm tra tính sẵn sàng dữ liệu và tính bất biến khi thay đổi dữ liệu chưa sẵn có.
  - [03_Train.ipynb](03_Train.ipynb): Walk-forward và purging, fit tiền xử lý trong từng fold, so sánh 12 ứng viên tại 3 mức ngân sách, lưu mô hình và mốc sẵn sàng trong mô phỏng.
  - [04_Metrics.ipynb](04_Metrics.ipynb): Đánh giá cuối theo thời gian, kiểm tra hash và phép đếm hợp không trùng, bootstrap, mô phỏng cảnh báo và đối chiếu kết quả QC.
- **Tài liệu chuẩn hóa:**
  - [README.md](README.md): Tổng quan, kết quả, giới hạn và hướng dẫn tái lập.
  - [PROCESS.md](PROCESS.md): Tiến trình thực nghiệm và quyết định dừng nhánh hiện tại.
  - [AGENTS.md](AGENTS.md): Phân định vai trò Codex/agy và quy tắc chống rò rỉ dữ liệu.
- **Dữ liệu & Mô hình:**
  - `data/secom/`: Chứa 3 tệp dữ liệu gốc (`secom.data`, `secom_labels.data`, `secom.names`).
  - `experiment.joblib`: Lưu trữ toàn bộ artifacts, metadata, mô hình đóng băng, thresholds và kết quả đối soát độc lập `final_evaluation`.

---

### 5.1 Phương pháp tiền xử lý theo phiên bản

Hai phiên bản cùng giữ quan hệ hàng–nhãn, sắp xếp thời gian ổn định và chỉ sử dụng dữ liệu đã sẵn sàng tại thời điểm dự báo. Các phép biến đổi học tham số được fit trên phần train của từng lần walk-forward; không fit trên toàn bộ dữ liệu trước khi chia tập.

#### Version 1

- **Đọc và căn chỉnh dữ liệu:** Đọc ma trận cảm biến 1567 × 590 và nhãn/timestamp theo đúng định dạng `%d/%m/%Y %H:%M:%S`; ánh xạ nhãn `-1 → Pass (0)`, `+1 → Fail (1)`; gắn `raw_row_id`, rồi sắp xếp tăng dần theo `timestamp` và `raw_row_id` bằng `mergesort` để giữ thứ tự ổn định khi timestamp trùng. Notebook kiểm tra kích thước, nhãn và tổng 104 Fail.
- **Tạo mẫu dự báo nhân quả:** Tạo origin mỗi 6 giờ sau warm-up lịch sử 168 giờ. Với origin `t`, chỉ dùng hàng có `timestamp + D ≤ t` trong `[t−168h, t)`; `D=6h` là giả định độ trễ QC, không phải thời gian đo được. Cấu hình chính trong `03_Train.ipynb` dùng `L=6h`, `H=24h`, `q=10%`, tối thiểu 5 quan sát trong cửa sổ mục tiêu nửa mở `[t+L, t+L+H)`. Nhãn mục tiêu được đánh dấu chưa xác định nếu không đủ mẫu; thời điểm sẵn sàng của nhãn là `target_end + D`.
- **Đặc trưng tạo tại mỗi origin:** 11 biến lịch sử gồm số mẫu sẵn sàng, tỷ lệ Fail và tỷ lệ ô cảm biến khuyết cho các cửa sổ 24/72/168 giờ; chênh lệch tỷ lệ Fail 24h–168h; số giờ từ lần có dữ liệu sẵn sàng gần nhất. Thêm 4 biến lịch tuần hoàn sin/cos cho giờ và thứ tại thời điểm bắt đầu cửa sổ mục tiêu, cùng trung bình 72 giờ của từng trong 590 kênh cảm biến (`include_sensor_means=True` trong luồng train). Như vậy ma trận đặc trưng có tối đa 605 cột trước các bước chọn đặc trưng của từng ứng viên.
- **Biến đổi học được trong `03_Train.ipynb`:** Các pipeline dùng `SimpleImputer(strategy="median")`. Logistic Regression và Ridge tiếp tục dùng `StandardScaler`; Random Forest và các pipeline cây không scale. Các ứng viên dùng cảm biến có chọn đặc trưng giám sát ngay trong pipeline: `lr_sensors_k8` dùng `SelectKBest(f_classif, k=8)`, `et_reg_history_calendar_sensors_k12` dùng `SelectKBest(f_regression, k=12)`. Các ứng viên chỉ dùng lịch sử/lịch không áp dụng selector cảm biến. Median, scaler và selector được fit cùng pipeline trên train fold hiện tại rồi dùng để biến đổi fold dự báo.

#### Version 2

- **Đọc và kiểm tra dữ liệu:** `load_raw()` xác minh SHA-256 riêng cho hai tệp dữ liệu và nhãn, phân tích timestamp tường minh, ánh xạ nhãn, giữ `raw_row_id` và sắp xếp ổn định theo timestamp/ID. Timestamp vẫn là timezone-naive.
- **Tạo origin và đặc trưng nhân quả:** Origin cách nhau 6 giờ, có warm-up 168 giờ. `feature_row()` chỉ lấy lịch sử trong `[t−168h, t)` với điều kiện `timestamp + D ≤ t`; `D=6h` vẫn là giả định. Phần phi cảm biến có 24 biến: số mẫu, tỷ lệ Fail và missingness của các cửa sổ 24/72/168 giờ; xu hướng Fail 24h–168h; thời gian từ kết quả gần nhất đã sẵn sàng; EWMA QC half-life 24h; 8 biến QC nhanh tính theo thời điểm sẵn sàng (`timestamp + D`) gồm số mẫu/tỷ lệ Fail 6h và 12h, chênh lệch tỷ lệ 6h–24h, thời gian từ Fail đã biết gần nhất, và tỷ lệ Fail của 5/10 kết quả gần nhất; cùng 4 biến sin/cos giờ và thứ tại `origin + L`.
- **Đặc trưng cảm biến và target của Branch A:** Với mỗi kênh, tạo 6 thống kê từ lịch sử: giá trị gần nhất trong 72h sau forward-fill trong cửa sổ, mean 24h, độ lệch chuẩn 24h, chênh lệch mean 24h–72h, tỷ lệ thiếu 24h và 72h. Cùng 24 biến phi cảm biến, thiết kế cho tối đa 3564 cột (24 + 590 × 6). `build_targets()` gán nhãn trên `[t+L, t+L+H)`, giữ mẫu thiếu hỗ trợ là chưa xác định, và đặt thời điểm nhãn sẵn sàng bằng `target_end + D`; development đã thử `H=6/12/24h`, chọn `H=6h` trước đánh giá cuối. Branch A tái huấn luyện hàng ngày trên cửa sổ rolling 56 ngày và chỉ dùng nhãn đã trưởng thành.
- **Đầu vào của Branch B:** Đây là bài toán phân loại rủi ro của chính mẫu hiện tại, dùng 590 giá trị cảm biến raw của hàng đó, không dùng ma trận 3564 đặc trưng lịch sử của Branch A. Giả định riêng cho nhánh này là cảm biến sẵn sàng tại timestamp đo; nhãn QC chỉ vào train sau `timestamp + D ≤ t`. Mô hình refit hàng ngày trên rolling 56 ngày; khi chưa đủ 100 hàng hoặc chưa có ít nhất 5 Pass và 5 Fail, luồng dùng fallback tỷ lệ Fail lịch sử. Hai ứng viên undersampling chỉ lấy ngẫu nhiên/so le 50% Pass trong tập train; dữ liệu đánh giá vẫn giữ nguyên.
- **Lọc kênh cảm biến và biến đổi trong `03_Train.ipynb`:** Ở từng lần fit, bộ lọc chất lượng cảm biến chỉ dùng raw của train: với forecast, từ `min(train_origin)−168h` đến `max(train_origin)−D`; với QC triage, các hàng raw tương ứng với train. Kênh hằng số hoặc có tỷ lệ thiếu trên 50% bị loại khỏi các đặc trưng cảm biến tương ứng; đặc trưng missing-fraction được giữ. Ứng viên history-only loại các cột cảm biến. Sau đó, pipeline fit `SimpleImputer(strategy="median", add_indicator=True, keep_empty_features=True)`, `VarianceThreshold(threshold=0)`, lựa chọn đặc trưng khi có cấu hình K, rồi `RobustScaler` trên train hiện tại.
  - **K theo candidate trong code hiện tại:** Branch A: `lr_sensor16`/`ridge_sensor16` dùng K=16; `hgb_poisson24`/`et_rate24` dùng K=24. Branch B: `balanced_lr_k1` dùng K=1, `balanced_lr_k8` dùng K=8; `balanced_lr_k24`, `balanced_lr_k24_c01`, `lr_qc_k24_half_odd`, `lr_qc_k24_half_rand` dùng K=24; `balanced_et_k64` dùng K=64. `balanced_rf` và `balanced_hgb` không đặt K. Bộ chọn suy ra K từ chuỗi tên candidate; vì vậy hai candidate `hgb_poisson24` và `et_rate24` cũng thực tế chọn K=24.
  - **Cách chọn:** Chỉ áp dụng khi candidate có K, không phải history-only và số cột lớn hơn K. Chọn tối đa 4K ứng viên theo `f_classif` cho phân loại/QC hoặc `f_regression` cho hồi quy, rồi loại tuần tự các đặc trưng có tương quan tuyệt đối `≥0.98` với đặc trưng đã giữ cho đến K hoặc hết ứng viên. Candidate không yêu cầu K dùng toàn bộ đặc trưng train còn lại sau lọc phương sai. Các thống kê lọc, imputer, variance filter, selector và scaler đều được fit lại trong train fold/walk-forward hiện tại; không dùng holdout để chọn đặc trưng.

**Khác biệt chính:** V1 biểu diễn cảm biến bằng một mean 72h cho mỗi kênh và dùng median imputation cùng StandardScaler cho Logistic/Ridge; V2 mở rộng lên sáu thống kê nhân quả mỗi kênh, bổ sung QC nhanh theo thời điểm sẵn sàng, lọc chất lượng cảm biến theo train, thêm missing indicators/variance filtering và dùng RobustScaler. Mô tả này ghi nhận cách tiền xử lý của từng phiên bản, không phải kết luận V2 có hiệu năng tốt hơn.

## 6. Môi trường & Quy trình tái lập thực nghiệm (Reproducibility)

### 6.1 Phiên bản môi trường phần mềm (Đo lường thực tế)
- **Hệ điều hành:** Windows
- **Python:** `3.13.1`
- **NumPy:** `2.5.4`
- **Pandas:** `3.0.6`
- **Scikit-Learn:** `1.9.1`
- **Joblib:** `1.6.0`
- **Kernel Jupyter:** `industry4-ai` (đã cài đặt sẵn trong môi trường ảo).

### 6.2 Lệnh PowerShell thực thi tuần tự
Mở PowerShell tại máy trạm và chạy tuần tự các lệnh sau:

```powershell
# 1. Di chuyển vào thư mục dự án
cd "D:\AI_Bussiness_Huflit\Industrial_AI_on_UCISECOM"

# 2. Thiết lập bảng mã UTF-8 cho console
$env:PYTHONIOENCODING = "utf-8"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 3. Đường dẫn Python ảo đã được chuẩn hóa
$PYTHON_EXE = "D:\AI_Bussiness_Huflit\Đồ án\Industry_4_AI\.venv\Scripts\python.exe"

# 4. Thực thi tuần tự 4 notebook thông qua nbconvert với kernel industry4-ai
& $PYTHON_EXE -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=industry4-ai --ExecutePreprocessor.timeout=240 "01_EDA.ipynb"
& $PYTHON_EXE -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=industry4-ai --ExecutePreprocessor.timeout=240 "02_Preprocessing.ipynb"
& $PYTHON_EXE -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=industry4-ai --ExecutePreprocessor.timeout=240 "03_Train.ipynb"
& $PYTHON_EXE -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=industry4-ai --ExecutePreprocessor.timeout=240 "04_Metrics.ipynb"
```

> [!CAUTION]
> **Cảnh báo về việc chạy lại thực nghiệm:**  
> Việc thực thi lại `03_Train.ipynb` sẽ ghi đè tệp `experiment.joblib` và xóa kết quả đánh giá cuối cùng trong trường `final_evaluation` cho đến khi `04_Metrics.ipynb` được chạy tiếp theo. Việc chạy lại cùng một giao thức đóng băng nhằm mục đích kiểm tra tính tái lập là hoàn toàn hợp lệ, nhưng **tuyệt đối không được phép tinh chỉnh lại mô hình (retuning) sau khi đã quan sát kết quả Holdout**. Mọi tuyên bố vận hành công nghiệp mới đều bắt buộc phải được kiểm chứng trên một tập dữ liệu tương lai độc lập hoàn toàn mới.
