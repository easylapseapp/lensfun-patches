# Lensfun 数据库锚定与合规仓

本仓用于 **Lensfun 官方镜头数据库**的版本锚定与合规存放。与
[libraw-patches](https://github.com/easylapseapp/libraw-patches)（源码 patch 仓）不同，
本仓不包含 lensfun 库代码，也不含对库源码的任何修改（patch 数为 0），
收录的只有上游数据库原文件、逐文件校验清单与 NOTICE 模板。

## 授权结构

| 组成 | 授权 | 本仓处理方式 |
|---|---|---|
| lensfun C 库 | LGPL-3.0 | 不收录、不分发（本仓无库代码） |
| 镜头数据库（`data/db/*.xml`） | CC-BY-SA-3.0 | 原样分发，仅触发署名义务（见 `NOTICE-lensfun-db.md`；许可证全文见 `COPYING.CC_BY-SA_3.0`） |

红线（违反即合规事故）：

- `data/db/` **禁止任何改动（一个字节都不改）**；向其中添加或混入任何数据后分发，
  会触发 CC-BY-SA-3.0 的 share-alike 衍生传递；
- 数据库升级 = 整体替换 + `db_manifest.json` 重生成，禁止在原文件上原地修改。

## 上游锚定

| 项 | 值 |
|---|---|
| 版本 | **v0.3.4**（GitHub releases 最新非预发布版） |
| tag 日期 | 2023-07-12 |
| commit | `101c745e847a5de4a1e569a94368ce2027198598` |
| 来源 | [v0.3.4 tarball](https://github.com/lensfun/lensfun/archive/refs/tags/v0.3.4.tar.gz) |
| 收录 | 上游 `data/db/` 全部 **56 文件**（55 个 XML + `timestamp.txt`），字节级原样 |
| 清单 | `db_manifest.json`（逐文件 SHA-256 + 字节数，共 4,249,590 字节） |

> 注意：上游存在 `v0.3.95` tag，其 commit 日期为 **2018-06-29**（旧版），
> 勿被版本号数字误导；以 GitHub releases 的非预发布最新版为准。

## 目录结构

```
data/db/            上游 v0.3.4 数据库原样（slr-*.xml / mil-*.xml / compact-*.xml / misc*.xml / ...）
db_manifest.json    逐文件 SHA-256 清单 + 上游锚定信息
NOTICE-lensfun-db.md NOTICE 段模板（随发布引用）
COPYING.CC_BY-SA_3.0  CC-BY-SA-3.0 许可证全文（上游 data/COPYING.CC_BY-SA_3.0；
                      v0.3.4 tarball 时点上游尚未收录该文件，取自上游 master
                      的同名文件——CC-BY-SA-3.0 标准法律文本，内容恒定）
scripts/verify_manifest.py  清单校验脚本
patches/            （当前不存在——本仓不含源码修改）
```

## 清单校验用法

在仓根执行（任何 Python 3.8+）：

```bash
python scripts/verify_manifest.py
```

脚本会逐文件重算 SHA-256 与 `db_manifest.json` 比对，并检测 `data/db/` 下
未登记的多余文件；任一不符即非零退出。
