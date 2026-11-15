"""T-062 G1: sinh hai dashboard Grafana cho G2 (provisioning, Infinity đọc JSON định dạng 0.2 của T-061).

- grafana/dashboards/rca-g2-chinh.json     : trang chính, KHÔNG đọc đáp án (chỉ `<thư mục>/<mã>.json` và chỉ mục `chi-muc/danh-sach-su-co.json`).
- grafana/dashboards/rca-g2-phat-lai.json  : trang phát lại có đáp án, chỉ đọc `<thư mục>/phat-lai/...`.
- grafana/dashboards/provider.yaml         : khai báo provisioning (đường dẫn trong container).

Nhãn nút dẫn xuất ở dashboard (JSONata của Infinity, chạy trong trình duyệt) từ `vai_tro` và `hang`, không dùng
`hien_thi.nhan_trong` của định dạng (chữ "không cờ" bị Minh chê). Màu lấy `hien_thi.mau` (chỉ phụ thuộc vai trò, D8).
Cách dùng: py -3 -B dung-dashboard.py   (trong results/T-062/giao-dien)
"""
import json
import sys
import urllib.parse
from pathlib import Path

sys.dont_write_bytecode = True
GOC = Path(__file__).resolve().parent
RA = GOC / 'grafana' / 'dashboards'
DS = {'type': 'yesoreyeram-infinity-datasource', 'uid': 'infinity-rca'}
PROM = {'type': 'prometheus', 'uid': 'prometheus'}
LOKI = {'type': 'loki', 'uid': 'loki'}
TEMPO = {'type': 'tempo', 'uid': 'tempo'}
# Grafana tự gọi chính nó (trong container); thư mục rca-ket-qua gắn vào public/rca.
URL_GOC = 'http://localhost:3000/public/${thu_muc}'
# Trang phát lại: tập chấp nhận mức nút và root khai trước (T-062 e2.py); file T-061 không có khóa mới thì lùi về
# [thanh_phan_tiem]. Phân biệt khóa không tồn tại với tập rỗng. Chỉ dùng ở trang phát lại (F2′, phản biện G1).
J_TAP = '''$tap := $append([], ("tap_chap_nhan" in $keys(phat_lai) ? ( $t := phat_lai.tap_chap_nhan; $t ? $t : [] ) : ( $t := phat_lai.thanh_phan_tiem; $t ? $t : [] )));
        $root := "root_khai_truoc" in $keys(phat_lai) ? phat_lai.root_khai_truoc : phat_lai.thanh_phan_tiem;'''
UID_CHINH, UID_PL = 'rca-g2', 'rca-g2-phat-lai'
SLUG_CHINH, SLUG_PL = 'rca-xem-su-co', 'rca-phat-lai-co-dap-an'

MAU = {'nghi_nguon': '#E02F44', 'bi_keo_theo': '#FF9830', 'binh_thuong': '#8E8E8E', 'thieu_du_lieu': '#CA95E5'}

# Hàm JSONata dùng chung: tên vai trò dễ hiểu, chữ trong nút, ánh xạ tên thực thể M1 -> service_name của telemetry
# (ngược với ALIASES/INFRA của adapter results/T-058/dem-2026-11-10/src/m1/adapter_flashticket.py).
J_HAM = '''
$vt := function($v){ $v = "nghi_nguon" ? "nghi là nguồn" : $v = "bi_keo_theo" ? "bị kéo theo" : $v = "binh_thuong" ? "bình thường" : $v = "thieu_du_lieu" ? "thiếu dữ liệu" : $v };
$ngan := function($s){ $length($s) > 48 ? $substring($s, 0, 47) & "…" : $s };
$co_hang := function($n){ $n.vai_tro in ["nghi_nguon","bi_keo_theo"] and $exists($n.hang) and $n.hang != null };
$chu := function($n){ $co_hang($n) ? "#" & $string($n.hang) : $n.vai_tro = "thieu_du_lieu" ? "?" : $n.vai_tro in ["nghi_nguon","bi_keo_theo"] ? "–" : "" };
$svc := function($id){ ( $m := {"config-discovery":"discovery-server","postgresql-shared-instance":"postgres","mongodb-instance":"user-db","cache":"redis","broker":"rabbitmq"}; $x := $lookup($m, $id); $x ? $x : $id ) };
$khoa := function($n){ $exists($n.hang) and $n.hang != null ? $n.hang : 9999 };
$vung := function($n){ $n.goc_vung ? "gốc vùng nghi ngờ" : $n.trong_vung_cach_1 ? "trong vùng (cách 1)" : $n.trong_vung_cach_2 ? "trong vùng (cách 2)" : "ngoài vùng" };
'''


def inf(ref_id, url, expr, cols, hide=False):
    # Parser backend của Infinity 4.1.6 chạy JSONata (jsonata-go) khi biểu thức bắt đầu bằng `$`; `$$.( … )` = khối trên gốc.
    t = {'refId': ref_id, 'datasource': DS, 'type': 'json', 'source': 'url', 'parser': 'backend', 'format': 'table',
         'url': url, 'url_options': {'method': 'GET', 'data': ''}, 'root_selector': '$$.(' + ' '.join(expr.split()) + ')',
         'columns': [{'selector': c, 'text': c, 'type': t} for c, t in cols]}
    if hide:
        t['hide'] = True
    return t


def jexpr(body):
    return J_HAM + body


def explore(ds, query_obj, tu='${t_tu}', den='${t_den}'):
    """URL Explore (Grafana 13, schemaVersion 1). Chuỗi giữ chỗ ZZ..ZZ được thay bằng biến Grafana sau khi mã hóa."""
    q = dict(query_obj)
    q.setdefault('refId', 'A')
    q['datasource'] = ds
    panes = {'a': {'datasource': ds['uid'], 'queries': [q], 'range': {'from': 'ZZTUZZ', 'to': 'ZZDENZZ'}}}
    s = urllib.parse.quote(json.dumps(panes, ensure_ascii=False, separators=(',', ':')), safe='')
    return '/explore?schemaVersion=1&orgId=1&panes=' + s.replace('ZZTUZZ', tu).replace('ZZDENZZ', den)


def thay(url, **kv):
    for k, v in kv.items():
        url = url.replace('ZZ' + k.upper() + 'ZZ', v)
    return url


