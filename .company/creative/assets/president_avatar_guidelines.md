# 社長アバター生成ガイドライン (President Avatar Guidelines)

## 🎯 目的
このドキュメントは、School-AI-Companyの社長（ユーザー）のアイデンティティを一貫して保ちつつ、用途に応じて多様なテイストのアバターを自律的に生成するための「マスター記述」と「プロンプト集」です。

---

## 🧔🏽 マスター個人記述 (Base Identity)
すべての生成プロンプトの核となる記述です。

```text
A friendly young East Asian man in his 20s. He has natural, short black hair. His face is round with smooth, healthy skin. He has soft dark brown eyes with a gentle expression. His eyebrows are relatively thick and natural. His overall appearance is friendly, warm, and approachable.
Background is strictly pure white, plain, and empty with no distracting elements. Any specific items requested should be the only elements besides the character.
```

---

## 🎨 テイスト別プロンプト集

### 1. プロフェッショナル (Professional Portrait)
*   **用途**: プレゼン資料、プロフィール、公式文書
*   **プロンプト**:
    > [Master Identity], a high-quality professional portrait photograph. He is wearing a dark navy suit, a white dress shirt, and a blue patterned tie. Standing with a slight, confident smile and hands clasped. Pure white studio background, clean even lighting. Masterpiece, 4k, professional finish.

### 2. カジュアル・モダン (Flat Illustration)
*   **用途**: スライド、Webサイト、ブログ
*   **プロンプト**:
    > [Master Identity], a modern vector illustration, flat design style. He is wearing a casual dark t-shirt with a subtle tech logo. One hand is pointing to a digital screen. The background is strictly pure white and transparent-style with no background graphics. Masterpiece, clean lines.

### 3. 親しみやすいSNS (Anime Style)
*   **用途**: SNSアイコン、チャットボット、Slack/Discord
*   **プロンプト**:
    > [Master Identity], a high-quality anime-style character design icon. He is wearing a black cap and a grey mesh hoodie. Winking with a warm grin. Pure white solid background, suitable for transparent cutout. Sharp lines, vibrant colors, masterpiece, 4k.

### 4. フューチャリスティック (3D Render)
*   **用途**: メタバース、バーチャルイベント、先進的な演出
*   **プロンプト**:
    > [Master Identity], a 3D rendered character avatar, like from a Pixar movie. Wearing a light beige collared knit shirt. Holding a camera, with glasses on. Simple empty studio background, pure white. Masterpiece, high resolution, 3D rendering, detailed.

---

## 🛠️ 生成時の注意点 (Negative Prompts)
生成時には以下の要素を排除するように設定してください。
```text
(negative prompt), cartoon, illustration, painting, deformed, mutated, disfigured, bad anatomy, bad hands, extra fingers, missing fingers, extra limbs, missing limbs, fused fingers, tilted head, bad lighting, low resolution, blurred, text, watermark.
```

---
최종 갱신: 2026-03-31
ステータス: Active
