import re

file_path = 'core/templates/base_new.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

loader_html = """
    <!-- Global Loader Overlay -->
    <div id="loader-overlay" style="display: none; position: fixed; inset: 0; background: rgba(255, 255, 255, 0.9); z-index: 9999; flex-direction: column; align-items: center; justify-content: center; text-align: center; transition: opacity 0.2s ease;">
        <i class="ri-loader-4-line ri-spin" style="font-size: 3rem; color: var(--primary);"></i>
        <p style="margin-top: 1rem; font-size: 1.1rem; font-weight: 600; color: var(--text-main);">Processing...</p>
        
        <div id="loader-progress-track" style="width: 240px; height: 4px; background: rgba(0,0,0,0.05); border-radius: 2px; margin: 16px auto 0; overflow: hidden; position: relative;">
            <div id="loader-progress-bar" style="width: 0%; height: 100%; background: linear-gradient(90deg, var(--primary), #60a5fa); border-radius: 2px; transition: width 0.3s ease;"></div>
        </div>
        <div id="loader-progress-label" style="font-size: 12px; color: var(--text-muted); text-align: center; margin-top: 8px; font-family: 'Courier New', monospace; letter-spacing: 1px;">0%</div>
    </div>
"""

# add loader_html right before </body>
if 'id="loader-overlay"' not in content:
    content = content.replace('</body>', loader_html + '\n</body>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Added global loader to base_new.html")