def lien_ket_nut(svc_ref):
    """Liên kết trong menu của nút: chọn service, Explore Tempo/Loki/Prometheus đúng cửa sổ sự cố."""
    return [
        {'title': 'Trong trang này/① Xem bằng chứng và thao tác của thành phần này (cuộn xuống)',
         'url': f'/d/{UID_CHINH}/{SLUG_CHINH}?orgId=1&var-thu_muc=${{thu_muc}}&var-ca=${{ca}}&var-dv=${{__data.fields.id}}&${{__url_time_range}}'},
        {'title': 'Mở dữ liệu gốc, đúng cửa sổ sự cố/Tempo: trace của service ↗', 'targetBlank': True,
         'url': thay(explore(TEMPO, {'queryType': 'traceql', 'query': '{resource.service.name="ZZSVCZZ"}', 'limit': 50,
                                     'tableType': 'traces'}), svc=svc_ref)},
        {'title': 'Mở dữ liệu gốc, đúng cửa sổ sự cố/Loki: log của service ↗', 'targetBlank': True,
         'url': thay(explore(LOKI, {'expr': '{service_name="ZZSVCZZ"}', 'queryType': 'range'}), svc=svc_ref)},
        {'title': 'Mở dữ liệu gốc, đúng cửa sổ sự cố/Prometheus: số request mỗi giây theo route ↗', 'targetBlank': True,
         'url': thay(explore(PROM, {'expr': 'sum by (http_request_method, http_route) (rate(http_server_request_duration_seconds_count{service_name="ZZSVCZZ"}[1m]))',
                                    'range': True}), svc=svc_ref)},
    ]


# ------------------------------------------------------------------ biến
def bien_thu_muc(chinh=True):
    if chinh:
        q = 'Thư mục chính rca-ket-qua (kết quả mới nhất) : rca,Mẫu T-061 (2 ca cũ) : rca/mau'
        opts = [('Thư mục chính rca-ket-qua (kết quả mới nhất)', 'rca'), ('Mẫu T-061 (2 ca cũ)', 'rca/mau')]
    else:
        q = 'Thư mục phát lại chính rca-ket-qua/phat-lai : rca/phat-lai,Phát lại mẫu T-061 : rca/mau/phat-lai'
        opts = [('Thư mục phát lại chính rca-ket-qua/phat-lai', 'rca/phat-lai'), ('Phát lại mẫu T-061', 'rca/mau/phat-lai')]
    return {'name': 'thu_muc', 'label': 'Nguồn kết quả', 'type': 'custom', 'query': q,
            'current': {'text': opts[0][0], 'value': opts[0][1]},
            'options': [{'text': t, 'value': v, 'selected': i == 0} for i, (t, v) in enumerate(opts)],
            'hide': 0, 'includeAll': False, 'multi': False}


def bien_inf(name, label, target, hide=0, sort=0):
    t = dict(target)
    t.pop('refId', None)
    return {'name': name, 'label': label, 'type': 'query', 'datasource': DS,
            'query': {'queryType': 'infinity', 'infinityQuery': t, 'query': '', 'refId': 'variable'},
            'definition': f'Infinity: {label}', 'refresh': 1, 'hide': hide, 'sort': sort,
            'includeAll': False, 'multi': False, 'current': {}, 'options': []}


def cac_bien(chinh=True):
    chi_muc = 'chi-muc/danh-sach-su-co.json' if chinh else 'chi-muc/danh-sach-phat-lai.json'
    file_ca = '${ca}.json' if chinh else '${ca}.phat-lai.json'
    ca = bien_inf('ca', 'Sự cố', inf('v', f'{URL_GOC}/{chi_muc}', '''
        [su_co.{"__text": $substring(t_utc, 8, 2) & "/" & $substring(t_utc, 5, 2) & " " & $substring(t_utc, 11, 5) & " UTC — " & ma
                 & " — " & (nghi_nguon_hang_1 = "—" ? "không nghi thành phần nào" : "nghi " & nghi_nguon_hang_1),
                "__value": ma}]''', [('__text', 'string'), ('__value', 'string')]))
    dv = bien_inf('dv', 'Thành phần đang xem', inf('v', f'{URL_GOC}/{file_ca}', jexpr('''
        [nut^($khoa($), id).{"__text": ($chu($) != "" ? $chu($) & " " : "") & id & " — " & $vt(vai_tro), "__value": id}]'''),
        [('__text', 'string'), ('__value', 'string')]))
    dv_svc = bien_inf('dv_svc', 'service_name trong telemetry', inf('v', f'{URL_GOC}/{file_ca}', jexpr('[{"v": $svc("${dv}")}]'),
                                                                     [('v', 'string')]), hide=2)
    t_tu = bien_inf('t_tu', 'đầu cửa sổ nền (ms)', inf('v', f'{URL_GOC}/{file_ca}', '''
        [{"v": $string(su_co.cua_so_nen ? su_co.cua_so_nen.tu_ms : $floor(su_co.moc.t_ns / 1000000) - 300000)}]''',
        [('v', 'string')]), hide=2)
    t_den = bien_inf('t_den', 'cuối cửa sổ sự cố (ms)', inf('v', f'{URL_GOC}/{file_ca}', '''
        [{"v": $string(su_co.cua_so_su_co ? su_co.cua_so_su_co.den_ms : $floor(su_co.moc.t_ns / 1000000) + 300000)}]''',
        [('v', 'string')]), hide=2)
    return [bien_thu_muc(chinh), ca, dv, dv_svc, t_tu, t_den]


# ------------------------------------------------------------------ panel
_id = [0]


def pid():
    _id[0] += 1
    return _id[0]


def ghi_de(ten, **props):
    return {'matcher': {'id': 'byName', 'options': ten}, 'properties': [{'id': k, 'value': v} for k, v in props.items()]}


def an_cot(*ten):
    return [{'matcher': {'id': 'byName', 'options': t}, 'properties': [{'id': 'custom.hidden', 'value': True}]} for t in ten]


BANG_MAC_DINH = {'custom': {'align': 'left', 'cellOptions': {'type': 'auto'}, 'inspect': True}}


def panel_bang(title, gp, targets, overrides=(), desc='', links=None, opts=None, defaults=None):
    p = {'id': pid(), 'type': 'table', 'title': title, 'description': desc, 'gridPos': gp, 'datasource': DS,
         'targets': targets,
         'fieldConfig': {'defaults': defaults or BANG_MAC_DINH,
                         'overrides': list(overrides)},
         'options': dict({'showHeader': True, 'cellHeight': 'sm', 'footer': {'show': False}}, **(opts or {})),
         # backend trả cột theo thứ tự chữ cái: xếp lại theo thứ tự khai báo
         'transformations': [{'id': 'organize', 'options': {
             'indexByName': {c['text']: i for i, c in enumerate(targets[0]['columns'])}, 'excludeByName': {}, 'renameByName': {}}}]}
    if links:
        p['links'] = links
    return p


