from flask import Flask, flash, redirect, escape, request, render_template, url_for
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/')
def index():    
    return render_template('index.html')

# Form에서 입력받은 데이터를 가공해서 결과를 전달해줌
@app.route('/result', methods=['GET', 'POST'])
def result():

    dayofweek=request.form.get('dayofweek')
    gender=request.form.get('gender')
    age=request.form.get('age')
    gu=request.form.get('gu')
    temperature = request.form.get('Temperature')
    rainfall = request.form.get('Rainfall')
    game_count = request.form.get('game_count')

    print(type(dayofweek), type(gender), type(age), type(gu), type(temperature), type(rainfall), type(game_count))

    # 모든 값을 int형으로 바꿔줘야함
    dayofweek = int(dayofweek)
    gender = int(gender)
    age = int(age)
    gu = int(gu)
    temperature = float(temperature)
    rainfall = round(float(rainfall), 2)
    game_count = int(game_count)

    print(dayofweek, gender, age, gu, temperature, rainfall, game_count)

    # 의사결정트리 함수에 입력값 전달
    result_value = decision_tree(dayofweek, gender, age, gu, temperature, rainfall, game_count)
    
    if result_value == 0:
        message = "오늘은 주문이 저조할 것 같습니다 T.T"
        
    elif result_value == 1:
        message = "오늘은 평소처럼 준비하시면 되겠습니다! :)"
        
    else:
        message = "오늘은 주문이 많겠네요! 미리 대비해주세요! :D"


    return render_template('result.html', message=message)    
    #return render_template('index.html')


# 의사결정트리를 생성하고 유저가 입력한 값을 받아 예측한 결과값을 전달
def decision_tree(dayofweek, gender, age, gu, temperature, rainfall, game_count):
    chCall_df = pd.read_csv("C:/ai/workspace/Module_project02/decision_tree_table.csv")
    y_label = chCall_df['CALLCNT']
    chCall_df.drop('CALLCNT', axis=1, inplace=True)
    X_train, X_test, y_train, y_test = train_test_split(chCall_df, y_label)
    dt_clf = DecisionTreeClassifier()
    dt_clf=dt_clf.fit(X_train, y_train)
    dt_prediction = dt_clf.predict(X_test)  

    new_data = np.array([[dayofweek, gender, age, gu, temperature, rainfall, game_count]])
    predict_value = dt_clf.predict(new_data)
    return predict_value

# result 페이지에서 홈버튼을 눌렀을 시 index 페이지로 이동
@app.route('/go_home')
def go_home():    
    return redirect(url_for('index'))

# python app.py로 실행
if __name__ == '__main__':
    app.run(debug=True) 