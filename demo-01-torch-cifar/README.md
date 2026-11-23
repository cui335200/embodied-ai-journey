# Demo 01: CIFAR-10 从零训练

手写 PyTorch 训练循环，不用 Trainer / Lightning。

## 环境
- Ubuntu 22.04 (WSL2)
- Python 3.10, PyTorch 2.5.1 + CUDA 12.1
- RTX 3070 8GB

## 运行
python demo-01-torch-cifar/train.py

## 结构
- 3 层卷积 + 3 次池化 + 2 层全连接
- CrossEntropyLoss + Adam (lr=1e-3)
- 20 epoch, batch size 128

## 结果
- 训练约 4 分钟
- test acc = 0.75（换成你的实际数字）

## 踩坑
- `DataLoader` 大小写：写成 `Dataloader` 会 ImportError
- 训练循环里 `zero_grad()` 不能漏，否则梯度累加