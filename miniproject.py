# =============================================================
#   MINI PROJECT: HỆ THỐNG QUẢN LÝ ĐƠN HÀNG ĐẠI LÝ
#   Sinh viên: [Họ và Tên]
#   Mô tả: Chương trình quản lý đơn hàng bằng Python
# =============================================================


# -------------------------------------------------------
# HÀM 1: Hiển thị danh sách đơn hàng
# Nhận vào: danh sách đơn hàng
# Không trả về giá trị (None)
# -------------------------------------------------------
def show_orders(orders_list):
    # Kiểm tra nếu danh sách rỗng
    if len(orders_list) == 0:
        print("\n[Thông báo]: Hiện chưa có đơn hàng nào trong hệ thống.")
        return

    # In tiêu đề bảng
    print("\n" + "=" * 65)
    print(f"{'MÃ ĐƠN':<10} {'TÊN ĐẠI LÝ':<25} {'GIÁ TRỊ':>15} {'TRẠNG THÁI':<12}")
    print("=" * 65)

    # Duyệt qua từng đơn hàng và in ra
    for order in orders_list:
        print(f"{order['id']:<10} {order['agent_name']:<25} {order['total_amount']:>15,} {'  ' + order['status']:<12}")

    print("=" * 65)


# -------------------------------------------------------
# HÀM 2: Tạo mới đơn hàng
# Nhận vào: danh sách đơn hàng gốc
# Thêm đơn hàng mới trực tiếp vào danh sách
# -------------------------------------------------------
def create_order(orders_list):
    print("\n--- TẠO MỚI ĐƠN HÀNG ---")

    # Nhập mã đơn hàng, không được để trống
    while True:
        order_id = input("Nhập mã đơn hàng: ").strip()
        if order_id == "":
            print("[Lỗi]: Mã đơn hàng không được để trống. Vui lòng nhập lại!")
        else:
            break

    # Kiểm tra trùng mã (ERR-01)
    for order in orders_list:
        if order['id'] == order_id:
            print(f"[Lỗi] ERR-01: Mã đơn hàng này đã tồn tại trong hệ thống!")
            return  # Hủy thao tác, quay về menu

    # Nhập tên đại lý, không được để trống
    while True:
        agent_name = input("Nhập tên đại lý: ").strip()
        if agent_name == "":
            print("[Lỗi]: Tên đại lý không được để trống. Vui lòng nhập lại!")
        else:
            break

    # Nhập giá trị đơn hàng, phải là số và lớn hơn 0 (ERR-02)
    while True:
        try:
            total_amount = int(input("Nhập giá trị đơn hàng (VND): "))
            if total_amount <= 0:
                print("[Lỗi] ERR-02: Giá trị đơn hàng phải là số tiền lớn hơn 0!")
            else:
                break
        except ValueError:
            print("[Lỗi] ERR-02: Giá trị đơn hàng phải là số tiền lớn hơn 0!")

    # Tạo bản ghi mới với trạng thái mặc định là Unpaid
    new_order = {
        'id': order_id,
        'agent_name': agent_name,
        'total_amount': total_amount,
        'status': 'Unpaid'
    }

    # Thêm vào danh sách gốc
    orders_list.append(new_order)
    print(f"[Thành công]: Đơn hàng {order_id} đã được tạo mới thành công!")


# -------------------------------------------------------
# HÀM 3: Cập nhật trạng thái thanh toán
# Nhận vào: danh sách đơn hàng gốc
# Tìm theo mã và đổi trạng thái sang Paid
# -------------------------------------------------------
def update_payment_status(orders_list):
    print("\n--- CẬP NHẬT TRẠNG THÁI THANH TOÁN ---")

    # Nhập mã đơn hàng cần cập nhật
    order_id = input("Nhập mã đơn hàng cần cập nhật: ").strip()

    # Tìm kiếm đơn hàng trong danh sách
    found_order = None
    for order in orders_list:
        if order['id'] == order_id:
            found_order = order
            break

    # Nếu không tìm thấy (ERR-03)
    if found_order is None:
        print(f"[Lỗi] ERR-03: Không tìm thấy đơn hàng nào có mã [{order_id}]!")
        return

    # Nếu đơn hàng đã Paid rồi (ERR-04)
    if found_order['status'] == 'Paid':
        print(f"[Lỗi] ERR-04: Đơn hàng này đã được thanh toán trước đó!")
        return

    # Cập nhật trạng thái từ Unpaid -> Paid
    found_order['status'] = 'Paid'
    print(f"[Thành công]: Đơn hàng {order_id} đã được cập nhật trạng thái ĐÃ THANH TOÁN.")


