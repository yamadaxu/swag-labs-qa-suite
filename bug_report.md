# Swag Labs 演示商城 QA 缺陷归档

> 被测对象：SauceLabs 官方 Demo 商城 `https://www.saucedemo.com`
> 归档人：实习生测试岗项目
> 举证方式：每条缺陷对应一个自动化用例（`tests/test_bug_repro.py`），
> 用例一旦修复即解除 xfail 挂起，恢复为正断言——这就是"持续跟踪保证 bug 修复结果"的机制。

## 缺陷跟踪表

| 缺陷单 | 严重级别 | 状态 | 复现账号 | 关联用例 | 期望行为 | 实际行为 |
| --- | --- | --- | --- | --- | --- | --- |
| BUG-001 | P1 严重 | OPEN（已挂起跟踪） | problem_user | `test_bug_001_problem_user_images_load` | 商品图片正常加载 | 商品图全部为 404 占位图，`naturalWidth=0` |
| BUG-002 | P2 一般 | OPEN（已挂起跟踪） | locked_out_user | `test_bug_002_locked_out_user_can_login` | 登录不受限 | 提示账户被锁定，无法进入商城 |
| BUG-003 | P1 严重 | OPEN（已挂起跟踪） | error_user | `test_bug_003_error_user_add_all_items` | 加购全部规格商品成功 | 加购部分商品弹出 `Epic sadface: This function is broken` |
| REG-004 | - | 已验证通过 | error_user | `test_error_user_checkout_input_exactness` | 表单输入精确匹配 | 通过（证明 BUG-003 不影响结账表单，缺陷影响面收敛） |

## BUG-001：problem_user 商品图片全部加载失败

- **优先级**：P1（核心购物体验受阻，图片为商品信息主要载体）
- **复现步骤**（即自动化路径）：
  1. 以 `problem_user` 登录 `https://www.saucedemo.com`；
  2. 进入商品列表页；
  3. 遍历 `div.inventory_item_img img` 读取每个 `naturalWidth`。
- **预期**：所有 `naturalWidth > 0`；
- **实际**：全部为 0（src 指向 404 占位图）；
- **根因假设**：静态资源地址写错/资源被下架，商品图片 CDN 目录变更未同步；
- **跟踪方式**：用例挂 `xfail(reason="BUG-001")`，CI 保留该回归路径，图片恢复即自动转绿。
- **建议**：修复静态资源引用，补充图片加载的 E2E 断言进入回归集。

## BUG-002：locked_out_user 无法登录

- **优先级**：P2（属账号级限制，但文案与逻辑是否属"误伤"需产品确认）
- **复现步骤**：
  1. 以 `locked_out_user` + `secret_sauce` 登录；
  2. 观察提示：`Sorry, this user has been locked out.`
  3. 断言页面停留在登录态且无法进入 `div.inventory_list`。
- **预期**：正常进入商品页；
- **实际**：登录被拦截；
- **说明**：若该用户在业务上不属于黑名单，则为一处误伤风险；作为 QA 需与产品确认封禁来源后再判定。
- **跟踪方式**：同 BUG-001，xfail 挂起 + CI 回归。

## BUG-003：error_user 加购报系统错误

- **优先级**：P1（对部分商品加购直接失败，下单主流程受损）
- **复现步骤**：
  1. 以 `error_user` 登录；
  2. 依次点击各商品 `Add to cart`；
  3. 断言全程不出现 `div.error-message-container.error`。
- **预期**：加购全程无错误横幅；
- **实际**：部分商品的加购按钮触发 `Epic sadface: This function is broken`（后端加购接口对该账号返回异常）；
- **根因假设**：前端按钮绑定事件与后端接口对该账号配置不一致；
- **跟踪方式**：xfail 挂起 + CI 回归；修复后恢复正断言。
- **补充（REG-004）**：排查确认该缺陷不影响结账表单输入（`#first-name` 键入精确匹配），排除缺陷扩散，避免重复提单。

## 测试执行方式

```bash
pip install -r requirements.txt
pytest tests/ --headless -m "not known_bug" \
    --html=reports/report.html --self-contained-html \
    --cov=pages --cov-report=html:reports/coverage
```