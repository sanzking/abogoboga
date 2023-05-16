from flask import Flask, request, render_template, jsonify
import requests, json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def add_domains():
    if request.method == 'POST':
        # Cloudflare credentials
        cf_email = []
        cf_token = []
        apikey = request.form['apikey']
        if apikey == 'superwanwan09@gmail.com':
            cf_email.append('superwanwan09@gmail.com')
            cf_token.append('25c3cdd46b522e7d991f2991e9fc5e2371ea5')
        elif apikey == 'faqihkapo80@gmail.com':
            cf_email.append('faqihkapo80@gmail.com')
            cf_token.append('4e967692b8f05a2c49bb5c680a9f35ee24aaa')
        domains = request.files['domain_list']
        lines = domains.readlines()

        results = []

        for line in lines:
            domain = line.strip().decode('utf-8')

            # API URL
            api_url = 'https://api.cloudflare.com/client/v4/zones'

            # API call payload
            payload = {
                'name': domain,
                'jump_start': True
            }

            # send API request
            response = requests.post(api_url, headers={
                'X-Auth-Email': cf_email[0],
                'X-Auth-Key': cf_token[0],
                'Content-Type': 'application/json'
            }, json=payload)

            data = json.loads(response.text)

            if data['success'] == True:
                result = f'{domain} Berhasil ditambahkan'
            elif "already exists" in data['errors'][0]['message']:
                result = f'{domain} Domain sudah ada'
            else:
                result = f'{domain} Gagal ditambahkan'

            results.append(result)

        return jsonify(results=results)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)