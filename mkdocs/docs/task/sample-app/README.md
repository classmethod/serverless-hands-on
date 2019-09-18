# サンプルアプリケーションのデプロイ

この課題ではサンプルのアプリケーションのコードを確認し､デプロイを行います｡  

## サンプルアプリケーションの取得

1. 作業ディレクトリに移動します｡
```bash
cd ~/environment
```
1. サンプルアプリケーションを取得します｡
```bash
sam init -r python3.6
```
1. 取得できていることを確認します｡
```bash
ls sam-app
```
(例)
```bash
hello_world  README.md  template.yaml  tests
```

## ディレクトリ構成

サンプルアプリケーションの構成は下記の様になっています｡  

```bash
sam-app/
├── hello_world                     # アプリケーションディレクトリ
│   ├── app.py                      # Lambda関数
│   ├── app.pyc
│   ├── __init__.py
│   ├── __init__.pyc
│   └── requirements.txt            # ライブラリ定義
├── README.md                       # 説明
├── template.yaml                   # SAMテンプレート(AWSの構成情報)
└── tests                           # テストディレクトリ
    └── unit                        # ユニットテストディレクトリ
        ├── __init__.py
        ├── __init__.pyc
        ├── test_handler.py         # Lambda関数のテストコード
        └── test_handler.pyc
```

## app.py

`app.py`はLambda関数として使用されるコードです｡行いたい処理内容を記載します｡  

```python hl_lines="4 6 13" 
import json
import requests

# Lambdaハンドラー
def lambda_handler(event, context):
    # 実行処理
    try:
        ip = requests.get("http://checkip.amazonaws.com/")
    except requests.RequestException as e:
        print(e)

        raise e
    # レスポンス
    return {
        "statusCode": 200,
        "body": json.dumps(
            {"message": "hello world", "location": ip.text.replace("\n", "")}
        ),
    }
```

### Lambdaハンドラー

Lambda関数は作成する際に､ハンドラーを指定します。これはコードを実行する際に､AWS Lambdaがどの関数を呼び出すかの宣言です。 
<!-- TODO: Lambdaハンドラーのスクリーンショット -->
引数は下記の通りです｡  

- event: 呼び出し元から受け取るイベントデータです｡このパラメータは通常､Pythonのdict型です｡
呼び出し元により､構成は異なります｡
- context: ランタイム情報です｡(ハンズオンでは取り扱いません｡)

<a href="https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-programming-model-handler-types.html" target="_blank">PythonのAWS Lambda関数ハンドラー
 :fa-external-link: </a>

### 実行処理

Lambda内で実行する処理を書きます｡
このアプリケーションでは､`http://checkip.amazonaws.com/`というアクセス元のグローバルIPアドレスをレスポンスするサイトを使って
Lambda関数のグローバルIPアドレスを取得しています｡  
例外(requests.RequestException)が発生した場合は､内容を`print`で出力します｡
Lambda関数の標準出力は<a href="https://docs.aws.amazon.com/ja_jp/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html" target="_blank">Amazon CloudWatch Logs :fa-external-link: </a>に保存されます｡  

### レスポンス

Lambda関数が後続の処理に返す処理結果を記載します｡どのサービスと連携するかによって戻り値の構成は異なります｡  
このアプリケーションでは､<a href="https://docs.aws.amazon.com/ja_jp/apigateway/latest/developerguide/welcome.html" target="_blank">Amazon API Gateway :fa-external-link: </a>に返すので､HTTPレスポンス形式です｡  

## test_handler.py

`test_handler.py`は`app.py`のテストコード､つまりLambda関数のテストコードです｡  
pytestを利用しています｡  

```python hl_lines="6 14"
import json
import pytest
from collections import namedtuple
from hello_world import app

# テストデータ
@pytest.fixture()
def apigw_event():

    return {
    # 省略: API GatewayがLambda関数に渡すeventのテストデータです
    }

# テスト
def test_lambda_handler(apigw_event, mocker):

    requests_response_mock = namedtuple("response", ["text"])
    requests_response_mock.text = "1.1.1.1\n"

    request_mock = mocker.patch.object(
        app.requests, 'get', side_effect=requests_response_mock)

    ret = app.lambda_handler(apigw_event, "")
    assert ret["statusCode"] == 200

    for key in ("message", "location"):
        assert key in ret["body"]

    data = json.loads(ret["body"])
    assert data["message"] == "hello world"
```

