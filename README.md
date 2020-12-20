# DOANTN
Link database: https://drive.google.com/drive/folders/1SYV7wxFMUD2o12T_CbQfEJVMumOTr0oc?usp=sharing

Hướng dẫn cài đặt và sử dụng hệ thống

1.	Hướng dẫn cài đặt chương trình

1.1.	Bật server
-	Mở thư mục …\DOANTN\API\
-	Tất cả thư viện đã được lưu trong file requirements.txt, vì thế ta tiến hành cài thư viện như sau:
   Mở terminal và gõ lệnh: pip install -r requirements.txt
-	Tạo cơ sở dữ liệu với tên là rsblog, tiến hành import 1 collection viblo_posts từ file csv viblo_posts.csv. Sử dụng hệ quản trị cơ sở dữ liệu MongoDb.

1.2.	Bật terminal để start server bằng cách gõ lần lượt 2 câu lệnh sau:
•	set FLASK_APP=app.py

•	flask run

1.3.	Cài đặt Chrome Extension
-	Mở trang Extensions trong Google Chrome bằng cách truy cập thanh điều hướng với địa chỉ chrome://extensions/.
-	Bật chế độ Developer Mode và lựa chọn Load unpacked sau đó chọn đường dẫn là …\DOANTN\Extensions\ để tải ứng dụng lên cửa hàng extensions của chrome. Ta sẽ thấy biểu tượng tiện ích mở rộng được bật bên cạnh thanh địa chỉ. Vậy Extension đã được cài đặt thành công.

2.	Hướng dẫn sử dụng chương trình
-	Truy cập website viblo nơi chia sẻ các kiến thức hay về IT:   https://viblo.asia/
-	Click vào những bài posts và đọc.
-	Click vào biểu tượng extension và quan sát các bài posts được gợi ý.

