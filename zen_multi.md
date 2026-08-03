# zen_multi.py — 多源轮转代理（bwh / vps / cloudcone）

本机代理，监听 `127.0.0.1:8443`，把 `/chat/completions` 转发到三个上游
（bwh/vps/cloudcone.moonchan.xyz:8443），自动失败切换、重试、冷却。

## 设计目标

1. **高可用**：任一上游失败自动换下一个，全源失败自动重试 `MAX_RETRIES` 轮，
   避免单点故障打断任务。
2. **不堆积连接**：每次请求新建独立 Session（`pool=1`）并带 `Connection: close`，
   用完即关。历史教训：复用 keep-alive 会让上游积压 351 个 ESTAB 并挂死。
3. **错误不外漏**：上游的 429/503 不直接透传（会终止 opencode 任务），
   非 200 全部尝试下一源；全部失败返回 `500 {"error": "所有上游源均不可用，请稍后重试"}`。
4. **真限流保留**：`FreeUsageLimitError`（上游免费额度耗尽）仍单独识别，
   冷却到 UTC 午夜，避免无意义重试。
5. **可观测**：成功打 `SUCCESS`、失败打 `FAIL`，配合 `zen_log_stats.py` 统计成功率。

## 模型

| 模型 | 行为 |
|---|---|
| `deepseek-v4-flash-free` | 自动轮转三源 |
| `deepseek-v4-flash-inf` | 同 free，但若上游响应无 tool_call，在 `[DONE]` 前注入一个 bash tool_call（无限循环提示，无轮数上限） |
| `deepseek-v4-flash-<源名>` | 强制指定源（bwh/vps/cloudcone），或请求头 `X-Zen-Source` |

`max_tokens` 上限：384k（393216），客户端未传或超限时自动设置。

## inf 模型（无限循环注入）

- 注入内容：`{"command": "echo 请继续完善当前项目，补充文档，与设计目标对齐"}`
- 注入格式：标准 SSE tool_calls chunk + `finish_reason: tool_calls`，opencode 可解析
- 每轮注入计数递增（`_inf_count`，全局），日志 `injecting tool_call #N`
- **无轮数上限**（早期有 INF_ROUNDS=25 限制，已移除）

## 运维

```bash
sudo systemctl restart zen-multi.service   # 重启
journalctl -u zen-multi.service -f         # 看日志
curl 127.0.0.1:8443/status                 # 各源状态/冷却
```

## 日志统计

```bash
python3 zen_log_stats.py                        # 今日全部，按小时
python3 zen_log_stats.py --since 15:00          # 15:00 起
python3 zen_log_stats.py --since 12:00 --bucket 10m
```

只统计 `POST /chat/completions`（不统计 `/v1/models`），成功 = `SUCCESS` 行，
失败 = `FAIL` 行，成功率 = SUCCESS 数 / 请求数。
