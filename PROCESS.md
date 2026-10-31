# Nhật Ký Tiến Độ Dự Án (PROCESS.md)

Tài liệu này ghi nhận toàn bộ tiến trình triển khai, các quyết định kỹ thuật đã thống nhất, trạng thái thực tế và kết quả đối soát độc lập cho dự án dự báo rủi ro lỗi quy trình bán dẫn UCI SECOM.

---

## 1. Trạng thái dự án & Tổng quan các pha triển khai

**Thời điểm cập nhật mốc hoàn tất kỹ thuật:** 2026-10-24 ~08:56 (Múi giờ Asia/Saigon).  
**Trạng thái hiện tại:** Cả 4 notebook thực nghiệm (`01_EDA.ipynb`, `02_Preprocessing.ipynb`, `03_Train.ipynb`, `04_Metrics.ipynb`) đã được thực thi thành công và đối soát độc lập bởi Codex. **Báo cáo kỹ thuật (Pha 9) đã hoàn tất nhưng KHÔNG ĐẠT TIÊU CHÍ NGHIỆM THU NGHIỆP VỤ (BUSINESS ACCEPTANCE NOT MET / PRODUCTION_READY = FALSE)**.

### Bảng theo dõi các pha công việc (Phases & Status)

| Pha | Nội dung công việc | Trạng thái | Ghi chú & Trách nhiệm |
| :---: | :--- | :---: | :--- |
| **1** | **Thống nhất phạm vi & bài toán (Scope Agreement)** | **Đã hoàn thành (Accepted)** | Thống nhất bài toán dự báo rủi ro khoảng thời gian, mục tiêu $\ge 70\%$ bao phủ Fail ở các kịch bản workload 20/25/30%. |
| **2** | **Xác nhận công cụ & quyền truy cập (CLI Read/Write Verification)** | **Đã hoàn thành (Verified)** | Xác nhận công cụ thao tác tệp (read/write/edit) hoạt động bình thường trong workspace mới. |
| **3** | **Khởi tạo bộ tài liệu chuẩn (Documentation Bootstrap)** | **Đã hoàn thành (Accepted)** | Codex đã thẩm định độc lập và phê duyệt bộ 3 tài liệu nền tảng sau các hiệu chỉnh chuẩn hóa. |
| **4** | **Nạp dữ liệu & kiểm tra tính toàn vẹn (Data Ingestion)** | **Đã hoàn thành (Verified)** | Nạp thành công secom.data (1567x590) & secom_labels.data (104 Fail), kiểm tra hash SHA-256. Bản sao lưu hợp lệ tại `data/secom/`. |
| **5** | **Khám phá dữ liệu thời gian & cảm biến (`01_EDA.ipynb`)** | **Đã hoàn thành (Executed)** | 01_EDA thực thi thành công; dev 1253 rows 87 Fail; cutoff 2008-10-02 20:54; ghi nhận 314 quan sát holdout từng hiển thị trước đây. |
| **6** | **Thiết kế nhãn dự báo & tiền xử lý (`02_Preprocessing.ipynb`)** | **Đã hoàn thành (Executed)** | 02_Preprocessing thực thi thành công; 269 dev origins; vượt qua kiểm tra xáo trộn 590 trung bình cảm biến (unavailable perturbation) và bất biến tương lai (future-invariance). |
| **7** | **Walk-Forward, Purging & Huấn luyện (`03_Train.ipynb`)** | **Đã hoàn thành (Executed)** | Walk-forward 3 outer spans cố định (879 mẫu, 35 Fail); khảo sát 12 ứng viên tại 3 mức ngân sách (20%, 25%, 30%). Lựa chọn mô hình `lr_history_c01` đóng băng. |
| **8** | **Đánh giá chỉ số & phân tích Workload (`04_Metrics.ipynb`)** | **Đã hoàn thành (Executed)** | Đánh giá độc lập trên tập Holdout đóng băng (297 mẫu, 16 Fail); toàn bộ assertions SHA-256, availability gating, independent rawID union PASS. |
| **9** | **Tổng kết thực nghiệm & Báo cáo kỹ thuật** | **Hoàn thành kỹ thuật - Không đạt nghiệm thu (Completed Technical Report - Acceptance NOT Met)** | Lập báo cáo kết quả trung thực: mô hình đạt 50% bao phủ Fail tại workload 37.71%; chính thức dừng nhánh nghiên cứu hiện tại. |

---

## 2. Các quyết định kỹ thuật đã thống nhất (Accepted Decisions)

1. **Bản chất bài toán:**
   - Dự báo rủi ro một khoảng thời gian trong tương lai có tỷ lệ Fail cao dựa trên thông tin sẵn có tại thời điểm dự báo $t$.
   - Không thực hiện bài toán phân loại trên từng dòng riêng lẻ ($X \to y$ cùng hàng).
   - Không tuyên bố là bài toán bảo trì dự đoán thiết bị hỏng vì dữ liệu SECOM không có nhãn thiết bị hay lịch sử bảo trì.

2. **Chỉ số đánh giá chính thức:**
   - Tên chỉ số: **Tỷ lệ bao phủ Fail được cảnh báo trước** (mục tiêu đạt $\ge 70\%$).
   - Tính toán bằng hợp (union) các khoảng thời gian được cảnh báo hợp lệ trước thời điểm bắt đầu tối thiểu một khoảng lead time $L$.
   - Mỗi quan sát Fail chỉ được tính tối đa một lần.
   - Cố định mẫu số (toàn bộ Fail trong khung đánh giá sau warm-up/quy tắc biên) và không được loại bỏ các Fail trong khoảng thưa mẫu hoặc vùng mô hình từ chối đưa ra quyết định.

3. **Khối lượng công việc (Workload):**
   - Khảo sát các kịch bản workload: 20%, 25%, 30% tổng số thực thể sản xuất được quan sát trong cùng khung thời gian đánh giá.
   - Mức $\le 30\%$ là trần workload mong muốn tạm thời khi thiết kế chính sách cảnh báo, không phải trần cố định chắc chắn trong vận hành tương lai; mọi vi phạm đều phải ghi nhận trung thực.
   - Báo cáo độc lập: Tỷ lệ thực thể bị cảnh báo, tỷ lệ thời gian chịu cảnh báo, tỷ lệ cảnh báo cấp khoảng, độ chính xác cảnh báo (precision), số lượng cảnh báo sai, độ biến thiên và độ bất định.

4. **Hệ thống cảnh báo 3 mức:**
   - Ba mức hiển thị: "Bình thường", "Cần theo dõi", "Nguy cơ cao". Đây là các trạng thái quyết định (decision states), không phải trạng thái sức khỏe vật lý đã được chứng minh.
   - Mức "Bình thường" chỉ phản ánh điểm số rủi ro của mô hình nằm dưới ngưỡng theo dõi, không khẳng định quy trình ổn định hay không có lỗi.
   - Chỉ có mức "Nguy cơ cao" mới được tính vào chỉ số bao phủ Fail chính thức. Mức "Cần theo dõi" được theo dõi riêng.
   - Ngưỡng quyết định dựa trên chính sách phân vị/điểm số từ dữ liệu quá khứ, không dùng xếp hạng nhìn trước tương lai (no top-k hindsight).

5. **Chống rò rỉ dữ liệu & Kiểm soát Holdout:**
   - Walk-forward validation kết hợp cơ chế Purging để loại bỏ dữ liệu gối đầu (overlapping future windows).
   - Toàn bộ các bước tiền xử lý có học (imputation, scaling, feature selection) phải được fit hoàn toàn bên trong fold huấn luyện.
   - **Ghi nhận lịch sử về tập Holdout:** 314 quan sát cuối cùng trong dữ liệu gốc đã từng bị nhìn thấy trong notebook cũ ở workspace trước đó. Do đó, phải ghi nhận rõ tiền sử lộ thông tin này; không được tuyên bố 314 quan sát đó là hoàn toàn mù (newly blind/untouched). Toàn bộ lựa chọn mô hình/ngưỡng phải thực hiện trên tập phát triển (development data) và tuyệt đối không được tối ưu lặp đi lặp lại trên tập holdout này.

