# MCP Archiva Library --- Test Scenario Prompt

## 1. ตรวจสอบ Method ของระบบ

- บอกว่ามีทั้งหมดกี่ method ใน class Library\
- บอกว่ามีกี่ method ที่โหลดเสร็จแล้ว\
- จากนั้นโหลด method ที่เหลือทั้งหมด

---

## 2. สมัครสมาชิก (Register)

- Register name = Alice username = alice password = 1234\
- Register name = Bob username = bob password = 1234\
- Register name = Lenny username = lenny password = 1234\
- Register name = Ton username = ton password = 1234

---

## 3. ทดสอบ Login

- Login username = alice password = 1233 _(ควร error เพราะ password ผิด)_\
- Login username = alice password = 1234

---

## 4. ทดสอบการค้นหาหนังสือและการยืม

- ขอดูหนังสือที่ว่างทั้งหมด\
- ค้นหาหนังสือที่มีคำว่า AI\
- ยืม isbn = 103 payment = cash

---

## 5. อัปเกรดเป็น Member

- อัปเกรด user ปัจจุบันให้เป็น Member\
- ยืม isbn = 103 payment = qr\
- Logout

---

## 6. ทดสอบการยืม + การจอง (Bob)

- Login bob 1234\
- Upgrade member\
- ยืม 103 cash\
- จอง 103 cash\
- Logout

---

## 7. ทดสอบว่าหนังสือที่ถูกจองจะยืมไม่ได้

- Login Alice 1234\
- ขอดู lending ของตัวเอง\
- คืน lending 103\
- ยืม 103 qr _(ควรยืมไม่ได้ เพราะ bob จองอยู่)_\
- Logout

---

## 8. ทดสอบว่าคนที่จองสามารถยืมได้

- Login bob 1234\
- ยืม 103 cash _(ควรยืมได้)_

---

## 9. ทดสอบระบบจองห้อง

- จองห้อง R001 พรุ่งนี้ 14.00 4 qr\
- จองห้อง R001 พรุ่งนี้ 14.00 4 qr _(ควร error เพราะจองซ้ำ)_\
- จองห้อง R005 พรุ่งนี้ 14.00 4 qr _(ควร error เพราะไม่มีห้อง)_\
- จองห้อง R001 พรุ่งนี้ 18.00 4 qr _(ควร error เพราะไม่มี slot)_\
- จองห้อง R001 2027-03-12 5 12.00 qr _(ควร error เพราะเกิน 7 วัน)_\
- จองห้อง R001 2026-03-10 6 12.00 qr _(ควร error เพราะวันที่ผ่านไปแล้ว)_

### Cancel ห้อง

- Cancel R001\
- จองห้อง R001 พรุ่งนี้ 14.00 4 qr\
- Logout

---

## 10. ทดสอบคิวการจองหนังสือ

ตอนนี้ bob ยืมหนังสือ 103

- Login alice 1234\
- จอง 103 qr\
- Logout
- Login lenny 1234\
- จอง 103 qr\
- Logout
- Login ton 1234\
- จอง 103 qr
- ดูคิวทั้งหมดของหนังสือ 103 _(ควรได้ Alice, Lenny, Ton)_

---

## 11. ทดสอบยกเลิกการจอง

- Login Alice 1234\
- ยกเลิกการจอง 103\
- Logout

---

## 12. ทดสอบคืนหนังสือ + ค่าปรับ

- Login bob 1234\
- ดู lending ของตัวเองทั้งหมด\
- คืน 103\
- จ่าย fine cash\
- Logout

---

## 13. ทดสอบลำดับคิวการยืม

- Login ton 1234\
- ยืม 103 cash _(ควรยืมไม่ได้ เพราะยังไม่ถึงคิว)_\
- Logout
- Login lenny 1234\
- ยืม 103 cash _(ควรยืมได้)_\
- Logout

---

## 14. Admin Feature

- Login admin admin123

### เพิ่มหนังสือ

- เพิ่มหนังสือ 101 hahaha lol 500 general _(isbn ซ้ำ)_\
- เพิ่มหนังสือ 105 hahaha lol 500 general

### เพิ่ม BookItem

- เพิ่ม bookitem 105 BC001 _(barcode ซ้ำ)_\
- เพิ่ม bookitem 105 BC009

### Rack

- เพิ่ม rack 1 A _(ซ้ำ)_\
- เพิ่ม rack 2 B

### วางหนังสือใน rack

- เอา bookitem BC009 เข้า rack 2 B

### ดูหนังสือ

- ขอดูหนังสือทั้งหมด

### ลบหนังสือ

- ลบหนังสือ 105\
- ขอดูหนังสือทั้งหมด\
- ลบหนังสือ 103 _(ควรลบไม่ได้เพราะมีคนยืม)_

### ลบ BookItem

- ลบ BookItem B001

### ห้อง

- ลบห้อง R003\
- ขอดูห้องว่างทั้งหมด

### User

- ลบ member 68010004

### สร้างพนักงาน

- สร้างพนักงาน Zoro zoro 1234 worker

---

## 15. Credit Card Format

(เผื่ออาจารย์อยากลองใช้ credit card นะครับ)

    card_number = 4111111111111111
    holder = John Smith
    expiry = 12/28
    cvv = 123
