from flask import Flask, request, jsonify
app = Flask(__name__)
#from phpserialize import *
#from collections import OrderedDict
import json

#import helper

@app.route('/')
def index():
    return 'Hmm , Hello '

@app.route('/get-params', methods = ['POST'])
def params():


    if request.method == 'POST':
        uids = json.loads(request.form['uids'])
        print( uids )


    return 'Done'

@app.route('/add-friend', methods = ['POST'])
def add_friend():
    if request.method == 'POST':
        #c_user = request.form['c_user']
        #xs = request.form['xs']
        #uids = request.form['uids']

        clone = json.loads(request.form['clone'])

        print(clone)

        proxy = json.loads(request.form['proxy'])

        print(proxy)

        uids = json.loads(request.form['uids'])

        print(uids)


        '''

        ip = "123.31.47.8"
        port = 3128

        c_user = '100025055117657'
        xs = '32%3A6UmlBxPGvbIkQg%3A2%3A1522086654%3A-1%3A-1'


        driver = helper._init(ip, port, c_user, xs)


        uids = [
            '100011684994866',
            '100005920479740',
            '100012323105979',

            '100005000386196',

            '100016481881153',

            '100024281617327',

            '100007324654796',

            '100003006073815',

            '100004906892695',

            '100013449164615',

            '100006946448779',

            '100006002023894',

            '100014929969142',

            '100009964545150',

            '100004508137703',

            '100001494211864',

            '100013330413038',

        ]

        for uid in uids:
            try:
                helper.add_friend(driver, uid)
            except Exception as e:
                print(e)

        driver.quit()
        '''

    return 'Done'

if __name__ == '__main__':
   app.run(host='0.0.0.0')
