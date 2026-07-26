import re

file_path = 'core/templates/base_new.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

js_block = """
<script>
(function () {

  // ── Elements ───────────────────────────────────
  const overlay = document.getElementById('loader-overlay');
  const bar     = document.getElementById('loader-progress-bar');
  const label   = document.getElementById('loader-progress-label');

  let fakeTimer   = null;
  let currentPct  = 0;
  let loaderShown = false;
  let xhrCount    = 0; // track concurrent requests

  // ── Progress Helpers ───────────────────────────

  function setProgress(pct) {
    currentPct = Math.min(Math.max(pct, 0), 100);
    if (bar)   bar.style.width     = currentPct + '%';
    if (label) label.textContent   = Math.round(currentPct) + '%';
  }

  function showLoader() {
    if (loaderShown) return;
    loaderShown = true;
    setProgress(0);
    if (overlay) {
      overlay.style.display  = 'flex';
      overlay.style.opacity  = '0';
      setTimeout(function () {
        overlay.style.transition = 'opacity 0.2s ease';
        overlay.style.opacity    = '1';
      }, 10);
    }
  }

  function hideLoader() {
    if (!loaderShown) return;
    setProgress(100);
    setTimeout(function () {
      if (overlay) {
        overlay.style.opacity = '0';
        setTimeout(function () {
          overlay.style.display = 'none';
          overlay.style.opacity = '1';
          loaderShown = false;
          setProgress(0);
        }, 200);
      }
    }, 300);
    stopFakeProgress();
  }

  // ── Staged Fake Progress ───────────────────────
  // Used for navigation and non-XHR actions where
  // real progress is not measurable

  function startFakeProgress() {
    clearInterval(fakeTimer);
    setProgress(0);

    const stages = [
      { target: 25,  step: 3,    ms: 30  },
      { target: 55,  step: 1.5,  ms: 50  },
      { target: 75,  step: 0.8,  ms: 70  },
      { target: 88,  step: 0.3,  ms: 100 },
      { target: 93,  step: 0.1,  ms: 150 },
    ];

    let i = 0;
    function runStage() {
      if (i >= stages.length) return;
      const s = stages[i];
      fakeTimer = setInterval(function () {
        if (currentPct >= s.target) {
          clearInterval(fakeTimer);
          i++;
          runStage();
        } else {
          setProgress(currentPct + s.step);
        }
      }, s.ms);
    }
    runStage();
  }

  function stopFakeProgress() {
    clearInterval(fakeTimer);
  }

  // ── CSRF Helper ────────────────────────────────

  function getCsrf() {
    const el = document.querySelector('[name=csrfmiddlewaretoken]');
    if (el) return el.value;
    const match = document.cookie.match(
      /csrftoken=([^;]+)/
    );
    return match ? match[1] : '';
  }

  // ── Should Skip? ───────────────────────────────

  function shouldSkip(el) {
    if (!el) return false;
    if (el.dataset.noLoader === 'true') return true;
    
    // Auto-skip common interactive elements that don't reload page
    if (el.classList && (
        el.classList.contains('tab') || 
        el.classList.contains('accordion-toggle') ||
        el.classList.contains('close-modal-btn') ||
        el.classList.contains('sidebar-toggle') ||
        el.classList.contains('dropdown-toggle')
    )) return true;
    
    if (el.dataset.bsToggle || el.dataset.toggle || el.dataset.modalTarget || el.dataset.drawerTarget) return true;
    
    return false;
  }

  function isExternalHref(href) {
    if (!href) return false;
    return href.startsWith('http://') ||
           href.startsWith('https://') ||
           href.startsWith('//');
  }

  function isVoidHref(href) {
    if (!href) return true;
    return href === '#' ||
           href.startsWith('javascript:') ||
           href === '';
  }

  // ── Category 1: Form Submissions ──────────────

  document.addEventListener('submit', function (e) {
    const form = e.target;
    if (shouldSkip(form)) return;

    // Skip GET forms (search, filters)
    const method = (form.method || 'get').toLowerCase();
    if (method === 'get') return;

    showLoader();
    startFakeProgress();
  }, true);

  // ── Category 2: Link / Button Navigation ──────

  document.addEventListener('click', function (e) {
    const el = e.target.closest('a, button');
    if (!el) return;
    if (shouldSkip(el)) return;

    // Anchor tags
    if (el.tagName === 'A') {
      const href = el.getAttribute('href');
      if (isVoidHref(href)) return;
      if (isExternalHref(href)) return;
      // Skip download links if they have download attribute
      if (el.hasAttribute('download')) return;
      // Skip target="_blank"
      if (el.getAttribute('target') === '_blank') return;
      
      showLoader();
      startFakeProgress();
      return;
    }

    // Buttons
    if (el.tagName === 'BUTTON') {
      const type = (el.type || 'submit').toLowerCase();

      if (type === 'button') {
        const hasAction = el.dataset.action ||
                          el.form ||
                          el.closest('form');
        if (!hasAction) return;
        return;
      }
      if (type === 'submit') return;
      if (type === 'reset') return;
    }
  }, true);

  // ── Category 3: Global XHR Intercept ──────────

  const OrigXHR = window.XMLHttpRequest;
  function PatchedXHR() {
    const xhr = new OrigXHR();

    xhr.addEventListener('loadstart', function () {
      xhrCount++;
      showLoader();
      startFakeProgress();
    });

    xhr.upload.addEventListener('progress', function (evt) {
      if (evt.lengthComputable && xhrCount <= 1) {
        stopFakeProgress();
        setProgress((evt.loaded / evt.total) * 55);
      }
    });

    xhr.addEventListener('progress', function (evt) {
      if (evt.lengthComputable && xhrCount <= 1) {
        stopFakeProgress();
        setProgress(55 + (evt.loaded / evt.total) * 40);
      }
    });

    xhr.addEventListener('loadend', function () {
      xhrCount = Math.max(0, xhrCount - 1);
      if (xhrCount === 0) hideLoader();
    });

    return xhr;
  }
  PatchedXHR.prototype = OrigXHR.prototype;
  window.XMLHttpRequest = PatchedXHR;

  // ── Global fetch() Intercept ──────────────────

  const origFetch = window.fetch;
  window.fetch = function () {
    xhrCount++;
    showLoader();
    startFakeProgress();
    return origFetch.apply(this, arguments)
      .then(function (response) {
        xhrCount = Math.max(0, xhrCount - 1);
        if (xhrCount === 0) hideLoader();
        return response;
      })
      .catch(function (err) {
        xhrCount = Math.max(0, xhrCount - 1);
        if (xhrCount === 0) hideLoader();
        throw err;
      });
  };

  // ── Category 4: Browser Back / Forward ────────

  window.addEventListener('popstate', function () {
    showLoader();
    startFakeProgress();
  });

  // ── Category 5: Page Unload ───────────────────

  window.addEventListener('beforeunload', function () {
    showLoader();
  });

  // ── Safety: Hide on DOMContentLoaded ──────────

  document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
      if (loaderShown) hideLoader();
    }, 100);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && loaderShown) {
      hideLoader();
    }
  });

  window.PASLoader = {
    show:        showLoader,
    hide:        hideLoader,
    setProgress: setProgress,
    startFake:   startFakeProgress,
    stopFake:    stopFakeProgress,
  };

})();
</script>
"""

# append to base_new.html before </body> if not there
if 'window.PASLoader' not in content:
    content = content.replace('</body>', js_block + '\n</body>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Added global JS to base_new.html")
