# Quy Chế Vận Hành & Phân Định Trách Nhiệm (AGENTS.md)

Tài liệu này xác định nguyên tắc cộng tác giữa Codex và agy, phân định quyền hạn, các quy tắc chống rò rỉ dữ liệu và kỷ luật thực nghiệm bắt buộc trong workspace `Industrial_AI_on_UCISECOM`.

---

## 1. Phân định vai trò & Trách nhiệm (Roles & Responsibilities)

### 1.1 Codex (Chuyên gia phân tích chính & Thẩm định viên độc lập)
- **Vai trò:** Là người ra quyết định kỹ thuật chính (Technical Decision Maker) và thẩm định viên độc lập (Independent Reviewer). Đại diện cho người dùng đưa ra các quyết định kỹ thuật thường nhật.
- **Quyền hạn & Phạm vi:**
  - Xác định phạm vi công việc, mục tiêu kỹ thuật, giả thuyết và tiêu chí nghiệm thu cho từng tác vụ cụ thể.
  - Đọc tệp, kiểm tra diff, chạy kiểm tra/notebook/lệnh độc lập để xác minh kết quả.
  - Phê duyệt hoặc yêu cầu điều chỉnh các thay đổi do agy đệ trình.
  - **Giới hạn nghiêm ngặt:** Codex **KHÔNG BAO GIỜ** tự tay viết, chỉnh sửa hay vá mã nguồn hoặc tế bào notebook.

### 1.2 agy (Đại lý triển khai - Implementation Agent)
- **Vai trò:** Là tác nhân kỹ thuật chịu trách nhiệm hiện thực hóa các yêu cầu của Codex vào mã nguồn và tài liệu.
- **Quyền hạn & Phạm vi:**
  - Viết và chỉnh sửa **TOÀN BỘ** mã nguồn, các tế bào notebook và tập lệnh hỗ trợ (nếu thực sự cần thiết).
  - Tự cập nhật tài liệu theo dõi tiến độ (`PROCESS.md`) sau mỗi tác vụ hoàn thành.
  - **Giới hạn nghiêm ngặt:**
    - Không tự ý mở rộng cấu trúc thư mục hay tạo thêm công cụ khi chưa được giao nhiệm vụ.
    - Không triệu hồi thêm các subagent khác trừ khi có yêu cầu rõ ràng từ Codex.
    - Không tự ý chạy huấn luyện mô hình nặng hoặc thử nghiệm ngầm trong các tác vụ chỉ yêu cầu viết tài liệu.
    - Không thay đổi cấu hình môi trường toàn cục, không cài đặt các gói ngoài phạm vi nhiệm vụ.

### 1.3 Cơ chế kích hoạt & Hợp đồng giao việc (Task Delegation Contract)
- **Chỉ thị bắt buộc trong mỗi lượt giao việc:** Do hệ thống chưa kiểm chứng được việc tự động tải tệp `AGENTS.md` vào ngữ cảnh của agy, Codex **BẮT BUỘC** phải đính kèm câu lệnh:  
  `"Đọc và tuân thủ AGENTS.md và PROCESS.md trong workspace hiện tại"` trong mỗi thông điệp phân công nhiệm vụ cho agy.
- **Hợp đồng công việc nhỏ gọn (Small-task Contract):**
  - Mỗi tác vụ phải có ranh giới rõ ràng, giới hạn trong một thay đổi có thể kiểm tra độc lập.
  - Báo cáo kết quả của agy phải ngắn gọn: liệt kê tệp thay đổi, lệnh/kiểm tra đã chạy, chỉ số thực tế đo được, các vướng mắc/blockers (nếu có), không in toàn bộ nội dung tệp hay log quá dài.

---

## 2. Quy tắc chống rò rỉ dữ liệu & Bảo vệ tính toàn vẹn thời gian

Mọi mã nguồn và phân tích thực hiện trong dự án phải tuân thủ nghiêm ngặt các nguyên tắc sau:

### 2.1 Trình tự thời gian & Giả định giao thức vs. Thực tế kiểm chứng
- **Bóc tách thời gian rõ ràng:** Chuỗi thời gian phải được phân tích cú pháp tường minh, giả định múi giờ nhất quán (giữ nguyên timestamp naive, không tự ý localize sang múi giờ Asia/Saigon), sắp xếp theo thứ tự thời gian tăng dần và duy trì liên kết hàng - nhãn ổn định.
- **Xử lý thời gian trùng nhau (Ties/Duplicates):** Phải giữ trên ranh giới nhất quán, không nội suy hay tái lấy mẫu vượt qua ranh giới tương lai.
- **Tính sẵn sàng tại thời điểm dự báo ($t$):** Mọi đặc trưng cảm biến và nhãn kiểm định chất lượng (QC) được sử dụng để đưa ra quyết định tại thời điểm $t$ bắt buộc phải có thời điểm sẵn sàng thực tế $\le t$.
- **Độ trễ báo cáo nhãn QC ($D$):** Nhãn QC thực tế luôn cần thời gian đo kiểm. Do tập dữ liệu UCI SECOM không ghi nhận thời điểm trả kết quả QC thực tế, **độ trễ $D=6\text{h}$ là một giả định kỹ thuật (assumed, not measured)**.
  - *Ghi nhận thực nghiệm:* V1 đã thử độ nhạy cửa sổ $H=24\text{h}/48\text{h}$. V2 đã thử $H=6\text{h}/12\text{h}/24\text{h}$ trong development, chọn H=6h trước đánh giá cuối; đã kiểm tra riêng D=6/12/24h trên development với cấu hình A đã chốt, không chọn lại D từ các kết quả đó. **Lead time $L$ và ngưỡng tỷ lệ lỗi $q$ chưa được kiểm tra độ nhạy đầy đủ.** Độ trễ QC thực tế vẫn chưa được đo; các kiểm tra hồi cứu không thay thế xác thực thời điểm sẵn sàng dữ liệu trong vận hành.