def mau_vai_tro(ten_cot):
    """Tô nền ô theo chữ vai trò."""
    return {'matcher': {'id': 'byName', 'options': ten_cot}, 'properties': [
        {'id': 'custom.cellOptions', 'value': {'type': 'color-background', 'mode': 'basic'}},
        {'id': 'mappings', 'value': [{'type': 'value', 'options': {
            'nghi là nguồn': {'color': MAU['nghi_nguon'], 'index': 0},
            'bị kéo theo': {'color': MAU['bi_keo_theo'], 'index': 1},
            'bình thường': {'color': 'transparent', 'index': 2},
            'thiếu dữ liệu': {'color': MAU['thieu_du_lieu'], 'index': 3}}}]}]}


def panel_huong_dan(gp, chinh=True):
    ch = ('<b>Cách dùng:</b> chọn sự cố ở bảng <i>Danh sách sự cố</i> (bấm mã) hoặc ô <i>Sự cố</i> ở đầu trang. '
          'Bấm một nút trên đồ thị → mục ① để xem bằng chứng và thao tác của thành phần đó; các mục ↗ mở Tempo/Loki/Prometheus '
          'đúng cửa sổ thời gian của sự cố.')
    if not chinh:
        ch = ('<b>Trang phát lại — CÓ ĐÁP ÁN.</b> Đáp án chỉ được ghép sau khi kết quả cả đợt đã băm (T-061 §5). '
              'Màu, hạng, vùng trên đồ thị vẫn là dự đoán của M1, không đổi theo đáp án. Đáp án gồm <b>root khai trước</b> '
              '(lỗi trên tuyến gọi: một <i>cạnh có hướng</i> bên gọi → bên được gọi) và <b>tập chấp nhận mức nút</b> (với cạnh: cả hai đầu). '
              'Mọi thành phần thuộc tập có dấu <b>◆</b> ở tên nút; ◆ chỉ nghĩa “thuộc tập chấp nhận”, không khẳng định từng đầu là chỗ tiêm '
              'hay M1 đã định vị đúng cạnh. Đây là hiển thị, không phải chấm điểm. Không dùng trang này để chẩn đoán.')
    o = lambda c: f'<span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:{c};margin:0 4px -1px 10px"></span>'
    html = (f'<div style="font-size:13px;line-height:1.5">{ch}<br>'
            f'<b>Màu nút:</b>{o(MAU["nghi_nguon"])}<b>#hạng</b> nghi là nguồn'
            f'{o(MAU["bi_keo_theo"])}<b>#hạng</b> bị kéo theo'
            f'{o(MAU["binh_thuong"])}bình thường (không ghi hạng)'
            f'{o(MAU["thieu_du_lieu"])}<b>?</b> thiếu dữ liệu (M1 không có kênh dùng được)<br>'
            '<span style="opacity:.75">Hạng do M1 xếp; nhiều thành phần có thể cùng hạng. Mã lớp M1, tầng, điểm và khóa xếp hạng '
            'chỉ có trong menu chi tiết của nút. Mốc sự cố do bộ điều phối cấp (chế độ a), Grafana không tự phát hiện.</span></div>')
    return {'id': pid(), 'type': 'text', 'title': '', 'gridPos': gp, 'transparent': True,
            'options': {'mode': 'html', 'content': html}}


def panel_danh_sach(gp, chinh=True):
    uid, slug = (UID_CHINH, SLUG_CHINH) if chinh else (UID_PL, SLUG_PL)
    chi_muc = 'chi-muc/danh-sach-su-co.json' if chinh else 'chi-muc/danh-sach-phat-lai.json'
    cols = [('moc', 'timestamp_epoch'), ('ma', 'string'), ('ket_luan', 'string'), ('nghi', 'string')]
    them = ''
    if not chinh:
        # Trường mới (F1′); chỉ mục cũ chưa sinh lại thì lùi về trường cũ và ghi rõ là chỉ mục cũ.
        them = ''', "dap_an": "dap_an_root" in $keys($) ? dap_an_root : dap_an_thanh_phan & " (chỉ mục cũ)",
                  "tap": "dap_an_tap" in $keys($) ? ($count(dap_an_tap) > 0 ? $join(dap_an_tap, ", ") : "—") : "chỉ mục cũ: chưa có tập",
                  "m1_tap": "m1_trong_tap" in $keys($) ? m1_trong_tap : "chỉ mục cũ: " & m1_vai_tro_cua_dap_an & ($exists(m1_hang_cua_dap_an) and m1_hang_cua_dap_an != null ? " #" & $string(m1_hang_cua_dap_an) : "") & " (chỉ phần tử đầu)",
                  "hang_tot": "hang_tot_nhat_e2_hien_thi" in $keys($) ? hang_tot_nhat_e2_hien_thi : "—",
                  "ho_loi": dap_an_ho_loi'''
        cols += [('dap_an', 'string'), ('tap', 'string'), ('m1_tap', 'string'), ('hang_tot', 'string'), ('ho_loi', 'string')]
    cols += [('trang_thai', 'string'), ('co_hang', 'string'), ('tu', 'string'), ('den', 'string')]
    expr = '''[su_co.{"moc": t_ms, "ma": ma, "ket_luan": ket_luan_hien_thi,
                      "nghi": nghi_nguon_hang_1 = "—" ? "—" : nghi_nguon_hang_1''' + them + ''',
                      "trang_thai": trang_thai = "OK" ? "chạy xong" : trang_thai = "NO_EVIDENCE" ? "không có bằng chứng" : "M1 lỗi: " & trang_thai,
                      "co_hang": $string(so_thuc_the_co_hang) & "/" & $string(so_thuc_the_quan_sat),
                      "tu": $string(t_ms - 900000), "den": $string(t_ms + 900000)}]'''
    ov = [ghi_de('moc', displayName='Mốc sự cố (giờ máy bạn)', unit='dateTimeAsLocal', **{'custom.width': 170}),
          ghi_de('ma', displayName='Mã sự cố (bấm để mở)', **{'custom.width': 150}, links=[
              {'title': 'Mở sự cố này',
               'url': f'/d/{uid}/{slug}?orgId=1&var-thu_muc=${{thu_muc}}&var-ca=${{__value.raw}}&from=${{__data.fields.tu}}&to=${{__data.fields.den}}'}]),
          ghi_de('ket_luan', displayName='Kết luận của M1'),
          ghi_de('nghi', displayName='M1 nghi là nguồn (#1)'),
          ghi_de('trang_thai', displayName='Trạng thái lượt M1', **{'custom.width': 150}),
          ghi_de('co_hang', displayName='M1 trả hạng / quan sát', **{'custom.width': 150})] + an_cot('tu', 'den')
    if not chinh:
        ov += [ghi_de('dap_an', displayName='ĐÁP ÁN: root khai trước'),
               ghi_de('tap', displayName='Tập chấp nhận mức nút'),
               ghi_de('m1_tap', displayName='M1 xếp các thành phần trong tập'),
               ghi_de('hang_tot', displayName='Hạng tốt nhất trong tập (theo e2)', **{'custom.width': 130}),
               ghi_de('ho_loi', displayName='Họ lỗi')]
    return panel_bang('Danh sách sự cố — mới nhất ở trên' + ('' if chinh else ' (có đáp án)'), gp,
                      [inf('ds', f'{URL_GOC}/{chi_muc}', expr, cols)], ov,
                      desc='Đọc file chỉ mục ' + chi_muc + ' trong thư mục kết quả. Bấm mã để mở; khung giờ đặt ±15 phút quanh mốc. '
                           '"M1 trả hạng / quan sát": số thành phần M1 trả hạng, kể cả nhóm bình thường xếp chung hạng; dashboard không hiện hạng của nhóm bình thường.'
                           + ('' if chinh else ' Hạng tốt nhất trong tập là số của e2 ở mức nút, không phải kết luận M1 định vị đúng cạnh.'))


