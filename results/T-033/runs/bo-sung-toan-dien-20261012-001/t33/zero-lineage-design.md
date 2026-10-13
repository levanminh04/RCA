# Hai ca bị triệt tiêu parent weight bằng số thực

Kiểm cả hai first-MAP contrasts bị loại khỏi bảng vì FF R-parent bằng0: dev-3ae0a6c15a tại411 và dev-ba831dbeb8 tại522. Source predictive density tại hai parent hiện xét đều dương. Không gọi trạng thái này là model support bằng0 trước kiểm.

Với parent r trước observation i, start=i−r. Nhánh này là reset tại start (hoặc prior tại0) rồi r lần growth. Từ source R[0,start], predictive density và normalizer đã lưu, log-weight theo lineage là:

`log R_r(i) = log R_0(start) + Σ_{s=start}^{i−1} [log f_s(s−start) + log(.98) − log Z_s]`.

Đây tái dựng một lineage với normalizer nguồn giữ nguyên. Nó không rerun posterior, không thay CP, và không khẳng định là posterior của một detector log-domain đã renormalize mọi lineage. Khi saved PDF dương dùng nguyên saved PDF. Nếu PDF bằng0, giữ event riêng, dựng targeted native state đúng thứ tự và kiểm Student-t logpdf hữu hạn/shape SPD; không thay PDF trong nguồn. Native df dương, shape SPD, X hữu hạn ⇒ mật độ Student-t có support dương toàn không gian; numeric zero khác support model bằng0.

Ghi bước đầu R trên lineage thành0, R/PDF/numerator/normalizer tại bước ấy, log-weight phục hồi, số PDF0 và finite/SPD state checks. Chênh growth log-weight hai parent được phân rã thành feedback logR + relative conditional-extra logdensity như ca hữu hạn; algebra bound1e-10, còn index/CP/hash nguồn giữ exact. Phân rã nguồn hữu hạn và log-lineage diagnostic giữ cột riêng. Nếu final recovered weight lớn, phải nêu normalizer frozen làm đây là diagnostic, không coi là stable posterior thay thế hay ưu điểm P6 đã xác nhận.