- **Tính sẵn sàng của nhãn huấn luyện:** Cửa sổ nhãn tương lai của các mẫu huấn luyện trong quá khứ phải hoàn tất đầy đủ và sẵn sàng trước thời điểm dự báo $t$ thì mẫu đó mới được đưa vào tập huấn luyện.

### 2.2 Tiền xử lý theo từng Fold (No Global Preprocessing Leakage)
- **Tập trung trong từng fold:** Mọi bước biến đổi dữ liệu có tham số học được (điền giá trị khuyết thiếu - imputation, chuẩn hóa tỉ lệ - scaling, lựa chọn đặc trưng - feature selection, cân bằng trọng số lớp, hiệu chuẩn xác suất) **bắt buộc phải fit bên trong từng fold huấn luyện của tập train**.
- **Tuyệt đối cấm tiền xử lý toàn cục:** Nghiêm cấm fit bất kỳ bước biến đổi nào trên toàn bộ tập dữ liệu trước khi phân chia tập huấn luyện/thẩm định.
- **Cấm chọn đặc trưng toàn cục dựa trên nhãn:** Không thực hiện bất kỳ phép lọc tương quan hay lựa chọn đặc trưng nào trên nhãn của toàn bộ tập dữ liệu.
- **Đặc trưng quá khứ nhân quả (Causal Rolling/Lag Features):** Chỉ tạo các đặc trưng thống kê trượt dựa trên dữ liệu quá khứ sẵn có trước thời điểm $t$.

### 2.3 Giao thức Walk-Forward & Purging
- **Phân chia theo thời gian thực:** Áp dụng Walk-Forward validation theo ranh giới thời gian thực tế; tuyệt đối không dùng Shuffled Cross-Validation cho dữ liệu chuỗi thời gian.
- **Loại bỏ dữ liệu gối đầu (Purging):** Các cửa sổ thời gian gối đầu nhau là các quan sát phụ thuộc, không phải bằng chứng độc lập bổ sung. Bắt buộc phải loại bỏ (purge) các mẫu huấn luyện trong quá khứ có khoảng nhãn tương lai chồng lấn vào khoảng thời gian đánh giá hoặc vùng dữ liệu chưa sẵn sàng.

### 2.4 Bảo vệ tập Holdout & Không tinh chỉnh lại mô hình
- **Tách biệt tập đánh giá:** Dành riêng một giai đoạn thời gian độc lập làm tập đánh giá cuối cùng (Holdout), không dùng để chọn lọc mô hình hay tối ưu ngưỡng.
- **Minh bạch tiền sử 314 quan sát cuối:** 314 quan sát cuối cùng đã từng được hiển thị trong workspace cũ trước đây; không bao giờ được tuyên bố 314 quan sát này là hoàn toàn mù (never call newly blind).
- **Quy tắc bất biến sau khi unblinded:** Sau khi `04_Metrics.ipynb` đã thực thi và mở băng kiểm định holdout, tập dữ liệu này đã chính thức bị unblinded. **Tuyệt đối cấm việc tinh chỉnh lại mô hình (retuning), lựa chọn lại đặc trưng hay thử nghiệm lại ngưỡng trên tập holdout này**. Mọi xác minh vận hành trong tương lai bắt buộc phải thu thập trên một tập dữ liệu hoàn toàn mới.

---

## 3. Quy tắc toàn vẹn chỉ số & Quyết định cảnh báo