6. **Nguyên tắc so sánh Baseline:**
   - Luôn xây dựng và so sánh công bằng với mô hình cơ sở trước (tỷ lệ Fail gần nhất, EWMA) ở cùng mức workload thực tế và cùng tham số lead/horizon trước khi đánh giá mô hình học máy phức tạp.
   - Báo cáo độ lớn cải thiện, độ bất định và biến thiên thời gian; ghi nhận trung thực khi mô hình phức tạp không thể hiện sự cải thiện rõ rệt so với baseline.

---

## 3. Mẫu nhật ký thực nghiệm chuẩn (Reusable Experiment Log Template)

```markdown
### [EXP-YYYYMMDD-XX] Tiêu đề ngắn gọn của thực nghiệm
- **Ngày giờ:** YYYY-MM-DD HH:MM (Asia/Saigon)
- **Người thực hiện:** agy (theo phân công của Codex)
- **Giả thuyết thực nghiệm (Hypothesis):** Nêu rõ giả thuyết kỹ thuật cần kiểm chứng.
- **Giao thức đóng băng (Frozen Protocol):**
  - Thời gian báo trước $L$: [ví dụ: ... giờ]
  - Cửa sổ dự báo $H$: [khoảng nửa mở [t+L, t+L+H), ví dụ: ... giờ]
  - Chu kỳ phát dự báo (Forecast cadence): [ví dụ: ... giờ]
  - Cửa sổ lịch sử $W$: [ví dụ: ... giờ]
  - Độ trễ nhãn QC $D$: [ví dụ: ... giờ / giả định công bố]
  - Tiêu chí tỷ lệ Fail cao $q$ (nhãn sự kiện thực tế): [ví dụ: ... %]
  - Hỗ trợ mẫu tối thiểu: [số lượng quan sát tối thiểu/khoảng; không có mẫu = undefined]
  - Ngưỡng điểm số theo dõi (chọn trên validation quá khứ): [ngưỡng điểm số ...]
```

---

## 4. Tổng hợp các mốc thực nghiệm

Phần này được biên tập lại từ tiến trình phiên làm việc; các mã mốc dưới đây không phải bản lưu nguyên văn nhật ký ban đầu. Toàn bộ mã nguồn, notebook và tập lệnh hỗ trợ do agy viết; Codex quyết định kỹ thuật, thực thi, kiểm tra và hiệu đính báo cáo.

### [LOG-20261024-01] Khởi tạo tài liệu và thống nhất phương pháp luận
- Xem lại phiên bản khởi tạo ban đầu, thiết lập ranh giới bài toán và trách nhiệm giữa Codex và agy.

### [LOG-20261024-02] Thực thi hoàn tất `01_EDA.ipynb`
- Xác nhận kích thước 1567 dòng, 590 cảm biến, 104 Fail. Xác lập tập phát triển 1253 dòng (87 Fail) với điểm cắt `2008-10-02 20:54:00`. Ghi nhận 314 quan sát sau cutoff là tập holdout có tiền sử lộ thông tin.

### [LOG-20261024-03] Thực thi hoàn tất `02_Preprocessing.ipynb`
- Sinh 269 origins trên tập dev. Khắc phục lỗi kiểm tra nhân quả và hoàn tất các bài kiểm tra rò rỉ thông tin.

### [LOG-20261024-04] Bổ sung đặc trưng Calendar và hoàn thiện 12 ứng viên trong `03_Train.ipynb`
- Bổ sung 4 đặc trưng thời gian (sin/cos hour và sin/cos day-of-week). Bổ sung 3 ứng viên mới (`lr_history_calendar_c01`, `rf_reg_history_calendar`, `et_reg_history_calendar_sensors_k12`).
- Kết quả đối soát từ Codex cho thấy 3 mô hình bổ sung không cải thiện được kết quả so với họ mô hình trước đó.

### [LOG-20261024-05] Đối soát chi tiết kết quả huấn luyện tập phát triển (`03_Train.ipynb`)
- **Giao thức chính thức:** $L=6\text{h}, H=24\text{h}, W=168\text{h}, D=6\text{h}$, chu kỳ $6\text{h}, q=10\%$, tối thiểu 5 mẫu.
- **Tập phát triển:** 1253 quan sát, 87 Fail, 269 origins (72 rủi ro cao, 157 bình thường, 40 thưa mẫu).
- **Thẩm định Walk-forward trên 3 outer spans cố định:**
  - Tổng số mẫu: 879 quan sát, 35 ca Fail.
  - Các mốc thời gian: `2008-08-21 18:00` $\to$ `09-04 18:00` $\to$ `09-18 18:00` $\to$ `10-02 18:00`.
  - Mô hình chiến thắng được chọn: **`lr_history_c01`** tại nominal budget 0.20:
    - Bao phủ Fail tổng hợp: $15 / 35 = 42.857\%$.
    - Khối lượng kiểm tra (Workload): $256 / 879 = 29.124\%$.
    - Tỷ lệ bao phủ từng fold: $0/15\ (0\%)$, $4/5\ (80\%)$, $11/15\ (73.33\%)$.
    - Workload từng fold: $0\%$, $39.216\%$, $53.846\%$.
    - Train AP vs. OOT AP từng fold: $0.8512 / 0.1633$, $0.8134 / 0.5302$, $0.7242 / 0.1385$. Khoảng cách Train-OOT AP rất lớn thể hiện nguy cơ quá khớp (overfitting) hoặc trôi dạt phân phối (distribution drift) kết hợp với cỡ mẫu Fail nhỏ; không thể phân tách nguyên nhân duy nhất.
  - Mô hình Ridge đạt $16/35 = 45.71\%$ Fail nhưng vi phạm trần workload ($32.76\% > 30\%$) nên không hợp lệ.
  - Thử nghiệm Fixed H24 trước đó đạt $11/35 = 31.43\%$ tại workload $240/879 = 27.30\%$ (ghi nhận của Codex xác nhận mức budget 0.20; log trước ghi 0.30 là chưa chính xác và được đính chính tại đây).
  - Thử nghiệm Fixed H48 tốt nhất đạt $5/35 = 14.29\%$ tại workload $93/879 = 10.58\%$.
- **Đóng băng chính sách:** Mô hình triển khai được fit trước origin hiệu chuẩn đầu tiên `2008-09-17 12:00`, chính sách ngưỡng hoàn tất tại `2008-10-02 20:54`. Origin đánh giá holdout sớm nhất là `2008-10-03 00:00`.

### [LOG-20261024-06] Thực thi và nghiệm thu độc lập `04_Metrics.ipynb` (Thời điểm ~08:56 Asia/Saigon)
- Toàn bộ mã nguồn notebook do agy biên soạn (theo hợp đồng ủy quyền kỹ thuật từ Codex), được root/Codex thực thi độc lập.
- **Kết quả kiểm định tính toàn vẹn:**
  - Kiểm tra SHA-256 khớp tuyệt đối với dữ liệu thô ban đầu.
  - Kiểm tra rào chắn tính sẵn sàng (availability gating) đạt chuẩn: `model_ready_time <= policy_ready_time <= first_eval_origin` và `max_feature_available <= origin`.
  - Tái tính toán độc lập ma trận hợp quan sát (independent rawID union recomputation) và mẫu số cố định đều PASS.
- **Kế toán mẫu Holdout (Toàn bộ 314 quan sát / 17 Fail):**
  - Ranh giới lịch đã đóng băng trước kiểm định: $[2008\text{-}10\text{-}03\ 06:00:00, 2008\text{-}10\text{-}17\ 06:00:00)$ (53 forecast origins).
  - Giai đoạn warm-up trước span: 15 quan sát (1 Fail).
  - Khung đánh giá cố định: 297 quan sát (16 Fail).
  - Giai đoạn sau span: 2 quan sát (0 Fail).
  - Việc loại trừ 1 ca Fail trước span thuần túy dựa trên ranh giới lịch đã đóng băng từ trước, không phải chọn lọc thiên vị.
