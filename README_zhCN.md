# Poe Direct for Claude Code

这是一个更轻量的 Poe + Claude Code 配置仓库。

它直接使用 Poe 官方提供的 Anthropic-compatible API，因此 Claude Code 可以直接连到 Poe，不需要本地代理。

---

## 仓库定位

这个仓库是最小化、官方路径优先的版本。

它适合这些目标：

- 不跑本地 proxy
- 不维护额外兼容层
- 用最短路径把 Claude Code 接到 Poe 的 Claude 模型

它和重型代理版仓库是成对分工的：一个追求最小配置，一个追求兼容层可控。

---

## 为什么要单独做这个仓库

Poe 现在已经官方提供 Claude Code 接入说明，以及 Anthropic-compatible `/v1/messages` 接口。

如果目标只是：

- 让 Claude Code 通过 Poe 使用 Claude
- 保持在 Claude 模型范围内
- 让配置尽量简单、README 尽量真实

那么就没必要继续带着本地代理。

这个仓库只保留最小可用的说明和脚本。

---

## 工作原理

```text
Claude Code (VS Code)
  |
  | ANTHROPIC_BASE_URL=https://api.poe.com
  | ANTHROPIC_AUTH_TOKEN=<你的 Poe API Key>
  | ANTHROPIC_API_KEY=
  v
Poe Anthropic-compatible API (/v1/messages)
  |
  v
Poe 上的 Claude 模型
```

这个仓库里没有本地 proxy。
Claude Code 直接用它原生的 Anthropic-compatible 协议去访问 Poe。

---

## 准备工作

1. 已安装并能正常使用 Claude Code。
2. 已有 Poe 账号。
3. 已在 https://poe.com/api/keys 获取 Poe API Key。
4. 本机有 Python 3，用来运行辅助脚本。

---

## 文件说明

| 文件 | 用途 |
|------|------|
| `setup_poe.py` | 将 Claude Code 配置为 Poe 直连模式 |
| `restore_clean.py` | 删除 Poe 相关配置，还原为默认路径 |
| `README.md` | 英文说明 |

---

## 快速开始

执行：

```bash
python setup_poe.py --token p-xxxxxxxxxxxxxxxxxxxx
```

脚本会自动完成：

1. 向 `~/.claude/settings.json` 写入 Poe 直连所需环境变量。
2. 清除 `~/.claude.json` 中的 `cachedExtraUsageDisabledReason`。
3. 输出重启后 Claude Code 将使用的配置。

写入后的配置大致如下：

```json
"env": {
  "ANTHROPIC_BASE_URL": "https://api.poe.com",
  "ANTHROPIC_AUTH_TOKEN": "p-xxx...",
  "ANTHROPIC_API_KEY": ""
}
```

---

## 验证

重启 Claude Code 后，在会话里执行：

```text
/status
```

应看到：

```text
Anthropic base URL: https://api.poe.com
```

---

## 还原到默认官方路径

如果你不再使用 Poe，执行：

```bash
python restore_clean.py
```

它会删除 Poe 相关环境变量，并清理 Claude Code 的额度缓存状态。

---

## 适用范围

这个轻量仓库刻意只做一件事。

适合的场景：

- 你只需要 Claude Code -> Poe 的直连
- 你只需要 Poe 上的官方 Claude 模型
- 你不需要把 Poe 其他能力伪装成 Anthropic 接口

不适合的场景：

- 你要接入自定义 bot
- 你要接入非 Claude 提供商模型
- 你要在 Anthropic 外壳下包一层更广义的 Poe 兼容层

这些场景仍然更适合代理型项目。

---

## 注意事项

- 运行任一脚本后，都需要重启 Claude Code。
- Poe API 会消耗 Poe 订阅积分或 add-on points。
- Poe 的 Anthropic-compatible API 只支持官方 Claude 模型。
- 如果你的目标超出 Claude 官方模型直连，这个仓库就太轻了，应该改用代理方案。
