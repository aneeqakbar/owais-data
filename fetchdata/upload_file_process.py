from django.conf import settings
from PyPDF2 import PdfFileWriter, PdfFileReader
from django.core.files.base import File
import pdfplumber
from datetime import date
import glob, sys, fitz
import pdfrw
import os
import sys
from urllib.parse import urlparse
import io

from .models import ProcessedFile


def findLine(starter, LINES):
    for line in LINES:
        if line.startswith(starter):
            return line
    return ""
 
def findLineAndNumber(starter, LINES):
    for lineNumber,line in enumerate(LINES):
        if line.startswith(starter):
            return lineNumber,line
    return None


class ProcessPdf:

    def __init__(self, temp_directory):
        print('\n##########| Initiating Pdf Creation Process |#########\n')
        
        print('\nFinal Pdf will be: ', temp_directory)
        self.temp_directory = temp_directory

    def add_data_to_pdf(self, template_path, data):
        print('\nAdding data to pdf...')
        template = pdfrw.PdfReader(template_path)

        for page in template.pages:
            annotations = page['/Annots']
            if annotations is None:
                continue

            for annotation in annotations:

                if annotation['/Subtype'] == '/Widget':
                    if annotation['/T']:
                        key = annotation['/T'][1:-1] 
                       
                        if key in data:
                            annotation.update(
                                pdfrw.PdfDict(V=self.encode_pdf_string(data[key]))
                            )
                        annotation.update(pdfrw.PdfDict(Ff=1))

        template.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
        pdfrw.PdfWriter().write(self.temp_directory, template)
        print('Pdf saved')

    def encode_pdf_string(self, value):
        if value:
            return pdfrw.objects.pdfstring.PdfString.encode(value)
        else:
            return pdfrw.objects.pdfstring.PdfString.encode('')


