from flask import Flask, render_template, jsonify
import requests
import re
from pymongo import MongoClient

app = Flask(__name__)


client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.myproject


@app.route('/')
def home():
    return render_template('main.html')

@app.route('/mypage')
def my_page():
    return 'This is My Page!'

@app.route('/post')
def post_page():
    return render_template('post.html')

@app.route('/review', methods=['GET'])
def read_reviews():
    return jsonify({'result': 'success', 'msg': '이 요청은 GET!'})


@app.route('/review', methods=['POST'])
def write_review():
    # title_receive로 클라이언트가 준 title 가져오기
    registration_receive = requests.data['registration_give']  #
    company_receive = requests.data['company_give']
    phone_receive = requests.data['phone_give']
    day_receive = requests.data['day_give']
    contents_receive = requests.contents['contents_give']
    xml = f"""<map id='ATTABZAA001R08'><pubcUserNo/><mobYn>N</mobYn>				<inqrTrgtClCd>1</inqrTrgtClCd><txprDscmNo>{registration_receive}</txprDscmNo>					<dongCode>05</dongCode><psbSearch>Y</psbSearch><map id='userReqInfoVO'/>		</map>"""
    response = requests.post('https://teht.hometax.go.kr/wqAction.do'
                             '?actionId=ATTABZAA001R08&screenId=UTEABAAA13&popupYn'
                             '=false&realScreenId=', data=xml)

    corp_status = re.search(r'(?<=Cntn>).*(?=</trt)', response.text).group()
    if corp_status.find('등록되어 있는 사업자등록번호 입니다.') > 0:
        print('사업자등록이 되어 있는 번호입니다')
    else:
        print('사업자등록이 되어 있지 않은 번호입니다')
    # DB에 삽입할 review 만들기
    review = {
        'registration': registration_receive,
        'company': company_receive,
        'phone': phone_receive,
        'day' : day_receive,
        'contents' : contents_receive
    }
    # reviews에 review 저장하기
    db.reviews.insert_one(review)
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success', 'msg': '리뷰가 성공적으로 작성되었습니다.'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
