from lxml import etree


def get_html(response):
    index_html = ''
    try:
        index_html = response.content.decode('utf-8')
    except UnicodeDecodeError:
        try:
            index_html = response.content.decode('gbk')
        except UnicodeDecodeError:
            try:
                index_html = response.content.decode(response.apparent_encoding)
            except UnicodeDecodeError:
                return ''
    except Exception as error:
        return ''
    return index_html


def get_title(html):
    try:
        tree = etree.HTML(html)
        title = tree.xpath('//title/text()')[0]
    except Exception as error:
        title = ''
    return title

