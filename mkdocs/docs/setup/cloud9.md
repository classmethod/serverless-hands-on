# Cloud9による環境の準備

## Cloud9とは

AWSが提供しているクラウド上で動く､アプリケーション開発環境です｡  
コードエディタと開発環境がWeb上から使えます｡  
AWS CLIとAWS SAM CLIなどAWSを使った開発に必要なツールや基本的な言語環境が
インストール済みです｡  

<a href="https://aws.amazon.com/jp/cloud9/" target="_blank">AWS Cloud9（Cloud IDE でコードを記述、実行、デバッグ）\| AWS :fa-external-link: </a>	

## なぜ今回Cloud9を使うか

- 最初からAWSを使った開発に必要なツールがインストールされている
- 環境の準備という本質的でない所でつまづいて欲しくない
- ハンズオンの性質上ローカルマシンを統一できない

弊社で実績はありませんが､実際にプロダクトで使用されている例はあります｡  

<a href="https://speakerdeck.com/marumoto/jaws-days2018?slide=75" target="_blank">ユーザー企業におけるサーバレスシステムへの移行/JAWS DAYS2018 :fa-external-link: </a>	

## Cloud9 Environmentの作成

!!! Warning
    マネジメントコンソールの右上で､
    リージョンが**東京(ap-northeast-1)**になっている事を確認してください｡

!!! Info
    SafariでCloud9を使用する場合には､**サイト越えトラッキングを防ぐ**と**すべてのCookieをブロック**を無効にする必要があります｡  
    <a href="https://support.apple.com/ja-jp/guide/safari/sfri11471/mac" target="_blank">Mac の Safari で Cookie と Web サイトのデータを管理する :fa-external-link: 
</a>

1. <a href="https://ap-northeast-1.console.aws.amazon.com/cloud9/home/product" target="_blank">AWS Cloud9 :fa-external-link: </a>を開く	
1. **Create environment**を選択します｡  
1. 環境を設定し､**Next step**を選択します｡  
    - Name: sls-hands-on
    - Description: 何も入力しない
1. デフォルトの設定のまま､**Next step**を選択します｡ 
    - Environment type: Create a new instance for environment (EC2)
    - Instance type: t2.micro (1 GiB RAM + 1 vCPU)
    - Platform: Amazon Linux
    - Cost-saving setting: Afrer 30minutes(default)
    - IAM role: AWSServiceRoleForAWSCloud9
1. 設定を確認し､**Create environment**を選択します｡
1. Cloud9が起動します｡  

!!! Info
    Cloud9を開いているウィンドウを閉じてしまった場合は､再度<a href="https://ap-northeast-1.console.aws.amazon.com/cloud9/home/product" target="_blank">AWS Cloud9 :fa-external-link: </a>を開き､
    **sls-hands-on**の**Open IDE**を選択します｡
    
## Python3のデフォルト設定

Cloud9(Amazon Linux)では､Python3系がデフォルトになっていますが､pipはPython2系になっています｡  

2019/09/18時点の確認
```
python --version
# Python 3.6.8
pip --version
# pip 9.0.3 from /usr/lib/python2.7/dist-packages (python 2.7)
```

ハンズオンではPython3系を使用するので､設定を変更します｡  


1. 下記のコマンドを実行します｡  
```
sudo update-alternatives --config python
```
1. Python3系を選択します｡(下記の場合は2)
```
There are 2 programs which provide 'python'.

  Selection    Command
-----------------------------------------------
*+ 1           /usr/bin/python2.7
   2           /usr/bin/python3.6

Enter to keep the current selection[+], or type selection number: 2
```
1. バージョンがPython3系になっている事を確認します｡
```
python --version
pip --version
```
(例)
```text
Python 3.6.8
pip 9.0.3 from /usr/lib/python3.6/dist-packages (python 3.6)
```

## pipenvのインストール

一部の課題ではpipenvを使ってライブラリの管理を行います｡その為､pipenvをインストールします｡

```bash
pip install --user pipenv
```
(例)
```text
Collecting pipenv
  Using cached https://files.pythonhosted.org/packages/13/b4/3ffa55f77161cff9a5220f162670f7c5eb00df52e00939e203f601b0f579/pipenv-2018.11.26-py3-none-any.whl
Requirement already satisfied: virtualenv in /usr/local/lib/python3.6/site-packages (from pipenv)
Requirement already satisfied: virtualenv-clone>=0.2.5 in /usr/local/lib/python3.6/site-packages (from pipenv)
Requirement already satisfied: pip>=9.0.1 in /usr/lib/python3.6/dist-packages (from pipenv)
Requirement already satisfied: setuptools>=36.2.1 in /usr/lib/python3.6/dist-packages (from pipenv)
Requirement already satisfied: certifi in /home/ec2-user/.local/lib/python3.6/site-packages (from pipenv)
Installing collected packages: pipenv
Successfully installed pipenv-2018.11.26
You are using pip version 9.0.3, however version 19.2.3 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
```

## AWSリージョンの設定

ハンズオンではAWS CLIを使い､コマンドラインでAWSを操作します｡  
利用するAWSリージョンを指定する為に､環境変数を設定します｡  

```bash
echo 'AWS_DEFAULT_REGION="ap-northeast-1"' >> ~/.bashrc
source ~/.bashrc
```

設定を確認します｡  
```bash
echo ${AWS_DEFAULT_REGION}
aws ec2 describe-instances --query \
    'sort_by(Reservations[].Instances[].{Tags:Tags[?Key==`Name`].Value|[0],InstanceType:InstanceType,State:State.Name},&Tags)' --output table
```
(例)
```text
ap-northeast-1
-----------------------------------------------------------------------------------------
|                                   DescribeInstances                                   |
+--------------+----------+-------------------------------------------------------------+
| InstanceType |  State   |                            Tags                             |
+--------------+----------+-------------------------------------------------------------+
|  t2.micro    |  running |  aws-cloud9-sls-hands-on-[Random alphanumeric]              |
+--------------+----------+-------------------------------------------------------------+
```

## SAMアーティファクト用バケットの作成

SAMについては後ほど課題の中で説明します｡
SAMのデプロイには<a href="https://docs.aws.amazon.com/ja_jp/AmazonS3/latest/gsg/GetStartedWithS3.html" target="_blank">S3バケット :fa-external-link: </a>(AWSが提供するオブジェクトストレージ)が必要です｡  
バケット名は全世界でユニークな必要があります｡なので､今回はバケット名に末尾に乱数を追加しています｡意図して名前をつける場合は､AWSアカウントIDを末尾に付ける事も良くあります｡  

バケットの名前を生成します｡
```bash
SAM_ARTIFACTS_BUCKET="sls-hands-on-$(($RANDOM * $RANDOM))"
echo ${SAM_ARTIFACT_BUCKET}
```

(例) 
```text
sls-hands-on-841850128
```

S3バケットを作成します｡
```bash
aws s3 mb s3://${SAM_ARTIFACT_BUCKET}
```
(例)
```text
make_bucket: sls-hands-on-841850128
```

別のターミナルに切り替えても環境変数を引き継げるように永続化します｡
```bash
echo "SAM_ARTIFACT_BUCKET=${SAM_ARTIFACT_BUCKET}" >> ~/.bashrc
source ~/.bashrc
```
