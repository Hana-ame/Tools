# 远程连接与仿真运行指南

## 1. 项目概况

| 项目 | 路径 |
|------|------|
| 本地工作目录 | `/mnt/d/cent65/Proj/uvm` |
| 远程 Git 仓库 (bare) | `lzc@192.168.1.53:~/work/mac-uvm` |
| 远程工作目录 | `lzc@192.168.1.53:~/work/uvm` |

Git remote: `ssh://lzc@localhost/~/work/mac-uvm`（经本地端口转发到 192.168.1.53）

## 2. SSH 连接

### 2.1 使用封装脚本（推荐，已含自动重试）

```bash
bash ~/script/ssh/lzc.sh
```

脚本特性：
- 连接 `lzc@192.168.1.53`，启用压缩 (`-C`) 和 X11 转发 (`-Y`)
- **丢包/超时自动重试**：最多 10 次，间隔 5 秒
- 正常退出 (0) 或 Ctrl+C (130) 不重试
- 连接超时设 10 秒，心跳保活 5 秒

### 2.2 直接 SSH

```bash
ssh -CY -oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedKeyTypes=+ssh-rsa lzc@192.168.1.53
```

### 2.3 连接故障排查

```bash
# 1. 检查主机是否可达
ping -c 3 192.168.1.53

# 2. 检查端口是否开放
nc -zv 192.168.1.53 22

# 3. 如果主机在线但 SSH 不通，检查远程 sshd：
#    sudo systemctl status sshd
```

## 3. 运行 UVM 仿真

### 3.1 登录远程并进入项目

```bash
bash ~/script/ssh/lzc.sh
# 登录后：
cd ~/work/uvm
```

### 3.2 可用 Case 列表

位于 `uvm/case/` 目录：

| Case 文件 | Test Name | 说明 |
|-----------|-----------|------|
| `my_case0.sv` | my_case | case 0 |
| `my_case1.sv` | my_case | case 1 |
| `my_case2.sv` | my_case | case 2 |
| `my_case3.sv` | my_case | case 3 (常用) |
| `my_case4.sv` | my_case | case 4 |
| `my_case5.sv` | my_case | case 5 |
| `my_case6.sv` | my_case | case 6 |

### 3.3 运行 Case（完整命令）

以 **case3** 为例，**不 dump FSDB 波形**：

```bash
cd ~/work/uvm

# 准备运行目录
mkdir -p dlr_test/uvm_my_case3
cd dlr_test/uvm_my_case3
ln -sf ~/work/uvm/uvm uvm
ln -sf ~/work/uvm/src src

# 运行 VCS 仿真（注意：去掉了 +fsdb+force）
vcs -full64 -R -LDFLAGS -Wl,--no-as-needed \
  -sverilog -lca -timescale=1ns/1ps \
  -l vrun.log -licqueue +v2k +lint=none \
  +incdir+./src \
  -f uvm/filelist.f \
  uvm/top_tb.sv \
  uvm/case/my_case3.sv \
  -P $VERDI_HOME/share/PLI/VCS/LINUX64/novas.tab \
  $VERDI_HOME/share/PLI/VCS/LINUX64/pli.a \
  -debug_all -notice -ntb_opts uvm-1.2 -CFLAGS -DVCS \
  +UVM_VERBOSITY=UVM_MEDIUM \
  +UVM_TESTNAME=my_case \
  -top top_tb \
  +define+CASE_LOOP_NUMBER=10

# 查看结果
grep '\[base_test\]' vrun.log
```

### 3.4 关键参数说明

| 参数 | 作用 | 改法 |
|------|------|------|
| `+fsdb+force` | **强制 dump FSDB 波形（文件很大）** | **去掉此参数则不 dump** |
| `-debug_all` | 全调试信息 | 可改为 `-debug_typical` 加快编译 |
| `+UVM_VERBOSITY=UVM_MEDIUM` | UVM 打印级别 | 可改为 `UVM_LOW` 减少日志 |
| `+define+CASE_LOOP_NUMBER=10` | 循环次数 | 修改数字即可 |
| `+UVM_TESTNAME=my_case` | 指定 test case 名称 | 对应 case 文件中注册的 test 类名 |

### 3.5 切换 Case

只需改两处（以 case5 为例）：
```bash
# 1. case 文件路径
uvm/case/my_case5.sv

# 2. 运行目录名
mkdir -p dlr_test/uvm_my_case5 && cd dlr_test/uvm_my_case5
```

### 3.6 三种仿真模式

```bash
# 纯净环回（默认，无注错）
# MODE=clean 或 不设 MODE

# 单比特误码注入（NACK 重传测试）
# 需在 VCS 命令末尾加: +define+INJECT_BIT_ERROR

# 链路中断注入（超时重传测试）
# 需在 VCS 命令末尾加: +define+INJECT_LINK_DOWN
```

## 4. 查看结果

```bash
# 仿真结果关键字
grep -E '\[base_test\]|PASS|FAIL|ERROR|UVM_FATAL|UVM_ERROR' vrun.log

# 统计 UVM 报告
grep -c 'UVM_ERROR\|UVM_FATAL' vrun.log

# 仿真耗时
grep 'total exec time' vrun.log

# 查看完整日志
less vrun.log
```

## 5. 覆盖率合并（urg）

```bash
cd ~/work/uvm
source urg.sh
# 合并多个 case 的覆盖率数据并生成报告
```

## 6. 从本地 Push 到远程

```bash
# 本地提交后
git push origin master
# 远程 bare repo: lzc@localhost:~/work/mac-uvm
# （远程工作目录 ~/work/uvm 需要手动 pull）
```

## 7. 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| SSH 连接超时 | 远程机器未开机或 IP 变了 | 检查 ping，确认 IP 地址 |
| `licqueue` 等待 | VCS license 被占满 | 等待或 kill 无用进程 |
| FSDB 文件太大 | `+fsdb+force` 总是 dump | 去掉该参数 |
| `Host key verification failed` | known_hosts 过期 | `ssh-keygen -R 192.168.1.53` |
