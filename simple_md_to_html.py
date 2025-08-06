#!/usr/bin/env python3
"""
Simple Markdown to HTML converter without external dependencies
"""

import re
import os

def simple_markdown_to_html(md_content):
    """Convert basic markdown to HTML"""
    
    # Replace markdown syntax with HTML
    html = md_content
    
    # Headers
    html = re.sub(r'^### (.*$)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*$)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*$)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.*$)', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    
    # Bold and italic
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    
    # Code blocks
    html = re.sub(r'```python\n(.*?)\n```', r'<pre><code class="python">\1</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'```bash\n(.*?)\n```', r'<pre><code class="bash">\1</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'```ini\n(.*?)\n```', r'<pre><code class="ini">\1</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'```(.*?)\n(.*?)\n```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
    
    # Inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # Links
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
    
    # Lists
    lines = html.split('\n')
    in_list = False
    result_lines = []
    
    for line in lines:
        if re.match(r'^\s*-\s+', line):
            if not in_list:
                result_lines.append('<ul>')
                in_list = True
            item = re.sub(r'^\s*-\s+(.*)$', r'<li>\1</li>', line)
            result_lines.append(item)
        elif re.match(r'^\s*\d+\.\s+', line):
            if not in_list:
                result_lines.append('<ol>')
                in_list = True
            item = re.sub(r'^\s*\d+\.\s+(.*)$', r'<li>\1</li>', line)
            result_lines.append(item)
        else:
            if in_list:
                result_lines.append('</ul>')
                in_list = False
            result_lines.append(line)
    
    if in_list:
        result_lines.append('</ul>')
    
    html = '\n'.join(result_lines)
    
    # Tables - simplified table handling
    table_lines = []
    in_table = False
    
    lines = html.split('\n')
    result_lines = []
    
    for line in lines:
        if '|' in line and not line.strip().startswith('<'):
            if not in_table:
                result_lines.append('<table>')
                in_table = True
            
            # Check if it's a separator row
            if re.match(r'^\s*\|[\s\-\|]+\|\s*$', line):
                continue
            
            # Process table row
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            if len(cells) > 0:
                row_html = '<tr>'
                for cell in cells:
                    if '**' in cell:  # Header row
                        cell = cell.replace('**', '')
                        row_html += f'<th>{cell}</th>'
                    else:
                        row_html += f'<td>{cell}</td>'
                row_html += '</tr>'
                result_lines.append(row_html)
        else:
            if in_table:
                result_lines.append('</table>')
                in_table = False
            result_lines.append(line)
    
    if in_table:
        result_lines.append('</table>')
    
    html = '\n'.join(result_lines)
    
    # Paragraphs
    paragraphs = html.split('\n\n')
    html_paragraphs = []
    
    for para in paragraphs:
        para = para.strip()
        if para and not para.startswith('<'):
            para = f'<p>{para}</p>'
        html_paragraphs.append(para)
    
    html = '\n\n'.join(html_paragraphs)
    
    # Clean up multiple newlines
    html = re.sub(r'\n{3,}', '\n\n', html)
    
    return html

def create_styled_html(content):
    """Create a complete HTML document with styling"""
    
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>pytest vs APITestCase in Django REST Framework - Decision Guide</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 30px;
            color: #333;
            background-color: #fafafa;
        }}
        
        .container {{
            background-color: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 15px;
            margin-bottom: 30px;
            font-size: 2.2em;
        }}
        
        h2 {{
            color: #34495e;
            margin-top: 40px;
            margin-bottom: 20px;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 10px;
            font-size: 1.6em;
        }}
        
        h3 {{
            color: #2c3e50;
            margin-top: 30px;
            margin-bottom: 15px;
            font-size: 1.3em;
        }}
        
        h4 {{
            color: #7f8c8d;
            margin-top: 25px;
            margin-bottom: 10px;
            font-size: 1.1em;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 25px 0;
            font-size: 14px;
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 12px 15px;
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
        
        tr:hover {{
            background-color: #e8f4f8;
        }}
        
        code {{
            background-color: #f4f4f4;
            padding: 3px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            color: #e74c3c;
            font-size: 0.9em;
        }}
        
        pre {{
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-radius: 6px;
            padding: 20px;
            overflow-x: auto;
            margin: 20px 0;
            font-size: 13px;
        }}
        
        pre code {{
            background-color: transparent;
            color: #333;
            padding: 0;
            border-radius: 0;
        }}
        
        .python {{
            background-color: #f0f8ff;
            border-left: 4px solid #3776ab;
        }}
        
        .bash {{
            background-color: #f5f5f5;
            border-left: 4px solid #000;
        }}
        
        .ini {{
            background-color: #fff8e1;
            border-left: 4px solid #ff9800;
        }}
        
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 25px 0;
            padding: 15px 25px;
            background-color: #f8f9fa;
            font-style: italic;
        }}
        
        ul, ol {{
            margin: 20px 0;
            padding-left: 35px;
        }}
        
        li {{
            margin: 8px 0;
        }}
        
        strong {{
            color: #2c3e50;
        }}
        
        em {{
            color: #7f8c8d;
        }}
        
        .highlight {{
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        
        .success {{
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }}
        
        .warning {{
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }}
        
        .footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            text-align: center;
            color: #7f8c8d;
            font-style: italic;
        }}
        
        @media print {{
            body {{
                font-size: 12pt;
                line-height: 1.4;
                background-color: white;
            }}
            
            .container {{
                box-shadow: none;
                padding: 20px;
            }}
            
            h1 {{
                font-size: 18pt;
                page-break-after: avoid;
            }}
            
            h2 {{
                font-size: 16pt;
                page-break-after: avoid;
            }}
            
            h3 {{
                font-size: 14pt;
                page-break-after: avoid;
            }}
            
            h4 {{
                font-size: 12pt;
                page-break-after: avoid;
            }}
            
            table {{
                font-size: 10pt;
                page-break-inside: auto;
            }}
            
            tr {{
                page-break-inside: avoid;
                page-break-after: auto;
            }}
            
            pre {{
                font-size: 10pt;
                page-break-inside: avoid;
            }}
            
            .page-break {{
                page-break-before: always;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {content}
        <div class="footer">
            <p>Generated Document: pytest vs APITestCase in Django REST Framework</p>
            <p>Decision Guide for Testing Framework Selection</p>
        </div>
    </div>
</body>
</html>"""

def main():
    # Read the markdown file
    md_file = '/workspace/pytest_vs_apitestcase_drf_comparison.md'
    
    if not os.path.exists(md_file):
        print(f"Error: {md_file} not found!")
        return 1
    
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert to HTML
    html_content = simple_markdown_to_html(md_content)
    
    # Create styled HTML document
    styled_html = create_styled_html(html_content)
    
    # Save HTML file
    html_file = '/workspace/pytest_vs_apitestcase_drf_comparison.html'
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(styled_html)
    
    print(f"✅ Styled HTML document created: {html_file}")
    print(f"📄 File size: {os.path.getsize(html_file)} bytes")
    
    # Print instructions for PDF conversion
    print(f"""
🔧 To convert to PDF:

1. **Using Web Browser (Recommended):**
   - Open {html_file} in any web browser
   - Press Ctrl+P (or Cmd+P on Mac)
   - Select "Save as PDF" or "Print to PDF"
   - Choose A4 paper size with margins
   
2. **Using wkhtmltopdf (if available):**
   wkhtmltopdf --page-size A4 --margin-top 20mm --margin-right 15mm --margin-bottom 20mm --margin-left 15mm "{html_file}" "pytest_vs_apitestcase_drf_comparison.pdf"

3. **Using Chrome/Chromium headless:**
   google-chrome --headless --disable-gpu --print-to-pdf="pytest_vs_apitestcase_drf_comparison.pdf" "{html_file}"

📋 The HTML document is professionally formatted and ready for reading or printing!
    """)
    
    return 0

if __name__ == "__main__":
    main()