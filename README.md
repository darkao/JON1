# JON1 Secure File Encryptor

Advanced and secure file encryption CLI tool based on **ChaCha20-Poly1305**.
()

---

## 🇬🇧 English

### 📌 Overview

**JON1** is a secure, streaming file encryption utility designed to safely encrypt and decrypt files or entire directories using modern authenticated encryption.

## ⚠️ Disclaimer / Sorumluluk Reddi

### 🇬🇧 English
This software is provided **"as is"**, without warranty of any kind, express or implied. The author shall not be held liable for any damages, data loss, misuse, or legal consequences arising from the use of this software.

This tool is intended **for educational, personal backup, and legitimate security purposes only**. You are solely responsible for ensuring that your use of this software complies with all applicable local, national, and international laws.

By using this software, you acknowledge that **cryptographic software can permanently destroy data if misused**, including but not limited to:
- Forgetting or losing the password
- Interrupting the encryption/decryption process
- Modifying encrypted files

Use at your own risk.

---

### 🇹🇷 Türkçe
Bu yazılım **"olduğu gibi"** sunulmaktadır; açık veya zımni hiçbir garanti verilmez. Yazılımın kullanımından doğabilecek veri kaybı, yanlış kullanım, hukuki sonuçlar veya diğer zararlardan geliştirici sorumlu tutulamaz.

Bu araç **yalnızca eğitim, kişisel yedekleme ve meşru güvenlik amaçları** için tasarlanmıştır. Yazılımın kullanımının yürürlükteki yerel, ulusal ve uluslararası yasalara uygunluğundan tamamen kullanıcı sorumludur.

Bu yazılımı kullanarak, **kriptografik araçların hatalı kullanım durumunda verileri kalıcı olarak erişilemez hale getirebileceğini** kabul etmiş olursunuz. Buna aşağıdakiler dahildir ancak bunlarla sınırlı değildir:
- Şifrenin unutulması veya kaybedilmesi
- Şifreleme/çözme işleminin yarıda kesilmesi
- Şifreli dosyaların değiştirilmesi

Tüm risk kullanıcıya aittir.

Key goals:

* Strong cryptography
* Zero silent corruption
* Crash-safe file handling
* Large-file support
* Simple and safe CLI usage

---

### 🔐 Cryptography Design

**Encryption Algorithm**

* ChaCha20-Poly1305 (AEAD)

**Key Derivation**

* PBKDF2-HMAC-SHA256
* 480,000 iterations
* 16-byte random salt per file
* 32-byte derived key

**Nonce Strategy**

* 12-byte cryptographically secure random nonce
* Unique per encrypted block

**File Format**

```
[4 bytes ] Magic Header: JON1
[16 bytes] Salt
REPEATED:
  [4 bytes ] Ciphertext Length (big-endian)
  [12 bytes] Nonce
  [N bytes ] Ciphertext + Poly1305 Tag
```

---

### 🧱 Engineering Features

* Streaming I/O (64 KB blocks)
* Atomic file replacement
* Crash-safe temporary files
* Recursive directory support
* Hidden password input (`getpass`)

---

### 🖥️ Usage

```bash
python jon1.py -m enc -p myfile.txt
python jon1.py -m dec -p myfile.txt.enc
```

---

## 🇹🇷 Türkçe

### 📌 Genel Bakış

**JON1**, modern doğrulanmış şifreleme kullanarak dosya ve klasörleri güvenli şekilde şifrelemek ve çözmek için tasarlanmış, akış (streaming) destekli bir CLI aracıdır.

Temel hedefler:

* Güçlü kriptografi
* Sessiz veri bozulması yok
* Çökme durumunda veri güvenliği
* Büyük dosya desteği
* Basit ve güvenli kullanım

---

### 🔐 Kriptografik Tasarım

**Şifreleme Algoritması**

* ChaCha20-Poly1305 (AEAD)

**Anahtar Türetme**

* PBKDF2-HMAC-SHA256
* 480.000 iterasyon
* Dosya başına 16 byte rastgele salt
* 32 byte anahtar

**Nonce Stratejisi**

* 12 byte kriptografik olarak güvenli nonce
* Her blok için benzersiz

**Dosya Formatı**

```
[4 byte ] Magic Header: JON1
[16 byte] Salt
TEKRARLANIR:
  [4 byte ] Şifreli Veri Uzunluğu
  [12 byte] Nonce
  [N byte ] Şifreli Veri + Poly1305 Etiketi
```

---

### 🧱 Mühendislik Özellikleri

* 64 KB bloklarla streaming okuma/yazma
* Atomik dosya değiştirme
* Hata durumunda güvenli temizleme
* Klasörleri recursive işleme
* Şifreyi gizli alma (`getpass`)

---

### 🖥️ Kullanım

```bash
python jon1.py -m enc -p dosya.txt
python jon1.py -m dec -p dosya.txt.enc
```

---

## 📄 License / Lisans

MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.


> Simple. Secure. Predictable.
>
> Basit. Güvenli. Öngörülebilir.