- **Kết quả đánh giá mô hình chính thức (`lr_history_c01`, nominal budget 0.20):**
  - **Tỷ lệ bao phủ Fail (Coverage):** $8 / 16 = 50.00\%$ (**THẤT BẠI**, mục tiêu $\ge 70\%$).
  - **Khối lượng kiểm tra (Workload):** $112 / 297 = 37.7104\%$ (**THẤT BẠI**, vi phạm trần mong muốn $\le 30\%$).
  - **Thời gian chịu cảnh báo (Time under alert):** $26.7857\%$.
  - **Số mẫu lành bị bao phủ (Covered Pass):** 104 quan sát.
  - **Độ chính xác cấp thực thể (Unique Fail Precision):** $8 / 112 = 7.14\%$ (lưu ý: Workload không đồng nhất với tỷ lệ cảnh báo sai).
  - **Thống kê cảnh báo cấp origin:** Có 8 origins phát cảnh báo "Nguy cơ cao", trong đó có 7 false high-event (tỷ lệ Fail tương lai $< 10\%$, dù vậy các khung này vẫn có thể chứa Fail lẻ tẻ) và 0 origins thưa mẫu.
  - **Độ chính xác và độ nhạy cửa sổ (Window Metrics):** Window Precision = $12.50\%$, Window Recall = $9.09\%$.
- **Khảo sát mô tả bổ sung (Descriptive Only - Không chọn sau kiểm định):**
  - Cùng mô hình LR tại nominal budget 0.25 / 0.30: đạt $12 / 16 = 75\%$ bao phủ Fail nhưng Workload tăng lên $121 / 297 = 40.7407\%$ (vi phạm nghiêm trọng trần workload 30%, không được chấp nhận).
  - Baseline Rate 24h (.20): Coverage $4 / 16 = 25.0\%$, Workload $78 / 297 = 26.26\%$.
  - Baseline Rate 72h (.20): Coverage $15 / 16 = 93.75\%$, Workload $177 / 297 = 59.596\%$.
  - Baseline Rate 168h (.20): Coverage $14 / 16 = 87.50\%$, Workload $173 / 297 = 58.249\%$.
  - *Nhận xét:* Các baseline có chi phí workload thực tế hoàn toàn khác biệt; không thể tuyên bố mô hình phức tạp vượt trội hơn baseline ở cùng mức tải.
- **Khám phá Block Bootstrap 2 ngày (1000 lượt mô phỏng, 7 blocks lịch, seed 42):**
  - Khoảng phân vị 2.5–97.5% của Coverage: $[14.2857\%, 58.3333\%]$.
  - Khoảng phân vị 2.5–97.5% của Workload: $[6.9662\%, 63.1124\%]$.
  - *Ý nghĩa:* Kết quả mô phỏng trên chuỗi thời gian ngắn cho thấy độ bất định rất lớn; không bảo đảm khoảng tin cậy chính thức cho việc vận hành.
- **Lưu trữ artifact:** Toàn bộ 53 quyết định trực tuyến, bảng audit đo kiểm QC đã trưởng thành, chẩn đoán từng ngày, so sánh baseline, bootstrap, kiểm tra tính nhân quả và ranh giới thời gian đã được lưu an toàn trong `experiment.joblib` dưới khóa `final_evaluation`.
- **Cổng nghiệm thu:** Cả hai mục tiêu định lượng đều thất bại; gắn nhãn `production_ready = False`.

---

## 5. Kết luận khoa học, Quyết định dừng & Bàn giao bước tiếp theo

### 5.1 Quyết định dừng có cơ sở khoa học (Negative Feasibility Finding)
- **Kết luận:** Các cấu hình dự báo khoảng thời gian đã thử chưa đồng thời đạt bao phủ Fail tối thiểu 70% và workload tối đa 30%. Đây là kết quả âm trong phạm vi thực nghiệm này, chưa chứng minh mọi cách xây dựng mô hình trên SECOM đều không khả thi.
- **Lý do dừng nhánh nghiên cứu:**
  1. Mô hình được chọn chưa đồng thời đạt hai mục tiêu trên tập phát triển và giai đoạn đánh giá cuối theo thời gian.
  2. Hiệu năng chênh lệch lớn giữa huấn luyện và ngoài thời gian huấn luyện; coverage từng fold từ 0% đến 80%, workload từ 0% đến 53.8%.
  3. Chỉ có 35 Fail trong các khoảng validation và 16 Fail trong khung đánh giá cuối; bằng chứng còn hạn chế và chưa cho thấy hiệu năng ổn định để vận hành.
- **Kỷ luật khoa học:** Một tập hợp hữu hạn các cấu hình không thành công không phải là bằng chứng của tính bất khả thi về mặt toán học. Tuy nhiên, việc dừng nhánh nghiên cứu này là quyết định đúng đắn để tránh việc "săn tìm chỉ số" (test chasing) hoặc cố tình điều chỉnh hồi tố tham số trên tập holdout đã bị unblinded.

### 5.2 Bàn giao & Định hướng nghiên cứu khả thi tiếp theo
1. **Trạng thái mô hình hiện tại:** Giữ nguyên mô hình dự báo rủi ro như một nguyên mẫu nghiên cứu (research prototype), không đưa vào vận hành thực tế.
2. **Hướng nghiên cứu nghiệp vụ mới có tiềm năng:**
   - Chuyển từ bài toán dự báo rủi ro khoảng thời gian sang **bài toán phân loại ưu tiên kiểm định chất lượng tại điểm đo kiểm (Quality Inspection Triage at test-point)** trước khi có kết quả QC.
   - Hướng tiếp cận này chỉ khả thi nếu giả định về tính sẵn sàng của 590 phép đo cảm biến tại thời điểm đo kiểm là có thật trong thực tế.
   - Cần thiết kế lại toàn bộ: định nghĩa nhãn đơn lẻ độc lập, thời gian báo trước mới, và quy trình đánh giá riêng biệt; không được trình bày như một bài toán dự báo rủi ro tương lai đã giải quyết xong.
3. **Yêu cầu đối với hệ thống sản xuất thực tế:**
   - Cần thu thập dữ liệu về tính sẵn sàng thực tế của cảm biến (sensor availability metadata).
   - Cần dữ liệu thực tế về sản lượng/công suất nhà máy (volume/capacity data) và định danh máy móc/mã lô sản xuất.
   - Cần sự tham gia và phê chuẩn hành động nghiệp vụ từ các kỹ sư quản lý chất lượng (QC engineers).
   - Tuyệt đối không tự suy diễn các lợi ích nghiệp vụ hay tiết kiệm chi phí nếu chưa có dữ liệu kiểm chứng.
4. **Bảo toàn tập Holdout:** Tập holdout 314 quan sát hiện tại đã chính thức bị unblinded trong đợt đánh giá này, do đó **không được phép tái sử dụng tập này để lựa chọn mô hình trong tương lai**. Mọi đánh giá mới bắt buộc phải thu thập trên dữ liệu thời gian tương lai độc lập.

### 5.3 Điểm bàn giao sau thẩm định cuối — 2026-10-24