def panel_su_co(gp, chinh=True):
    file_ca = '${ca}.json' if chinh else '${ca}.phat-lai.json'
    them = ''
    if not chinh:
        them = ''',
          {"k": "◆ ĐÁP ÁN: root khai trước", "v": $root ? $root : "không tiêm lỗi trong cửa sổ này"},
          {"k": "Họ lỗi", "v": phat_lai.ho_loi ? phat_lai.ho_loi : "—"},
          {"k": "Tập chấp nhận mức nút (◆ trên đồ thị)", "v": $count($tap) > 0 ? $join($tap, ", ") : "rỗng: không đánh dấu nút nào"},
          {"k": "Hạng tốt nhất trong tập (theo e2, mức nút; không phải kết luận M1 định vị đúng cạnh)", "v": $count($tap) = 0 ? "—" : "hang_tot_nhat" in $keys(phat_lai) ? (phat_lai.hang_tot_nhat ? "#" & $string(phat_lai.hang_tot_nhat) : "không có hạng") : "— (file không có trường này)"},
          {"k": "Nhận xét phát lại", "v": phat_lai.nhan_xet},
          {"k": "Cảnh báo", "v": phat_lai.canh_bao}'''
    expr = jexpr(('' if chinh else J_TAP) + '''
        $gio := function($u){ $u ? $substring($u, 0, 10) & " " & $substring($u, 11, 8) & " UTC" : "—" };
        $cs := function($w){ $w ? $substring($w.tu_utc, 11, 8) & " → " & $substring($w.den_utc, 11, 8) & " UTC" : "—" };
        [
          {"k": "Mã sự cố", "v": su_co.ma},
          {"k": "Kết luận của M1", "v": su_co.ket_luan_hien_thi ? su_co.ket_luan_hien_thi : "—"},
          {"k": "Trạng thái lượt M1", "v": (su_co.trang_thai = "OK" ? "chạy xong (OK)" : su_co.trang_thai = "NO_EVIDENCE" ? "chạy xong, không có kênh nào có cờ (NO_EVIDENCE)" : "M1 lỗi (" & su_co.trang_thai & ")") & (su_co.loi ? " — " & su_co.loi : "")},
          {"k": "Mốc sự cố", "v": $gio(su_co.moc.t_utc) & " (do bộ điều phối cấp)"},
          {"k": "Cửa sổ nền / sự cố", "v": $cs(su_co.cua_so_nen) & "  |  " & $cs(su_co.cua_so_su_co)},
          {"k": "M1 nghi là nguồn", "v": ( $x := nut[vai_tro = "nghi_nguon"]^($khoa($)); $count($x) > 0 ? $join($x.(("#" & $string(hang)) & " " & id), ", ") : "không có" )},
          {"k": "Bị kéo theo", "v": ( $x := nut[vai_tro = "bi_keo_theo"]^($khoa($)); $count($x) > 0 ? $join($x.(("#" & $string(hang)) & " " & id), ", ") : "không có" )},
          {"k": "Thiếu dữ liệu", "v": ( $x := nut[vai_tro = "thieu_du_lieu"]; $count($x) > 0 ? $join($x.id, ", ") : "không có" )},
          {"k": "Vùng nghi ngờ", "v": vung.ap_dung ? "gốc: " & $join(vung.goc, ", ") & " · cách 1: " & $join(vung.hop_cach_1, ", ") & " · cách 2: " & $join(vung.hop_cach_2, ", ") : "không áp dụng (" & (vung.ly_do ? vung.ly_do : "M1 không kết luận có nguồn") & ")"},
          {"k": "Độ phủ", "v": su_co.trang_thai in ["ERROR", "UNSUPPORTED"] ? "không có (M1 không trả kết quả)" : "M1 trả hạng cho " & $string(do_phu.so_tra_hang) & "/" & $string(do_phu.so_quan_sat) & " thành phần (kể cả nhóm bình thường xếp chung hạng); " & $string(do_phu.so_canh_quan_sat) & " cạnh gọi quan sát; " & $string($count(do_phu.thuc_the_khong_co_canh)) & " thành phần không có cạnh (DB, broker… M1 không thấy cạnh)"}''' + them + '''
        ]''')
    ov = [ghi_de('k', displayName='Mục', **{'custom.width': 120}),
          ghi_de('v', displayName='Giá trị', **{'custom.cellOptions': {'type': 'auto', 'wrapText': True}})]
    return panel_bang('Sự cố đang xem: ${ca:value}', gp, [inf('su_co', f'{URL_GOC}/{file_ca}', expr, [('k', 'string'), ('v', 'string')])],
                      ov, opts={'showHeader': False, 'cellHeight': 'sm'},
                      links=[{'title': '⏱ Đặt khung giờ dashboard đúng cửa sổ nền + sự cố',
                              'url': f'/d/{UID_CHINH if chinh else UID_PL}/{SLUG_CHINH if chinh else SLUG_PL}?orgId=1&var-thu_muc=${{thu_muc}}&var-ca=${{ca}}&var-dv=${{dv}}&from=${{t_tu}}&to=${{t_den}}'}],
                      desc='Bản ghi sự cố của định dạng 0.2. Cửa sổ nền/sự cố là cửa sổ M1 dùng.')


