import re

def main():
    file_path = r'c:\Users\Kyle\Desktop\projects\pastrack-versions\cloneD\PASTrack\core\templates\core\submit_case.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace the entire CSS block with the new CSS
    css_start = content.find('{% block extra_css %}')
    css_end = content.find('{% endblock %}', css_start) + len('{% endblock %}')
    
    new_css = '''{% block extra_css %}
<style>
/* New Wizard Progress CSS */
.step-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    font-weight: 500;
    color: #94a3b8;
}
.step-indicator.active {
    color: #4f46e5;
}
.step-indicator.done {
    color: #94a3b8;
}
.step-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #e2e8f0;
    display: inline-block;
    flex-shrink: 0;
}
.step-indicator.active .step-dot {
    background: #4f46e5;
    box-shadow: 0 0 0 3px rgba(79,70,229,0.15);
}
.step-indicator.done .step-dot {
    background: #a5b4fc;
}

/* Input Form Styling */
input[type="text"],
input[type="email"],
input[type="tel"],
input[type="number"],
select,
textarea {
    width: 100%;
    border: 1.5px solid #e2e8f0;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 14px;
    color: #1e293b;
    background: #f8fafc;
    outline: none;
    transition: border-color 0.15s, 
                box-shadow 0.15s,
                background 0.15s;
}
input:focus, select:focus, textarea:focus {
    border-color: #6366f1;
    background: #fff;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12);
}
input::placeholder, textarea::placeholder {
    color: #cbd5e1;
}
label {
    display: block;
    font-size: 13px;
    font-weight: 500;
    color: #374151;
    margin-bottom: 5px;
}
.form-group {
    margin-bottom: 20px;
}
.error-msg {
    font-size: 0.75rem;
    color: #dc2626;
    margin-top: 0.2rem;
    display: block;
}
.alert-error {
    background: #fee2e2;
    color: #991b1b;
    padding: 0.75rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
    font-size: 0.85rem;
}

/* Step 2 Document Upload Card Styling */
.doc-upload-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border: 1.5px solid #e2e8f0;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 10px;
    background: #fff;
    transition: border-color 0.15s;
}
.doc-upload-card.uploaded {
    border-color: #bbf7d0;
    background: #f0fdf4;
}
.doc-upload-left {
    display: flex;
    align-items: center;
    gap: 12px;
}
.doc-upload-icon {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    background: #f1f5f9;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    color: #64748b;
    flex-shrink: 0;
}
.doc-upload-card.uploaded .doc-upload-icon {
    background: #dcfce7;
    color: #16a34a;
}
.doc-upload-name {
    display: block;
    font-size: 13px;
    font-weight: 500;
    color: #1e293b;
}
.doc-upload-filename {
    display: block;
    font-size: 11px;
    color: #16a34a;
    margin-top: 2px;
}
.doc-upload-hint {
    display: block;
    font-size: 11px;
    color: #94a3b8;
    margin-top: 2px;
}
.doc-upload-btn {
    background: #4f46e5;
    color: #fff;
    font-size: 12px;
    font-weight: 600;
    padding: 7px 14px;
    border-radius: 7px;
    cursor: pointer;
    white-space: nowrap;
    transition: background 0.15s;
    border: none;
}
.doc-upload-btn:hover {
    background: #4338ca;
}

/* Misc old classes that might be needed by JS */
.view-pending, .view-dropzone, .view-completed { display: none; }
.state-pending .view-pending { display: flex; align-items: center; justify-content: space-between; width: 100%; }
.state-dropzone .view-dropzone { display: block; width: 100%; }
.state-completed .view-completed { display: flex; align-items: center; justify-content: space-between; width: 100%; }

.icon-btn {
    width: 32px;
    height: 32px;
    border-radius: 6px;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: 0.2s;
    background: transparent;
}
.icon-btn:hover { background-color: #f1f5f9; }
.delete-btn { color: #ef4444; }
.rename-btn { color: #3b82f6; }

/* Grid for Step 1 */
.form-grid { display: grid; grid-template-columns: repeat(12, 1fr); gap: 1.25rem 1rem; }
.col-2 { grid-column: span 2; }
.col-4 { grid-column: span 4; }
.col-6 { grid-column: span 6; }
.col-12 { grid-column: span 12; }
@media (max-width: 1023px) {
    .col-2, .col-4, .col-6, .col-12 { grid-column: span 12; }
}

/* Modal Animations */
@keyframes slideDown { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
</style>
{% endblock %}'''

    content = content[:css_start] + new_css + content[css_end:]

    # 2. Replace the main layout wrappers
    content_start = content.find('{% block content %}')
    content_end = content.find('{% endblock %}', content_start) + len('{% endblock %}')
    
    # Extract parts before mutating content for offsets
    main_content_start = content.find('<!-- ===== RIGHT COLUMN: MAIN CONTENT ===== -->')
    step1_start = content.find('{% if step == 1 %}', main_content_start)
    step2_start = content.find('{% elif step == 2 %}', main_content_start)
    step3_start = content.find('{% else %}', step2_start)
    
    # Extract Step 1 form (from after {% if step == 1 %} up to the form actions)
    step1_body = content[step1_start + len('{% if step == 1 %}'):content.find('<div class="form-actions"', step1_start)]
    step1_body = re.sub(r'<div class="wizard-right-card step-1-card">.*?<form', '<form', step1_body, flags=re.DOTALL)
    
    # Extract Modals from Step 1
    step1_modals_start = content.find('<!-- Minimalistic Validation Modal for Step 1 Draft -->', step1_start)
    step1_modals = content[step1_modals_start:step2_start].replace('</div>\n                </form>', '').replace('</div>\n            </div>', '')

    # Extract Modals from Step 2
    step2_modals_start = content.find('<!-- Minimalistic Validation Modal for Step 2 Uploads -->', step2_start)
    step2_modals = content[step2_modals_start:step3_start].replace('</div>\n                </form>', '').replace('</div>\n            </div>', '')

    new_content_block = f'''{{% block content %}}
<div class="min-h-screen bg-white flex flex-col">

  <!-- Top of page, full width -->
  <div class="w-full relative">
    <a href="{{% url 'dashboard' %}}" class="text-xs text-gray-400 hover:text-gray-600 absolute top-4 left-6">&#8592; Back to Dashboard</a>
    
    <!-- Step Labels -->
    <div class="flex justify-center gap-12 py-4 mt-6">
      <div class="step-indicator {{% if step == 1 %}}active{{% elif step > 1 %}}done{{% else %}}inactive{{% endif %}}">
        <span class="step-dot"></span>
        <span class="step-label">General Information</span>
      </div>
      <div class="step-indicator {{% if step == 2 %}}active{{% elif step > 2 %}}done{{% else %}}inactive{{% endif %}}">
        <span class="step-dot"></span>
        <span class="step-label">Checklist & Attachments</span>
      </div>
      <div class="step-indicator {{% if step == 3 %}}active{{% else %}}inactive{{% endif %}}">
        <span class="step-dot"></span>
        <span class="step-label">Review & Submit</span>
      </div>
    </div>

    <!-- Progress Bar -->
    <div class="w-full h-0.5 bg-gray-100">
      <div class="h-0.5 bg-indigo-600 transition-all duration-500"
           style="width: {{% if step == 1 %}}33%{{% elif step == 2 %}}66%{{% else %}}100%{{% endif %}}">
      </div>
    </div>
  </div>

  <!-- Centered content -->
  <div class="flex-1 flex flex-col items-center justify-start pt-12 pb-16 px-4">
    <div class="w-full max-w-2xl">

      <!-- Step heading -->
      <div class="mb-8 text-center">
        <h1 class="text-3xl font-bold text-gray-900 tracking-tight mb-2">
          {{% if step == 1 %}}
            Let's set up the case
          {{% elif step == 2 %}}
            Upload required documents
          {{% else %}}
            Review before submitting
          {{% endif %}}
        </h1>
        <p class="text-sm text-gray-400">
          {{% if step == 1 %}}
            Fill in the client details and property information accurately.
          {{% elif step == 2 %}}
            Upload all supporting documents for this transaction type.
          {{% else %}}
            Confirm all details are correct before final submission.
          {{% endif %}}
        </p>
      </div>

      {{% if step == 1 %}}
      {step1_body}
        
      <!-- Navigation buttons for Step 1 -->
      <div class="flex items-center justify-between mt-10 pt-6 border-t border-gray-100">
        <div class="flex gap-4">
          <button type="submit" id="btn-draft-step1" name="save_draft" value="1" class="text-sm font-semibold text-gray-600 bg-white border border-gray-200 px-6 py-2.5 rounded-lg hover:bg-gray-50 transition-colors" formnovalidate>Save as Draft</button>
        </div>
        <button type="submit" name="save_continue" value="1" class="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold px-6 py-2.5 rounded-lg transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
          Next Step &#8594;
        </button>
      </div>
      
      {step1_modals}
      </form>
      
      {{% elif step == 2 %}}
      <form method="post" enctype="multipart/form-data">
        {{% csrf_token %}}
        {{{{ formset.management_form }}}}

        {{% if formset.non_form_errors %}}
        <div class="alert-error">{{{{ formset.non_form_errors }}}}</div>
        {{% endif %}}

        <div class="doc-list">
            {{% for row in rows %}}
            <div class="doc-upload-card doc-row {{% if row.doc and row.doc.file %}}uploaded state-completed{{% else %}}state-pending{{% endif %}}"
                id="row-{{{{ forloop.counter0 }}}}" data-is-custom="{{{{ row.is_custom|yesno:'true,false' }}}}">

                <div style="display: none;">
                    {{{{ row.form.doc_type }}}}
                    {{{{ row.form.custom_doc_type }}}}
                    {{{{ row.form.old_doc_type }}}}
                    {{{{ row.form.file }}}}
                    {{{{ row.form.is_deleted }}}}
                </div>

                <div class="doc-upload-left">
                    <div class="doc-upload-icon">
                        {{% if row.doc and row.doc.file %}}
                            <i class="ri-check-line text-lg"></i>
                        {{% else %}}
                            <i class="ri-file-text-line text-lg"></i>
                        {{% endif %}}
                    </div>
                    <div class="doc-upload-info">
                        <span class="doc-upload-name">
                            <span class="custom-name-display" style="{{% if not row.is_custom %}}display: none;{{% endif %}}">{{{{ row.form.custom_doc_type.value|default:row.doc_type|default:"Custom Document" }}}}</span>
                            <span class="standard-name-display" style="{{% if row.is_custom %}}display: none;{{% endif %}}">{{{{ row.doc_type }}}}</span>
                        </span>
                        {{% if row.doc and row.doc.file %}}
                        <span class="doc-upload-filename" id="filename-{{{{ forloop.counter0 }}}}">
                            {{{{ row.filename|default:row.doc.file.name|cut:"cases/" }}}}
                        </span>
                        {{% else %}}
                        <span class="doc-upload-hint" id="filename-{{{{ forloop.counter0 }}}}">
                            PDF, JPG, PNG accepted (Max 25MB)
                        </span>
                        {{% endif %}}
                    </div>
                </div>

                <div class="flex items-center gap-2">
                    {{% if row.is_custom %}}
                        <button type="button" class="icon-btn rename-btn" style="{{% if not row.is_custom %}}display: none;{{% endif %}}" onclick="renameCustomDoc('row-{{{{ forloop.counter0 }}}}')" title="Rename Document"><i class="ri-edit-line"></i></button>
                    {{% endif %}}
                    {{% if row.doc_type != 'Legacy Document Scan' %}}
                        <button type="button" class="icon-btn delete-btn" onclick="confirmDeleteDoc('row-{{{{ forloop.counter0 }}}}', '{{{{ row.form.file.id_for_label }}}}')" title="Remove"><i class="ri-delete-bin-fill"></i></button>
                    {{% endif %}}
                    <label class="doc-upload-btn mb-0" onclick="document.getElementById('{{{{ row.form.file.id_for_label }}}}').click();">
                        {{% if row.doc and row.doc.file %}}
                            &#8635; Replace
                        {{% else %}}
                            + Upload
                        {{% endif %}}
                    </label>
                </div>
            </div>
            {{% endfor %}}
        </div>
        
        <div id="custom-add-container" style="padding-top: 1rem;">
            <div id="btn-show-custom-input" style="display: flex; justify-content: flex-start; align-items: center; width: 100%;">
                <button type="button" onclick="this.parentElement.style.display='none'; document.getElementById('custom-input-wrapper').style.display='flex'; document.getElementById('custom_attachment_name').focus();" style="background: transparent; color: #4f46e5; border: none; font-weight: 600; padding: 0.5rem 0; cursor: pointer; display: flex; align-items: center; gap: 0.4rem; font-size: 13px;">
                    <i class="ri-add-line"></i> Add Document
                </button>
            </div>
            
            <div id="custom-input-wrapper" style="display: none; justify-content: space-between; align-items: center; width: 100%;" class="doc-upload-card">
                <div class="doc-upload-left w-full">
                    <input type="text" id="custom_attachment_name" placeholder="Name of the Attachment" style="flex:1; padding: 0.6rem 0.8rem; border: 1.5px solid #e2e8f0; border-radius: 6px; font-size: 13px; outline: none;" onfocus="this.style.borderColor='#4f46e5'" onblur="this.style.borderColor='#e2e8f0'" />
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-left: 10px;">
                    <button type="button" class="doc-upload-btn" onclick="triggerCustomUpload()">
                        Upload
                    </button>
                    <button type="button" onclick="cancelCustomAdd()" title="Cancel" class="icon-btn" style="background: #f1f5f9; color: #0f172a;">
                        <i class="ri-close-line"></i>
                    </button>
                </div>
            </div>
        </div>

        <!-- Navigation buttons for Step 2 -->
        <div class="flex items-center justify-between mt-10 pt-6 border-t border-gray-100">
            <button type="submit" name="go_back" value="1" class="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700 transition-colors bg-transparent border-none cursor-pointer">
                &#8592; Back
            </button>
            
            <div class="flex gap-4 items-center">
                <button type="submit" name="save_draft" value="1" class="text-sm font-semibold text-gray-600 bg-white border border-gray-200 px-6 py-2.5 rounded-lg hover:bg-gray-50 transition-colors">
                    Save as Draft
                </button>
                <button type="submit" class="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold px-6 py-2.5 rounded-lg transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2" id="btn-continue-step2">
                    Next Step &#8594;
                </button>
            </div>
        </div>
        
        {step2_modals}
      </form>
      
      {{% else %}}
        <!-- STEP 3 NEW DESIGN -->
        <div class="bg-gray-50 rounded-xl border border-gray-100 p-6 mb-6 mt-4 text-left">
            <h3 class="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-4">
                Case Information
            </h3>
            <div class="grid grid-cols-2 gap-x-8 gap-y-4">
                <div>
                    <p class="text-xs text-gray-400 mb-0.5">Full Name</p>
                    <p class="text-sm font-medium text-gray-800">{{{{ case.client_display_name }}}}</p>
                </div>
                <div>
                    <p class="text-xs text-gray-400 mb-0.5">Phone Number</p>
                    <p class="text-sm font-medium text-gray-800">{{{{ case.client_number|default:"—" }}}}</p>
                </div>
                <div>
                    <p class="text-xs text-gray-400 mb-0.5">Email</p>
                    <p class="text-sm font-medium text-gray-800">{{{{ case.client_email|default:"—" }}}}</p>
                </div>
                <div>
                    <p class="text-xs text-gray-400 mb-0.5">LGU Origin</p>
                    <p class="text-sm font-medium text-gray-800">{{{{ case.area|default:"—" }}}}</p>
                </div>
                <div>
                    <p class="text-xs text-gray-400 mb-0.5">Transaction Type</p>
                    <p class="text-sm font-medium text-gray-800">{{{{ case.get_case_type_display|default:"—" }}}}</p>
                </div>
                {{% if case.needs_taxmapping %}}
                <div>
                    <p class="text-xs text-gray-400 mb-0.5">Tax Mapping</p>
                    <p class="text-sm font-medium text-amber-600">Required</p>
                </div>
                {{% endif %}}
            </div>
        </div>

        <div class="bg-gray-50 rounded-xl border border-gray-100 p-6 text-left">
            <h3 class="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-4">
                Checklist & Attachments
            </h3>
            
            {{% for doc in documents %}}
            <div class="flex items-center justify-between py-3 border-b border-gray-100 last:border-0">
                <span class="text-sm text-gray-700 font-medium">{{{{ doc.doc_type }}}}</span>
                <span class="text-xs font-semibold text-green-600 bg-green-50 px-3 py-1 rounded-full">
                    &#10003; Uploaded
                </span>
            </div>
            {{% empty %}}
            <p class="text-sm text-gray-500 italic py-2">No documents attached.</p>
            {{% endfor %}}

            {{% for item in checklist %}}
            {{% if not item.uploaded %}}
            <div class="flex items-center justify-between py-3 border-b border-gray-100 last:border-0">
                <span class="text-sm text-gray-700 font-medium">{{{{ item.doc_type }}}}</span>
                <span class="text-xs font-semibold text-amber-600 bg-amber-50 px-3 py-1 rounded-full">
                    Missing
                </span>
            </div>
            {{% endif %}}
            {{% endfor %}}
        </div>

        <form method="post" id="step3SubmitForm">
            {{% csrf_token %}}
            <div class="flex items-center justify-between mt-10 pt-6 border-t border-gray-100">
                <button type="submit" name="go_back" value="1" class="flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700 transition-colors bg-transparent border-none cursor-pointer">
                    &#8592; Back
                </button>
                <button type="submit" class="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold px-6 py-2.5 rounded-lg transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
                    Submit Case
                </button>
            </div>
        </form>

        <!-- No Documents Warning Modal -->
        <div id="noDocsModal" style="display:none; position:fixed; inset:0; background:rgba(0,0,0,0.4); z-index:9999; justify-content:center; align-items:center;">
            <div style="background:white; border-radius:16px; padding:2rem; width:420px; box-shadow:0 20px 60px rgba(0,0,0,0.2); border-top: 4px solid #dc2626;">
                <h3 style="margin:0 0 0.75rem 0; font-size:1.1rem; color:#dc2626;"><i class="ri-error-warning-line"></i> Missing Documents</h3>
                <p style="margin:0 0 1.5rem 0; font-size:0.9rem; color:#64748b;">
                    Please upload at least 1 document for this transaction.
                </p>
                <button type="button" onclick="document.getElementById('noDocsModal').style.display='none';" style="width:100%; padding:0.65rem; border-radius:8px; background:#4f46e5; color:white; border:none; font-weight:600; cursor:pointer; font-size:0.9rem;">OK, Go Back</button>
            </div>
        </div>

      {{% endif %}}

    </div>
  </div>
</div>
{{% endblock %}}'''

    full_content = content[:content_start] + new_content_block + content[content_end:]
    
    full_content = full_content.replace("row.classList.add('state-completed');", "row.classList.add('state-completed', 'uploaded');\n                    const icon = row.querySelector('.doc-upload-icon i');\n                    if (icon) { icon.className = 'ri-check-line text-lg'; }\n                    const iconContainer = row.querySelector('.doc-upload-icon');\n                    if (iconContainer) { iconContainer.style.background = '#dcfce7'; iconContainer.style.color = '#16a34a'; }\n                    const uploadBtn = row.querySelector('.doc-upload-btn');\n                    if (uploadBtn) { uploadBtn.innerHTML = '&#8635; Replace'; }")
    full_content = full_content.replace("row.classList.remove('state-completed');", "row.classList.remove('state-completed', 'uploaded');\n                    const icon = row.querySelector('.doc-upload-icon i');\n                    if (icon) { icon.className = 'ri-file-text-line text-lg'; }\n                    const iconContainer = row.querySelector('.doc-upload-icon');\n                    if (iconContainer) { iconContainer.style.background = '#f1f5f9'; iconContainer.style.color = '#64748b'; }\n                    const uploadBtn = row.querySelector('.doc-upload-btn');\n                    if (uploadBtn) { uploadBtn.innerHTML = '+ Upload'; }")

    with open('new_submit_case.html', 'w', encoding='utf-8') as f:
        f.write(full_content)
    
if __name__ == '__main__':
    main()
