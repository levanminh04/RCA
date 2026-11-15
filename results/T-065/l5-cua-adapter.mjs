// L5: tương thích CUA mới; không đổi nguồn dashboard hoặc kết quả M1.
export function adaptL5(runner, deep, tab) {
  if (!runner.cuaAdapted) {
    const originalPanel = runner.panel.bind(runner);
    runner.panel = function (id) {
      const panel = originalPanel(id);
      if (id !== 4 && id !== 25) return panel;
      return new Proxy(panel, { get(target, key) {
        if (key === 'getByRole') return (role, options) => role === 'link' && options?.name
          ? target.getByText(options.name, { exact: !!options.exact })
          : target.getByRole(role, options);
        const value = target[key];
        return typeof value === 'function' ? value.bind(target) : value;
      } });
    };
    runner.cuaAdapted = true;
  }
  const originalReady = deep.opReady.bind(deep);
  deep.opReady = async function () {
    const links = await runner.panel(25).getByRole('link').evaluateAll(es => es.map(e => e.getAttribute('href')));
    // Grafana còn giữ bảng trước trong lúc tải. Chỉ đọc khi link đã khớp op hiện tại.
    if (!this.op.lien_ket.every(link => links.includes(link.url))) return 'pending';
    return originalReady();
  };
  return deep;
}
