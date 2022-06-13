from flask import Flask, render_template, request
import geoip2.webservice
import geoip2.database

app = Flask(__name__, template_folder='./templates/')

@app.route('/', methods =["GET", "POST"])
def index():
    result = ''
    response = ''
    if request.method == "POST":
        response = request.form.get("ip")
        result = []
        if response:
            ips = response.split(',')
            with geoip2.database.Reader('./database/GeoLite2-City.mmdb') as reader:
                for ip in ips:
                    cityInfo = {'ip': ip, 'countryCode' : '-', 'postalCode' : '-', 'cityName' : '-', 'timeZone' : '-', 'acc' : '-'}
                    try:
                        response = reader.city(ip)
                        if response:
                            cityInfo['ip'] = ip
                            cityInfo['countryCode'] = response.country.iso_code
                            cityInfo['postalCode'] = response.postal.code
                            cityInfo['cityName'] = response.city.name
                            cityInfo['timeZone'] = response.location.time_zone
                            cityInfo['acc'] = response.location.accuracy_radius
                            result.append(cityInfo)
                    except:
                        result.append(cityInfo)
    return render_template('index.html', result = result, response=response)


if __name__ == '__main__':
    app.run(debug=True)