### 3.1 Đo lường chỉ số chấp nhận chính & Toàn vẹn dữ liệu
- **Tỷ lệ bao phủ Fail được cảnh báo trước:** Đo lường trên tập đánh giá cố định bằng hợp (union) của tất cả các khoảng thời gian $[t+L, t+L+H)$ được cảnh báo hợp lệ.
- **Không bỏ sót Fail:** Mẫu số bao gồm toàn bộ các quan sát Fail thực tế trong khung thời gian đánh giá cố định (sau giai đoạn warm-up đã công bố). Các khoảng dữ liệu thưa thớt (sparse intervals), thiếu mẫu hỗ trợ hoặc vùng mô hình từ chối dự báo tuyệt đối không được dùng làm lý do để âm thầm loại bỏ ca Fail khỏi mẫu số chính.
- **Xử lý khung không có Fail & Khoảng trống:** Nếu khung đánh giá không xuất hiện quan sát Fail nào (tổng Fail = 0), tỷ lệ bao phủ chính phải báo cáo là N/A kèm tử số và mẫu số rõ ràng (ví dụ 0/0), không được tự gán 0% hay 100%. Khoảng thời gian không có quan sát nào có tỷ lệ Fail là không xác định (undefined), không phải bằng 0.
- **Chỉ mức Nguy cơ cao được tính:** Trong 3 mức hiển thị ("Bình thường", "Cần theo dõi", "Nguy cơ cao"), chỉ có mức "Nguy cơ cao" mới cấu thành cảnh báo hành động hợp lệ tính vào tỷ lệ bao phủ Fail chính. Mức "Cần theo dõi" phải được báo cáo riêng biệt.
- **Cấm dùng thông tin tương lai để quyết định cảnh báo:** Tuyệt đối không dùng số lượng mẫu thực tế hoặc nhãn của khoảng TƯƠNG LAI để phát hoặc hủy cảnh báo trực tuyến; số lượng mẫu tương lai chỉ dùng cho việc gán nhãn sự kiện và đánh giá ngoại tuyến.

### 3.2 Tối ưu hóa ngưỡng & Đo lường Workload
- **Tách biệt tối ưu ngưỡng:** Việc lựa chọn ngưỡng quyết định cảnh báo $\tau$ phải tách biệt với quá trình huấn luyện mô hình và chỉ được thực hiện trên dữ liệu thẩm định trong quá khứ.
- **Không dùng xếp hạng nhìn trước tương lai (No Future Top-k):** Quyết định cảnh báo trực tuyến không được dùng xếp hạng top-k dựa trên việc so sánh điểm số giữa các khoảng thời gian trong tương lai.
- **Trần Workload kỳ vọng:** Mức $\le 30\%$ thực thể sản xuất bị cảnh báo là trần workload mong muốn tạm thời khi thiết kế ngưỡng, không phải là mức trần bảo đảm chắc chắn trong vận hành thực tế. Mọi trường hợp vi phạm hạn mức workload trong tương lai đều phải được đo lường và báo cáo trung thực.
- **Phân biệt rạch ròi các khái niệm:**
  - Tỷ lệ thực thể sản xuất bị bao phủ (Workload).
  - Tỷ lệ thời gian chịu cảnh báo (Time under alert).
  - Tỷ lệ khoảng thời gian có cảnh báo.
  - Độ chính xác của cảnh báo cấp khoảng (Period Alert Precision) và tỷ lệ Fail trong số thực thể bị cảnh báo (Unique Fail Precision).
  - Workload bao phủ tất cả thực thể sản xuất KHÔNG PHẢI là tỷ lệ cảnh báo sai (Workload is NOT false alarm fraction).

---

## 4. Kỷ luật cấu trúc tệp & Liêm chính khoa học

### 4.1 Cấu trúc tệp tối giản
- Toàn bộ công việc thực nghiệm được giới hạn trong đúng 4 notebook chính:
  1. `01_EDA.ipynb`
  2. `02_Preprocessing.ipynb`
  3. `03_Train.ipynb`
  4. `04_Metrics.ipynb`
- Không tự ý tạo thêm các module `.py` hay framework pipeline trừ khi có sự đồng thuận rõ ràng từ Codex khi phát sinh nhu cầu tái sử dụng thực sự.
- Các tệp tài liệu duy trì trong workspace: `README.md`, `PROCESS.md`, `AGENTS.md`.

### 4.2 Liêm chính khoa học & Đạo đức dữ liệu
- **Thử nghiệm mô hình cơ sở trước:** Bắt buộc xây dựng và so sánh công bằng với các mô hình cơ sở đơn giản (tỷ lệ Fail lịch sử gần nhất 24h/72h/168h, EWMA). Không được tuyên bố mô hình máy học vượt trội hơn baseline nếu chi phí workload thực tế không tương đương.
- **Thừa nhận hạn chế của dữ liệu:** Cỡ mẫu chỉ có 104 Fail trên 1567 quan sát. Bắt buộc phải báo cáo đầy đủ độ bất định, khoảng tin cậy, biến thiên theo thời gian và số lượng cảnh báo sai.
- **Không tự bịa đặt kịch bản bảo trì:** Tuyệt đối không suy diễn sự thay đổi chất lượng sản phẩm thành hỏng hóc máy móc hay thời gian ngừng máy (downtime).
- **Quyết định dừng trung thực:** Mục tiêu 70% bao phủ Fail cần được kiểm chứng. Có thể dừng một nhánh thực nghiệm hữu hạn khi các cấu hình đã thử chưa đạt đồng thời các mục tiêu và hiệu năng còn bất ổn. Phải báo cáo phạm vi đã thử; không suy ra toàn bộ bài toán là bất khả thi, không ngụy tạo kết quả và không điều chỉnh theo kết quả holdout để đạt chỉ số mong muốn.
