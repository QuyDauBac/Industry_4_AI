# Version 2: Industrial AI on UCI SECOM Rebuild

Tài liệu này xác định **Decision Charter** và kiến trúc triển khai cho `Version 2` của dự án `Industrial_AI_on_UCISECOM`.
Toàn bộ mã nguồn và phân tích tuân thủ nghiêm ngặt quy chế vận hành tại `AGENTS.md` và `PROCESS.md`.

---

## 1. Kết quả đã thực thi và quyết định kỹ thuật — 2026-10-26

**Đã hoàn tất bản viết lại V2 và chạy đủ bốn notebook; cả hai nhánh chưa đạt mục tiêu. `PRODUCTION_READY = FALSE`.** Version 1 và artifact gốc được giữ nguyên, đã đối chiếu SHA-256. Toàn bộ code/notebook do agy viết; Codex quyết định phạm vi, review và thực thi đối soát. Các sửa đổi Markdown trong tài liệu này do Codex tổng hợp từ kết quả chạy thực tế.

| Nhánh / giai đoạn | Fail phát hiện / tổng Fail | Fail coverage hoặc Recall | Mẫu cảnh báo / tổng mẫu | Workload thực tế | Precision trên mẫu cảnh báo |
| --- | ---: | ---: | ---: | ---: | ---: |
| A — development | 12/35 | 34,29% | 221/879 | 25,14% | 5,43% |
| **A — đánh giá cuối** | **9/16** | **56,25%** | **133/297** | **44,78%** | **6,77%** |
| B — development sau hiệu chỉnh chính sách | 16/35 | 45,71% | 237/879 | 26,96% | 6,75% |
| **B — đánh giá cuối** | **5/17** | **29,41%** | **86/314** | **27,39%** | **5,81%** |

A đo Fail duy nhất thuộc hợp các cửa sổ cảnh báo trước ít nhất 6 giờ. B đo Recall của chính mẫu hiện tại trước kết quả QC theo giả định độ trễ. Workload tính cả mẫu Pass và Fail bị cảnh báo; không phải tỷ lệ báo động giả. Hai nhánh có bài toán và mẫu số đánh giá khác nhau.

**Kết luận theo mục tiêu ≥70% và workload ≤30%:** A trượt cả hai điều kiện; B đạt giới hạn workload nhưng trượt Recall. Chưa có bằng chứng đủ để triển khai vận hành công nghiệp hoặc khẳng định dự đoán hỏng máy. Kết quả cuối mang tính hồi cứu vì giai đoạn này đã từng được thấy từ V1; không phải kiểm chứng mù mới. Không tinh chỉnh tiếp theo kết quả cuối.

### Cấu hình đã chốt trước đánh giá cuối

- **A:** Hồi quy `ridge_history`, alpha=10, lịch sử/QC/lịch chu kỳ; lead=6h, H=6h, dự báo `[t+6h, t+12h)`, cadence=6h, nominal budget=30%, threshold lookback=7 ngày. Ngưỡng theo workload quá khứ không bảo đảm workload tương lai dưới 30%; đánh giá cuối thực tế đã vượt trần.
- **B:** `HistGradientBoostingClassifier` cân bằng lớp (`balanced_hgb`), 60 vòng, tối đa 7 lá, min leaf=10, L2=10, không early stopping; hard prefix quota=30%, threshold budget=40%, lookback=14 ngày. Threshold budget chỉ điều khiển ngưỡng trên điểm quá khứ; quota giới hạn số mẫu thực sự cảnh báo theo lượng mẫu đã đến trong mỗi block báo cáo.
- Cả hai refit mỗi ≥24h trên cửa sổ train 56 ngày, chỉ dùng nhãn đã trưởng thành. Đây là mô phỏng **test-then-train** theo quy tắc định trước, không phải một mô hình cố định cho toàn bộ kỳ test. Điểm lịch sử dùng để chọn ngưỡng là điểm OOS đã phát tại thời điểm đó.

### Metric bổ sung và độ bất định