def panel_do_thi(gp, chinh=True):
    file_ca = '${ca}.json' if chinh else '${ca}.phat-lai.json'
    dap = ''
    tieu_de = 'id'
    if not chinh:
        dap = J_TAP
        tieu_de = '(id in $tap ? "◆ " & id : id)'
    # Bố cục cố định theo tầng gọi: hàng 0 = chỉ gọi đi, hàng 1 = vừa được gọi vừa gọi, hàng 2 = chỉ được gọi,
    # các hàng dưới = thành phần không có cạnh (5 nút một hàng). Chỉ là vị trí vẽ, không mang nghĩa xếp hạng.
    bo_cuc = '''
        $E := canh; $N := nut;
        $vao := function($i){ $count($E[dich = $i]) }; $ra := function($i){ $count($E[nguon = $i]) };
        $tang := function($i){ $vao($i) = 0 and $ra($i) > 0 ? 0 : $vao($i) > 0 and $ra($i) > 0 ? 1 : $vao($i) > 0 ? 2 : 3 };
        $cung := function($i){ $N[$tang(id) = $tang($i)].id };
        $vt_trong := function($i){ $count($cung($i)[$ < $i]) };
        $rong := $max([$count($cung($N[0].id)), 5, $count($N[$tang(id) = 0]), $count($N[$tang(id) = 1]), $count($N[$tang(id) = 2])]);
        $soHangCo := $count($distinct($N.$tang(id)[$ < 3]));
        $soHangHT := $ceil($count($N[$tang(id) = 3]) / 5);
        $cx := ($rong - 1) * 70; $cy := (($soHangCo + $soHangHT - 1) * 115 + ($soHangHT > 0 ? 30 : 0)) / 2;
        $x := function($i){ ( $t := $tang($i); $k := $vt_trong($i);
              ($t < 3 ? ($k + ($rong - $count($cung($i))) / 2) * 140 : (($k % 5) + ($rong - 5) / 2) * 140) - $cx ) };
        $y := function($i){ ( $t := $tang($i); $k := $vt_trong($i);
              ($t < 3 ? ( $l := $N.$tang(id)[$ < $t]; $exists($l) ? $count($distinct($l)) : 0 ) * 115 : ($soHangCo + $floor($k / 5)) * 115 + 30) - $cy ) };
    '''
    nodes = jexpr(dap + bo_cuc + '''
        [nut.{
          "id": id,
          "fixedX": $x(id), "fixedY": $y(id),
          "title": ''' + tieu_de + ''',
          "mainstat": $chu($),
          "secondarystat": $vt(vai_tro),
          "color": hien_thi.mau,
          "nodeRadius": 36,
          "svc": $svc(id),
                    "detail__hang": $co_hang($) ? "#" & $string(hang) & (so_dong_hang > 1 ? " (cùng hạng với " & $string(so_dong_hang - 1) & " thành phần khác)" : "") : ($exists(hang) and hang != null ? "— (bình thường: M1 không coi là nghi ngờ)" : "không có hạng"),
          "detail__vung": $vung($),
          "detail__bang_chung": $count(bang_chung) > 0 ? $string($count(bang_chung)) & " kênh: " & $join($filter(bang_chung, function($v, $i){ $i < 3 }).( $ngan($split($, "|")[1] = "op" ? $replace($split($, "|")[3], /([a-z_][a-z0-9_]*\\.)+/, "") : $split($, "|")[3]) & ( $contains($, "|len") ? " ↑" : " ↓") ), ", ") & ($count(bang_chung) > 3 ? ", … (+" & $string($count(bang_chung) - 3) & ", xem bảng bằng chứng)" : "") : "không có",
          "detail__lop_m1": lop_m1 & (tang_m1 ? " (tầng " & $string(tang_m1) & ")" : ""),
          "detail__diem": khoa_m1 ? "s lớn nhất = " & $formatNumber(khoa_m1[1], "#,##0.###") & "; số kênh có cờ = " & $string(khoa_m1[3]) : "—",
''' + ('' if chinh else '''
          "detail__dap_an": id in $tap ? "◆ thuộc tập chấp nhận mức nút của root " & $root : ($count($tap) > 0 ? "ngoài tập chấp nhận" : "không có tập chấp nhận (không tiêm lỗi)"),''') + '''
          "detail__khoa": khoa_m1 ? "[" & $join(khoa_m1.$formatNumber($, "0.###"), ", ") & "]" : "—"
        }]''')
    edges = jexpr('''
        [canh.{
          "id": id, "source": nguon, "target": dich,
          "color": $count(bang_chung) > 0 ? "#E02F44" : "#7a7a7a",
          "detail__chieu": "bên gọi → bên được gọi",
          "detail__nguon_goc": nguon_goc = "quan_sat" ? "quan sát được từ trace (span cha → span con)" : "quan sát hoặc mô hình tĩnh (M1 gộp, không tách được)",
          "detail__bang_chung": $count(bang_chung) > 0 ? $join(bang_chung, ", ") : "không có bằng chứng trên cạnh"
        }]''')
    ncols = [('id', 'string'), ('title', 'string'), ('mainstat', 'string'), ('secondarystat', 'string'), ('color', 'string'),
             ('nodeRadius', 'number'), ('fixedX', 'number'), ('fixedY', 'number'), ('svc', 'string'), ('detail__hang', 'string'),
             ('detail__vung', 'string'), ('detail__bang_chung', 'string'), ('detail__lop_m1', 'string'),
             ('detail__diem', 'string')]
    if not chinh:
        ncols.append(('detail__dap_an', 'string'))
    ncols.append(('detail__khoa', 'string'))
    ecols = [('id', 'string'), ('source', 'string'), ('target', 'string'), ('color', 'string'),
             ('detail__chieu', 'string'), ('detail__nguon_goc', 'string'), ('detail__bang_chung', 'string')]
    ten = {'detail__hang': 'Hạng chi tiết', 'detail__vung': 'Vùng nghi ngờ',
           'detail__bang_chung': 'Bằng chứng', 'detail__lop_m1': 'Mã lớp M1', 'detail__diem': 'Điểm M1 (không so giữa kênh)',
           'detail__khoa': 'Khóa xếp hạng M1 (3−tầng, max s, m, số kênh, Σs)', 'detail__chieu': 'Chiều',
           'detail__nguon_goc': 'Nguồn gốc cạnh', 'detail__dap_an': '◆ Tập chấp nhận (phát lại)'}
    ten.update({'title': 'Thành phần', 'mainstat': 'Hạng (chữ trên nút)', 'secondarystat': 'Vai trò (chữ dưới nút)', 'color': 'Màu theo vai trò'})
    # Node graph lấy nhãn menu từ config.displayName; override displayName không tới được, organize thì có.
    thu_tu = ['id', 'title', 'mainstat', 'secondarystat', 'detail__dap_an', 'detail__hang', 'detail__vung', 'detail__bang_chung',
              'detail__lop_m1', 'detail__diem', 'detail__khoa', 'color', 'nodeRadius', 'fixedX', 'fixedY', 'svc',
              'source', 'target', 'detail__chieu', 'detail__nguon_goc']
    bien_doi = [{'id': 'organize', 'options': {'renameByName': ten, 'indexByName': {k: i for i, k in enumerate(thu_tu)}, 'excludeByName': {}}}]
    ov = []
    ov.append(ghi_de('id', links=lien_ket_nut('${__data.fields.svc}') if chinh else lien_ket_nut('${__data.fields.svc}')[1:]))
    return {'id': pid(), 'type': 'nodeGraph', 'title': 'Đồ thị dịch vụ — sự cố ${ca:value}' + ('' if chinh else ' (phát lại)'),
            'description': 'Nút = thành phần M1 quan sát; cạnh = bên gọi → bên được gọi, M1 thấy từ trace. '
                           'Bấm nút để mở menu chi tiết. Thành phần hạ tầng (DB, broker, cache…) không có cạnh khi M1 không thấy cạnh tới chúng; '
                           'số lượng ở dòng Độ phủ của panel Sự cố đang xem.'
                           + ('' if chinh else ' ◆ = thuộc tập chấp nhận mức nút của đáp án.'),
            'gridPos': gp, 'datasource': DS,
            'targets': [inf('nodes', f'{URL_GOC}/{file_ca}', nodes, ncols), inf('edges', f'{URL_GOC}/{file_ca}', edges, ecols)],
            'fieldConfig': {'defaults': {}, 'overrides': ov}, 'transformations': bien_doi,
            'options': {'nodes': {'mainStatUnit': 'none', 'secondaryStatUnit': 'none', 'arcs': []},
                        'edges': {'mainStatUnit': 'none', 'secondaryStatUnit': 'none'},
                        'zoomMode': 'cooperative', 'layoutAlgorithm': 'layered'}}


