# Mac環境

- [ ] Intel系 Mac
- [x] Arm系 Mac

# 前提とする環境

- Homebrew
- Python3.10（pyenvでインストールされたもの）

# インストール方法

本リポジトリを以下のようにクローンします。

```
git clone --recursive https://github.com/toppers/hakoniwa-pybullet-simasset-plugin.git
```

クローンが終わったら、以下のようにディレクトリ移動します。

```
cd hakoniwa-pybullet-simasset-plugin/
```

そして、必要な箱庭モジュール類をインストールします。

arm系の場合：

```
bash native/template/runtime/ai/mac/install.bash arm
```

intel系の場合：

```
bash native/template/runtime/ai/mac/install.bash intel
```

途中、パスワードが聞かれますので、入力してください。


# シミュレーション実行方法

以下のコマンドで箱庭を起動します。

```
bash runtime/run.bash
```

起動成功すると、以下のログが出力されます。

```
INFO: PYTHON MODE
INFO: ACTIVATING HAKONIWA-CONDUCTOR
delta_msec = 20
max_delay_msec = 100
INFO: shmget() key=255 size=80768 
Server Start: 127.0.0.1:50051
INFO: ACTIVATING :src/hako_runner.py ./data/config.json
pybullet build time: Aug  8 2023 05:29:50
filepath= ./data/config.json
Version = 4.1 Metal - 83.1
Vendor = Apple
Renderer = Apple M2 Pro
b3Printf: Selected demo: Physics Server
startThreads creating 1 threads.
starting thread 0
started thread 0 
MotionThreadFunc thread started
START
robo: SampleRobo
create:channel_id=1
create:typename=String
create:pdu_size=256
INFO: SampleRobo create_lchannel: logical_id=1 real_id=0 size=256
subscribe:channel_id=0
subscribe:typename=Twist
subscribe:pdu_size=48
apl: SampleRobo
create:channel_id=0
create:typename=Twist
create:pdu_size=48
INFO: SampleRobo create_lchannel: logical_id=0 real_id=1 size=48
subscribe:channel_id=1
subscribe:typename=String
subscribe:pdu_size=256
WAIT START:
```

また、下図のように、pybullet の GUI 画面が出力されます。

<img width="1024" alt="スクリーンショット 2023-08-11 15 53 03" src="https://github.com/toppers/hakoniwa-pybullet-simasset-plugin/assets/164193/504211d6-1731-4fba-81b5-7a4d850a9cd0">


この状態でシミュレーションを実行させるには、別端末上で、以下のコマンドを実行します。

## シミュレーション開始する

```
hako-cmd start
```

## シミュレーション停止する

```
hako-cmd stop
```

## シミュレーション・リセットする

```
hako-cmd reset
```