- **A:** 9 Fail được bao phủ, 7 Fail bị bỏ sót; 124/133 mẫu cảnh báo là Pass. Time under alert=48,21%. Event Precision=35,71%, Event Recall=71,43%, event ROC-AUC=0,5170, event AP=0,2857. **Event Recall chỉ tính sự kiện cửa sổ đủ mẫu; chỉ số chấp nhận chính vẫn là Fail coverage 56,25%.** Có 9 cảnh báo cửa sổ đủ mẫu nhưng không có sự kiện dương tính; 13 cảnh báo cửa sổ thưa mẫu được báo riêng và vẫn tính vào workload/bao phủ Fail chính. MAE dự báo tỷ lệ=0,09888 (9,89 điểm phần trăm); RMSE=0,12274 (12,27 điểm phần trăm).
- **B:** TP=5, FP=81, FN=12, TN=216; F1=0,0971; Specificity=72,73%; ROC-AUC=0,5474; AP=0,09622; Accuracy=70,38%; Balanced Accuracy=51,07%. Accuracy không phải tiêu chí chấp nhận cho lớp Fail hiếm. Precision thấp: 81/86 cảnh báo là Pass. Có 51 quyết định đạt ngưỡng điểm nhưng bị quota giữ lại. Trạng thái “Bình thường” vẫn duy trì QC tiêu chuẩn; mô hình không tự động cho xuất mẫu.
- Bootstrap block lịch 2 ngày, 1.000 lượt: CI 95% của A coverage **0–76,47%**; B Recall **16,67–83,33%**. Đây là bất định có điều kiện trên luồng cảnh báo đã chốt, với chỉ 16/17 Fail; không bao gồm toàn bộ bất định do chọn mô hình và không chứng minh đạt 70% trên dữ liệu mới.

Bảng mô phỏng ba mức trong artifact: A có 27 mốc dự báo “Nguy cơ cao”, 6 “Cần theo dõi”, 23 “Bình thường” (56 mốc); B có 86 mẫu “Nguy cơ cao”, 75 “Cần theo dõi”, 153 “Bình thường” (314 mẫu). Chỉ mức Nguy cơ cao được tính vào các metric chính. Các quyết định lưu riêng với bảng đối chiếu nhãn sau khi đã trưởng thành; điểm rủi ro không phải xác suất hỏng máy đã hiệu chuẩn.

### Biến động theo thời gian trên development

| Giai đoạn báo cáo | A coverage | A workload | B Recall | B workload |
| --- | ---: | ---: | ---: | ---: |
| 21/08 18:00–04/09 18:00 | 5/15 (33,33%) | 100/362 (27,62%) | 7/15 (46,67%) | 85/362 (23,48%) |
| 04/09 18:00–18/09 18:00 | 2/5 (40,00%) | 48/153 (31,37%) | 1/5 (20,00%) | 45/153 (29,41%) |
| 18/09 18:00–02/10 18:00 | 5/15 (33,33%) | 73/364 (20,05%) | 8/15 (53,33%) | 107/364 (29,40%) |

Các mốc dữ liệu là timestamp naive của SECOM năm 2008, không tự quy đổi múi giờ. A có một giai đoạn development vượt 30% workload dù tổng thể dưới 30%. B tuân thủ hard quota trong từng block gốc; quota không bảo đảm giới hạn riêng từng ngày.

### Độ nhạy giả định trễ QC — chỉ trên development

| D giả định | A coverage | Workload |
| --- | ---: | ---: |
| 6h — cấu hình đã chốt | 12/35 (34,29%) | 221/879 (25,14%) |
| 12h | 9/35 (25,71%) | 197/879 (22,41%) |
| 24h | 14/35 (40,00%) | 246/879 (27,99%) |

Không chọn lại D theo bảng này. D là giả định vì SECOM không có thời điểm trả QC thực tế; lead L và ngưỡng sự kiện q chưa được kiểm tra độ nhạy đầy đủ.

### Nhận định từ feature analysis và phạm vi đã thử