- Cả 24 code cells của 4 notebook đều đã thực thi, không có output lỗi. Giữ nguyên mô hình đã chọn trước khi xem kết quả cuối; không tiếp tục tìm ngưỡng trên holdout.
- Codex đã đối chiếu các số phụ trong README với output thực thi, sửa số liệu thời gian chịu cảnh báo, làm rõ mẫu số và giới hạn kết luận. Mã nguồn notebook và tập lệnh đều do agy viết; các hiệu đính cuối của Codex chỉ là văn bản báo cáo.
- Đã lưu mô hình và kết quả trong `experiment.joblib`; bản sao phục hồi ngoài dự án tại `C:\Users\ductr\AppData\Local\Temp\codex-antigravity-secom\experiment-final-evaluation.joblib`.
- Mục tiêu bao phủ Fail tối thiểu 70% tại workload tối đa 30% **chưa đạt**. Đây là điểm dừng của nhánh thực nghiệm hữu hạn đã mô tả, không phải nghiệm thu vận hành và không phải bằng chứng bài toán bất khả thi.
- Không có bộ đếm đáng tin cậy để xác nhận chính xác mốc 5% token của ứng dụng; không ghi nhận mốc đó như một sự kiện đã đo.
- Người dùng đã ủy quyền tắt máy. Helper do agy viết nằm ngoài dự án tại `C:\Users\ductr\AppData\Local\Temp\codex-antigravity-secom\shutdown-after-save.ps1`; khi được kích hoạt sẽ chờ ít nhất 60 giây, ghi log và gửi `Stop-Computer` không dùng chế độ force. Trạng thái yêu cầu nằm trong `shutdown-after-save.log` cùng thư mục; việc gửi lệnh không tự xác nhận máy đã tắt.
- **Chưa kích hoạt helper hoặc gửi lệnh tắt máy:** Mục tiêu đánh giá chưa đạt và chưa xác nhận được điều kiện còn khoảng 5% token. Giữ đúng điều kiện người dùng đã giao; không coi việc hoàn tất báo cáo là đạt yêu cầu vận hành.


---

## 6. Phân tích lại 590 Đặc trưng Gốc (Feature Re-audit) — 2026-10-25

- **Phạm vi & Trách nhiệm:** agy viết phần phân tích bổ sung; Codex đã thực thi và kiểm tra lại bản cuối gồm 9 code cells, không có output lỗi. Assertion cutoff và bảng hỗ trợ mẫu (`n_pass`, `n_fail`) đã được thực thi. Mã nguồn của 8 cells ban đầu được đối chiếu với bản sao trước phân tích và giữ nguyên. Notebook hiện nằm tại [Version 1/01_EDA.ipynb](<Version 1/01_EDA.ipynb>) sau khi cấu trúc thư mục thay đổi trong phiên làm việc; không di chuyển tệp trở lại.
- **Khuyết thiếu & Dư thừa:** Tập dev ($1253 \times 590 = 739,270$ ô) có 34,831 ô khuyết thiếu (4.71%). Phân bố 5 nhóm: 0% (148 biến), (0, 5%] (390), (5, 20%] (0), (20, 50%] (28), (50, 100%] (24); all-missing = 0. Có 122 biến hằng số, 0 biến cận hằng số (modal $\ge 99\%, n \ge 100$), 0 biến phi hằng số trùng lặp chính xác. Khuyết thiếu dòng: Med = 0.0475, P95 = 0.0746, Max = 0.1695; Pass_mean = 0.0472, Fail_mean = 0.0459 (chỉ là thống kê mô tả, chưa kiểm định khác biệt).
- **Cộng tuyến & Ngoại lai:** 288 cặp có $|r| \ge 0.95$, 131 cặp $|r| \ge 0.99$ trên 109,038 cặp hữu hạn (`min_periods=100`). Một số cặp $r=1.0$ chỉ có 138 dòng quan sát chung, không phải trùng lặp toàn phần hay cùng thiết bị vật lý. Tỷ lệ ngoại lai Tukey $3\times\text{IQR}$ cao nhất ở sensor_545 (29.05%), sensor_543 (22.27%), sensor_544 (19.55%), sensor_40 (16.19%), sensor_116 (13.09%); dữ liệu chỉ được đánh dấu flag, không xóa.
- **Liên kết đồng hàng & Kiểm định BH-q:** 460 biến đủ mẫu ($n_{Pass} \ge 20, n_{Fail} \ge 10$). Tách đồng hàng mạnh nhất là sensor_59 (cột 60, AUC = 0.7275, BH-q = $6.29\times 10^{-10}$), sensor_247 (0.6760), sensor_519 (0.6752), sensor_103 (0.6456). Đây là liên kết mô tả in-sample trên cùng hàng, không chứng minh khả năng dự báo trước tương lai. Kiểm định BH-q chỉ mang tính khám phá do tương quan thời gian và đa biến, không khẳng định nhân quả hay thẩm định độc lập.
- **Biến thiên thời gian (3 giai đoạn):** P1 ($n=201$, Fail = 29, 14.43%), P2 ($n=542$, Fail = 38, 7.01%), P3 ($n=510$, Fail = 20, 3.92%). AUC thô dao động giữa các giai đoạn: sensor_59 (0.5806, 0.7355, 0.6458), sensor_103 (0.4757, 0.6129, 0.5229), sensor_290 (0.4098, 0.6758, 0.5170), sensor_129 (0.3921, 0.6031, 0.6713). Ghi nhận 20 biến có trôi dạt trung vị $\ge 1\text{ IQR}_{P1}$ và 36 biến chuyển dịch khuyết thiếu $\ge 20\text{ pp}$. Đây là mô tả biến thiên tiến trình thực tế, không suy diễn nguyên nhân hỏng máy hay bảo trì.
- **Bảo toàn mô hình:** Không undersampling hoặc huấn luyện lại; hash SHA-256 của `experiment.joblib` vẫn là `A0F354C7F9A4C640ECF934E7FDF2D25EED1C046031ACC62911A43DD94095917E`. Thống kê và thứ hạng trong đợt này chỉ dùng development, không dùng holdout để chọn lại đặc trưng.

---

## 7. Khởi Tạo Lại Version 2: Stage 1 (Decision Charter & Core Preprocessing / EDA Rebuild) — 2026-10-26

- **Tuân thủ phân định trách nhiệm & Quyền hạn:** agy thực hiện viết mới toàn bộ nội dung cho `Version 2/01_EDA.ipynb`, `Version 2/02_Preprocessing.ipynb` và `Version 2/README.md`. Toàn bộ mã nguồn và cấu trúc Version 1 giữ nguyên bất biến (`Version 1/` IMMUTABLE; hash SHA-256 của `experiment.joblib` gốc giữ vững `A0F354C7F9A4C640ECF934E7FDF2D25EED1C046031ACC62911A43DD94095917E`). Không thực thi mã nguồn huấn luyện mô hình, không tự ý cài đặt gói hay thay đổi cấu hình môi trường toàn cục.
- **Decision Charter & Phân định rạch ròi hai bài toán:**
  - **Bài toán A (Primary):** Dự báo rủi ro chất lượng theo cửa sổ thời gian ($L=6\text{h}$, $D=6\text{h}$, $W=168\text{h}$, cadence $6\text{h}$, $H \in \{6\text{h}, 12\text{h}, 24\text{h}\}$, $q=0.10$, $n_{\text{event}} \ge 5$). Đánh giá bằng tỷ lệ bao phủ sự cố (Unique Fail Coverage) với hợp workload $\le 30\%$. Bổ sung 6 họ đặc trưng trên từng kênh cảm biến (`last72`, `mean24`, `std24`, `delta_mean24_minus_mean72`, `missing_fraction24`, `missing_fraction72`) cùng các đặc trưng lịch sử QC (EWMA 24h) và lịch thời gian.
  - **Bài toán B (Secondary):** Phân luồng kiểm định chất lượng tức thời (QC Inspection Triage) bằng 590 phép đo cảm biến đồng hàng nhằm dự đoán lỗi của chính mẫu đó trước khi có kết quả QC ($D=6\text{h}$). Đo lường bằng Raw Recall và Inspection Workload. Phân định rõ ràng: Bài toán B không đại diện cho dự báo cửa sổ tương lai và không đo lường sức khỏe thiết bị.
  - **Dữ liệu đánh giá:** Tập Development $< \text{2008-10-02 20:54:00}$ (1253 mẫu, 87 Fail). 3 chu kỳ báo cáo phát triển cố định `[2008-08-21 18:00, 2008-10-02 18:00)` (879 mẫu, 35 Fail). Tập holdout đánh giá cuối cùng gồm Primary test span `[2008-10-03 06:00, 2008-10-17 06:00)` (297 mẫu, 16 Fail) và Secondary test (314 mẫu, 17 Fail); đã từng unblinded trong Version 1 nên tuyệt đối không được coi là hoàn toàn mù và không dùng để chọn lọc mô hình.
