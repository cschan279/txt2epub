#!/usr/bin/env python3
import json
import os
import re
import mimetypes

def create_epub():
    # Load metadata
    with open('txt/info.json', 'r', encoding='utf-8') as f:
        info = json.load(f)

    title = info.get('title', 'Untitled')
    author = info.get('author')
    translator = info.get('translator')
    transcriber = info.get('transcribler')          # matches your JSON key exactly
    source_urls = info.get('source URL(s)')

    # Get and sort all chapter files
    txt_dir = './txt'
    txt_files = [f for f in os.listdir(txt_dir) if re.match(r'^\d{3}\.txt$', f)]
    txt_files.sort(key=lambda x: int(x.split('.')[0]))

    # Read everything into one big string
    full_content = ''
    for txt_file in txt_files:
        with open(os.path.join(txt_dir, txt_file), 'r', encoding='utf-8') as f:
            full_content += f.read() + '\n'

    # Split on chapter titles (lines that start with '#', possibly with spaces)
    chapters = []
    current_chapter = []
    chapter_title = None

    for line in full_content.splitlines():
        stripped = line.strip()
        if stripped.startswith('#'):
            # Save previous chapter (if any)
            if current_chapter:
                chapters.append((chapter_title, '\n'.join(current_chapter)))
            # New chapter title
            chapter_title = stripped.lstrip('#').strip()
            current_chapter = []
        else:
            current_chapter.append(line)

    # Don't forget the last chapter
    if current_chapter:
        chapters.append((chapter_title, '\n'.join(current_chapter)))

    # Fallback if the file contains no '#' at all
    if not chapters:
        chapters.append(('Chapter 1', full_content))

    # ──────────────────────────────────────────────────────────────
    # Create the EPUB
    # ──────────────────────────────────────────────────────────────
    book = epub.EpubBook()

    book.set_identifier('id_' + title.replace(' ', '_'))
    book.set_title(title)
    book.set_language('zh')                     # change to 'en' if you prefer

    if author:
        book.add_author(author)

    if translator:
        book.add_metadata('DC', 'contributor', translator, {'property': 'translator'})
    if transcriber:
        book.add_metadata('DC', 'contributor', transcriber, {'property': 'transcriber'})
    if source_urls:
        sources = ', '.join(source_urls) if isinstance(source_urls, list) else source_urls
        book.add_metadata('DC', 'source', sources)

    # ───── Title page ─────
    title_page_html = f'<h1>{title}</h1>'
    if author:
        title_page_html += f'<p>作者：{author}</p>'
    if translator:
        title_page_html += f'<p>譯者：{translator}</p>'
    if transcriber:
        title_page_html += f'<p>錄入：{transcriber}</p>'
    if source_urls:
        sources = ', '.join(source_urls) if isinstance(source_urls, list) else source_urls
        title_page_html += f'<p>來源：{sources}</p>'

    title_page = epub.EpubHtml(title='封面頁', file_name='title_page.xhtml', lang='zh')
    title_page.content = title_page_html
    book.add_item(title_page)

    # ───── Chapters ─────
    epub_chapters = []
    for i, (ch_title, ch_content) in enumerate(chapters, start=1):
        safe_title = ch_title or f'第{i}章'
        chapter = epub.EpubHtml(
            title=safe_title,
            file_name=f'chap_{i:03d}.xhtml',
            lang='zh'
        )
        # Simple conversion: keep line breaks visible
        body = ch_content.replace('\n', '<br/>')
        chapter.content = f'<h1>{safe_title}</h1><p>{body}</p>'
        book.add_item(chapter)
        epub_chapters.append(chapter)

    # ───── TOC & Spine ─────
    book.spine = [title_page] + epub_chapters

    book.toc = [epub.Link('title_page.xhtml', '封面頁', 'intro')]
    for i, (ch_title, _) in enumerate(chapters, start=1):
        safe_title = ch_title or f'第{i}章'
        book.toc.append(epub.Link(f'chap_{i:03d}.xhtml', safe_title, f'chap{i}'))

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # ───── Hidden original .txt files (for future editing) ─────
    # These files are inside the EPUB but NOT in the spine or TOC,
    # so normal readers will never show them.
    SOURCE_DIR_IN_EPUB = 'txt/'                     # appears as a "txt" folder when you unzip
    for txt_file in txt_files:
        path = os.path.join(txt_dir, txt_file)
        with open(path, 'rb') as f:
            content = f.read()

        mime, _ = mimetypes.guess_type(path)
        if mime is None:
            mime = 'text/plain'

        item = epub.EpubItem(
            uid=f'txt_{txt_file}',
            file_name=f'{SOURCE_DIR_IN_EPUB}{txt_file}',
            media_type=mime,
            content=content
        )
        book.add_item(item)

    # ───── Write the file ─────
    output_name = title.replace(' ', '_').replace('/', '_') + '.epub'
    epub.write_epub(output_name, book)
    print(f'✓ EPUB created: {output_name}')
    print('   • TOC is included (EPUB 2 + EPUB 3 compatible)')
    print('   • Original .txt files are packed inside (hidden from readers)')

if __name__ == '__main__':
    try:
        from ebooklib import epub
    except ImportError:
        print("ebooklib is not installed.")
        print("Please run: pip install ebooklib")
        exit(1)

    create_epub()