122 cột hằng số, 24 cột thiếu >50% và nhiều cặp tương quan cao trong khám phá development dẫn tới lọc chất lượng, imputation, loại phương sai thấp và chọn đặc trưng **bên trong từng tập train**. A tạo 3.564 đặc trưng nhân quả để so sánh mô hình dùng cảm biến với mô hình dùng lịch sử. Mô hình được chọn vẫn là history-only; các phép đo cảm biến chưa cho thấy lợi ích đủ mạnh cho tiêu chí dự báo tương lai trong các cấu hình đã thử. B dùng cảm biến của mẫu hiện tại theo giả định chúng sẵn sàng trước QC.

Đã chạy 357 hàng cấu hình ban đầu và 45 hàng chính sách bổ sung (có cấu hình trùng để đối soát), không phải 402 mô hình độc lập. Vòng bổ sung chỉ quét lại chính sách cho hai mô hình đã thắng. Không có nested CV nên kết quả chọn trên development có thể lạc quan. Lấy bớt 50% Pass chỉ trong train đã được thử ở B; trên development tại budget 30%, cách giữ Pass xen kẽ bắt 11/35 Fail, cách ngẫu nhiên bắt 9/35, đều chưa đạt 70%. Workload giữa các cách khác nhau nên không suy ra ưu thế khi chi phí bằng nhau. Dữ liệu đánh giá luôn giữ toàn bộ Pass/Fail.

So với V1 trên cùng khung 297 mẫu/16 Fail, A của V2 tăng bao phủ từ 8 lên 9 Fail nhưng workload cũng tăng từ 112 lên 133 mẫu; chưa khắc phục tiêu chí vận hành. H và cách refit đã đổi, nên không dùng metric sự kiện để kết luận thắng V1. Oracle trong EDA dùng trước nhãn tương lai chỉ là chẩn đoán hình học, không phải kết quả mô hình.

### Bàn giao và tái lập

- [01_EDA.ipynb](01_EDA.ipynb), [02_Preprocessing.ipynb](02_Preprocessing.ipynb), [03_Train.ipynb](03_Train.ipynb), [04_Metrics.ipynb](04_Metrics.ipynb): đã có output thực thi, không có error output trong bản bàn giao. Tám kiểm tra dữ liệu nhân tạo PASS; tái tạo điểm development, cổng trưởng thành nhãn, hợp khoảng cảnh báo và quota đã vượt kiểm tra runtime.
- [experiment.joblib](experiment.joblib) chứa dữ liệu cấu hình, bảng development, lựa chọn hai giai đoạn, trạng thái mô hình, source hashes và `final_evaluation_v2` gồm metric, bootstrap, bảng theo ngày, quyết định ba mức và đối chiếu nhãn sau khi trưởng thành.
- SHA-256 artifact V2 cuối: `7ABBE2F501CE565BAC835DEDE491908096652DCB93B9C4B43FF3C236218F9B99`.
- Môi trường thực thi dùng kernel `industry4-ai`: Python 3.13.1, NumPy 2.5.4, pandas 3.0.6, scikit-learn 1.9.1, joblib 1.6.0. Interpreter đúng nằm trong `.venv` của workspace `Đồ án/Industry_4_AI`; cần dùng đúng môi trường này để mở artifact, không thay bằng Python mặc định có phiên bản thư viện khác. Root đã mở lại artifact từ tiến trình mới, đối chiếu metric, các cờ kiểm tra và mẫu số thành công. Chạy theo thứ tự 01 → 02 → 03 (driver và cell hiệu chỉnh) → 04 từ project hoặc thư mục V2; bootstrap tự tìm dữ liệu chung tại `data/secom`. Chạy lại 03 sẽ thay artifact phát triển và cần 04 để tái lập báo cáo cuối; không chạy riêng cell hiệu chỉnh nhiều lần vì nó nối thêm bảng kết quả.
- Giữ lựa chọn đã chốt để kiểm chứng tiếp trên dữ liệu hoàn toàn mới. Muốn làm bảo trì máy cần thêm machine/tool ID, lịch sử hỏng/bảo trì và thời điểm sẵn sàng từng tín hiệu. Chưa thể xác nhận ROI, nguyên nhân hỏng máy, hoặc phân hạng mức cần bảo trì từ nhãn Pass/Fail hiện có.

---

## 2. Decision Charter: Phân Định Rạch Ròi Hai Bài Toán

