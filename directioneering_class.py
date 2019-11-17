"""
Author: John Pham @ Expose: Data Exposed
Intent: Web Scrapping



"""

import requests
from azure.storage.blob import BlockBlobService
from io import BytesIO
from bs4 import BeautifulSoup
import re


class config():
    def __init__(self):
        self.url = "https://ct2.cpiworld.com/login.aspx?x=1"
        self.report_url = "https://ct2.cpiworld.com/Reports/ReportItems.aspx?Type=Admin"
        self.account_name = ""
        self.account_key = ""
        self.blob_path = "directioneering_production_folder/"
        self.s = requests.session()
        self.get_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-AU,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            'Host': 'ct2.cpiworld.com',
            'Referer': 'https://ct2.cpiworld.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            }
        self.post_body = {
            '_LASTFOCUS': '',
            'ctl00_RadScriptManager1_TSM': ';;System.Web.Extensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-US:b7585254-495e-4311-9545-1f910247aca5:ea597d4b:b25378d2',
            '_EVENTTARGET': '',
            '_EVENTARGUMENT': '',
            '__VIEWSTATE': '/wEPDwULLTEzOTUxNzYzNDFkZEa0t8XC34GWI/cQGEupnm3i7IcU3eDDjPJf2U9/Kqmh',
            '_VIEWSTATEGENERATOR': 'C2EE9ABB',
            '_SCROLLPOSITIONX': '0',
            '_SCROLLPOSITIONY': '0',
            '__EVENTVALIDATION': '/wEdAAfyWMYrxfK15CpbReDHY7ycrOnd2U+ZndqublerCNp6a8NLkYDJptMqtzL0wjsm4H1DyRB5FEVHrwKplEgeyLhIueiPhSKQgP+qrkjSS970uUNZqwSuQEoekfVzh/C83DB8NmNCYn5pPuFUzrqmuOS6tuTgQbFFQGa9bwGW1QyytyMjJFwTlNbWjkiG8iaZ0Qc=',
            'ctl00$hidMsgText' : '',
            'ctl00$hidDCEmail': '',
            'ctl00$hidEmail': '',
            'ctl00$cph1$txtUserID' : '',
            'ctl00$cph1$txtPassword' : '',
            'ctl00$cph1$cmdLogin': 'Login'
            }
        self.post_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-AU,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'ct2.cpiworld.com',
            'Origin': 'https://ct2.cpiworld.com',
            'Referer': 'https://ct2.cpiworld.com/login.aspx?x=1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
            }
        self.result = self.s.get(self.url, headers=self.get_headers)
        print("Logging in")
        self.post_result = self.s.post(url=self.url, headers=self.post_headers, data=self.post_body)
        self.report_get_resource = self.s.get(url=self.report_url, headers=self.get_headers)
        print("getting report resource")
        self.html = BeautifulSoup(self.report_get_resource.content, 'html.parser')
        self.viewstate = self.html.select("#__VIEWSTATE")[0]['value']
        self.viewstategen = self.html.select("#__VIEWSTATEGENERATOR")[0]['value']
        self.event_valudation = self.html.select("#__EVENTVALIDATION")[0]['value']
        print("Web scrapping javascript values like Viewstate")
    def participant_report(self):
        post_report_participation = {
            'ctl00_RadScriptManager1_TSM': ';;System.Web.Extensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-US:b7585254-495e-4311-9545-1f910247aca5:ea597d4b:b25378d2;Telerik.Web.UI, Version=2015.1.401.40, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-US:f5c550b9-a65b-4cfb-8f9c-9833432cbee6:16e4e7cd:f7645509:24ee1bba:e330518b:2003d0b8:c128760b:88144a7a:1e771326:c8618e41:1a73651d:333f8d94:16d8629e',
            'ctl00_cph1_TreeView1_ExpandState': 'eennnnnnnnnnnnnnnnnnnnnnnnnnnnnnn',
            'ctl00_cph1_TreeView1_SelectedNode': 'ctl00_cph1_TreeView1t20',
            '__EVENTTARGET': 'ctl00$cph1$TreeView1',
            '__EVENTARGUMENT': 'sRO0\CA0\RI4',
            'ctl00_cph1_TreeView1_PopulateLog': '',
            '__VIEWSTATE': self.viewstate,
            '__VIEWSTATEGENERATOR': self.viewstategen,
            '__EVENTVALIDATION': self.event_valudation,
            'ctl00$hidMsgText': '',
            'ctl00$hidDCEmail': '',
            'ctl00$hidEmail': '',
            'ctl00_HorizMenu1_HorizMenu1_ClientState': '',
            'ctl00_ProgramsHorizMenu1_ProgsHorizMenu_ClientState': '',
            'ctl00_HorizMenu2_HorizMenu1_ClientState': '',
            'ctl00_ProgramsHorizMenu2_ProgsHorizMenu_ClientState': '',
            'ctl00_mnuNav_ClientState': ''
            }           
        post_report_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-AU,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'ct2.cpiworld.com',
            'Origin': 'https://ct2.cpiworld.com',
            'Referer': 'https://ct2.cpiworld.com/Reports/ReportItems.aspx?Type=Admin',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
            }
        print("verifing states")
        self.resource_get_participant = self.s.post(url=self.report_url, data=post_report_participation, headers=post_report_headers)
        print("moving towards participant reports")
        html2 = BeautifulSoup(self.resource_get_participant.content, 'html.parser')
        viewstate2 = html2.select("#__VIEWSTATE")[0]['value']
        viewstategen2 = html2.select("#__VIEWSTATEGENERATOR")[0]['value']
        event_valudation2 = html2.select("#__EVENTVALIDATION")[0]['value']
        print("web scrapping stategen2")
        get_report_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-AU,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'ct2.cpiworld.com',
            'Origin': 'https://ct2.cpiworld.com',
            'Referer': 'https://ct2.cpiworld.com/Reports/ReportItems.aspx?Type=Admin',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
            }
        get_report_body = {
            'ctl00_RadScriptManager1_TSM': ';;System.Web.Extensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-US:b7585254-495e-4311-9545-1f910247aca5:ea597d4b:b25378d2;Telerik.Web.UI, Version=2015.1.401.40, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-US:f5c550b9-a65b-4cfb-8f9c-9833432cbee6:16e4e7cd:f7645509:24ee1bba:e330518b:2003d0b8:c128760b:88144a7a:1e771326:c8618e41:1a73651d:333f8d94:16d8629e;AjaxControlToolkit, Version=3.0.20820.16598, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:en-US:707835dd-fa4b-41d1-89e7-6df5d518ffb5:b14bb7d5:cecc93f9:dc2d6e36:5acd2e8e:13f47f54:4cda6429:35ff259d:efde3e73:ca84c49e',
            'ctl00_cph1_TreeView1_ExpandState': 'eennnnnnnnnnnnnnnnnnnnnnnnnnnnnnn',
            'ctl00_cph1_TreeView1_SelectedNode': 'ctl00_cph1_TreeView1t20',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            'ctl00_cph1_TreeView1_PopulateLog': '',
            '__VIEWSTATE':viewstate2,
            '__VIEWSTATEGENERATOR': viewstategen2,
            '__SCROLLPOSITIONX': '0',
            '__SCROLLPOSITIONY': '300',
            '__EVENTVALIDATION': event_valudation2,
            'ctl00$hidMsgText': '',
            'ctl00$hidDCEmail': '',
            'ctl00$hidEmail': '',
            'ctl00_HorizMenu1_HorizMenu1_ClientState': '',
            'ctl00_ProgramsHorizMenu1_ProgsHorizMenu_ClientState': '',
            'ctl00_HorizMenu2_HorizMenu1_ClientState': '',
            'ctl00_ProgramsHorizMenu2_ProgsHorizMenu_ClientState': '',
            'ctl00_mnuNav_ClientState': '',
            'ctl00$cph1$cbx1': '389',
            'ctl00$cph1$cbx2': 'All',
            'ctl00$cph1$txt3': '',
            'ctl00$cph1$txt4': '',
            'ctl00$cph1$txt5': '01/01/2011',
            'ctl00$cph1$txt6': '05/31/2080',
            'ctl00$cph1$lbx7': 'All',
            'ctl00$cph1$txt8': '',
            'ctl00$cph1$txt9': '',
            'ctl00$cph1$txt10': '',
            'ctl00$cph1$txt11': '',
            'ctl00$cph1$txt12': '',
            'ctl00$cph1$txt13': '',
            'ctl00$cph1$cbx14': '0',
            'ctl00$cph1$cbx15': '_null_',
            'ctl00$cph1$txt16': '', 
            'ctl00$cph1$txt17': '',
            'ctl00$cph1$cmdViewXLS': 'View as Excel'
            }
        participation = self.s.post(url=self.report_url, data=get_report_body, headers=get_report_headers)
        print("making post to participation to get Excel")
        print(participation)
        print("web scrapping reportpopper")
        soup = BeautifulSoup(participation.content, 'html.parser')
        report = soup.find(string=re.compile("ReportOutput"))
        url = report[14:91]
        participant_report_url = url[:4] + "s" + url[4:]
        print(" Rename to Participant_Report")
        participation_get_headers = {
            'Host': 'ct2.cpiworld.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-AU,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            }
        participation_get_results = self.s.get(url=participant_report_url, headers=participation_get_headers, stream=True)
        print("Getting content now :)")
        with BytesIO(participation_get_results.content) as input_blob:
            blob_service = BlockBlobService(account_name=self.account_name, account_key=self.account_key)
            blob_service.create_blob_from_stream('csv-blob', blob_name=self.blob_path + 'Participation_Reports_Production/Participant_Report.xls', stream=input_blob)
            generator = blob_service.list_blobs('csv-blob')
            for blob in generator:
                print("\t Blob name: " + blob.name)
    def sales_report(self):
        post_sales_report_body = {
            'ctl00_RadScriptManager1_TSM': ';;System.Web.Extensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-US:b7585254-495e-4311-9545-1f910247aca5:ea597d4b:b25378d2;Telerik.Web.UI, Version=2015.1.401.40, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-US:f5c550b9-a65b-4cfb-8f9c-9833432cbee6:16e4e7cd:f7645509:24ee1bba:e330518b:2003d0b8:c128760b:88144a7a:1e771326:c8618e41:1a73651d:333f8d94:16d8629e',
            'ctl00_cph1_TreeView1_ExpandState': 'eennnnnnnnnnnnnnnnnnnnnnnnnnnnnnn',
            'ctl00_cph1_TreeView1_SelectedNode': ' ctl00_cph1_TreeView1t29',
            '__EVENTTARGET': 'ctl00$cph1$TreeView1',
            '__EVENTARGUMENT': 'sRO0\CA0\RI8',
            'ctl00_cph1_TreeView1_PopulateLog': '',
            '__VIEWSTATE': self.viewstate,
            '__VIEWSTATEGENERATOR': self.viewstategen,
            '__EVENTVALIDATION': self.event_valudation,
            'ctl00$hidMsgText': '',
            'ctl00$hidDCEmail': '',
            'ctl00$hidEmail': '',
            'ctl00_HorizMenu1_HorizMenu1_ClientState': '',
            'ctl00_ProgramsHorizMenu1_ProgsHorizMenu_ClientState': '',
            'ctl00_HorizMenu2_HorizMenu1_ClientState': '',
            'ctl00_ProgramsHorizMenu2_ProgsHorizMenu_ClientState': '',
            'ctl00_mnuNav_ClientState': ''
            }
        sales_report_get_resource_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-AU,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'ct2.cpiworld.com',
            'Origin': 'https://ct2.cpiworld.com',
            'Referer': 'https://ct2.cpiworld.com/Reports/ReportItems.aspx?Type=Admin',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
            }
        print("verifing states")
        resource_get_sales_report = self.s.post(url=self.report_url, data=post_sales_report_body, headers=sales_report_get_resource_headers)
        print("moving towards Sales reports")
        print(resource_get_sales_report)
        html2 = BeautifulSoup(resource_get_sales_report.content,'html.parser')
        viewstate2 = html2.select("#__VIEWSTATE")[0]['value']
        viewstategen2 = html2.select("#__VIEWSTATEGENERATOR")[0]['value']
        event_valudation2 = html2.select("#__EVENTVALIDATION")[0]['value']
        print("web scrapping stategen2")
        report_get_resource = self.s.get(url=self.report_url, headers=self.get_headers)     
        print(report_get_resource)
        sales_report = {
            'ctl00_RadScriptManager1_TSM': ';;System.Web.Extensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-US:b7585254-495e-4311-9545-1f910247aca5:ea597d4b:b25378d2;Telerik.Web.UI, Version=2015.1.401.40, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-US:f5c550b9-a65b-4cfb-8f9c-9833432cbee6:16e4e7cd:f7645509:24ee1bba:e330518b:2003d0b8:c128760b:88144a7a:1e771326:c8618e41:1a73651d:333f8d94:16d8629e;AjaxControlToolkit, Version=3.0.20820.16598, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:en-US:707835dd-fa4b-41d1-89e7-6df5d518ffb5:b14bb7d5:cecc93f9:dc2d6e36:5acd2e8e:13f47f54:4cda6429:35ff259d:efde3e73:ca84c49e',
            'ctl00_cph1_TreeView1_ExpandState': 'eennnnnnnnnnnnnnnnnnnnnnnnnnnnnnn',
            'ctl00_cph1_TreeView1_SelectedNode': 'ctl00_cph1_TreeView1t29',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            'ctl00_cph1_TreeView1_PopulateLog': '',
            '__VIEWSTATE':viewstate2,
            '__VIEWSTATEGENERATOR': viewstategen2,
            '__SCROLLPOSITIONX': '0',
            '__SCROLLPOSITIONY': '100',
            '__EVENTVALIDATION': event_valudation2,
            'ctl00$hidMsgText': '',
            'ctl00$hidDCEmail': '',
            'ctl00$hidEmail': '',
            'ctl00_HorizMenu1_HorizMenu1_ClientState': '',
            'ctl00_ProgramsHorizMenu1_ProgsHorizMenu_ClientState': '',
            'ctl00_HorizMenu2_HorizMenu1_ClientState': '',
            'ctl00_ProgramsHorizMenu2_ProgsHorizMenu_ClientState': '',
            'ctl00_mnuNav_ClientState': '',
            'ctl00$cph1$cbx1': '389',
            'ctl00$cph1$txt2': '',
            'ctl00$cph1$cbx3': '_null_',
            'ctl00$cph1$cbx4': '_null_',
            'ctl00$cph1$cbx5': '0',
            'ctl00$cph1$cbx6': '0',
            'ctl00$cph1$cbx7': '_null_',
            'ctl00$cph1$cbx8': '_null_',
            'ctl00$cph1$txt9': '',
            'ctl00$cph1$txt10': '',
            'ctl00$cph1$txt11': '02/01/2011',
            'ctl00$cph1$txt12': '05/23/2080',
            'ctl00$cph1$txt13': '',
            'ctl00$cph1$txt14': '',
            'ctl00$cph1$cbx15': '0',
            'ctl00$cph1$cmdViewXLS': 'View as Excel'
            }
        sales_report = self.s.post(url=self.report_url, data=sales_report, headers=sales_report_get_resource_headers)
        print(sales_report)
        soup = BeautifulSoup(sales_report.content, 'html.parser')
        report = soup.find(string=re.compile("ReportOutput"))
        url = report[14:91] 
        sales_report_url = url[:4] + "s" + url[4:]
        print(" Rename to Sales_Report")
        sales_report_get_headers = {
            'Host': 'ct2.cpiworld.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-AU,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            }
        sales_report = self.s.get(url=sales_report_url, headers=sales_report_get_headers)
        print("Getting content now :)")
        with BytesIO(sales_report.content) as input_blob:
            blob_service = BlockBlobService(account_name=self.account_name, account_key=self.account_key)
            blob_service.create_blob_from_stream('csv-blob', blob_name= self.blob_path + 'Sales_Report_Production/sales_report.xls', stream=input_blob)
            generator = blob_service.list_blobs('csv-blob')
            for blob in generator:
                print("\t Blob name: " + blob.name)
    def time_tracker(self):
        post_report_participation = {
            'ctl00_RadScriptManager1_TSM': ';;System.Web.Extensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-US:b7585254-495e-4311-9545-1f910247aca5:ea597d4b:b25378d2;Telerik.Web.UI, Version=2015.1.401.40, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-US:f5c550b9-a65b-4cfb-8f9c-9833432cbee6:16e4e7cd:f7645509:24ee1bba:e330518b:2003d0b8:c128760b:88144a7a:1e771326:c8618e41:1a73651d:333f8d94:16d8629e',
            'ctl00_cph1_TreeView1_ExpandState': 'eennnnnnnnnnnnnnnnnnnnnnnnnnnnnnn',
            'ctl00_cph1_TreeView1_SelectedNode': 'ctl00_cph1_TreeView1t31',
            '__EVENTTARGET': 'ctl00$cph1$TreeView1',
            '__EVENTARGUMENT': 'sRO0\CA0\RI22',
            'ctl00_cph1_TreeView1_PopulateLog': '',
            '__VIEWSTATE': self.viewstate,
            '__VIEWSTATEGENERATOR': self.viewstategen,
            '__EVENTVALIDATION': self.event_valudation,
            'ctl00$hidMsgText': '',
            'ctl00$hidDCEmail': '',
            'ctl00$hidEmail': '',
            'ctl00_HorizMenu1_HorizMenu1_ClientState': '',
            'ctl00_ProgramsHorizMenu1_ProgsHorizMenu_ClientState': '',
            'ctl00_HorizMenu2_HorizMenu1_ClientState': '',
            'ctl00_ProgramsHorizMenu2_ProgsHorizMenu_ClientState': '',
            'ctl00_mnuNav_ClientState': ''
            }
        post_report_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-AU,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'ct2.cpiworld.com',
            'Origin': 'https://ct2.cpiworld.com',
            'Referer': 'https://ct2.cpiworld.com/Reports/ReportItems.aspx?Type=Admin',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
            }
        print("verifing states")
        resource_get_timetracker = self.s.post(url=self.report_url, data=post_report_participation, headers=post_report_headers)
        print("moving towards timetracker reports")
        print(resource_get_timetracker)
        html2 = BeautifulSoup(resource_get_timetracker.content,'html.parser')
        viewstate2 = html2.select("#__VIEWSTATE")[0]['value']
        viewstategen2 = html2.select("#__VIEWSTATEGENERATOR")[0]['value']
        event_valudation2 = html2.select("#__EVENTVALIDATION")[0]['value']
        print("web scrapping stategen2")
        get_other_report_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-AU,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'ct2.cpiworld.com',
            'Origin': 'https://ct2.cpiworld.com',
            'Referer': 'https://ct2.cpiworld.com/Reports/ReportItems.aspx?Type=Admin',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
            }
        get_other_report_body = {
            'ctl00_RadScriptManager1_TSM': ';;System.Web.Extensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-US:b7585254-495e-4311-9545-1f910247aca5:ea597d4b:b25378d2;Telerik.Web.UI, Version=2015.1.401.40, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-US:f5c550b9-a65b-4cfb-8f9c-9833432cbee6:16e4e7cd:f7645509:24ee1bba:e330518b:2003d0b8:c128760b:88144a7a:1e771326:c8618e41:1a73651d:333f8d94:16d8629e;AjaxControlToolkit, Version=3.0.20820.16598, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:en-US:707835dd-fa4b-41d1-89e7-6df5d518ffb5:b14bb7d5:cecc93f9:dc2d6e36:5acd2e8e:13f47f54:4cda6429:35ff259d:efde3e73:ca84c49e',
            'ctl00_cph1_TreeView1_ExpandState': 'eennnnnnnnnnnnnnnnnnnnnnnnnnnnnnn',
            'ctl00_cph1_TreeView1_SelectedNode': 'ctl00_cph1_TreeView1t31',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            'ctl00_cph1_TreeView1_PopulateLog': '',
            '__VIEWSTATE':viewstate2,
            '__VIEWSTATEGENERATOR': viewstategen2,
            '__SCROLLPOSITIONX': '0',
            '__SCROLLPOSITIONY': '300',
            '__EVENTVALIDATION': event_valudation2,
            'ctl00$hidMsgText': '',
            'ctl00$hidDCEmail': '',
            'ctl00$hidEmail': '',
            'ctl00_HorizMenu1_HorizMenu1_ClientState': '',
            'ctl00_ProgramsHorizMenu1_ProgsHorizMenu_ClientState': '',
            'ctl00_HorizMenu2_HorizMenu1_ClientState': '',
            'ctl00_ProgramsHorizMenu2_ProgsHorizMenu_ClientState': '',
            'ctl00_mnuNav_ClientState': '',
            'ctl00$cph1$cbx1': '389',
            'ctl00$cph1$txt2': '',
            'ctl00$cph1$txt3': '12/29/2011',
            'ctl00$cph1$txt4': '05/31/2080',
            'ctl00$cph1$txt5': '',
            'ctl00$cph1$txt6': '',
            'ctl00$cph1$cbx7': 'All',
            'ctl00$cph1$cbx8': '0',
            'ctl00$cph1$cbx9': '377411',
            'ctl00$cph1$cmdViewXLS': 'View as Excel'
            }
        time_tracker = self.s.post(url=self.report_url, data=get_other_report_body, headers=get_other_report_headers)
        print(time_tracker)
        print("web scrapping reportpopper")
        soup = BeautifulSoup(time_tracker.content,'html.parser')
        report_url3 = soup.find(string=re.compile("ReportOutput"))
        url = report_url3[14:91] 
        time_Tracker_url = url[:4] + "s" + url[4:]
        print(" Rename into Time_tracker")
        time_tracker_get_headers = {
            'Host': 'ct2.cpiworld.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-AU,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            }
        time_tracker = self.s.get(url=time_Tracker_url, headers=time_tracker_get_headers, timeout=5)
        print("Getting content now :)")
        print(time_tracker)
        with BytesIO(time_tracker.content) as input_blob:
            blob_service = BlockBlobService(account_name=self.account_name, account_key=self.account_key)
            blob_service.create_blob_from_stream('csv-blob', blob_name=self.blob_path + 'Time_Tracker_Production/time_tracker.xls', stream=input_blob)
            generator = blob_service.list_blobs('csv-blob')
            for blob in generator:
                print("\t Blob name: " + blob.name)
                



































if __name__ == "__main__":
    data = config()
    participant = data.participant_report()
    sales_report = data.sales_report()
    time_tracker = data.time_tracker()

