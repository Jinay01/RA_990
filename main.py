import os
import pandas as pd
from lxml import etree

# Function to scrape XML file
def scrape_xml_file(file_path):
    # Parse XML file
    tree = etree.parse(file_path)
    
    # Define namespace
    ns = {'ns': 'http://www.irs.gov/efile'}
    
    # List of variables to scrape from XML
    one = ['ReturnHeader_ReturnTs', 'ReturnHeader_TaxPeriodEndDt', 'ReturnHeader_ReturnTypeCd', 'ReturnHeader_TaxPeriodBeginDt', 'Filer_EIN', 'USAddress_StateCd', 'USAddress_ZIPCd', 'ReturnHeader_TaxYr', 'I9_GroupReturnForAffiliatesInd', 'I9_Organization501c3Ind', 'I9_WebsiteAddressTxt', 'I9_TypeOfOrganizationCorpInd', 'I9_FormationYr', 'I9_LegalDomicileStateCd', 'I9_VotingMembersGoverningBodyCnt', 'I9_VotingMembersIndependentCnt', 'I9_TotalEmployeeCnt', 'I9_TotalVolunteersCnt', 'I9_CYContributionsGrantsAmt', 'I9_CYProgramServiceRevenueAmt', 'I9_CYTotalRevenueAmt', 'I9_CYGrantsAndSimilarPaidAmt', 'I9_CYBenefitsPaidToMembersAmt', 'I9_CYSalariesCompEmpBnftPaidAmt', 'I9_CYTotalProfFndrsngExpnsAmt', 'I9_CYTotalFundraisingExpenseAmt', 'I9_CYOtherExpensesAmt', 'I9_CYTotalExpensesAmt', 'I9_TotalAssetsEOYAmt', 'I9_TotalLiabilitiesEOYAmt', 'I9_NetAssetsOrFundBalancesEOYAmt', 'I9_MissionDesc', 'I9_Organization501cInd', 'I9_Organization501cTypeTxt', 'I9_TypeOfOrganizationTrustInd', 'I9_AddressChangeInd', 'I9_NameChangeInd', 'I9_TransactionWithControlEntInd']

    # Dictionary to store scraped data
    data = {}
    
    # Extract data for each variable
    for variable in one:
        namespace_prefix, element_name = variable.split('_')
        try:
            element = tree.find(f'.//ns:{namespace_prefix}/ns:{element_name}', namespaces=ns)
            data[variable] = [element.text]
        except Exception as e:
            print("Error scraping variable:", variable, "File:", file_path, "Error:", e)
            # data[variable] = ['']

    temp = tree.find(".//ns:Filer/ns:BusinessName/ns:BusinessNameLine1Txt", namespaces=ns)
    two = ['Filer_BusinessName_BusinessNameLine1Txt']
    for variable in two:
        namespace_prefix, second, element_name = variable.split('_')
        
        try:
            element = tree.find(f'.//ns:{namespace_prefix}/ns:{second}/ns:{element_name}', namespaces=ns)
            data[variable] = [element.text]
        except Exception as e:
            print("Error scraping variable:", variable, "File:", file_path, "Error:", e)
            data[variable] = ['']
    
    return pd.DataFrame(data)

# Directory containing XML files
directory = '/Users/jinay/Desktop/RA/2023_TEOS_XML_12A'

# List to store DataFrames for each XML file
dfs = []

# Iterate over files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.xml'):
        file_path = os.path.join(directory, filename)
        print("Scraping:", file_path)
        df = scrape_xml_file(file_path)
        dfs.append(df)

# Concatenate DataFrames for all XML files
result_df = pd.concat(dfs, ignore_index=True)

# Specify the Excel file path
excel_file_path = 'output.xlsx'

# Save the DataFrame to an Excel file
result_df.to_excel(excel_file_path, index=False)

print(f"Output saved to {excel_file_path}")
