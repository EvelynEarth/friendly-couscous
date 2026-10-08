# 06 计算机视觉：分类 / 检测 / 分割

> 适用：图像任务（2023 坑洼道路、2025 集装箱）。MathorCup 视觉题常按“**分类 → 检测 → 分割**」递进。

## 1. 三级任务与指标

| 任务 | 输出 | 指标 |
|---|---|---|
| 分类 | 有无残损/类别 | Accuracy、Precision、Recall、F1、混淆矩阵、ROC-AUC |
| 检测 | 目标框 + 类别 | mAP@.5、mAP@.5:.95、Precision/Recall（IoU 匹配） |
| 分割 | 像素掩膜/边缘 | mIoU、Dice、像素 Accuracy、IoU；面积占比 |

类别/正负不平衡时重 macro-F1、mAP 与少数类召回（见 `04-imbalanced-data.md`）。

## 2. 数据准备

```python
# 统一尺寸 / 归一化；训练集与标签目录结构（如 JPEGImages + labels）
# 划分训练/验证（分层），报告类别分布与样本数
```
- 背景复杂、光照/反光/阴影/污渍：做光照校正（HE/CLAHE/Gamma）、背景净化（先用轻量检测裁出目标区域）。
- **数据增强**：翻转、旋转、裁剪、亮度/对比度、色彩抖动、加噪；少样本类过采样、多样本类欠采样。

```python
# 例：torchvision / albumentations
import albumentations as A
aug = A.Compose([A.HorizontalFlip(), A.RandomBrightnessContrast(),
                 A.Rotate(limit=15), A.Normalize()])
```

## 3. 分类：预训练骨干 + 轻量头

```python
# 常用预训练骨干（ImageNet 权重 + 迁移学习）：
# ResNet、MobileNet（轻量化）、DenseNet、VGG、EfficientNet、ViT
# 40 篇中 ResNet 86、DenseNet 65、ViT 48、VGG 36、MobileNet 37 次出现
import timm, torch
m = timm.create_model("resnet50", pretrained=True, num_classes=n_class)
# 小数据：冻结骨干只训头，再浅层微调；防过拟合 + 早停
```
可加**注意力块（CBAM/SE/自注意力）**、多尺度特征融合；2025 轻量化方案为 MobileNet + YOLO 协同。

## 4. 检测：YOLO 为主线

```python
# YOLOv8 / v11（n/s/m 按算力选）；备选 Faster R-CNN、SSD、RetinaNet
# 40 篇中 YOLO 出现 355 次，是检测绝对主力
# 标注为 YOLO/COCO 格式；训练后输出框 + 类别 + 置信度
```
小目标/多尺度缺陷：多尺度训练、特征金字塔、注意力；难区分相似类（深凹痕 vs 破损）用难例挖掘。

## 5. 分割与面积估计

```python
# 语义/实例分割：U-Net、Mask R-CNN；边缘提取后估计面积
# 指标 mIoU / Dice；面积占比 = 缺陷像素/总像素（复赛常要求整数百分比）
```

## 6. 进阶手段（作为创新点，需验证）

- **GAN/超分辨率**：样本少或图像模糊时，用超分 GAN 增强/生成少数类特征（2023 有用 GAN 43 次、超分 27 次）。
- “分类-检测-分割”一体化/级联：轻量化预筛 + 高精度定位分割，协同提速提精度。

## 7. 验证要点

- 分层划分，验证集类别分布与训练一致；报告混淆矩阵与逐类指标。
- 检测报告 mAP 与 IoU 阈值口径；分割报告 mIoU/Dice 与可视化结果。
- 多随机种子/折，报告均值±波动；可视化典型成功与失败案例。
- 预训练/外部数据要说明来源与可得性，不引入违规数据。

## 8. 标注语义门：检测框不能当分割 mask

训练前先盘点图像、标签配对与类别 ID，并区分：

- `class cx cy width height`（5 列）：YOLO 检测**边界框**；可训练检测模型，但不等于真实像素分割标注。
- `class x1 y1 x2 y2 x3 y3 ...`（至少三个顶点）：YOLO polygon 分割；仍应核对闭合与几何合法性。
- 如果题目要求分割而只有 bbox：需取得真实 mask、明确弱监督/伪掩膜方案或承认无 ground-truth 分割评价；禁止报告未实际计算的真实 mIoU/Dice。
- 所有 split 考虑近重复图像、同一拍摄场景与同一集装箱实体的跨集泄漏；无明确实体信息则如实记录约束。

标注预检命令：`python skills/big-data-competition-skill/tools/bigdata_preflight.py yolo --root DATASET --split train --task detect --classes 3`。
