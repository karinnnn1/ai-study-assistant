# AI Study Assistant

PDF教材を使った学習を支援するStreamlitアプリです。

PDFのアップロード、テキスト抽出、簡易要約、学習履歴の記録などの機能を実装しています。

## Overview

AI Study Assistantは、PDF教材から学習に必要な情報を取り出し、効率的な復習を支援することを目的としたWebアプリケーションです。

現在は無料で動作する抽出型要約を使用しています。

## Features

- PDFファイルのアップロード
- PDFのファイル名とサイズの表示
- PDFページ数の取得
- PDFテキストの抽出
- 無料の簡易要約
- 学習内容の記録
- サイドバーによる機能切り替え

## Current Status

| Feature | Status |
| --- | --- |
| 学習記録 | Completed |
| PDFアップロード | Completed |
| PDFテキスト抽出 | Completed |
| 簡易要約 | Completed |
| Quiz | Planned |
| Flashcards | Planned |
| データベース保存 | Planned |
| AI API連携 | Planned |

## Tech Stack

- Python
- Streamlit
- pypdf
- Git
- GitHub

## Project Structure

```text
ai-study-assistant/
├── src/
│   ├── __init__.py
│   ├── pdf_utils.py
│   ├── summarizer.py
│   └── ui.py
├── app.py
├── requirements.txt
├── README.md
└── .gitignore