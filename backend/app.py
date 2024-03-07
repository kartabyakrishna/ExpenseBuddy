from flask import Flask, render_template, request, jsonify
import gspread
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1QFBuMsR0E2xom3nQAY3F-xqncGVC4vWFihWbWSe0AD8'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_expense():
    if request.method == 'POST':
        data = request.form.to_dict()

        creds = None
        token_path = 'token.json'
        credentials_path = 'ExpenseBuddy.json'

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)

            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        gc = gspread.authorize(creds)
        sheet = gc.open_by_key(SPREADSHEET_ID).sheet1

        row = [data.get('description'), data.get('categories'), data.get('account'),
               data.get('debitCredit'), float(data.get('amount'))]

        sheet.append_row(row)

        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid request method'})

if __name__ == '__main__':
    app.run(debug=True)