Version 2 thiết lập hai luồng bài toán độc lập với mục tiêu, giao thức và hệ thống chỉ số đo lường riêng biệt:

### Bài toán A (PRIMARY): Dự Báo Cửa Sổ Rủi Ro Chất Lượng (Quality-Risk Forecast Windows)
1. **Mục tiêu kỹ thuật:** Phát hiện sớm các khoảng thời gian có nguy cơ cao xảy ra lỗi trước khi sản xuất, hỗ trợ kỹ sư QC ưu tiên kiểm tra, giữ chuẩn quy trình đo kiểm QC thông thường. Do 590 kênh cảm biến hoàn toàn ẩn danh (anonymous channels) và không có mã buồng/thiết bị, **tuyệt đối không bịa đặt hay khẳng định hành động điều chỉnh buồng máy (chamber), thông số thiết bị hay wafer**.
2. **Cấu hình thời gian:**
   - **Lead time ($L$):** Cố định $L = 6\text{h}$ (thời gian báo trước tối thiểu).
   - **Độ trễ báo cáo QC ($D$):** Giả định kỹ thuật $D = 6\text{h}$ (assumed, not measured).
   - **Độ dài cửa sổ lịch sử ($W$):** $W = 168\text{h}$ (7 ngày).
   - **Tần suất kích hoạt dự báo (Cadence):** Chu kỳ 6 giờ một lần (`cadence = 6h`).
   - **Độ dài cửa sổ cảnh báo tương lai ($H$):** Đánh giá 3 cấu hình ứng viên $H \in \{6\text{h}, 12\text{h}, 24\text{h}\}$.
3. **Định nghĩa sự kiện & Nhãn:**
   - Cửa sổ mục tiêu nửa mở: $[t + L, t + L + H)$.
   - Ngưỡng tỷ lệ lỗi mục tiêu: $q = 0.10$ (10%).
   - Số mẫu tối thiểu để phân loại sự kiện: $n_{\text{future}} \ge 5$.
   - **Toàn vẹn mẫu số:** Giữ lại toàn bộ quan sát thô, không âm thầm loại bỏ các điểm thưa mẫu hoặc bỏ sót ca Fail.
4. **Đặc trưng nhân quả:**
   - 24 đặc trưng lịch sử/QC/chu kỳ (bao gồm tỷ lệ lỗi, xu hướng, QC EWMA 24h, và 8 đặc trưng QC nhanh tính theo thời điểm sẵn sàng thực tế `timestamp + delay_h`).
   - 6 họ đặc trưng trên từng kênh trong 590 cảm biến ($590 \times 6 = 3,540$ đặc trưng): giá trị gần nhất 72h (`last72`), trung bình 24h (`mean24`), độ lệch chuẩn 24h (`std24`), chênh lệch xu hướng (`delta_mean24_minus_mean72`), tỷ lệ khuyết thiếu 24h (`missing_fraction24`) và 72h (`missing_fraction72`).
   - Không dùng mặt nạ lọc toàn cục cố định (no fixed `sensor_59`).
5. **Tiến trình huấn luyện Prequential (Test-then-Train):**
   - Tái huấn luyện cuốn chiếu hàng ngày (daily rolling 56 ngày) chỉ sử dụng các kết quả QC đã trưởng thành hoàn toàn ($t_{\text{end}} + D \le t_{\text{fit}}$).
   - Điều chỉnh ngưỡng trực tuyến linh hoạt (`capacity_threshold`) chỉ sử dụng các điểm số ngoài mẫu thực tế trong quá khứ (REAL past OOS scores) đã trưởng thành. Tuyệt đối không chấm điểm lại lịch sử bằng mô hình tương lai.
   - Quá trình đánh giá cuối cùng áp dụng giao thức chuẩn công bố trước **Test-then-Train**, không sử dụng mô hình đóng băng tĩnh (static frozen model) và tuyệt đối không có can thiệp thủ công tinh chỉnh ngưỡng (no human manual retune).
