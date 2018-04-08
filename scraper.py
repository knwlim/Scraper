import re
import requests  # http://docs.python-requests.org/en/master/

email_reg = r"[a-zA-Z0-9#$%&~’*-.=?~_‘|{}.]+@[a-zA-Z0-9#$%&~’*+-.=?~_‘|{}.]+\.(?!png)[a-zA-Z]{2,7}"
url_d_quote = r"href=\"(http[s]?:[a-zA-Z0-9#$%&~’*+\-\/=?~_‘|{}.:]+)\""   # double quote
url_s_quote = r"href=\'(http[s]?:[a-zA-Z0-9#$%&~’*+\-\/=?~_‘|{}.:]+)\'"   # single quote
image = r"href=\"//([A-Za-z0-9/, .:_.]+(jpg|png))\""
webm = r"href=\"//([A-Za-z0-9/, .:_.]+webm)\""
gif = r"href=\"//([A-Za-z0-9/, .:_.]+gif)\""

url_for_scraping = r"<a href=\"(http[a-zA-Z0-9#$%&~’*+\-\/=?~_‘|{}.:]+)\">"
url_wo_protocol = r"href=\"(?!http)(.+html)\"" # relative hyperlinks


def image_url(link):
    this_page = requests.get(link)
    found = re.findall(image, this_page.text)
    found_image = [x[0] for x in found]
    return list(set(found_image))


def webm_url(link):
    this_page = requests.get(link)
    found = re.findall(webm, this_page.text)
    return list(set(found))


def gif_url(link):
    this_page = requests.get(link)
    found = re.findall(gif, this_page.text)
    return list(set(found))


def scraper_image(link):
    all_image = []
    all_image += image_url(link)
    list_of_urls = find_urls(link)
    for e in list_of_urls:
        all_image += image_url(e)
    return all_image


def scraper_gif(link):
    webm_urls = webm_url(link)
    gif_urls = gif_url(link)
    stringofhtml = "<!DOCTYPE html>\n" \
                   " <html>\n" \
                   "    <head></head>\n" \
                   "  <body>\n"
    for e in webm_urls:
        stringofhtml += '<p><video width="480" height="360" controls><source src="http://{}" type="video/mp4"></video></p>'.format(e)
    for e in gif_urls:
        stringofhtml += '<p><img src="http://{}" width="600";></p>'.format(e)

    stringofhtml += "\n</body>\n </html>"
    return stringofhtml


def return_html_url(listofurl):
    stringofhtml = "<!DOCTYPE html>\n" \
                   " <html>\n" \
                   "    <head></head>\n" \
                   "  <body>\n"
    for e in listofurl:
        stringofhtml += '<p><img src="http://{}" width="600";></p>'.format(e)

    stringofhtml += "\n</body>\n </html>"
    return stringofhtml


def find_emails(text):
    found_email = []

    if isinstance(text, list):  # if it is list
        for element in text:
            output = re.findall(email_reg, element)
            found_email.append(output)
    elif isinstance(text, str):  # if it is string
        found_email = re.findall(email_reg, text)
    else:
        raise TypeError("text must be a either string or list of string")
    return found_email


def find_urls(text):
    found_url = []

    if isinstance(text, list) :  # if it is list
        for element in text:
            output = re.findall(url_d_quote, element)
            found_url.append(output)
    elif isinstance(text, str) :  # if it is string
        found_url = re.findall(url_d_quote, text)      # double quote
        found_s_quote = re.findall(url_s_quote, text)  # single quote
        found_url += found_s_quote
    else:
        raise TypeError("text must be a either string or list of string")
    return found_url


# return the list of found urls in html page
def find_urls_scraping(this_page, url):
    found_w_protocol = re.findall(url_for_scraping, this_page.text)

    found_wo_protocol = re.findall(url_wo_protocol, this_page.text)
    wo_protocol_list = []
    for e in found_wo_protocol:
        e = url + e
        wo_protocol_list.append(e)

    found_all_url = found_w_protocol + wo_protocol_list
    return found_all_url


def all_the_emails(url, depth, emaillist = []):
    if depth > 0:
        this_page = requests.get(url)
        if this_page.ok:
            emaillist += find_emails(this_page.text)
            for this_url in find_urls_scraping(this_page, url):
                all_the_emails(this_url, depth-1, emaillist)
        else:
            print("{}".format(this_page.status_code))
    return list(set(emaillist))  # used set to remove duplicates
