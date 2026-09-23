"""登录用例：数据驱动，覆盖正常/锁定/坏凭证/边界。"""
import pytest

from pages import LoginPage
from tests.conftest import read_csv

USERS = read_csv("users.csv")


@pytest.mark.parametrize("row", USERS, ids=lambda r: f"{r['username'] or 'EMPTY'}->{r['expected']}")
def test_login_cases(sb, row):
    page = LoginPage(sb)
    page.open().login(row["username"], row["password"])

    expected = row["expected"]
    timeout = int(row["timeout"] or 10)

    if expected == "ok":
        assert page.is_on_inventory(), "正常用户应进入商品列表页"
    elif expected == "ok_extended":
        assert sb.wait_for_element_present("div.inventory_list", timeout=timeout), "慢速用户应在放宽超时内进入列表页"
    elif expected == "locked":
        assert page.has_error(), "锁定账号应出现错误提示"
        assert "locked out" in page.get_error_text().lower(), "错误文案应指向账户被锁定"
    elif expected in ("bad_credentials", "missing_username", "missing_password"):
        assert page.has_error(), "非法输入应出现错误提示"
    else:
        pytest.fail(f"未处理的状态: {expected}")