def start_process(inputFiles, output_ins):
    # Input files path will be given here
    print("started")
    print("input got:", inputFiles)
    # inputFiles = []
    # for name in glob.glob('Input/*'):
    #     inputFiles.append(name)
    output_format = f"{settings.BASE_DIR}{output_ins.file.url}"
    processed_files = []

    for input_file in inputFiles:
        OldPdfName = f"{settings.BASE_DIR}{input_file.input_file.url}"
        print("\nProcessing File: ", OldPdfName)
        data = {}
        with pdfplumber.open(OldPdfName) as pdf:
            first_page = pdf.pages[0]
            LINES = first_page.extract_text().split("\n")
            
            try:
                
                BusinessNameAndDBALine = findLine("Legal Business Name", LINES).split("DBA")
                try:
                    LegalBusinessName = BusinessNameAndDBALine[0].split(":")[1]
                except:
                    print("An exception occured when extracting Legal Business Name in your file.", OldPdfName )
                    LegalBusinessName = ""
                try:
                    DBA = BusinessNameAndDBALine[1].split(":")[1]
                    DBA = DBA.replace("P","")
                except:
                    print("An exception occured when extracting DBA in your file.", OldPdfName )
                    DBA = ""
                    
            except:
                print("Error extracting Legal Business Name and DBA Line in your file",  OldPdfName)
                LegalBusinessName = ""
                DBA = ""
                
                

                
            try:
                AddressPhoneAndStartedLine = findLine("Physical Address", LINES)

                try:
                    PhysicalAddress = AddressPhoneAndStartedLine.split()[:5][2:]
                    PhysicalAddress = " ".join(PhysicalAddress)
                    toBeRemoved = "Physical Address: " + PhysicalAddress
                    AddressPhoneAndStartedLine = AddressPhoneAndStartedLine.replace(toBeRemoved,"")
                except:
                    print("An exception occured when extracting PhysicalAddress in your file.", OldPdfName )
                    PhysicalAddress = ""
                try:
                    Telephone = AddressPhoneAndStartedLine.split("Date")[0].split(":")[1]
                except:
                    print("An exception occured when extracting Telephone in your file.", OldPdfName )
                    Telephone = ""

                try:
                    DateBusinessStarted = AddressPhoneAndStartedLine.split("Date")[1].split(":")[1]
                except:
                    print("An exception occured when extracting Date Business Started in your file.", OldPdfName )
                    DateBusinessStarted = ""
            except:
                print("Error extracting Physical Address, Phone and Date Business Started Line in your file",  OldPdfName)
                PhysicalAddress = ""
                Telephone = ""
                DateBusinessStarted = ""
                
            try:
                CityEmailOwnershipLine = findLine("City:", LINES)
                try:
                    City = CityEmailOwnershipLine.split("Email")[0].split(":")[1]
                    toBeRemoved = "City:" + City
                    CityEmailOwnershipLine = CityEmailOwnershipLine.replace(toBeRemoved,"")
                except:
                    print("An exception occured when extracting City in your file.", OldPdfName )
                    City = ""
                    
                    
                try:
                    Email = CityEmailOwnershipLine.split("of Ownership: ")[0].split(":")[1].replace("Length","")
                except:
                    print("An exception occured when extracting Email in your file.", OldPdfName )
                    Email = ""
                try:
                    LengthOfOwnership = CityEmailOwnershipLine.split("of Ownership: ")[-1]
                except:
                    print("An exception occured when extracting Length of Ownership in your file.", OldPdfName )
                    LengthOfOwnership = ""
                    
            except:
                print("Error extracting City, Email and Length of Ownership in your file",  OldPdfName)
                City = ""
                Email = ""
                LengthOfOwnership = ""
                
            try:
                StateFaxWebsiteLine = findLine("State:", LINES).split("Fax")
                try:
                    State = " "+ StateFaxWebsiteLine[0].split(":")[1] 
                except:
                    print("An exception occured when extracting State in your file.", OldPdfName )
                    State = ""
                try:
                    Fax = StateFaxWebsiteLine[1].split("Website")[0].split(":")[1]
                except:
                    print("An exception occured when extracting Fax in your file.", OldPdfName )
                    Fax = ""
                try:
                    Website = StateFaxWebsiteLine[1].split("Website")[1].split(":")[1].replace("O","")
                except:
                    print("An exception occured when extracting Website in your file.", OldPdfName )
                    Website = ""
                    
            except:
                print("Error extracting State, Fax and Website in your file",  OldPdfName)
                State = ""
                Fax = ""
                Website = ""
                
            try:
                ZipTaxNumberLine = findLine("Zip:", LINES)
                ZipTaxNumberLineNum = findLineAndNumber("Zip:", LINES)[0]
                try:
                    Zip = ZipTaxNumberLine.split("FederalTaxID:")[0].split(":")[1]
                except:
                    print("An exception occured when extracting Zip in your file.", OldPdfName )
                    Zip = ""
                    
                    
                try:
                    FederalTaxID = ZipTaxNumberLine.split("Preferred")[0].split(":")[-1]
                    ContactNumber = ZipTaxNumberLine.split("Preferred")[1].split(":")[1]

                    if Zip == " " and FederalTaxID==" " and ContactNumber=="":
                        Zip = LINES[ZipTaxNumberLineNum+1]
                        FederalTaxID = LINES[ZipTaxNumberLineNum+2].split(" ")[0]
                        ContactNumber = LINES[ZipTaxNumberLineNum+2].split(" ")[1]
                    elif Zip!=" " and FederalTaxID==" " and ContactNumber=="":
                        FederalTaxID = LINES[ZipTaxNumberLineNum+1].split(" ")[0]
                        ContactNumber = LINES[ZipTaxNumberLineNum+1].split(" ")[1]
                except:
                    print("Error extracting Federal Tax Id and Contact Number in your file",  OldPdfName)
                    FederalTaxID = ""
                    ContactNumber = ""
                    
            except:
                print("Error extracting Zip, Federal Tax Id and Contact Number in your file",  OldPdfName)
                Zip = ""
                FederalTaxID = ""
                ContactNumber = ""

            try:
                OwnerName = findLine("Owner Name:",LINES).split("Owner")[1].split(":")[1]
            except:
                print("Error extracting Owner Name in your file",  OldPdfName)
                OwnerName = ""
            try:
                HomeAddress = findLine("Home Address:",LINES).split()[:5][2:]
                HomeAddress = " ".join(HomeAddress)
            except:
                print("Error extracting Home Address in your file",  OldPdfName)
                HomeAddress = ""
                
            try:
                CityStateZip2 = findLine("City, State, Zip:",LINES).split("Zip:")[1:][0].split("City")[0]
                City2 = CityStateZip2.split(" ")[1]
                State2 = CityStateZip2.split(" ")[2]
                Zip2 = CityStateZip2.split(" ")[3]
            except:
                print("Error extracting City2, State2, and Zip2 in your file",  OldPdfName)
                City2 = ""
                State2 = ""
                Zip2 = ""
            try:
                DOB = findLine("Date of Birth:",LINES).split("Date")[1].split(":")[1]
            except:
                print("Error extracting Date Of Birth in your file",  OldPdfName)
                DOB = ""
            
            try:
                SS = findLine("SS#:",LINES).split("SS")[1].split(":")[1]
            except:
                print("Error extracting SS# in your file",  OldPdfName)
                SS = ""
            try:
                Cell = findLine("Cell #:",LINES).replace(" ","").split("Cell#:")[1].replace("C","")
            except:
                print("Error extracting Cell in your file",  OldPdfName)
                Cell = ""
            try:
                OwnerShipPercent = findLine("Ownership Percent:",LINES).split("Ownership")[1].split(":")[1]
            except:
                print("Error extracting OwnerShipPercent in your file",  OldPdfName)
                OwnerShipPercent = ""

    #         print(LegalBusinessName)
    #         print(DBA)
    #         print(PhysicalAddress)
    #         print(Telephone)
    #         print(DateBusinessStarted)

    #         print(City)
    #         print(Email)
    #         print(LengthOfOwnership)

    #         print(State)
    #         print(Fax)
    #         print(Website)

    #         print(Zip)
    #         print(FederalTaxID)
    #         print(ContactNumber)


    #         print(OwnerName)
    #         print(HomeAddress)
    #         print(City2)
    #         print(State2)
    #         print(Zip2)
    #         print(DOB)
    #         print(SS)
    #         print(Cell)
    #         print(OwnerShipPercent)



    #         for lineNum,line in enumerate(first_page.extract_text().split("\n")):
    #             print(lineNum)
    #             print(line)

            # Name = first_page.extract_text().split("\n")[31]
            # Address = first_page.extract_text().split("\n")[36]
            # City = Address.split(" ")[0]
            # State = Address.split(" ")[1]
            # Zip = Address.split(" ")[2]
                
                
                                                            
            data = {
                "Legal":LegalBusinessName,
                "DBA":DBA,
                "Address":PhysicalAddress,
                "City":City,
                "State":State,
                "Zip":Zip,
                "Phone":Telephone,
                "Mobil":ContactNumber,
                "Fax":Fax,
                "Email":Email,
                "Website":Website,
                "Federal Tax ID":FederalTaxID,
                "Date Business started":DateBusinessStarted,
                "Years at Location":LengthOfOwnership,
                "Full name":"                       "+OwnerName,
                "Home Address":HomeAddress,
                "City_2":City2,
                "State_2":State2,
                "Zip_2":"  "+Zip2,
                "SSN":SS,
                "DOB":DOB,
                "Home Phone":Cell,
                "% Ownership":OwnerShipPercent,
                "print name":" "+OwnerName,
                "print name2":" "+OwnerName,
                "Using the Money For": "  Working Capital",
                "Date": " "+date.today().strftime("%d/%m/%Y"),
                "Date_2": " "+date.today().strftime("%d/%m/%Y")
                
            }
        print(data, '\n\n')
        
        with open(OldPdfName, "rb") as in_f:
            input1 = PdfFileReader(in_f)
            output = PdfFileWriter()

            numPages = input1.getNumPages()

            x, y, w, h = (140.0948269, 675, 90.1579385, 24)

            page_x, page_y = input1.getPage(0).cropBox.getUpperLeft()
            upperLeft = [page_x.as_numeric(), page_y.as_numeric()] # convert PyPDF2.FloatObjects into floats
            new_upperLeft  = (upperLeft[0] + x, upperLeft[1] - y)
            new_lowerRight = (new_upperLeft[0] + w, new_upperLeft[1] - h)

            for i in range(numPages):
                page = input1.getPage(i)
                page.cropBox.upperLeft  = new_upperLeft
                page.cropBox.lowerRight = new_lowerRight

                output.addPage(page)

            with open("out.pdf", "wb") as out_f:
                output.write(out_f)
        # To get better resolution
        zoom_x = 2.0  # horizontal zoom
        zoom_y = 2.0  # vertical zoom
        mat = fitz.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension

        doc = fitz.open("out.pdf")  # open document
        for page in doc:  # iterate through the pages
            pix = page.get_pixmap(matrix=mat)  # render page to an image
            pix.save("sign.png")  # store image as a PNG


        parse_pdf_url = urlparse(OldPdfName)
        
        OutputFile_relative_path = f"/documents/processed/processed_" + os.path.basename(parse_pdf_url.path)
        OutputFile_absolute_path = f"{settings.MEDIA_ROOT}{OutputFile_relative_path}"
        # file_handle = fitz.open(NewPdfName)
        file_handle = fitz.open(output_format)
        page = file_handle[0]
        image = "sign.png"
        page.insert_image(
                    fitz.Rect(162, 705,275, 745),
                    filename=image
                )
        file_handle.save(OutputFile_absolute_path)

        Processor = ProcessPdf(OutputFile_absolute_path)
        Processor.add_data_to_pdf(OutputFile_absolute_path, data)

        processed_file = ProcessedFile.objects.create(
            input_file = input_file,
            processed_file = OutputFile_relative_path,
        )
        processed_files.append(processed_file)

        return processed_files