def panel_hang(gp, chinh=True):
    uid, slug = (UID_CHINH, SLUG_CHINH) if chinh else (UID_PL, SLUG_PL)
    file_ca = '${ca}.json' if chinh else '${ca}.phat-lai.json'
    dap_col = ''
    if not chinh:
        dap_col = ''', "dap_an": id in $tap ? "◆ trong tập chấp nhận" : ""'''
    expr = jexpr(('' if chinh else J_TAP) + '''
        [nut^($khoa($), id).{
          "hang": $co_hang($) ? "#" & $string(hang) : vai_tro = "thieu_du_lieu" ? "?" : "",
          "ten": id,
          "vai_tro": $vt(vai_tro),
          "dong_hang": $co_hang($) and so_dong_hang > 1 ? "cùng hạng với " & $string(so_dong_hang - 1) & " khác" : "",
          "so_bc": $count(bang_chung),
          "vung": vai_tro = "binh_thuong" or vai_tro = "thieu_du_lieu" ? "" : $vung($)''' + dap_col + '''
        }]''')
    cols = [('hang', 'string'), ('ten', 'string'), ('vai_tro', 'string'), ('dong_hang', 'string'), ('so_bc', 'number'),
            ('vung', 'string')]
    if not chinh:
        cols.append(('dap_an', 'string'))
    ov = [ghi_de('hang', displayName='Hạng', **{'custom.width': 60}),
          ghi_de('ten', displayName='Thành phần (bấm để xem bằng chứng)', links=[
              {'title': 'Xem bằng chứng của thành phần này',
               'url': f'/d/{uid}/{slug}?orgId=1&var-thu_muc=${{thu_muc}}&var-ca=${{ca}}&var-dv=${{__value.raw}}&${{__url_time_range}}'}]),
          ghi_de('vai_tro', displayName='Vai trò', **{'custom.width': 120}), mau_vai_tro('vai_tro'),
          ghi_de('dong_hang', displayName='Đồng hạng'),
          ghi_de('so_bc', displayName='Số kênh có cờ', **{'custom.width': 110}),
          ghi_de('vung', displayName='Vùng nghi ngờ')]
    if not chinh:
        ov.append(ghi_de('dap_an', displayName='Tập chấp nhận (đáp án)'))
    return panel_bang('Bảng hạng thành phần — sự cố ${ca:value}', gp, [inf('hang', f'{URL_GOC}/{file_ca}', expr, cols)], ov,
                      desc='Thứ tự theo hạng M1. Thành phần bình thường không ghi hạng (hạng của nhóm bình thường không phải mức nghi ngờ). '
                           '"?" = thiếu dữ liệu, M1 không xếp hạng.')


