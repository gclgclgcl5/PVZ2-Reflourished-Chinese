# 僵尸图鉴 FLAVOR 机翻扫描

触发：`ZOMBIE_SEAGULL_DESCRIPTION`（飞行常客里程 / 脑部美食度假）。
范围：全部 `ZOMBIE_*_DESCRIPTION` 的 `{FLAVOR}`；机制行不评。
权威：[`STYLE.md`](STYLE.md)、[`almanac/BAOKAI.md`](almanac/BAOKAI.md)。

- 有 FLAVOR：**562**
- 高风险 EN 习语/双关或 ZH 抽烟枪命中：**5**（P0=1 / P1=1 / P2=3）
- 账本：[`zombie_flavor_mt_ledger.json`](zombie_flavor_mt_ledger.json)

## 总判

僵尸图鉴 FLAVOR **很少**堆 `food for thought` / `cold shoulder` 这类英文习语；多数返茂原创段子是长叙述，问题更常是书面腔而非词典砸梗。
**与海鸥同型的复合双关砸碎，目前 P0 实锤主要就是海鸥一条。** 另有少量 P1（dead end 拼接等）需人工过。

## 严重度

| 级 | 含义 |
|----|------|
| P0 | ZH 已呈词典砸碎，或 EN 复合梗 + ZH 同款硬伤 |
| P1 | EN 含高风险习语/双关，或 ZH 轻拼接，建议过目 |
| P2 | 多半已重建或技术义可接受 |

## P0（1）

### `ZOMBIE_SEAGULL_DESCRIPTION`
- flags: frequent_flier(P0), cerebral_gastronomy(P0), gastronomy(P0), cerebral(P1), colleges(P1), zh_flier(P0), zh_brain_gastro(P0), zh_gastro_vacay(P0)
- EN: Seagull Zombie has racked up the frequent flier miles and dreams of going to the top colleges in the world on a cerebral gastronomy vacation.
- ZH: 海鸥僵尸攒够了飞行常客里程，梦想着靠脑部美食度假去世界顶尖大学。

## P1（1）

### `ZOMBIE_ZCORP_FEM_DESCRIPTION`
- flags: dead_end(P1), zh_deadend_job(P1)
- EN: Having been stuck at a dead end 9-to-5 job for almost 5 years now, you'd think applying for another similar job at ZCorp would be the last thing someone like her would want to do. But hey, they gave free coffee mugs at orientation!
- ZH: 在死胡同朝九晚五的岗位上困了将近五年，你大概觉得像她这样的人最不想再去僵企申一份类似工作。可嘿，入职培训送免费咖啡杯！

## P2（3）

### `ZOMBIE_CARNIE_ARMOR1_DESCRIPTION`
- flags: zh_as_we_all_know(P2)
- EN: It is a fact that everyone loves clowns, and zombies, and therefore clown zombies.
- ZH: 众所周知，人人爱小丑，也爱僵尸，因此也会爱小丑僵尸。

### `ZOMBIE_LUNAR_MONEYTREE_DESCRIPTION`
- flags: bone_to_pick(P2)
- EN: Moneytree Zombie has a particular bone to pick with the saying "Money doesn't just grow on trees." If his years of enlightenment from spiritual retreats, as well as his booming wood processing factory could say anything on the matter, it would be the fact that Money does in fact, grow from trees. The lack of foresight that the people of olden days have displayed regarding the benefits of potential business opportunities created from lumber has always been discrediting for him.
- ZH: 金钱树僵尸对「钱不会长在树上」这句特别有意见。若他多年灵修静养的觉悟，以及蓬勃的木材加工厂能对这事说点什么，那就是：钱确实是从树上长出来的。古人对木材可能带来的商机缺乏远见，这一直让他觉得丢人。

### `ZOMBIE_ZOMBOSSMECH_FUTURE_DESCRIPTION`
- flags: cerebral(P2)
- EN: When Dr. Zomboss is nestled into the comfy folds of his futuristic cerebral control pod he almost finds it hard to be evil. Of course once he sees a lawn full of happy plants that puts him right back where he needs to be, hungry and evil.
- ZH: 当僵王博士窝进未来脑控舱舒适的褶皱里，他几乎觉得很难继续作恶。当然，一看见满草坪快乐的植物，他就立刻回到该在的位置：饥饿，而且邪恶。

## 标签频次

- `cerebral`: 2
- `frequent_flier`: 1
- `cerebral_gastronomy`: 1
- `gastronomy`: 1
- `colleges`: 1
- `zh_flier`: 1
- `zh_brain_gastro`: 1
- `zh_gastro_vacay`: 1
- `dead_end`: 1
- `zh_deadend_job`: 1
- `zh_as_we_all_know`: 1
- `bone_to_pick`: 1

## 建议改稿顺序

1. **P0** `ZOMBIE_SEAGULL_DESCRIPTION`：重建 frequent flier × cerebral gastronomy × top colleges。
2. **P1** 逐条过目（死胡同朝九晚五等）。
3. 不扩扫「的」密集长句作 P0，避免误伤宝开长叙述。

## 专名补记（Lost Explorer）

- `Lost Explorer Zombie` 旧译「丢失探险家僵尸」义项错（丢失≠迷路）。
- 已锁定并全库改为 **迷失探险家僵尸**；`ZOMBIE_DARK_EXPLORER` FLAVOR 内「失落探险家」一并对齐；STYLE / `almanac_name_lock.json` 已更新。