6. **Không gian thử nghiệm cấu hình (Development Grid):**
   - Tổng cộng **330 cấu hình**:
     - 5 mô hình cơ sở (Baselines).
     - 6 mô hình học máy: `LogisticRegression` balanced ($C=0.1$, history-only), `LogisticRegression` balanced ($C=0.1$, chọn tối đa 16 đặc trưng), hồi quy `Ridge` (history-only, $\alpha=10$), hồi quy `Ridge` (chọn tối đa 16 đặc trưng, $\alpha=100$), `HistGradientBoostingRegressor` (Poisson loss), `ExtraTreesRegressor` (predict future rate). Lựa chọn đặc trưng bằng điểm đơn biến và loại tương quan cao bên trong tập train; không dùng PCA.
     - $\times$ 3 cửa sổ $H \in \{6\text{h}, 12\text{h}, 24\text{h}\}$.
     - $\times$ 5 mức ngân sách workload $\in \{10\%, 15\%, 20\%, 25\%, 30\%\}$.
     - $\times$ 2 cửa sổ tra cứu ngưỡng `lookback` $\in \{7\text{d}, 14\text{d}\}$.
   - **Cảnh báo nguy cơ quá khớp:** Không gian 330 cấu hình trên tập Development không sử dụng Nested CV, do đó cấu hình chiến thắng trên Dev có thể mang tính lạc quan (optimistically selected). Đánh giá giai đoạn cuối mang tính hồi cứu (retrospective only); lần thực nghiệm này không đạt đồng thời $\ge 70\%$ Fail coverage và $\le 30\%$ workload.

---

### Bài toán B (SECONDARY): Phân Luồng Kiểm Định Chất Lượng Tức Thời (QC Inspection Triage)
1. **Mục tiêu kỹ thuật:** Sử dụng 590 phép đo cảm biến tại thời điểm sản xuất của chính mẫu đó để dự báo nguy cơ lỗi của **chính mẫu hiện tại** (current-row risk) trước khi có kết quả đo kiểm chất lượng ngoại tuyến (QC).
2. **Bản chất bài toán:**
   - Giả định kỹ thuật: Tính sẵn sàng của 590 phép đo cảm biến tại thời điểm đo là có thực; độ trễ trả kết quả QC là $D = 6\text{h}$.
   - Đo lường bằng **Độ nhạy đồng hàng (Same-row Raw Recall)** và tỷ lệ kiểm tra thực tế (Inspection Workload).
3. **Phân định ranh giới nghiêm ngặt:**
   - **KHÔNG PHẢI là tỷ lệ bao phủ sự cố tương lai (Coverage).**
   - **KHÔNG PHẢI là hỏng hóc máy móc hay thời gian ngừng máy trong tương lai (Future machine failure / Downtime).**
   - Kết quả của Bài toán B tuyệt đối không được dùng để tuyên bố đã giải quyết Bài toán A.
4. **Không gian cấu hình (Development Grid):**
   - Tổng cộng **27 cấu hình**:
     - 9 mô hình: `Balanced Logistic Regression` ($k=1, C=0.1$), `Balanced Logistic Regression` ($k=8, C=0.1$), `Balanced Logistic Regression` ($k=24, C=0.1$), `Balanced Logistic Regression` ($k=24, C=0.01$), `Balanced Random Forest`, `HistGradientBoostingClassifier`, `ExtraTreesClassifier` ($k=64$), `Logistic Regression` ($k=24$, train-only 50% odd Pass undersampling), `Logistic Regression` ($k=24$, train-only 50% random Pass undersampling).
     - $\times$ 3 mức ngân sách kiểm tra $\in \{20\%, 25\%, 30\%\}$.
   - Dữ liệu đánh giá gốc giữ nguyên vẹn không lấy mẫu.
5. **Tiêu chí chấp nhận:** Độ nhạy (Raw Recall) $\ge 70\%$ với tỷ lệ kiểm tra thực tế $\le 30\%$. Kết quả thực thi tại mục 1 chưa đạt điều kiện Recall.

---

## 3. Phân Chia Tập Dữ Liệu & Tính Toàn Vẹn Thời Gian

