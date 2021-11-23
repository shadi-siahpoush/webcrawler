# Crawling the common Crawl service
# Description
### -  We First  create a list of  all the file paths in the common crawl websiote for each month in the year of 2020
### - Then  iterate over the file paths per month, for each month we extract the file paths of the segments for that month 
### - Then we iterate over the  for paths for eacb segment in each month and do template matching using regex  on two key catefgory of keywords
#### - Covid keyworks:
regex_covid = re.compile('\scovid-?(19)?\s|\spandemics?\s|\sepidemic\s|\scoronavirus\s|\suarantine\s|\ssocial\sdistance?(ing)?'
                         '|\sventilator\s|\ssars-cov-2\s|\sincubation(\s|-)period\s|\scovid\svaccine\s|\spfizer\s|\smoderna\s')


#### - Economy key words :
regex_economy = re.compile('\seconomy\s|\sfinancial|\seconomic\s|\sbank\s|\sfinance\s|\smortgage\s|\sloan\s|\slender\s|\sstock\s|\sbond\s|\shouse\sprice\s|'
                           '\sgas\sprices\s|\sstimulus\scheck\s|\scurrency\s|\sdebt\s|\sinflation\s|\sincome\s|\sjob\s|\slabor\s|\smoney\s|\stax\s|\sprofit\s|\ssaving\s|\strade\s'
                           '\s(un)?employment\s|\swage\s|\swealth\s')
and if there is a match for both cases, we return the page including those keywords  as a successful result
## we combine all the results and save the results in a file