- **Tái cấu trúc API Chuẩn hóa trong `02_Preprocessing.ipynb`:**
  - `load_raw()`: Xác thực SHA-256 dữ liệu thô (`20f0e...` và `12688...`), bóc tách nhãn và thời gian naive, sắp xếp ổn định `mergesort` bảo toàn `raw_row_id`.
  - `feature_row()` & `make_features()`: Trích xuất đặc trưng thuần túy nhân quả strictly available tại $t$, không rò rỉ tương lai.
  - `build_targets()` & `training_maturity_gate()`: Xây dựng cửa sổ mục tiêu nửa mở $[t+L, t+L+H)$ và bộ lọc trưởng thành $t_{\text{end}} + D \le t_{\text{fit}}$.
  - `incidence()` & `interval_metrics()`: Ma trận giao điểm và tính toán chỉ số bao phủ với hợp khối lượng công việc, bảo toàn mẫu số cố định và xử lý trường hợp 0 Fail bằng `NaN`.
  - `row_metrics()`: Tính toán chỉ số kiểm định cấp hàng cho Bài toán B.
  - `capacity_threshold()` & `qc_threshold()`: Thuật toán điều chỉnh ngưỡng trực tuyến chỉ dựa trên điểm ngoài mẫu đã trưởng thành trong quá khứ.
  - `run_synthetic_tests()`: Bộ 7 kiểm tra tự động trên dữ liệu nhân tạo xác thực tính đóng mở của cửa sổ, độ trễ $D=6\text{h}$, tính bất biến khi làm nhiễu dữ liệu tương lai và tính ổn định của ngưỡng.
- **Tích hợp Chẩn đoán Oracle Hindsight trong `01_EDA.ipynb`:**
  - Nhập khẩu trực tiếp các hàm từ `02_Preprocessing.ipynb`.
  - Khám phá dữ liệu cảm biến (34,831 ô khuyết thiếu, 122 đặc trưng hằng số, 24 đặc trưng khuyết thiếu $>50\%$) và AUC đơn biến khám phá chỉ trên tập Development.
  - Xây dựng bài toán quy hoạch tuyến tính nguyên hỗn hợp (MILP via `scipy.optimize.milp`) giải bài toán Oracle trên 3 chu kỳ phát triển (879 quan sát, 35 Fail, ngân sách thực thể $\le 263$) nhằm khảo sát giới hạn hình học lý thuyết của các cửa sổ $H=6\text{h}, 12\text{h}, 24\text{h}$.
  - Gắn nhãn cảnh báo rõ ràng: Oracle sử dụng thông tin tương lai trong tập phát triển, chỉ dùng để chẩn đoán giới hạn lý thuyết, không thể triển khai vận hành và không được dùng làm dự báo của mô hình.
- **Trạng thái bàn giao Stage 1:**
  - Mã nguồn của cả hai notebook `01_EDA.ipynb` và `02_Preprocessing.ipynb` đã được xác thực đạt chuẩn `nbformat` (v4.5) và vượt qua kiểm tra cú pháp toàn diện AST (`ast.parse()`).
  - Chưa thực thi các tế bào notebook; chờ Codex thẩm định độc lập và thực thi theo quy chế vận hành.
  - `Version 2/03_Train.ipynb` và `Version 2/04_Metrics.ipynb` hiện giữ nguyên là bản sao tạm thời và được đánh dấu cảnh báo **KHÔNG ĐƯỢC THỰC THI** cho đến Stage 2 và Stage 3.
### 7.1 Hiệu Chỉnh Kỹ Thuật Sau Thẩm Định Stage 1 (Root Review Patch) — 2026-10-26

- **Tuân thủ kỷ luật thực nghiệm & Quyền hạn:** agy thực hiện vá mã nguồn cho đúng 2 tệp `Version 2/01_EDA.ipynb` và `Version 2/02_Preprocessing.ipynb`. Không thực thi notebook, không chạy huấn luyện hay giải MILP trên holdout. Không chỉnh sửa Version 1 hay bất kỳ tệp nào khác ngoài phạm vi.
- **Chi tiết các điểm hiệu chỉnh theo phản hồi của Codex:**
  1. `capacity_threshold` và `qc_threshold`: Chỉ lọc các giá trị hữu hạn `np.isfinite(scores)` khi sinh phân vị ứng viên $\tau$; nếu không có giá trị hữu hạn, trả về $+\infty$. So sánh điều kiện cảnh báo bảo vệ `np.isfinite(scores) & (scores >= tau)`; các điểm $-\infty$ không bao giờ phát cảnh báo. Bổ sung kiểm tra an toàn trên hỗn hợp `NaN`, $-\infty$ và điểm hữu hạn.
  2. `interval_metrics`: Chuẩn hóa `warnings` thành mảng boolean theo vị trí có độ dài bằng `meta` (kiểm tra `warnings.index.equals(meta.index)` nếu là Series, không căn chỉnh ngầm). Đánh giá sự kiện và đếm sự kiện thưa trên vị trí nguyên (`iloc`), xử lý triệt để lỗi căn chỉnh khi `meta` dùng `DatetimeIndex` hoặc chỉ mục không liên tục. Bổ sung các assert hợp lệ: `eval_start < eval_end`, `target_end > target_start`, `leads >= 6h`.
  3. `capacity_threshold`: Bỏ giá trị cố định $t - 6\text{h}$ trong mẫu số thực thể quá khứ; sử dụng `past_meta['target_end'].max()` và xác thực `last_target_end <= current_origin`. Trả về `max_target_end` trong trường thông tin kiểm toán `audit`.
  4. `make_features`: Đặt mốc kết thúc mặc định của lưới dự báo là `floor(max_ts - lead_h - 6h)` độc lập với `delay_h` (tương ứng với cấu hình tối thiểu $H=6\text{h}$).
  5. `load_raw`: Bổ sung kiểm tra tường minh `raw_label in {-1, 1}` trước khi ánh xạ nhãn nhị phân.
  6. `run_synthetic_tests`: Khởi tạo khung dữ liệu nhân tạo đầy đủ 590 cột cảm biến (`sensor_0..589`); kiểm tra tính sẵn sàng khi mẫu có `timestamp + delay == origin` (bao gồm đầy đủ tất cả các bản ghi trùng lặp thời gian - duplicate ties); kiểm tra tính bất biến của đặc trưng khi làm biến đổi toàn bộ 590 cảm biến trong tương lai; gắn nhãn sự kiện thưa là `NaN` thay vì gán nhãn 1 hợp lệ; loại bỏ các khẳng định thời gian thực thi chưa đo kiểm.
  7. `01_EDA.ipynb`: Lọc các đặc trưng phi hằng số và thỏa mãn điều kiện hỗ trợ mẫu tối thiểu $n_{\text{Pass}} \ge 20, n_{\text{Fail}} \ge 10$; in số liệu `n_pass` và `n_fail` kèm thông cáo lưu ý (disclaimer) không xếp hạng hay cố định đặc trưng cho mô hình chuỗi thời gian. Đính chính nhãn của tập đánh giá 314 quan sát thành `[PREVIOUSLY EXPOSED / RETROSPECTIVE ONLY]`, không gọi tập dữ liệu này là mù.
  8. `solve_oracle_diagnostic`: Sử dụng lớp `scipy.optimize.Bounds` tường minh; xác thực độc lập `rec_workload <= budget_entities` và `abs(-res.fun - rec_fail_cov) < 1e-4`; xuất đầy đủ `res.status`, `is_optimal`, `mip_gap`, `mip_dual_bound`, `upper_fail_bound`; gán nhãn cột là `Feasible Hindsight Coverage (%)` và chỉ ghi nhận tối ưu khi `status == 0`.
- **Trạng thái xác thực:** Cả hai notebook đã vượt qua kiểm tra `nbformat` (v4.5) và phân tích cú pháp toàn diện AST (`ast.parse()`); chờ Codex tiếp tục thẩm định độc lập và thực thi.
### 7.2 Bổ Sung 8 Đặc Trưng QC Nhân Quả Nhanh & Ghi Nhận Kết Quả Thẩm Định Của Root — 2026-10-26

