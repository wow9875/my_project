from flask import Flask, render_template, jsonify
import requests
import re

# title_receive로 클라이언트가 준 title 가져오기
business_number = '7838601715'  #
xml = f"""<map id='ATTABZAA001R08'><pubcUserNo/><mobYn>N</mobYn>				<inqrTrgtClCd>1</inqrTrgtClCd><txprDscmNo>{business_number}</txprDscmNo>					<dongCode>05</dongCode><psbSearch>Y</psbSearch><map id='userReqInfoVO'/>		</map>"""
response = requests.post('https://teht.hometax.go.kr/wqAction.do'
                         '?actionId=ATTABZAA001R08&screenId=UTEABAAA13&popupYn'
                         '=false&realScreenId=', data=xml)

corp_status = re.search(r'(?<=Cntn>).*(?=</trt)', response.text).group()
if corp_status.find('등록되어 있는 사업자등록번호 입니다.') > 0:
    print('사업자등록이 되어 있는 번호입니다')
else:
    print('사업자등록이 되어 있지 않은 번호입니다')