Toàn bộ tập dữ liệu 1567 quan sát (104 Fail) được phân chia cố định theo trình tự thời gian:
1. **Tập Phát Triển (Development Set):**
   - Khoảng thời gian: $t < \text{2008-10-02 20:54:00}$ (1253 quan sát, 87 Fail).
   - 3 chu kỳ báo cáo phát triển cố định: `[2008-08-21 18:00, 2008-10-02 18:00)` gồm 879 quan sát, 35 Fail.
   - Toàn bộ việc khám phá dữ liệu, tối ưu tham số và chẩn đoán Oracle chỉ thực hiện trong phạm vi này.
2. **Tập Đánh Giá Ngoại Tuyến (Holdout Test Sets):**
   - **Bài toán A (Primary Test Span):** Cố định trong khung $[2008-10-03\text{ 06:00:00}, 2008-10-17\text{ 06:00:00})$ gồm 297 quan sát, 16 Fail; mốc dự báo sớm nhất từ $2008-10-03\text{ 00:00:00}$.
   - **Bài toán B (Secondary Test Set):** Toàn bộ 314 quan sát từ điểm cắt đến hết ($t \ge \text{2008-10-02 20:54:00}$), gồm 17 Fail.
3. **Nguyên tắc bảo vệ tập Holdout:**
   - 314 quan sát này đã từng được hiển thị trong Version 1; **tuyệt đối không bao giờ tuyên bố đây là tập dữ liệu hoàn toàn mù (previously exposed / retrospective only)**.
   - Không thực hiện lựa chọn mô hình hay tinh chỉnh lại ngưỡng (retuning) thủ công dựa trên kết quả của tập đánh giá này.
   - Thừa nhận kết quả thực tế một cách trung thực, không ngụy tạo thành công.

---

## 4. Bổ Sung Đặc Trưng Nhân Quả QC Nhanh (Fast Causal QC Addon — 2026-10-26)

Nhằm phản ánh đúng động thái chất lượng cận thời gian thực mà không vi phạm giả định độ trễ kiểm định $D=6\text{h}$, hàm trích xuất đặc trưng `feature_row()` bổ sung 8 đặc trưng QC dựa trên **thời điểm sẵn sàng thực tế (`timestamp + delay_h`)** thay vì thời điểm đo thô:
1. `qc_n_recent6`: Số lượng kết quả QC hoàn tất đo kiểm và sẵn sàng trong cửa sổ $[t-6\text{h}, t]$.
2. `qc_fail_rate_recent6`: Tỷ lệ lỗi trong số các kết quả QC sẵn sàng trong 6 giờ qua (`NaN` nếu không có mẫu).
3. `qc_n_recent12`: Số lượng kết quả QC hoàn tất đo kiểm và sẵn sàng trong cửa sổ $[t-12\text{h}, t]$.
4. `qc_fail_rate_recent12`: Tỷ lệ lỗi trong số các kết quả QC sẵn sàng trong 12 giờ qua (`NaN` nếu không có mẫu).
5. `qc_fail_trend6_vs24`: Chênh lệch xu hướng tỷ lệ lỗi ngắn hạn so với cửa sổ đo thô 24 giờ (`qc_fail_rate_recent6 - fail_rate24`).
6. `hours_since_last_fail_available`: Khoảng thời gian (giờ) tính từ kết quả QC Fail gần nhất đã biết và sẵn sàng tới thời điểm dự báo $t$ (`NaN` nếu chưa từng ghi nhận Fail).
7. `qc_last5_fail_rate`: Tỷ lệ lỗi của đúng 5 quan sát QC sẵn sàng gần nhất trong lịch sử.
8. `qc_last10_fail_rate`: Tỷ lệ lỗi của đúng 10 quan sát QC sẵn sàng gần nhất trong lịch sử.

Tổng số đặc trưng đầu ra của ma trận $X$ đạt **3,564 đặc trưng** (gồm 24 đặc trưng lịch sử/QC/lịch chu kỳ và $590 \times 6 = 3,540$ đặc trưng cảm biến). Toàn bộ nhóm đặc trưng phi cảm biến được phân nhóm động trong mô hình huấn luyện cuốn chiếu mà không dùng mặt nạ lọc toàn cục tĩnh.
