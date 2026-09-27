from scrapling.fetchers import DynamicFetcher
import json

def analyze_website(url):
    print(f"[*] جاري الاتصال بالموقع: {url}")
    
    # استخدام DynamicFetcher مع إيقاف الواجهة الرسومية
    # وتخطي الأخطاء إن حدثت بعد تحميل المحتوى الأساسي
    try:
        page = DynamicFetcher.fetch(
            url, 
            headless=True,
            wait_until="commit" # التوقف بمجرد بدء استلام البيانات، لا ننتظر الصور
        )
    except Exception as e:
        print(f"[!] تحذير أثناء التحميل (سيتم إكماله): {e}")
        # أحياناً يعطي خطأ timeout ولكنه يكون قد جلب الـ HTML بالفعل، لذا سنحاول أخذ النص إن وجد
        pass
    
    print("[+] اكتمل الاتصال المبدئي!\n")

    # سننتظر ثواني قليلة يدوياً لضمان تنفيذ بعض الجافاسكريبت الأساسي
    import time
    time.sleep(5) 

    # 2. حفظ الكود المصدري (HTML)
    # استخدام page.page للحصول على كائن playwright الأساسي لو احتجناه
    html_content = page.text
    with open("cyera_source_code.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("[*] تم حفظ الكود المصدري في ملف: cyera_source_code.html\n")

    # 3. استخراج التقنيات وملفات JavaScript
    print("--- التقنيات وملفات JavaScript المستخدمة ---")
    scripts = page.css('script')
    js_files = set()
    for script in scripts:
        src = script.attrib.get('src')
        if src:
            js_files.add(src)
    
    for js in js_files:
        print(f"- {js}")

    # 4. استخراج البيانات الوصفية (Meta Tags)
    print("\n--- البيانات الوصفية (Meta Tags) ---")
    meta_tags = page.css('meta')
    for meta in meta_tags:
        name = meta.attrib.get('name') or meta.attrib.get('property')
        content = meta.attrib.get('content')
        if name and content:
            print(f"{name}: {content}")

    # 5. جلب الروابط الخارجية (APIs/Services)
    print("\n--- الروابط الخارجية ---")
    links = page.css('link')
    for link in links:
        rel = link.attrib.get('rel')
        href = link.attrib.get('href')
        if rel in ['preconnect', 'dns-prefetch', 'stylesheet'] and href:
            print(f"[{rel}]: {href}")

if __name__ == "__main__":
    target_url = "https://secure-the-unknown.cyera.com/"
    analyze_website(target_url)