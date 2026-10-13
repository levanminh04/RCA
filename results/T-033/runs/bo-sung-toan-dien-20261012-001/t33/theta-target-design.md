# Targeted native states — khai trước phép tính, 12/10/2026

Root đã cho phép thay cách thu rẻ hơn sau pilot đạt, giữ source/attempt cũ. Đây là cách lấy cùng state của model, không là prior/detector khác.

Với trước quan sát thứ i và run length r, native state là prior cập nhật lần lượt trên X[i−r:i]. Code update_theta cập nhật từng hàng độc lập: dof/kappa+1, mean có trọng số, inverse precision-scale cộng outer product của residual rồi inverse. Không có tương tác giữa các run-length rows trong update; posterior không tham gia update_theta. Vì vậy có thể giữ một growth row qua r lần update native để dựng đúng state cần đọc, không giữ/tính tất cả run lengths của mọi thời điểm.

Kiểm trước dùng: every savedtheta parent tại lockedpoints/anchor phải exactdof/kappa/mu/scale; giữ integerdtype native. Density tính bằng native batch trên các selectedstates; nếu batchshape khác tạo khác biệt lastbit thì ghi relative/ULP nguồn, lấy stored predictive density làm numeric source chính. Phân rã log-density được đối chiếu scipy.logpdf và log(storedpdf), bound1e-10 đã khai trước chỉ cho algebra; không nới CP, theta hoặc sourcehash gate. Normalizer/posterior/MAP/CP tái dựng EXACT bằng stored R/predictive density đúng native multiplication/sum order. Pdfunderflow0 được ghi, không log0 hoặc chữa bằng epsilon.

Pilot4source của ca đầu (FP/PF/PP/full) trước. Nếu đạt và rẻ hơn thì giữ partial của worker cũ, dừng đúng PIDtheta mới đang chạy rồi chạy targeted120nguồn/607điểm. Native outputs cũ, heavyengine riêng và mọi lỗi giữ nguyên. Đọc source/cachearrays một lần mỗiNPZ để tránh lặp giải nén. Không gọi inverse precision-scale là covariance Student-t df2; báo predictive shape. Fixed-dimensional prior sensitivity vẫn không chứng minh defaultprior là nguyên nhân maskeffect.
