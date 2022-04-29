from flask import Flask, render_template
import redis

app = Flask(__name__)


def formatResults(res):
    res.strip("b'")
    res.strip("'")
    return res


@app.route('/')
def print_logs():
    result = [0, 0, 0, 0]
    universities_usa = ''
    avg_university_faculties = ''
    max_international_students = ''
    average_international_students = ''

    try:
        result.clear()
        conn = redis.StrictRedis(host='redis', port=6379)
        for key in conn.scan_iter("qs.log*"):
            str_k = str(key)
            str_k = str_k.strip("'")
            a = str_k.split(".")
            str_key = str(a[-1])

            val = str(conn.get(key))
            val = val.strip("b")
            val = val.strip("'")

            print(str_key)

            if(str_key == "universities_usa"):
                universities_usa = val
            elif(str_key == "avg_university_faculties"):
                avg_university_faculties = val
            elif(str_key == "max_international_students"):
                max_international_students = val
            elif(str_key == "average_international_students"):
                average_international_students = val

    except Exception as ex:
        output = 'Error:' + str(ex)

    return render_template('index.html', res1=universities_usa, res2=avg_university_faculties, res3=max_international_students, res4=average_international_students)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
