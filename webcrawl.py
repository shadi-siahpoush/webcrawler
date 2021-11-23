from warcio.archiveiterator import ArchiveIterator
import re
import requests
hits = 0

regex_covid = re.compile('\scovid-?(19)?\s|\spandemics?\s|\sepidemic\s|\scoronavirus\s|\suarantine\s|\ssocial\sdistance?(ing)?'
                         '|\sventilator\s|\ssars-cov-2\s|\sincubation(\s|-)period\s|\scovid\svaccine\s|\spfizer\s|\smoderna\s')

regex_economy = re.compile('\seconomy\s|\sfinancial|\seconomic\s|\sbank\s|\sfinance\s|\smortgage\s|\sloan\s|\slender\s|\sstock\s|\sbond\s|\shouse\sprice\s|'
                           '\sgas\sprices\s|\sstimulus\scheck\s|\scurrency\s|\sdebt\s|\sinflation\s|\sincome\s|\sjob\s|\slabor\s|\smoney\s|\stax\s|\sprofit\s|\ssaving\s|\strade\s'
                           '\s(un)?employment\s|\swage\s|\swealth\s')



def scrape_a_segment(file_name):
    global hits
    found_urls = []
    if hits>1000:
        return found_urls
    entries = 0
    matching_entries = 0
    stream = None
    if file_name.startswith("http://") or file_name.startswith(
        "https://"
    ):
        stream = requests.get(file_name, stream=True).raw
    else:
        stream = open(file_name, "rb")
    it = 0
    for record in ArchiveIterator(stream):
        if it%5000 == 0:
            print('-----------', it)
        it = it  +1
        if record.rec_type == "warcinfo":
            continue

        if not ".com/" in record.rec_headers.get_header(
            "WARC-Target-URI"
        ):
            continue

        entries = entries + 1
        contents = (
            record.content_stream()
            .read()
            .decode("utf-8", "replace")
        )
        # m = regex.search(contents)
        m1 = regex_covid.search(contents)
        m2 = regex_economy.search(contents)


        if m1 and m2:
            print('Found:::::::!', m1, m2)
            found = [item for item in record.rec_headers.headers if item[0] == 'WARC-Target-URI'][0][1]
            found_urls.append(found)
            matching_entries = matching_entries + 1
            hits = hits + 1

            print('Hit:', hits)
            if hits>1000:
                return found_urls

    print(
        "Python: "
        + str(hits)
        + " matches in "
        + str(matching_entries)
        + "/"
        + str(entries)
    )
    return found_urls

def scrape_for_month(file_paths_url):
    base_url = 'https://commoncrawl.s3.amazonaws.com/'
    import requests
    import gzip
    fcont = requests.get(file_paths_url)
    gzip_content = gzip.decompress(fcont.content)
    print(gzip_content)

    paths_list =  gzip_content.decode()
    paths_list = paths_list.split('\n')
    all_urls =[]
    month=0
    for path in paths_list:
        month = path[-24:-22]
        if hits > 1000:
            return {month:all_urls}
        if path:
            url = base_url + path
            print(url)
            found_urls = scrape_a_segment(url)
            all_urls.extend(found_urls)


    return {month:all_urls}


all_months = [
    'https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2020-05/warc.paths.gz',
    'https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2020-10/warc.paths.gz',
    'https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2020-16/warc.paths.gz',
    'https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2020-24/warc.paths.gz',
    'https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2020-34/warc.paths.gz',
    'https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2020-40/warc.paths.gz',
    'https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2020-45/warc.paths.gz',
    'https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2020-50/warc.paths.gz'

]
import json
if __name__ == '__main__':
    all_results = {}
    hits = 0

    for url in all_months:
        this_result = scrape_for_month(url)
        print('this_result: ', this_result)
        all_results.update(this_result)
        if hits > 1000:
            print(all_results)
            result_str = '\n'.join(all_results)
            with open('results', 'w') as f:
                for k, v in all_results.items():
                    f.write(json.dumps({k:v}))
                    f.write(',\n')


