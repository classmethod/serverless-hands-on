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
```
Python 3.6.8
pip 9.0.3 from /usr/lib/python3.6/dist-packages (python 3.6)
```