- **Tuân thủ phân định trách nhiệm & Kỷ luật bất biến:** agy chỉ sở hữu và cập nhật `Version 2/02_Preprocessing.ipynb`, `Version 2/README.md` và nối tiếp vào `PROCESS.md`. Giữ nguyên vẹn tuyệt đối `01_EDA.ipynb`, `03_Train.ipynb`, `04_Metrics.ipynb`, toàn bộ `Version 1/` và artifact hash `A0F354C7F9A4C640ECF934E7FDF2D25EED1C046031ACC62911A43DD94095917E`. Không thực thi huấn luyện mô hình hay dự phóng các chỉ số chưa thực thi.
- **Ghi nhận kết quả thực thi độc lập của Codex (Root Run):**
  - Notebook `02_Preprocessing.ipynb`: Cả 7 kiểm tra tự động trên dữ liệu nhân tạo (Synthetic Tests 1–7) đã chạy và vượt qua hoàn toàn (`PASS`).
  - Notebook `01_EDA.ipynb` (Hindsight Oracle Diagnostic via MILP): Đã thực thi tối ưu trên 3 chu kỳ phát triển cố định `[2008-08-21 18:00, 2008-10-02 18:00)` (879 thực thể, 35 Fail, ngân sách $\le 263$ thực thể):
    - Cấu hình $H=6\text{h}$: Bao phủ tối ưu $35/35$ Fail với khối lượng công việc $244/879$ thực thể ($27.76\% \le 30\%$).
    - Cấu hình $H=12\text{h}$: Bao phủ tối ưu $34/35$ Fail với khối lượng công việc $257/879$ thực thể ($29.24\% \le 30\%$).
    - Cấu hình $H=24\text{h}$: Bao phủ tối ưu $28/35$ Fail với khối lượng công việc $258/879$ thực thể ($29.35\% \le 30\%$).
    - Tất cả các nghiệm đều thỏa mãn ngân sách workload $\le 263$. Đây là **giới hạn hình học lý thuyết khi biết trước tương lai (Hindsight Known Truth)** nhằm chẩn đoán dung lượng cảnh báo, tuyệt đối không phải năng lực dự báo thực tế của mô hình máy học.
- **Triển khai 8 đặc trưng QC nhân quả nhanh trong `feature_row()`:**
  - Do độ trễ đo kiểm $D=6\text{h}$, cửa sổ đo thô 6 giờ trước $t$ sẽ không có mẫu sẵn sàng. Do đó, các đặc trưng QC ngắn hạn được tính toán dựa trên **thời điểm sẵn sàng thực tế (`timestamp + delay_h`)**:
    1. `qc_n_recent6`: Số lượng kết quả QC sẵn sàng trong $[t-6\text{h}, t]$.
    2. `qc_fail_rate_recent6`: Tỷ lệ lỗi trong các mẫu QC sẵn sàng trong 6 giờ qua (`NaN` nếu $n=0$).
    3. `qc_n_recent12`: Số lượng kết quả QC sẵn sàng trong $[t-12\text{h}, t]$.
    4. `qc_fail_rate_recent12`: Tỷ lệ lỗi trong các mẫu QC sẵn sàng trong 12 giờ qua (`NaN` nếu $n=0$).
    5. `qc_fail_trend6_vs24`: Chênh lệch xu hướng tỷ lệ lỗi ngắn hạn so với cửa sổ đo thô 24 giờ (`qc_fail_rate_recent6 - fail_rate24`).
    6. `hours_since_last_fail_available`: Số giờ trôi qua tính từ kết quả QC Fail gần nhất đã biết tới thời điểm $t$ (`NaN` nếu chưa có Fail).
    7. `qc_last5_fail_rate`: Tỷ lệ lỗi của 5 quan sát QC sẵn sàng gần nhất.
    8. `qc_last10_fail_rate`: Tỷ lệ lỗi của 10 quan sát QC sẵn sàng gần nhất.
  - Sắp xếp ổn định (`mergesort`) theo `timestamp` và `raw_row_id` trước khi lấy `tail()`.
  - Không thay đổi tên hay API của các đặc trưng hiện hữu; ma trận $X$ mở rộng thành **3,564 đặc trưng** ($24$ đặc trưng lịch sử/QC/chu kỳ + $3,540$ đặc trưng cảm biến).
- **Cập nhật bộ kiểm tra tự động `run_synthetic_tests()`:**
  - Bổ sung kiểm tra `Test 3B` xác minh tính chính xác của các đặc trưng QC tại đúng ranh giới thời điểm sẵn sàng (`avail_ts == origin`), kiểm tra độ cũ/khoảng cách thời gian luôn không âm (`staleness >= 0`).
  - Kiểm tra `Test 3` so sánh toàn bộ vector đặc trưng (bao gồm đầy đủ 8 trường QC mới) vẫn đảm bảo bất biến $100\%$ khi làm biến đổi toàn bộ 590 cảm biến trong tương lai.
- **Trạng thái bàn giao:** Tệp `Version 2/02_Preprocessing.ipynb` đã được xác thực `nbformat` (v4.5) và cú pháp AST (`ast.parse()`); sẵn sàng để Codex thực thi kiểm tra lại.
### 7.3 Cập Nhật Tài Liệu Trạng Thái Tạm & Đồng Bộ Lưới Thực Nghiệm Stage 2 — 2026-10-26

- **Tuân thủ phân định trách nhiệm & Kỷ luật bất biến:** agy chỉ sở hữu và cập nhật tài liệu `Version 2/README.md` và nối tiếp vào `PROCESS.md`. Giữ nguyên vẹn toàn bộ mã nguồn, các notebook `01_EDA.ipynb`, `02_Preprocessing.ipynb`, `03_Train.ipynb`, `04_Metrics.ipynb`, toàn bộ thư mục `Version 1/` và artifact hash gốc `A0F354C7F9A4C640ECF934E7FDF2D25EED1C046031ACC62911A43DD94095917E`. Tuyệt đối không tự ý chạy huấn luyện mô hình hay bịa đặt số liệu kết quả.
- **Trạng thái thực thi hiện tại (Provisional Status):**
  - Cả 4 notebook của `Version 2` đã được viết mới hoàn toàn từ đầu (Rebuild from scratch). Đã xóa bỏ cảnh báo cũ về việc coi 03/04 là bản sao V1.
  - `01_EDA.ipynb` và `02_Preprocessing.ipynb`: Đã được Codex (Root) thực thi thành công, 0 lỗi.
  - `03_Train.ipynb`: Codex (Root) hiện đang thực thi lại toàn bộ lưới mô hình (full grid rerun) do lượt chạy trước bị gián đoạn khi chưa lưu artifact `experiment_v2.joblib`. Chưa có kết quả số liệu cuối cùng.
  - `04_Metrics.ipynb`: Đã được agent chuyên trách viết mới hoàn chỉnh và đang trong giai đoạn thẩm định độc lập của Codex, chưa thực thi.
- **Đồng bộ hóa lưới mô hình thực nghiệm (Actual Prespecified Grid):**
  - **Bài toán A (Quality-Risk Forecast Windows):** Tổng cộng **330 cấu hình**:
    - 5 mô hình cơ sở (Baselines).
    - 6 mô hình học máy: `LogisticRegression` balanced ($C=0.1$, history-only), `LogisticRegression` balanced ($C=0.1$, sensor 16-PCA/k-best), `RidgeClassifier` (history-only, $\alpha=10$), `RidgeClassifier` (sensor 16-PCA/k-best, $\alpha=100$), `HistGradientBoostingRegressor` (Poisson loss), `ExtraTreesRegressor` (dự báo rate tương lai).
    - $\times$ 3 cửa sổ cảnh báo $H \in \{6\text{h}, 12\text{h}, 24\text{h}\}$.
    - $\times$ 5 mức ngân sách workload $\in \{10\%, 15\%, 20\%, 25\%, 30\%\}$.
    - $\times$ 2 cửa sổ tra cứu ngưỡng quá khứ `lookback` $\in \{7\text{d}, 14\text{d}\}$.
  - **Bài toán B (QC Inspection Triage):** Tổng cộng **27 cấu hình**:
    - 9 mô hình: `Balanced Logistic Regression` ($k=1, C=0.1$), `Balanced Logistic Regression` ($k=8, C=0.1$), `Balanced Logistic Regression` ($k=24, C=0.1$), `Balanced Logistic Regression` ($k=24, C=0.01$), `Balanced Random Forest`, `HistGradientBoostingClassifier`, `ExtraTreesClassifier` ($k=64$), `Logistic Regression` ($k=24$, train-only 50% odd Pass undersampling), `Logistic Regression` ($k=24$, train-only 50% random Pass undersampling). Đã loại bỏ mô hình LightGBM không có trong thiết kế thực tế.
    - $\times$ 3 mức ngân sách kiểm tra $\in \{20\%, 25\%, 30\%\}$.