### テストデータ

API GatewayがLambda関数を呼び出す際のeventをテスト様に生成しています｡  

### テスト

Lambda関数のテストコードです｡  
ユニットテストなので､外部へのリクエストを行う箇所は常に`1.1.1.1`を受け取るようにモックしています｡  
以下のテストを行っています｡

- ステータスコードが200(OK)である
- レスポンスボディに`message`, `location`という項目を含む
- レスポンスボディの`data`は`hello world`である

## template.yaml

<a href="https://docs.aws.amazon.com/ja_jp/serverless-application-model/latest/developerguide/what-is-sam.html" target="_blank">SAM(Serverless Application Model) :fa-external-link: </a>
はサーバーレス向けのAWS環境構築の為のフレームワークです｡  
<a href="https://docs.aws.amazon.com/ja_jp/AWSCloudFormation/latest/UserGuide/Welcome.html" target="_blank">AWS CloudFormation :fa-external-link: </a>の拡張で､
サーバーレスアプリケーションを構築する場合はより簡単・少ない記述でインフラストラクチャーを定義する事が可能です｡  
SAMはCloudFormationに変換してからAWSにデプロイします｡(AWS上ではCloudFormationとして扱われます)  

下記のようなSAMの定義ファイルを**SAMのテンプレート**と言います｡  

```yaml hl_lines="6 9"
AWSTemplateFormatVersion: '2010-09-09'
Transform: 'AWS::Serverless-2016-10-31'
Description: |
  sam-app
  Sample SAM Template for sam-app
Globals:
  Function:
    Timeout: 3
Resources:
  HelloWorldFunction:
    Type: 'AWS::Serverless::Function'
    Properties:
      CodeUri: hello_world/
      Handler: app.lambda_handler
      Runtime: python3.6
      Environment:
        Variables:
          PARAM1: VALUE
      Events:
        HelloWorld:
          Type: Api
          Properties:
            Path: /hello
            Method: get
      Description: ''
      MemorySize: ''
Outputs:
  HelloWorldApi:
    Description: API Gateway endpoint URL for Prod stage for Hello World function
    Value:
      'Fn::Sub': >-
        https://${ServerlessRestApi}.execute-api.${AWS::Region}.amazonaws.com/Prod/hello/
  HelloWorldFunction:
    Description: Hello World Lambda Function ARN
    Value:
      'Fn::GetAtt':
        - HelloWorldFunction
        - Arn
  HelloWorldFunctionIamRole:
    Description: Implicit IAM Role created for Hello World function
    Value:
      'Fn::GetAtt':
        - HelloWorldFunctionRole
        - Arn
```

!!! Info
    template.yamlを開くとフォームが表示される場合は､**View**､**Editors**､**Ace**と選択してください｡  
    ![](./img/001.png)
    
### Globals

このテンプレート内のリソース全体に適用する設定です｡  
Funcitonに対してTimeoutを3(秒)に設定しています｡このテンプレートで定義したLambda関数のタイムアウトは3秒に設定するという意味です｡  
個々のリソースで設定した場合は､その値が優先されます｡  

### Resources

リソースの定義です｡

| 項目名 | 項目の説明 | テンプレートの説明 |
| --- | --- | --- |
| Type | 作成するリソースの種類 | `AWS::Serverless::Function`はLambda関数を作成します |
| CodeUri | Lambda関数のディレクトリ | `hello_world/`にLambda関数のコードは配置されています |
| Handler | Lambda関数のハンドラー | **app**.pyの**lambda_handler**関数を呼び出したいので`app.lambda_handler`と指定します |
| Runtime | Lambda実行環境 | Python3.6で実行を保証するコードなので､`python3.6`と指定します |
| Environment | Lambda環境変数 | 定義されていますが､Lambda関数内では使用していません |
| Events | Lambda呼び出し元の定義 | API Gatewayが`/hello`に`GET`リクエストを受けた時Lambda関数を呼び出す |
| MemorySize | Lambdaのメモリサイズ | MB単位でLambda関数に割り当てるメモリサイズを指定します(省略するとデフォルト値) |

一件すると､作成されるリソースはLambda関数だけと捉えてしまいがちですが､`Events`で定義している為､API Gatewayも作成されます｡  
