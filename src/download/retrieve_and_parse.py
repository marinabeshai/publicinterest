# ------------------------------------------------------------------------------------------------------------------------
import xml.etree.ElementTree as ET
import urllib.request
import os
import slate3k as slate
import pikepdf
# ------------------------------------------------------------------------------------------------------------------------

# https://pypi.org/project/pdftotext/
# https://pypi.org/search/?q=pdf+to+text

# ------------------------------------------------------------------------------------------------------------------------
def parse(url, year, docid):
    with open("letstry.txt", 'a') as f2:
        with urllib.request.urlopen(url.replace('YEAR', year).replace('DOCID', docid)) as f:
            filename = docid + ".pdf"

            file = open(filename, 'wb')
            file.write(f.read())
            file.close()

            pdf = pikepdf.open(filename, allow_overwriting_input=True)
            pdf.save(temp)

            with open(temp, 'rb') as f:
                extracted_text = slate.PDF(f)
                x = list(extracted_text)

                honor, write = True, False

                f2.write(url.replace('YEAR', year).replace('DOCID', docid))
                f2.write("\n")
                # f2.write(year + "\n")

                for i in x:
                    for line in str(i).splitlines():
                        if 'https' in line:
                            break

                        if not line:
                            continue

                        print(line)

                        # if 'DC' in line:
                        #     f2.write(line)
                        #     f2.write("\n")

                        if 'Hon.' in line and honor:
                            honor = False
                            f2.write(line)
                            f2.write("\n")

                        elif 'State/District' in line:
                            f2.write(line)
                            f2.write("\n")

                        elif '[' in line and ']' in line:
                            write = True
                            f2.write(line)
                            f2.write("\n")

                        elif 'STATUS' in line or 'New' in line:
                            write = False
                            # f2.write("\n")

                        elif '(' in line and ')' in line:
                            if (line[line.find('(')+1:line.find(')')]).isalnum():
                                f2.write(line)
                                f2.write("\n")
                                write = True
                            elif write:
                                write = False

                        elif write:
                            f2.write(line)
                            f2.write("\n")

                f2.write("\n\n\n")

    os.remove(temp)
    os.remove(filename)
# ------------------------------------------------------------------------------------------------------------------------

# key = '6LEQ9QLDA21SOUR9'


url = "https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/YEAR/DOCID.pdf"
temp = "temp.pdf"
PTR = 'P'


for dirname in os.listdir("./static"):
    if "FD" not in dirname:
        continue

    year = dirname[0:4]
    tree = ET.parse('static/' + str(year) + 'FD/' + str(year) + 'FD.xml')
    root = tree.getroot()

    for prefix, last, first, suffix, filingtype, statedst,  year, filingdate, docid in zip(root.findall('Member/Prefix'), root.findall('Member/Last'), root.findall('Member/First'), root.findall('Member/Suffix'), root.findall('Member/FilingType'), root.findall('Member/StateDst'), root.findall('Member/Year'), root.findall('Member/FilingDate'), root.findall('Member/DocID')):

        if (filingtype.text != PTR):
            continue

        while True:
            try:
                parse(url, year.text, docid.text)
                break
            except TimeoutError:
                continue
        break 

            # if  (len(requests.get('https://www.alphavantage.co/query?function=EARNINGS&symbol=' +  line[line.find('(')+1:line.find(')')] + '&apikey='+ key).json()) > 0):
