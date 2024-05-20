from tqdm.contrib.concurrent import thread_map
from bs4 import BeautifulSoup
import pandas as pd
import requests
import streamlit as st


st.header('EZeeAssist Scrapring Test', divider='rainbow')

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}
link = requests.get('https://franchisesuppliernetwork.com/',headers=headers)
try:
    if link.status_code == 200:
        st.subheader(f'Scraping :blue[{link.url}]')
        code = BeautifulSoup(link.text,'html.parser')
        work_div = code.find('div',{'class':'home-why-choose-inner'})
        heading_home_page = [x.find('h3').text.strip() for x in work_div.find_all('li')]
        works_value_home_page = [x.find('p').text.strip() for x in work_div.find_all('li')]
        
        st.write('')
        st.write(f'Getting data from home page >> {link.url}')
        # How It Works Section
        how_it_works_dict = dict(zip(heading_home_page,works_value_home_page))
        st.subheader('Section :blue[How it works]')
        st.write(how_it_works_dict)

        # We’ve Helped Section
        st.write('')
        logo_div = code.find('div',{'class':'logos-inner'})
        companies_img_links = [x['src'] for x in logo_div.find_all('img')]
        company_names = [x['src'].split('/')[-1].replace('.jpg','') for x in logo_div.find_all('img')]
        section_2 = logo_div.find_previous().text.strip() # We’ve Helped
        companies_dict = dict(zip(company_names,companies_img_links))
        st.subheader('Section :blue[We’ve Helped]')
        st.write(companies_dict)
        
        # The FSN Difference
        st.write('')

        fsn_div = code.find('div',{'class':'process-con'})
        title_fsn = fsn_div.find_previous('h2').text.strip()
        fsn_text = fsn_div.find_previous('h2').find_next().text.strip()
        fsn_heading = [x.text.strip() for x in fsn_div.find_all('h3')]
        fsn_value = [x.text.strip() for x in fsn_div.find_all('p')]
        fsn_dict = dict(zip(fsn_heading,fsn_value))

        st.subheader('Section :blue[The FSN Difference]')
        st.write(title_fsn)
        st.write(fsn_text)
        st.write(fsn_dict)

        # 3 Ways We Help Franchisors:
        st.write('')

        section_3_title = code.find('h2',{'class':'hcwh-title'}).text.strip()
        section_3_div = code.find('div',{'class':'hcwh-sec-02'})
        section_3_div.find_all('h2')[2].find_next()
        section_3_div_key = [x.text.strip() for x in section_3_div.find_all('h2')]
        section_3_div_value = [x.find_next().text.strip() for x in section_3_div.find_all('h2')]
        section_dict = dict(zip(section_3_div_key,section_3_div_value))

        st.subheader('Section :blue[3 Ways We Help Franchisors]')
        st.write(section_dict)

        # about section
        st.subheader('Section :blue[About Us]')
        about = requests.get('https://franchisesuppliernetwork.com/about/',headers=headers)
        if about.status_code == 200:
            st.write('')
            st.write(f'Getting data from about page >> {about.url}')
            about_code = BeautifulSoup(about.text, 'html.parser')
            about_main_div = about_code.find('section',{'class':'inner-content'})
            about_heading =  about_main_div.find('div',{'class':'col-lg-12 contentside'}).find('h2').text.strip()
            about_text = ' '.join([x.text.strip() for x in about_main_div.find('div',{'class':'col-lg-12 contentside'}).find_all('p')])

            name = [x.text.strip() for x in about_main_div.find_all('h3')]
            designation = [x.text.strip() for x in about_main_div.find_all('h4')]
            profile_img_url = [x['src'] for x in about_main_div.find_all('img')]

            about_dict = {}
            for data in range(len(about_main_div.find_all('div',{'class':'col-md-9'}))):
                name = about_main_div.find_all('h3')[data].text.strip()
                designation = about_main_div.find_all('h4')[data].text.strip()
                para = ' '.join([x.text.strip() for x in about_main_div.find_all('div',{'class':'col-md-9'})[data].find_all('p')])
                about_dict['Name'] = name
                about_dict['Designation'] = name
                about_dict['About'] = para
                st.write(about_dict)

