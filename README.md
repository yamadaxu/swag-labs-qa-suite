# Web QA 自动化测试套件（SeleniumBase + POM + 数据驱动 + CI）

[![QA Regression](https://github.com/yamadaxu/swag-labs-qa-suite/actions/workflows/ci.yml/badge.svg)](https://github.com/yamadaxu/swag-labs-qa-suite/actions/workflows/ci.yml)

面向"测试实习生/测试开发"岗位的可讲项目：以 SauceLabs 官方演示商城
（Swag Labs, `https://www.saucedemo.com`）为被测系统，构建一整套
Web 端到端回归体系，覆盖**用例设计、缺陷发现与归档、覆盖率、CI 集成**。

## 定位与 JD 对应

| JD 要求 | 本项目的落地 |
| --- | --- |
| 发现产品缺陷、记录并跟踪修复 | `tests/test_bug_repro.py` + `bug_report.md`：3 条缺陷复现 + xfail 挂起跟踪 + CI 回归 |
| 用户体验/反馈复现 | `problem_user` 加载失败图片、`error_user` 加购失效均为真实可复现的体验缺陷 |
| 测试设计与用例编写执行 | POM 分层 + 数据驱动（`data/*.csv`）+ 等价类/边界/组合用例 + 21 条用例 |
| 输出测试报告 | pytest-html `reports/report.html` + coverage `reports/coverage` |
| 完善流程 | GitHub Actions `ci.yml` 冒烟/回归流水线 + Docker 一键运行 |
| Python 基础 | 全套 Python + pytest 实现 |

## 目录结构

```
testsuite/
  pages/            POM 页面对象（login/inventory/cart/checkout）
  data/             数据驱动文件（users.csv / checkout_data.csv）
  tests/            用例集：登录 / 商品 / 结算 / 缺陷复现
  reports/          测试报告与覆盖率（运行后生成）
  bug_report.md     缺陷归档（跟踪表 + 复现步骤 + 根因假设）
  Dockerfile / docker-compose.yml
  .github/workflows/ci.yml
```

## 本地运行

```bash
pip install -r requirements.txt

# 全量回归（排除已挂起缺陷，保证套件绿灯）
pytest tests/ --headless -m "not known_bug" \
    --html=reports/report.html --self-contained-html \
    --cov=pages --cov-report=html:reports/coverage

# 查看缺陷复现集（预期 3 XFAIL）
pytest tests/test_bug_repro.py --headless -rX
```

## Docker 运行

```bash
docker compose up --build
```

## CI（GitHub Actions）

- 推送/PR 触发，使用官方 `seleniumbase/ubuntu` 镜像（内置浏览器与 driver），
  无头跑回归并上传 reports 产物。
- 缺陷用 `xfail` 挂起，不会让 CI 长期红灯；修复后解除即自动验证"bug 修复结果"。

## 关键面试点

1. **用例设计**：等价类（用户名空/密码空/坏凭证）、边界（邮编 000000）、
   数据驱动（csv + parametrize）、业务闭环（浏览→加购→结算→致谢）。
2. **测试分析**：`test_order_total_math_consistency` 校验 Item total 与
   购物车金额一致、Subtotal+Tax=Total，防后台改价不同步。
3. **缺陷管理**：发现→归档→挂起跟踪→CI 回归，一套闭环。
4. **覆盖率**：pages 层 89%，报告可见。