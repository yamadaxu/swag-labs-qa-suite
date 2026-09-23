"""缺陷复现用例归档。

QA 工作流：写正向用例 -> 在特定账号下复现缺陷 -> 归档到 bug_report.md
-> 用 xfail 挂起防止 CI 长期红灯 -> 缺陷修复后改回正常断言。

每个用例 docstring 的第一行标注对应缺陷单号，便于跟踪。
"""
import pytest

from pages import CartPage, CheckoutPage, InventoryPage, LoginPage

PROBLEM_IMG_JS = "return arguments[0].naturalWidth > 0;"


@pytest.mark.known_bug
@pytest.mark.xfail(reason="BUG-001: problem_user 商品图片全部加载失败(404 占位图)", strict=False)
def test_bug_001_problem_user_images_load(sb):
    """BUG-001: problem_user 登录后商品图片应能正常加载。"""
    LoginPage(sb).open().login("problem_user", "secret_sauce")
    inv = InventoryPage(sb)
    assert inv.is_loaded()
    for el in inv.product_image_srcs():
        pass
    imgs = sb.find_elements("div.inventory_item_img img")
    assert imgs, "应存在商品图片"
    broken = 0
    for img in imgs:
        loaded = sb.execute_script(PROBLEM_IMG_JS, img)
        if not loaded:
            broken += 1
    assert broken == 0, f"存在 {broken} 张图片加载失败，正常用户应为 0"


@pytest.mark.known_bug
@pytest.mark.xfail(reason="BUG-002: locked_out_user 账号被锁定(登录入口拦截)", strict=False)
def test_bug_002_locked_out_user_can_login(sb):
    """BUG-002: 被锁定账号无法登录，提示文案含糊，追踪其安全机制是否误伤。"""
    LoginPage(sb).open().login("locked_out_user", "secret_sauce")
    assert LoginPage(sb).is_on_inventory(), "被锁定账号不应进入商品页"


@pytest.mark.known_bug
@pytest.mark.xfail(reason="BUG-003: error_user 加购部分商品报 Epic sadface broken", strict=False)
def test_bug_003_error_user_add_all_items(sb):
    """BUG-003: error_user 加购全部商品不应出现系统错误横幅。"""
    LoginPage(sb).open().login("error_user", "secret_sauce")
    inv = InventoryPage(sb)
    assert inv.is_loaded()
    for item_id in ("backpack", "bike-light", "bolt-shirt", "fleece-jacket", "onesie", "red-tshirt"):
        inv.add_to_cart(item_id)
        if inv.sb.is_element_present("div.error-message-container.error"):
            break
    assert not inv.sb.is_element_present("div.error-message-container.error"), "加购过程不应出现 Epic sadface 错误"


def test_error_user_checkout_input_exactness(sb):
    """关联 BUG-003 的回归补充：就算加购阶段有缺陷，结账表单本身输入必须精确。

    该断言反映"缺陷影响面分析"：输入框行为不受 BUG-003 影响，
    排除缺陷扩散猜测，避免被当作同一根因重复提单。
    """
    LoginPage(sb).open().login("error_user", "secret_sauce")
    inv = InventoryPage(sb)
    inv.add_to_cart("backpack")
    if inv.sb.is_element_present("div.error-message-container.error"):
        pytest.skip("加购已被 BUG-003 阻断，无法到达结账表单")
    inv.open_cart()
    CartPage(sb).checkout()

    sb.type("#first-name", "Mei")
    assert sb.get_attribute("#first-name", "value") == "Mei", "first-name 输入应精确匹配"