except Exception:
    print('Error in passing the link')


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}
def pagination_url():
    inner_page = requests.get('https://franchisesuppliernetwork.com/fsn-suppliers/',headers=headers)
    inner_page_code = BeautifulSoup(inner_page.text, 'html.parser')
    
    main_div = inner_page_code.find('section',{'class':'inner-content'})
    total_pages = int(main_div.find('div',{'class':'wp-pagenavi'}).find('span').text.split('of')[-1].strip())
    pagination_links = []
    pagination_links.append(inner_page.url)
    for i in range(2,total_pages+1):
        pagination_links.append(f"https://franchisesuppliernetwork.com/fsn-suppliers/page/{i}")
    return pagination_links

total_pagination_urls = pagination_url()

def suppliers_page(pass_link):
    data_dict = {}
    link = requests.get(pass_link,headers=headers)
    code = BeautifulSoup(link.text, 'html.parser')  
    main_div = code.find('section',{'class':'inner-content'})
    data_links = [x.find('a')['href'] for x in main_div.find_all('div',{'class':'fs-single'})]
    return data_links

suppliers_page_data_dict = thread_map(suppliers_page,total_pagination_urls)

clean_inner_page_links = [x for y in suppliers_page_data_dict for x in y]
st.write('')
st.header('Scrapring FSN  Suppliers Infomation', divider='rainbow')
st.write(f'Total links in fsn-suppliers section >> {len(clean_inner_page_links)}')

def inner_page_data(pass_link):
    suppliers_inner_page = requests.get(pass_link,headers=headers)
    suppliers_inner_page_code = BeautifulSoup(suppliers_inner_page.text, 'html.parser')
    
    supplier_data_dict = {}
    supplier_title = suppliers_inner_page_code.find('ol',{'class':'breadcrumb'}).find_all('span')[-1].text.strip()
    supplier_data_dict['Title'] = supplier_title
    
    main_supplier_div = suppliers_inner_page_code.find('section',{'class':'inner-content'})
    
    info_section_headings = [x.text.strip() for x in main_supplier_div.find('div',{'class':'row fs-body'}).find_all('h2')]
    info_section_data = [x.find_next_sibling().text.strip() if x.find_next_sibling() else '' for x in main_supplier_div.find('div', {'class': 'row fs-body'}).find_all('h2')]
    new_supplier_data_dict = dict(zip(info_section_headings,info_section_data))
    
    web_link = main_supplier_div.find('div',{'class':'row fs-body'}).find('h2').find_next_siblings()[-1].find('a')['href']
    location = main_supplier_div.find('div',{'class':'row fs-body'}).find('h2').find_next_siblings()[-1].text.strip().split('\n')[0]
    
    supplier_data_dict['Website'] = web_link
    supplier_data_dict['Location'] = location
    
    main_div_2 = main_supplier_div.find('div',{'class':'row fs-content'})
    try:
        ind_tags = ', '.join([x.text.strip() if x else '' for x in main_div_2.find('ul',{'class':'industry-tags'}).find_all('li')])
        to_remove = main_div_2.find_all('div',{'class':'col-lg-6'})[-1].find('strong').text.strip()
        supplier_data_dict['Industries'] = ind_tags
    except:
        supplier_data_dict['Industries'] = ''
        
    head_qurates = main_div_2.find_all('div',{'class':'col-lg-6'})[-1].text.strip().replace(to_remove,'').strip()
    
    
    supplier_data_dict['Headquarters Regions'] = head_qurates
    
    supplier_data_dict.update(new_supplier_data_dict)
    
    
    to_remove_2 = main_supplier_div.find('div',{'class':'col-lg-12'}).find('strong').text.strip()
    founded_date = main_supplier_div.find('div',{'class':'col-lg-12'}).text.strip().replace(to_remove_2,'').strip()
    
    des = main_supplier_div.find('div',{'id':'contentMain'}).get_text(strip=True)
    try:
        linkedin_page = main_supplier_div.find('div',{'class':'social-icons'}).find('a')['href']
        supplier_data_dict['LinkedIn'] = linkedin_page
    except:
        supplier_data_dict['LinkedIn'] = ''
    
    supplier_data_dict['Founded Date'] = founded_date
   

    return supplier_data_dict

inner_page_data_dict = thread_map(inner_page_data, clean_inner_page_links)
df = pd.DataFrame(inner_page_data_dict)

data_frame = st.dataframe(inner_page_data_dict)
st.write(f'Data Frame shape >> {df.shape}')
get_csv = st.button('Download CSV')
if get_csv:
    try:
        df.to_csv(f'suppliers_info.csv', index=False)
    except:
            st.write('Error in generating CSV')