# -------------------------------------------------------
# HÀM 4: Tính tổng doanh thu và chiết khấu
# Nhận vào: danh sách đơn hàng
# Trả về: Tuple (tong_doanh_thu, phan_tram_chiet_khau, tien_chiet_khau)
# -------------------------------------------------------
def calculate_financials(orders_list):
    # Tính tổng doanh thu từ các đơn hàng có trạng thái Paid
    tong_doanh_thu = 0
    for order in orders_list:
        if order['status'] == 'Paid':
            tong_doanh_thu += order['total_amount']

    # Áp dụng quy tắc chiết khấu
    if tong_doanh_thu >= 100000000:
        phan_tram_chiet_khau = 5
    else:
        phan_tram_chiet_khau = 0

    # Tính tiền chiết khấu
    tien_chiet_khau = tong_doanh_thu * phan_tram_chiet_khau / 100

    # Trả về tuple 3 giá trị (KHÔNG in trong hàm này)
    return (tong_doanh_thu, phan_tram_chiet_khau, tien_chiet_khau)


# -------------------------------------------------------
# HÀM MAIN: Điều phối chính - chứa vòng lặp menu
# -------------------------------------------------------
def main():
    # Dữ liệu mẫu ban đầu để chạy demo
    orders = [
        {'id': 'HD01', 'agent_name': 'Dai ly Hoang Long', 'total_amount': 45000000, 'status': 'Paid'},
        {'id': 'HD02', 'agent_name': 'Tap hoa Minh Thu',  'total_amount': 15000000, 'status': 'Unpaid'},
        {'id': 'HD03', 'agent_name': 'Cua hang Bao Chau', 'total_amount': 72000000, 'status': 'Paid'},
    ]

    # Vòng lặp menu vô hạn
    while True:
        # Hiển thị menu
        print("\n" + "=" * 40)
        print("   HỆ THỐNG QUẢN LÝ ĐƠN HÀNG ĐẠI LÝ")
        print("=" * 40)
        print("  1. Xem danh sách đơn hàng")
        print("  2. Tạo mới đơn hàng")
        print("  3. Cập nhật trạng thái thanh toán")
        print("  4. Tính tổng doanh thu & Chiết khấu")
        print("  5. Thoát chương trình")
        print("=" * 40)

        # Bắt lỗi khi người dùng nhập sai kiểu (chữ thay vì số)
        try:
            choice = int(input("Nhập lựa chọn của bạn: "))
        except ValueError:
            print("[Lỗi] ERR-05: Lựa chọn không hợp lệ. Vui lòng nhập số từ 1 đến 5!")
            continue

        # Điều hướng theo lựa chọn
        if choice == 1:
            show_orders(orders)

        elif choice == 2:
            create_order(orders)

        elif choice == 3:
            update_payment_status(orders)

        elif choice == 4:
            # Gọi hàm tính toán và nhận kết quả trả về (Tuple)
            ket_qua = calculate_financials(orders)
            tong_doanh_thu = ket_qua[0]
            phan_tram_chiet_khau = ket_qua[1]
            tien_chiet_khau = ket_qua[2]

            # Nơi gọi hàm thực hiện việc in kết quả ra màn hình
            print("\n--- THỐNG KÊ DOANH THU ---")
            print(f"  Tổng doanh thu thực tế : {tong_doanh_thu:>20,} VND")
            print(f"  Phần trăm chiết khấu   : {phan_tram_chiet_khau:>19}%")
            print(f"  Tiền chiết khấu        : {tien_chiet_khau:>20,.0f} VND")
            print("-" * 40)

        elif choice == 5:
            # Thoát chương trình
            print("\nCảm ơn bạn đã sử dụng hệ thống. Tạm biệt!")
            break

        else:
            # Số ngoài dải 1-5
            print("[Lỗi] ERR-05: Lựa chọn không hợp lệ. Vui lòng nhập số từ 1 đến 5!")


# Điểm khởi chạy chương trình
if __name__ == "__main__":
    main()