- **Chuẩn hóa diễn giải nghiệp vụ & Liêm chính khoa học:**
  - Do 590 kênh cảm biến hoàn toàn ẩn danh và không có siêu dữ liệu về máy móc hay mẻ sản xuất, đã xóa bỏ các tuyên bố về việc điều chỉnh buồng máy (chamber), thông số thiết bị hay wafer. Hành động giả lập chỉ giới hạn ở việc kỹ sư QC ưu tiên kiểm tra, giữ chuẩn quy trình đo kiểm.
  - Phân định rõ ràng: Bài toán A dự báo rủi ro tương lai theo chu kỳ 6 giờ với lead 6 giờ; Bài toán B dự báo nguy cơ lỗi của chính mẫu hiện tại (current-row risk), không phải hỏng hóc máy móc hay thời gian ngừng máy trong tương lai.
  - Quy trình đánh giá cuối cùng sử dụng giao thức **Test-then-Train** cập nhật cuốn chiếu hàng ngày từ các nhãn đã trưởng thành trong quá khứ ($t_{\text{end}} + D \le t_{\text{fit}}$), không dùng mô hình đóng băng tĩnh và không có can thiệp tinh chỉnh ngưỡng thủ công.
  - Nhìn nhận thẳng thắn: Việc thử nghiệm 357 cấu hình trên tập Development không có Nested CV có thể dẫn đến việc lựa chọn cấu hình mang tính lạc quan; đánh giá trên tập holdout 314 quan sát (đã từng exposed) mang tính hồi cứu thuần túy; các mục tiêu định lượng vẫn là giả thuyết chờ kết quả thực thi chính thức từ Root.

### 7.4 Đính chính tài liệu sau thẩm định nguồn — 2026-10-26

- Tên đúng của hai mô hình tuyến tính dự báo tỷ lệ là hồi quy `Ridge`, không phải `RidgeClassifier`. Bộ lọc đặc trưng dùng điểm đơn biến và loại tương quan cao trong từng tập train, không dùng PCA. Các mô tả khác tại mục 7.3 không thay đổi.
- Artifact của V2 có đường dẫn đúng `Version 2/experiment.joblib`; tên `experiment_v2.joblib` tại mục 7.3 là lỗi ghi chép, không có artifact thứ hai.
- Root đã kiểm tra mã băm bốn notebook V1 và artifact gốc; cả năm tệp vẫn khớp bản lưu trước khi bắt đầu V2.
- Bản vá đánh giá của agy giới hạn event ROC-AUC/AP và sai số hồi quy vào cửa sổ tương lai nằm trọn trong khoảng đánh giá, căn chỉnh điểm số/nhãn theo origin một-một và không tạo ngày lịch rỗng bên ngoài khoảng. Chưa có kết quả đánh giá V2 tại thời điểm ghi mục này.

### 7.5 Hoàn tất development V2 và chốt vòng bổ sung trước đánh giá cuối — 2026-10-26

- Root đã thực thi `Version 2/03_Train.ipynb` thành công, 0 lỗi; thời gian driver 1156,83 giây. Artifact mới đã lưu riêng tại `Version 2/experiment.joblib`.
- Toàn bộ 330 cấu hình A và 27 cấu hình B đã được chấm trên cùng 879 quan sát, 35 Fail trong development. A được chọn: hồi quy `ridge_history`, H=6h, nominal budget=30%, lookback=7 ngày; bao phủ 12/35 Fail (34,29%), workload 221/879 (25,14%). B được chọn: `balanced_hgb`, budget=30%, lookback=14 ngày; Recall 15/35 (42,86%), workload 182/879 (20,71%). Chưa nhánh nào đạt Recall/coverage 70%.
- **Đăng ký vòng bổ sung trước khi chạy đánh giá cuối:** Giữ nguyên hai mô hình, đặc trưng, điểm dự báo OOS và các mốc thời gian đã lưu. Chỉ thử chính sách trên development: A mở rộng nominal budget tới 50% với lookback 7/14 ngày, chỉ nhận cấu hình có workload thực tế tổng thể ≤30%; B tách threshold budget 20–100% khỏi hard prefix quota 20/25/30%. Đây là phép thử sử dụng dung lượng kiểm tra còn dư, không tăng trần workload mong muốn, không dùng xếp hạng tương lai.
- Vòng bổ sung chỉ dùng điểm số của hai mô hình đã thắng; không phải quét lại toàn bộ các mô hình với chính sách mới. Sau vòng hữu hạn này sẽ đóng băng lựa chọn và chạy `04_Metrics.ipynb`, không chỉnh mô hình theo kết quả giai đoạn cuối. Mọi chỉ số cuối hiện vẫn chưa được thực thi.

### 7.6 Chốt lựa chọn sau vòng chính sách hữu hạn, trước đánh giá cuối — 2026-10-26

- Root đã review và thực thi thành công duy nhất cell `v2_policy_refinement` của `03_Train.ipynb` bằng runner tạm do agy viết, không refit mô hình. Giữ toàn bộ kết quả driver cũ. Notebook ghi kết quả và artifact lưu cả lựa chọn vòng đầu, bảng chính sách bổ sung, điểm OOS, trạng thái mô hình và nhật ký fit.
- A: 18 chính sách trên điểm `ridge_history`, H=6h không cải thiện lựa chọn khả thi. Chốt nominal budget=30%, lookback=7 ngày; 12/35 Fail, 221/879 quan sát. Workload ba giai đoạn: 27,62% / 31,37% / 20,05%; một giai đoạn vượt mức mong muốn 30% dù tổng thể đạt.
- B: 27 chính sách trên điểm `balanced_hgb`; chốt hard prefix quota=30%, threshold budget=40%, lookback=14 ngày. Recall 16/35 (45,71%), workload 237/879 (26,96%). Workload ba giai đoạn: 23,48% / 29,41% / 29,40%. Threshold budget 40% chỉ điều khiển ngưỡng trên điểm quá khứ; số mẫu thực sự cảnh báo vẫn bị hard quota 30% giới hạn.
- Phạm vi thực nghiệm: 357 hàng cấu hình vòng đầu + 45 hàng chính sách bổ sung, trong đó có các cấu hình trùng để đối soát; không phải 402 mô hình độc lập. Chưa nhánh nào đạt mục tiêu 70% trên development. Dừng mở rộng lưới theo phạm vi hữu hạn đã chốt, chuyển sang báo cáo đánh giá cuối trung thực.
- Lựa chọn này được chốt **trước khi root chạy `04_Metrics.ipynb` V2**. Bước tiếp theo chỉ đánh giá, kiểm tra độ nhạy D=12/24h trên development và đối soát tính nhân quả; không chọn lại mô hình/ngưỡng theo giai đoạn cuối. Giai đoạn cuối đã từng được thấy từ V1, nên kết quả vẫn chỉ mang tính hồi cứu.

### 7.7 Hoàn tất thực thi và thẩm định V2 — 2026-10-26

