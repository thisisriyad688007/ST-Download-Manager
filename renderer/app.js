
// --- Quality Selector Modal Injection & Interceptor ---
(function() {
  const dlg = document.createElement("dialog");
  dlg.id = "st-quality-dlg";
  dlg.style.cssText = "border:1px solid #0078d7;border-radius:6px;padding:16px;background:#1e1e1e;color:#fff;min-width:320px;z-index:99999;";
  dlg.innerHTML = `
    <h4 id="st-q-title" style="margin:0 0 10px 0;font-size:13px;color:#61afef;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:300px;">Loading video info...</h4>
    <div style="margin-bottom:12px;">
      <label style="display:block;margin-bottom:5px;font-size:11px;color:#aaa;">Select Quality:</label>
      <select id="st-q-select" style="width:100%;padding:6px;background:#2d2d2d;color:#fff;border:1px solid #444;border-radius:4px;outline:none;"></select>
    </div>
    <div style="display:flex;justify-content:flex-end;gap:8px;">
      <button id="st-q-cancel" type="button" style="padding:4px 10px;background:#444;color:#fff;border:none;border-radius:3px;cursor:pointer;">Cancel</button>
      <button id="st-q-download" type="button" style="padding:4px 12px;background:#0078d7;color:#fff;border:none;border-radius:3px;cursor:pointer;">Download</button>
    </div>
  `;
  document.body.appendChild(dlg);
})();

window.askVideoQuality = function(videoUrl) {
  const dlg = document.getElementById("st-quality-dlg");
  const title = document.getElementById("st-q-title");
  const sel = document.getElementById("st-q-select");
  const btnOk = document.getElementById("st-q-download");
  const btnCancel = document.getElementById("st-q-cancel");

  title.textContent = "Fetching formats...";
  sel.innerHTML = "<option>Please wait...</option>";
  btnOk.disabled = true;
  dlg.showModal();

  return new Promise((resolve, reject) => {
    btnCancel.onclick = () => { dlg.close(); reject(new Error("Cancelled")); };
    
    const apiCall = window.electronAPI?.invoke || window.ipcRenderer?.invoke;
    if (!apiCall) {
      dlg.close();
      return resolve(null);
    }

    apiCall("fetch-video-resolutions", videoUrl)
      .then(info => {
        title.textContent = info.title || "Choose Quality";
        sel.innerHTML = "";
        (info.formats || []).forEach(f => {
          const opt = document.createElement("option");
          opt.value = f.format_id;
          opt.textContent = f.label;
          sel.appendChild(opt);
        });
        btnOk.disabled = false;
        btnOk.onclick = () => {
          const chosen = sel.value;
          dlg.close();
          resolve(chosen);
        };
      })
      .catch(err => {
        dlg.close();
        resolve(null);
      });
  });
};


