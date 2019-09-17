
# 并行化随机指令测试

## 运行方法
```
python run.sh worker数量
```
如
```
python run.sh 2
```
表示启动2个worker来并行测试.

worker之间会进行独立的测试, 通过python脚本不断重复地调用
```
make gen  # 生成新的随机指令汇编代码
make run  # 用生成的测试来运行测试对象, 目前支持NEMU和NOOP
```

脚本不提供正确的运行结果, 因此假设`make run`会同时启动differential testing.
若differential testing发现错误, `make run`需返回非0值, 让python脚本得知测试出错.

若某个worker测试出错. 该worker将保存导致运行错误的汇编代码和运行日志到相应工作目录, 然后退出.
进入相应的工作目录, 其中部分文件如下:
```
log.txt - 出错前总共通过的测试数量
run.log  - 出错时`make run`的运行日志
test.S - 导致出错的汇编代码
test.txt - 反汇编结果
```
可以在工作目录中直接运行`make run`来重现错误.

## 结束运行

```
make killall
```
注意这个命令会结束所有名字带有`python`, `java`和`qemu`的进程.

## 统计工具

统计通过测试的数量和指令数目:
```
make stat
```

观测cpu主频:
```
make cpu
```