- Root đã thực thi thành công `04_Metrics.ipynb`, lưu kết quả cùng `final_evaluation_v2` vào artifact V2. Bốn notebook có đầy đủ output và 0 error output trong bản bàn giao. Một lỗi ánh xạ tên trường ở bảng development (`recall` thay vì `coverage`) đã được agy sửa trước khi chấm điểm cuối; lỗi không làm đổi mô hình, điểm số hay lựa chọn chính sách.
- **A — kết quả chính thức trên cùng khung 297 mẫu/16 Fail:** bao phủ 9/16 (56,25%), workload 133/297 (44,78%), Precision 9/133 (6,77%), bỏ sót 7 Fail, 124 Pass thuộc khoảng cảnh báo. Time under alert 48,21%. Event Precision 35,71%, Event Recall 71,43%, event ROC-AUC 0,5170068, event AP 0,2856646. Event Recall không phải chỉ số chấp nhận chính và không được dùng để tuyên bố đạt mục tiêu 70% Fail coverage. Hồi quy rate: MAE 0,0988793; RMSE 0,1227361. A trượt cả coverage và workload.
- **B — kết quả chính thức trên toàn bộ 314 mẫu/17 Fail:** Recall 5/17 (29,41%), workload 86/314 (27,39%), Precision 5/86 (5,81%), F1 0,0970874, Specificity 72,73%; TP=5, FP=81, FN=12, TN=216. B đạt giới hạn workload trong luồng gốc nhưng trượt Recall. Không đổi sang mô hình hoặc ngưỡng khác sau kết quả này.
- **So chuẩn A đã khai báo trước**, cùng H và nominal budget/lookup: rate24h bao phủ 4/16 với workload 82/297; rate72h 5/16 với 122/297; rate168h 13/16 với 160/297. Chi phí thực tế khác nhau; không tuyên bố mô hình thắng baseline tại chi phí bằng nhau, không chọn lại baseline theo kết quả cuối.
- **Kiểm tra đã PASS trong lần thực thi cuối:** dữ liệu khớp SHA-256; replay development khớp cả tử/mẫu số A/B; tái tạo toàn bộ điểm OOS development từ luồng đầy đủ; timestamp fit/nhãn/đặc trưng đúng cổng khả dụng; hợp incidence đối soát độc lập đúng số mẫu và Fail; raw IDs một-một; hard prefix quota B; các mẫu số cố định và tổng block bootstrap đúng.
- **Đối chiếu đủ 314 mẫu:** A chấm trong khung cố định 297 mẫu/16 Fail; trước khung có 15 mẫu/1 Fail, sau khung có 2 mẫu/0 Fail, đều được ghi rõ. B chấm toàn bộ 314/17; không resample hoặc loại Fail khỏi tập đánh giá.
- **Độ nhạy D trên development, không chọn lại giả định:** D=6h 12/35 Fail, workload 221/879; D=12h 9/35, 197/879; D=24h 14/35, 246/879. D thực tế chưa đo; L và q còn thiếu độ nhạy đầy đủ.
- **Bất định:** bootstrap block 2 ngày, 1000 lượt; CI 95% coverage A 0–76,47%, Recall B 16,67–83,33%. Bất định có điều kiện theo các dự báo đã chốt, không gồm toàn bộ bước chọn mô hình, với chỉ 16/17 Fail trong kỳ cuối. Không coi giai đoạn đã thấy từ V1 là xác thực mù mới.
- Artifact V2 cuối SHA-256: `7ABBE2F501CE565BAC835DEDE491908096652DCB93B9C4B43FF3C236218F9B99`. Cập nhật báo cáo thực tế trong `Version 2/README.md`, thêm chỉ dẫn V2 ở README gốc, cập nhật tình trạng kiểm tra D trong AGENTS. Các notebook V1 và artifact gốc vẫn khớp năm mã băm trước khi làm V2.
- **Quyết định kỹ thuật:** kết thúc nhánh thực nghiệm hữu hạn và bàn giao kết quả chưa đạt; `PRODUCTION_READY = FALSE`. Giữ nguyên lựa chọn để kiểm chứng trên dữ liệu mới; không tiếp tục tối ưu theo kỳ đánh giá cuối. Các trạng thái ba mức trong notebook chỉ hỗ trợ kỹ sư QC ưu tiên xem xét, không chứng minh hỏng máy, sức khỏe thiết bị hoặc lợi ích bảo trì. Chưa xác nhận đủ điều kiện sử dụng công nghiệp; không phát lệnh shutdown máy trong phiên này.

### 7.8 Kiểm tra artifact sau khi lưu — 2026-10-26

- Root đã mở lại `Version 2/experiment.joblib` từ một tiến trình mới bằng đúng venv, đọc trực tiếp khóa `final_evaluation_v2`, không dùng fallback từ bảng development. Đã đối chiếu lại toàn bộ cờ causal/prefix đều True, mẫu số 314=15+297+2, các metric và số quyết định ba mức. SHA-256 artifact không đổi.
- B bổ sung: ROC-AUC 0,5474351; AP 0,0962169; Accuracy 0,7038217; Balanced Accuracy 0,5106952; 51 quyết định bị quota giữ lại. A có 9 cảnh báo sự kiện sai trong các cửa sổ đủ mẫu và 13 cảnh báo ở cửa sổ thưa mẫu; các cửa sổ thưa không bị loại khỏi metric chính.
- Mô phỏng A gồm 56 mốc: 27 Nguy cơ cao, 6 Cần theo dõi, 23 Bình thường. B gồm 314 mẫu: 86 Nguy cơ cao, 75 Cần theo dõi, 153 Bình thường. Chỉ Nguy cơ cao tính workload/Recall chính; các hành động là xem xét ưu tiên bởi kỹ sư QC.
- Môi trường mở lại: Python 3.13.1; pandas 3.0.6; NumPy 2.5.4; scikit-learn 1.9.1; joblib 1.6.0. Lượt agy chẩn đoán bằng Python mặc định khác môi trường đã được dừng; không dùng các cách tùy biến unpickler, không thay đổi gói toàn cục hoặc artifact. Script đọc cuối do agy viết, root thực thi; toàn bộ thay đổi sau đánh giá chỉ nằm ở tài liệu.

### 7.9 Ghi rõ tiền xử lý V1/V2 và đẩy snapshot lên GitHub — 2026-10-31

- Theo yêu cầu của người dùng, bổ sung mục 5.1 trong `README.md`, mô tả riêng luồng tiền xử lý V1 và V2 từ `02_Preprocessing.ipynb` và pipeline học được trong `03_Train.ipynb`. Nội dung nêu rõ căn chỉnh thời gian, đặc trưng causal, khác biệt Branch A/Branch B của V2, lọc chất lượng cảm biến, imputation, variance filtering, lựa chọn đặc trưng theo candidate/K và scaler; không kết luận một version tốt hơn.
- Tạo branch `tri_preprocessing` từ `origin/main` trong clone tạm `C:\Users\ductr\AppData\Local\Temp\Industry_4_AI_tri_preprocessing_push` và mirror toàn bộ 17 tệp của workspace vào gốc branch. Commit `758eb5f2b289bc3c9d9da31e39d056cefa9239eb` là commit snapshot ban đầu. Commit tài liệu `bf0287c71fc082aac5d263800dd50ecef8bdeec9` bổ sung mô tả tiền xử lý trong README và bản ghi PROCESS trước đó, đồng thời đính chính stable sort V2. Mục 7.9 này cùng danh sách candidate K đầy đủ được đưa vào commit tài liệu kế tiếp, là HEAD cuối của branch sau lần cập nhật này. Các tệp chỉ có trong tree cũ nhưng không thuộc workspace không được giữ trong branch mirror; `main` giữ nguyên tại `12f1ad8`.
- Đối chiếu danh sách 17 đường dẫn của workspace với Git index trước commit snapshot; hai danh sách khớp. GitHub xác nhận commit `bf0287c...` trước lần cập nhật này; bản ghi PROCESS và README được cập nhật tiếp trên cùng branch.
- Không sửa notebook hay mã nguồn; không thực thi notebook, huấn luyện, retune hoặc mở holdout. Thay đổi của tác vụ này chỉ nằm trong tài liệu; các notebook và artifact được đưa lên branch ở trạng thái sẵn có.