def panel_bang_chung(gp, chinh=True):
    file_ca = '${ca}.json' if chinh else '${ca}.phat-lai.json'
    expr = jexpr('''
        $enc := function($s){ $encodeUrlComponent($s) };
        $url := function($b){ (
          $lk := $b.lien_ket[0];
          $lk = null ? "" :
          $lk.kho = "prometheus" ? (
              $k := $keys($lk.bo_loc_chuoi)[0];
              $q := $k ? "(" & $lk.truy_van & ") and on(" & $k & ") label_replace(vector(1), \\"" & $k & "\\", \\"" & $lookup($lk.bo_loc_chuoi, $k) & "\\", \\"\\", \\"\\")" : $lk.truy_van;
              "/explore?schemaVersion=1&orgId=1&panes=" & $enc($string({"a": {"datasource": "prometheus", "queries": [{"refId": "A", "datasource": {"type": "prometheus", "uid": "prometheus"}, "expr": $q, "range": true}], "range": {"from": $string($lk.cua_so_ms[0]), "to": $string($lk.cua_so_ms[1])}}}))
            ) :
          $lk.kho = "tempo" ?
              "/explore?schemaVersion=1&orgId=1&panes=" & $enc($string({"a": {"datasource": "tempo", "queries": [{"refId": "A", "datasource": {"type": "tempo", "uid": "tempo"}, "queryType": "traceql", "query": $lk.truy_van, "limit": 50, "tableType": "traces"}], "range": {"from": $string($lk.cua_so_ms[0]), "to": $string($lk.cua_so_ms[1])}}}))
            : ""
        ) };
        [bang_chung[thuc_the = "${dv}"]^(khoi_phat_ns).{
          "kenh": kenh,
          "loai": $substringBefore(don_vi, "|") = "metric" ? "chỉ số (metric)" : $substringBefore(don_vi, "|") = "op" ? "thao tác (span)" : $substringBefore(don_vi, "|") = "log" ? "log" : $substringBefore(don_vi, "|"),
          "huong": huong = "len" ? "tăng ↑" : huong = "xuong" ? "giảm ↓" : huong,
          "lan": lop = "lan_nguoc" ? "lan ngược" : lop = "lan_xuoi" ? "lan xuôi" : lop = "khong_lan" ? "không lan" : lop,
          "khoi_phat": $substring(khoi_phat_utc, 11, 8) & " UTC",
          "s": s,
          "mo": $count(lien_ket) > 0 ? (lien_ket[0].kho = "prometheus" ? "Prometheus ↗" : lien_ket[0].kho = "tempo" ? "Tempo ↗" : lien_ket[0].kho) : (ly_do_khong_lien_ket ? ly_do_khong_lien_ket : "—"),
          "url": $url($),
          "don_vi": don_vi
        }]''')
    cols = [('kenh', 'string'), ('loai', 'string'), ('huong', 'string'), ('lan', 'string'), ('khoi_phat', 'string'),
            ('s', 'number'), ('mo', 'string'), ('url', 'string'), ('don_vi', 'string')]
    ov = [ghi_de('kenh', displayName='Kênh có cờ'), ghi_de('loai', displayName='Loại', **{'custom.width': 130}),
          ghi_de('huong', displayName='Hướng', **{'custom.width': 80}),
          ghi_de('lan', displayName='Kiểu lan (E5)', **{'custom.width': 110}),
          ghi_de('khoi_phat', displayName='Khởi phát', **{'custom.width': 110}),
          ghi_de('s', displayName='Điểm s', decimals=3, **{'custom.width': 100}),
          ghi_de('mo', displayName='Mở dữ liệu gốc', **{'custom.width': 130}, links=[
              {'title': 'Mở trong Explore (cửa sổ nền + sự cố)', 'url': '${__data.fields.url:raw}', 'targetBlank': True}]),
          ghi_de('don_vi', displayName='Đơn vị M1')] + an_cot('url')
    return panel_bang('Bằng chứng của ${dv:value} — các kênh M1 gắn cờ', gp,
                      [inf('bc', f'{URL_GOC}/{file_ca}', expr, cols)], ov,
                      defaults=dict(BANG_MAC_DINH, noValue='Không có: M1 không gắn cờ kênh nào của thành phần này.'),
                      desc='Mỗi dòng là một kênh có cờ ở thế giới P. Điểm s mang đơn vị khác nhau theo kênh: chỉ so trong cùng kênh. '
                           'Liên kết Prometheus = truy vấn nguyên văn của adapter, lọc đúng chuỗi của thành phần; liên kết Tempo = tìm span cùng service và tên thao tác (không phải trace M1 chọn).')


def panel_ke_thua(gp, chinh=True):
    file_ca = '${ca}.json' if chinh else '${ca}.phat-lai.json'
    expr = '''[giai_thich_ke_thua[thuc_the = "${dv}"].{
          "kenh": $split(kenh_ma, "|")[3] & ($contains(kenh_ma, "|len") ? " ↑" : " ↓"),
          "boi": $split(giai_thich_boi, "|")[0] & ": " & $split(giai_thich_boi, "|")[3] & ($contains(giai_thich_boi, "|len") ? " ↑" : " ↓"),
          "duong": $join(duong, " → "),
          "quy_tac": quy_tac = "lan_nguoc" ? "lan ngược" : quy_tac = "lan_xuoi" ? "lan xuôi" : quy_tac,
          "trang_thai": trang_thai = "ap_dung" ? "áp dụng" : trang_thai }]'''
    cols = [('kenh', 'string'), ('boi', 'string'), ('duong', 'string'), ('quy_tac', 'string'), ('trang_thai', 'string')]
    ov = [ghi_de('kenh', displayName='Kênh của ${dv:value}'), ghi_de('boi', displayName='Được giải thích bởi'),
          ghi_de('duong', displayName='Đường lan'), ghi_de('quy_tac', displayName='Quy tắc E5', **{'custom.width': 100}),
          ghi_de('trang_thai', displayName='Trạng thái', **{'custom.width': 90})]
    return panel_bang('Vì sao ${dv:value} bị coi là kéo theo (giải thích E5 của M1)', gp,
                      [inf('kt', f'{URL_GOC}/{file_ca}', expr, cols)], ov,
                      desc='Suy luận của M1 theo quy tắc E5, không phải quan hệ nhân quả đã quan sát. Trống khi thành phần không bị kéo theo.',
                      defaults=dict(BANG_MAC_DINH, noValue='Không có: M1 không coi thành phần này là bị kéo theo.'))


def panel_prom(title, gp, expr, unit, desc):
    return {'id': pid(), 'type': 'timeseries', 'title': title, 'description': desc, 'gridPos': gp, 'datasource': PROM,
            'targets': [{'refId': 'A', 'datasource': PROM, 'expr': expr, 'legendFormat': '{{http_request_method}} {{http_route}}',
                         'range': True}],
            'fieldConfig': {'defaults': {'unit': unit, 'custom': {'lineWidth': 1, 'fillOpacity': 0, 'showPoints': 'never'}},
                            'overrides': []},
            'options': {'legend': {'displayMode': 'table', 'placement': 'right', 'calcs': ['max'], 'showLegend': True},
                        'tooltip': {'mode': 'multi', 'sort': 'desc'}}}


