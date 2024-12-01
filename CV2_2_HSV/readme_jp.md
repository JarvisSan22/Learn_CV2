# 【CV2】: HSV vs RGB: イメージ処理におけるHSVの理解と活用

前回の記事では、OpenCVでのRGB画像の基本操作（プロットや明るさ・コントラストの調整など）について紹介しました [「【CV2】： 画像とは何か、画像の明るさとコントラストを調整しよう」](https://qiita.com/JarvisSan22/items/c86b28071dbc0343287a)。RGBはコンピュータ画面に適した色空間ですが、人間が自然界で色を認識する方法とは少し異なります。そこで登場するのがHSV（色相、彩度、明度）です。HSVは、人間の色の感じ方により近い形で色を表現するための色空間です。

今回は、HSVの基本、用途、そして画像を改善する面白いテクニックについて解説します。

## HSVとは？
HSVは以下の3つの要素で構成されています：

- Hue（色相）
色の種類（赤、緑、青など）を表します。通常は角度（0°～360°）で測られますが、OpenCVでは0～179に変換されます（8ビット整数に収めるため）。
例えば：

  - 0付近：赤
  - 60～89：緑
  - 120～149：青
  - 140～179：赤に戻り、円環状に循環します。
- Saturation（彩度）
色の鮮やかさや純度を表します。彩度が高いほど鮮やかで、低いと灰色が混じりくすんで見えます。

- Value（明度）
明るさや暗さを表します。これを分けることで、色検出や画像の改善が簡単になります。
以下の画像はHSVの色空間の分布を示したものです：

![Image HSV color space view ](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/vup6xvdsqn5pn8arhfwu.jpg)

# OpenCVで画像をHSVに変換する
OpenCVでは、cv2.cvtColor() 関数を使って画像をHSVに簡単に変換できます。コード例を見てみましょう：
```python
import cv2
import matplotlib.pyplot as plt

image = cv2.imread('./test.png')
plt.figure(figsize=(10,10))
plt.subplot(1,2,1)
plt.imshow(image[:,:,::-1]) # RGB表示
plt.title("RGB表示")
hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
plt.subplot(1,2,2)
plt.imshow(hsv)
plt.title("HSV表示")
plt.tight_layout()
plt.show()

```

![Image Profile hsv test ](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/9bri9v3lzf7addgfuj98.png)

一見すると、HSVプロットは奇妙で、まるで異世界のように見えるかもしれません。これは、コンピュータがHSVをRGB画像として表示しようとしているためです。HSVの要素（特にHue）は、RGB値に直接対応していないからです。たとえば：

Hue（色相・H）：角度として表され、OpenCVでは0から179までの範囲で扱われます（RGBチャンネルのように0から255ではありません）。そのため、HueチャンネルはRGBベースのプロットでは主に青っぽく見えることがあります。
次の例では、プロフィール画像ではなく、Flux AIの画像生成モデルで作られた暗めの画像を使います。この画像の方がHSVの効果がわかりやすく、より良い実例を提供できるからです。

![Image 1](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/4nwvylky255ts8140xan.png)

# HSVを使ったヒストグラムの比較

RGBとHSVの違いを理解するため、各チャンネルのヒストグラムをプロットしてみましょう：
```python
# ヒストグラムをプロット
plt.figure(figsize=(10, 6))

# RGBヒストグラム
plt.subplot(1, 2, 1)
for i, color in enumerate(['r', 'g', 'b']):
    plt.hist(image[:, :, i].ravel(), 256, [0, 256], color=color, histtype='step')
    plt.xlim([0, 256])
plt.title("RGBヒストグラム")

# HSVヒストグラム
plt.subplot(1, 2, 2)
for i, color in enumerate(['r', 'g', 'b']):
    plt.hist(hsv[:, :, i].ravel(), 256, [0, 256], color=color, histtype='step')
    plt.xlim([0, 256])
plt.title("HSVヒストグラム")
plt.show()
```

![Image historgram](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/tlkv5fzj5vf4j6a1mdc8.png)

このヒストグラムを見ると、Hue（色相）チャンネルが0～179の範囲に分布していることがわかります。Saturation（彩度）は色の強さ、Value（明度）は明るさを表します。

# HSVの視覚化
ここでは、HSV画像をそれぞれのチャンネルに分解して、それぞれが何を表しているのかを理解してみましょう。
```python
# HSVの個別チャンネルをプロット
plt.figure(figsize=(10, 6))
plt.subplot(1, 3, 1)
plt.imshow(hsv[:, :, 0], cmap='hsv')  # Hue
plt.title("Hue")
plt.subplot(1, 3, 2)
plt.imshow(hsv[:, :, 1], cmap='gray')  # Saturation
plt.title("Saturation")
plt.subplot(1, 3, 3)
plt.imshow(hsv[:, :, 2], cmap='gray')  # Value
plt.title("Value")
plt.tight_layout()
plt.show()
```
![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/999291/134fce06-940e-ce61-5555-64ae916822c1.png)
- Hue（色相）: 色の違いがはっきりと表示され、画像の主な色を確認できます。
- Saturation（彩度）: 明るい部分は鮮やかな色を示し、暗い部分は灰色っぽい落ち着いた色を表します。
- Value（明度）: 明るさの分布を示し、明るく照らされた部分がより明るく見えます。

これを通して、HSV各チャンネルが画像内でどのように情報を表現しているかを視覚的に理解できます。


# HSVのトリック

## 1. 明るさの改善
画像の明るさを均一化することで、暗い部分を見やすくできます：
```python
equ = cv2.equalizeHist(hsv[:, :, 2])  # 明度を均一化
new_hsv = cv2.merge((hsv[:, :, 0], hsv[:, :, 1], equ))
new_image = cv2.cvtColor(new_hsv, cv2.COLOR_HSV2BGR)

# 結果を表示
plt.figure(figsize=(10, 6))
plt.subplot(1, 2, 1)
plt.imshow(image)
plt.title("元画像")
plt.subplot(1, 2, 2)
plt.imshow(new_image)
plt.title("明るさ改善")
plt.tight_layout()
plt.show()

```

![Image ValEnhnaced](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/r6mikvo1b6gwcpmnj4jr.png)


## 2. 色彩の強調
彩度を強調することで、画像の色をより鮮やかにできます：
```python
equ = cv2.equalizeHist(hsv[:, :, 1])  # 彩度を均一化
new_hsv = cv2.merge((hsv[:, :, 0], equ, hsv[:, :, 2]))
new_image = cv2.cvtColor(new_hsv, cv2.COLOR_HSV2BGR)

# 結果を表示
plt.figure(figsize=(10, 6))
plt.subplot(1, 2, 1)
plt.imshow(image)
plt.title("元画像")
plt.subplot(1, 2, 2)
plt.imshow(new_image)
plt.title("色彩強調")
plt.tight_layout()
plt.show()


```
![Image SatEhnahced](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/o3867nu4tyy84h230n0a.png)



## 3. 特定の色の抽出
例えば、赤色を抽出する場合：
```python
lower_red = np.array([140, 0, 0])
upper_red = np.array([180, 255, 255])

mask = cv2.inRange(hsv, lower_red, upper_red)
filtered_image = cv2.bitwise_and(image, image, mask=mask)

# 結果を表示
plt.figure(figsize=(10, 6))
plt.subplot(1, 2, 1)
plt.imshow(image)
plt.title("元画像")
plt.subplot(1, 2, 2)
plt.imshow(filtered_image)
plt.title("赤色抽出")
plt.tight_layout()
plt.show()

```
![Image ColorSeg](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/xgzuyqcfqmbcj16na8gl.png)



# まとめ
HSVは、色（Hue）、強度（Saturation）、明るさ（Value）を分けて扱えるため、色検出や画像の調整に非常に便利です。RGBとは異なり、人間の色の見方に近い形で画像を処理できるので、分析やクリエイティブな編集に役立ちます。

あなたのお気に入りのHSVトリックは何ですか？ぜひ共有してください！

