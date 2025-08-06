#!/usr/bin/env python3
"""
Markdown to PDF converter using HTML as intermediate format
"""

import markdown
import os
import subprocess
import sys

def markdown_to_html(md_content):
    """Convert markdown content to HTML"""
    
    # Configure markdown with extensions for better formatting
    md = markdown.Markdown(extensions=[
        'markdown.extensions.tables',
        'markdown.extensions.fenced_code',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        'markdown.extensions.nl2br'
    ])
    
    # Convert markdown to HTML
    html_body = md.convert(md_content)
    
    # Create a complete HTML document with CSS styling
    html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>pytest vs APITestCase in Django REST Framework</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 5px;
        }}
        
        h3 {{
            color: #2c3e50;
            margin-top: 25px;
        }}
        
        h4 {{
            color: #7f8c8d;
            margin-top: 20px;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        
        th {{
            background-color: #f8f9fa;
            font-weight: bold;
            color: #2c3e50;
        }}
        
        tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}
        
        code {{
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            color: #e74c3c;
        }}
        
        pre {{
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 15px;
            overflow-x: auto;
            margin: 15px 0;
        }}
        
        pre code {{
            background-color: transparent;
            color: #333;
            padding: 0;
        }}
        
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 20px 0;
            padding: 10px 20px;
            background-color: #f8f9fa;
            font-style: italic;
        }}
        
        .toc {{
            background-color: #f8f9fa;
            border: 1px solid #ddd;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        
        .highlight {{
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }}
        
        .success {{
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
        }}
        
        .warning {{
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
        }}
        
        ul, ol {{
            margin: 15px 0;
            padding-left: 30px;
        }}
        
        li {{
            margin: 5px 0;
        }}
        
        .page-break {{
            page-break-before: always;
        }}
        
        @media print {{
            body {{
                font-size: 12pt;
                line-height: 1.4;
            }}
            
            h1 {{
                font-size: 18pt;
            }}
            
            h2 {{
                font-size: 16pt;
            }}
            
            h3 {{
                font-size: 14pt;
            }}
            
            code, pre {{
                font-size: 10pt;
            }}
            
            table {{
                font-size: 10pt;
            }}
        }}
    </style>
</head>
<body>
    {html_body}
</body>
</html>
    """
    
    return html_template

def main():
    # Read the markdown file
    md_file = '/workspace/pytest_vs_apitestcase_drf_comparison.md'
    
    if not os.path.exists(md_file):
        print(f"Error: {md_file} not found!")
        return 1
    
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert to HTML
    html_content = markdown_to_html(md_content)
    
    # Save HTML file
    html_file = '/workspace/pytest_vs_apitestcase_drf_comparison.html'
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ HTML file created: {html_file}")
    
    # Try to convert to PDF using various methods
    pdf_file = '/workspace/pytest_vs_apitestcase_drf_comparison.pdf'
    
    # Method 1: Try weasyprint (if available)
    try:
        import weasyprint
        doc = weasyprint.HTML(string=html_content)
        doc.write_pdf(pdf_file)
        print(f"✅ PDF file created using WeasyPrint: {pdf_file}")
        return 0
    except ImportError:
        print("❌ WeasyPrint not available")
    except Exception as e:
        print(f"❌ WeasyPrint failed: {e}")
    
    # Method 2: Try wkhtmltopdf (if available)
    try:
        result = subprocess.run([
            'wkhtmltopdf', 
            '--page-size', 'A4',
            '--margin-top', '20mm',
            '--margin-right', '20mm',
            '--margin-bottom', '20mm',
            '--margin-left', '20mm',
            '--encoding', 'UTF-8',
            html_file, 
            pdf_file
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ PDF file created using wkhtmltopdf: {pdf_file}")
            return 0
        else:
            print(f"❌ wkhtmltopdf failed: {result.stderr}")
    except FileNotFoundError:
        print("❌ wkhtmltopdf not available")
    except Exception as e:
        print(f"❌ wkhtmltopdf failed: {e}")
    
    # Method 3: Try headless Chrome/Chromium
    try:
        # Try different possible Chrome/Chromium executables
        chrome_executables = [
            'google-chrome',
            'chromium',
            'chromium-browser',
            'chrome'
        ]
        
        for chrome_exe in chrome_executables:
            try:
                result = subprocess.run([
                    chrome_exe,
                    '--headless',
                    '--disable-gpu',
                    '--print-to-pdf=' + pdf_file,
                    '--print-to-pdf-no-header',
                    html_file
                ], capture_output=True, text=True)
                
                if result.returncode == 0 and os.path.exists(pdf_file):
                    print(f"✅ PDF file created using {chrome_exe}: {pdf_file}")
                    return 0
            except FileNotFoundError:
                continue
        
        print("❌ No Chrome/Chromium executable found")
    except Exception as e:
        print(f"❌ Chrome/Chromium conversion failed: {e}")
    
    print(f"""
📄 HTML file is ready: {html_file}

To convert to PDF, you can:
1. Open the HTML file in a web browser and print to PDF
2. Install wkhtmltopdf: sudo apt install wkhtmltopdf
3. Install Chrome/Chromium browser
4. Use online HTML to PDF converters

The HTML file is formatted for easy reading and printing!
    """)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())