def cac_panel_thao_tac(y):
    sel = 'service_name="${dv_svc}"'
    mo_ta = ('Lớp thao tác (hướng 1): số đo theo route HTTP của service đang chọn, từ Prometheus, trong khung giờ của dashboard. '
             'Không phải đầu ra M1. Thành phần hạ tầng (DB, cache, broker) không có số đo này. Bấm ⏱ ở panel sự cố để đặt khung giờ đúng cửa sổ.')
    ps = [
        {'id': pid(), 'type': 'row', 'title': 'Lớp thao tác của ${dv:value} (service ${dv_svc}) — dữ liệu sống từ Prometheus / Tempo / Loki',
         'gridPos': {'h': 1, 'w': 24, 'x': 0, 'y': y}, 'collapsed': False, 'panels': []},
        panel_prom('Request/giây theo thao tác — ${dv_svc}', {'h': 9, 'w': 8, 'x': 0, 'y': y + 1},
                   f'sum by (http_request_method, http_route) (rate(http_server_request_duration_seconds_count{{{sel}}}[1m]))', 'reqps', mo_ta),
        panel_prom('Độ trễ p90 theo thao tác — ${dv_svc}', {'h': 9, 'w': 8, 'x': 8, 'y': y + 1},
                   f'histogram_quantile(0.9, sum by (le, http_request_method, http_route) (rate(http_server_request_duration_seconds_bucket{{{sel}}}[1m])))', 's', mo_ta),
        panel_prom('Lỗi 5xx/giây theo thao tác — ${dv_svc}', {'h': 9, 'w': 8, 'x': 16, 'y': y + 1},
                   f'sum by (http_request_method, http_route) (rate(http_server_request_duration_seconds_count{{{sel}, http_response_status_code=~"5.."}}[1m]))', 'reqps',
                   mo_ta + ' Nếu truy vấn thành công nhưng không trả dữ liệu: chưa có chuỗi metric HTTP server 5xx khớp service và khung giờ đang chọn. '
                           'Không suy ra service không có lỗi.'),
        {'id': pid(), 'type': 'table', 'title': 'Trace của ${dv_svc} trong khung giờ (bấm Trace ID để xem cây span cha → con)',
         'description': 'Tìm trace bằng TraceQL trên Tempo. Cây span trong trace là quan hệ cha–con quan sát được giữa các thao tác.',
         'gridPos': {'h': 10, 'w': 12, 'x': 0, 'y': y + 10}, 'datasource': TEMPO,
         'targets': [{'refId': 'A', 'datasource': TEMPO, 'queryType': 'traceql', 'query': '{resource.service.name="${dv_svc}"}',
                      'limit': 50, 'tableType': 'traces'}],
         'fieldConfig': {'defaults': {}, 'overrides': []}, 'options': {'showHeader': True, 'cellHeight': 'sm'}},
        {'id': pid(), 'type': 'logs', 'title': 'Log của ${dv_svc} có chữ error/exception/warn', 'gridPos': {'h': 10, 'w': 12, 'x': 12, 'y': y + 10},
         'description': 'Log từ Loki của service đang chọn, lọc chữ error/exception/warn, trong khung giờ của dashboard. Không phải đầu ra M1. '
                        'Nếu truy vấn thành công nhưng không trả dữ liệu: chưa có dòng log khớp service, khung giờ và bộ lọc error/exception/warn. '
                        'Không suy ra service không có lỗi.',
         'datasource': LOKI,
         'targets': [{'refId': 'A', 'datasource': LOKI, 'expr': '{service_name="${dv_svc}"} |~ "(?i)error|exception|warn"', 'queryType': 'range',
                      'maxLines': 200}],
         'options': {'showTime': True, 'wrapLogMessage': True, 'sortOrder': 'Descending', 'enableLogDetails': True,
                     'prettifyLogMessage': False, 'dedupStrategy': 'none'}},
    ]
    return ps


def dashboard(chinh=True):
    _id[0] = 0
    uid, ten = (UID_CHINH, 'RCA — xem sự cố (G2)') if chinh else (UID_PL, 'RCA — phát lại CÓ ĐÁP ÁN (G2)')
    panels = [panel_huong_dan({'h': 4, 'w': 24, 'x': 0, 'y': 0}, chinh),
              panel_danh_sach({'h': 7, 'w': 24, 'x': 0, 'y': 4}, chinh),
              panel_su_co({'h': 20, 'w': 8, 'x': 0, 'y': 11}, chinh),
              panel_do_thi({'h': 20, 'w': 16, 'x': 8, 'y': 11}, chinh),
              panel_hang({'h': 13, 'w': 9, 'x': 0, 'y': 31}, chinh),
              panel_bang_chung({'h': 8, 'w': 15, 'x': 9, 'y': 31}, chinh),
              panel_ke_thua({'h': 5, 'w': 15, 'x': 9, 'y': 39}, chinh)]
    if chinh:
        panels += cac_panel_thao_tac(44)
    links = ([{'title': 'Trang phát lại (chỉ mở khi đã chấm xong cả đợt)', 'type': 'link', 'icon': 'external link',
               'url': f'/d/{UID_PL}/{SLUG_PL}', 'targetBlank': False}] if chinh else
             [{'title': 'Về trang chính (không đáp án)', 'type': 'link', 'icon': 'dashboard', 'url': f'/d/{UID_CHINH}/{SLUG_CHINH}'}])
    return {'uid': uid, 'title': ten, 'tags': ['rca', 'T-062', 'G2'], 'timezone': 'browser', 'editable': True,
            'schemaVersion': 41, 'version': 1, 'refresh': '', 'graphTooltip': 0,
            'time': {'from': 'now-6h', 'to': 'now'}, 'links': links,
            'description': ('Giao diện G2 (T-062): danh sách sự cố → đồ thị → hạng → bằng chứng → Explore. Trang này chỉ hiện dự đoán của M1.' if chinh else
                            'Phát lại có đáp án (ghép sau khi băm cả đợt). Tách khỏi trang chính.'),
            'templating': {'list': cac_bien(chinh)}, 'annotations': {'list': []}, 'panels': panels}


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    RA.mkdir(parents=True, exist_ok=True)
    for chinh, ten in ((True, 'rca-g2-chinh.json'), (False, 'rca-g2-phat-lai.json')):
        d = dashboard(chinh)
        s = json.dumps(d, ensure_ascii=False, indent=1)
        if chinh:
            # chốt: trang chính không trỏ tới thư mục/khối đáp án
            for cam in ('phat_lai.', '.phat-lai.json', 'danh-sach-phat-lai', 'thanh_phan_tiem', 'tap_chap_nhan'):
                assert cam not in s, f'trang chính chứa {cam}'
            assert 'đáp án' not in s.lower(), 'trang chính chứa chữ "đáp án"'
        (RA / ten).write_text(s + '\n', encoding='utf-8')
        print(RA / ten, len(s))
    (RA / 'provider.yaml').write_text(
        'apiVersion: 1\nproviders:\n  - name: rca-g2\n    folder: RCA\n    type: file\n    disableDeletion: false\n'
        '    allowUiUpdates: true\n    updateIntervalSeconds: 30\n    options:\n      path: /etc/grafana/provisioning/dashboards\n'
        '      foldersFromFilesStructure: false\n', encoding='utf-8')


if __name__ == '__main__':
    sys.exit(main())
