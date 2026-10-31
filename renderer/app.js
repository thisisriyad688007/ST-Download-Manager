// --- Quality Selector Modal Injection & Interceptor ---
(function initQualityModal() {
  const modal = document.createElement('dialog');
  modal.id = 'quality-dialog';
  modal.style.cssText = 'border:1px solid #0078d7;border-radius:6px;padding:16px;background:#202020;color:#fff;min-width:320px;z-index:99999;box-shadow:0 8px 24px rgba(0,0,0,0.6);';
  modal.innerHTML = '<h4 id="quality-title" style="margin:0 0 10px 0;font-size:13px;color:#61afef;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:300px;">Fetching video info...</h4>' +
    '<div style="margin-bottom:12px;"><label style="display:block;margin-bottom:5px;font-size:11px;color:#aaa;">Select Quality:</label>' +
    '<select id="quality-select" style="width:100%;padding:6px;background:#111;color:#fff;border:1px solid #444;border-radius:4px;outline:none;"></select></div>' +
    '<div style="display:flex;justify-content:flex-end;gap:8px;">' +
    '<button id="quality-cancel" type="button" style="padding:4px 10px;background:#444;color:#fff;border:none;border-radius:3px;cursor:pointer;">Cancel</button>' +
    '<button id="quality-download" type="button" style="padding:4px 12px;background:#0078d7;color:#fff;border:none;border-radius:3px;cursor:pointer;">Download</button></div>';
  document.body.appendChild(modal);
})();

window.promptQuality = function(videoUrl) {
  const dlg = document.querySelector('#quality-dialog');
  const title = document.querySelector('#quality-title');
  const sel = document.querySelector('#quality-select');
  const btnOk = document.querySelector('#quality-download');
  const btnCancel = document.querySelector('#quality-cancel');

  title.textContent = 'Loading video formats...';
  sel.innerHTML = '<option>Please wait...</option>';
  btnOk.disabled = true;
  dlg.showModal();

  return new Promise((resolve, reject) => {
    btnCancel.onclick = () => { dlg.close(); reject(new Error('Cancelled')); };
    
    window.electronAPI.invoke('fetch-video-resolutions', videoUrl)
      .then(info => {
        title.textContent = info.title || 'Choose Resolution';
        sel.innerHTML = '';
        (info.formats || []).forEach(f => {
          const opt = document.createElement('option');
          opt.value = f.format_id;
          opt.textContent = f.label;
          sel.appendChild(opt);
        });
        btnOk.disabled = false;
        btnOk.onclick = () => {
          const val = sel.value;
          dlg.close();
          resolve(val);
        };
      })
      .catch(err => {
        dlg.close();
        reject(err);
      });
  });
};


