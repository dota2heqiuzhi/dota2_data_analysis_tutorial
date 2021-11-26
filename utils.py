from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
import pandas as pd
import requests
import random
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import time

def get_api_json(url, loop=True, proxy=None, print_error=False):
    try:
        return requests.get(url, headers={'User-Agent': 'Chrome'}, timeout=3, proxies=proxy).json()
    except requests.exceptions.RequestException as e:
        if print_error is True:
            print(e)
        return get_api_json(url, loop, proxy) if loop is True else None

def get_proxies():
    proxies = []
    for p in get_api_json("https://dota2.heqiuzhi.xyz/get_all"):
        if p["goal_web"] == "opendota":
            proxies.append({'http': f'http://{p["proxy"]}/', 'https': f'http://{p["proxy"]}/'})
    return proxies


def get_db_engine():
    return create_engine('postgresql://dota2_readonly:dota2@dota2.heqiuzhi.xyz:5432/dota2', poolclass=NullPool)

# 默认选取昨天的全阵营天梯模式比赛，要求对局时长>=20分钟
def get_hero_sample_match(hero_id, sample_match_count = 1000, lobby_type = 7, game_mode = 22, min_duration = 60 * 20):
    df = pd.read_sql(
        f"""select 
                match_id
            from match 
            where p_date = (select p_date from match group by p_date order by p_date desc limit 1 offset 1)
            and lobby_type = {lobby_type}
            and game_mode = {game_mode}
            and duration >= {min_duration}
            and ((radiant_pick_hero_ids ~ '([^\d]|^){hero_id}([^\d]|$)') or (dire_pick_hero_ids ~ '([^\d]|^){hero_id}([^\d]|$)'))
            order by random() limit {sample_match_count}
        """, get_db_engine())
    return df

def parallel_run_api(func, match_ids, min_proxy_count=2,  complete_rate=1):
    handled_match_ids, all_match_results = [], []
    handled_match_count = len(handled_match_ids)
    while len(handled_match_ids) < len(match_ids):
        proxies = get_proxies()
        if len(proxies) < min_proxy_count:#如果可用的代理太少，也跑不动...
            print(f"only have {len(proxies)} valid proxies! 当前进度:{len(handled_match_ids)}/{len(match_ids)}", end='\r')
            time.sleep(10)
            continue
        working_match_ids, run_proxies = [], []
#         print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '当前进度:{}/{}'.format(len(handled_match_ids), len(match_ids)))
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), f'可用代理数:{len(proxies)}, 当前进度:{len(handled_match_ids)}/{len(match_ids)}',  end='\r')
        for i, mi in enumerate(match_ids):
            if mi not in handled_match_ids:
                working_match_ids.append(match_ids[i])
                run_proxies.append(random.choice(proxies))
        with ThreadPoolExecutor(max_workers=min(32, len(proxies))) as executor:
            parameters = (working_match_ids, run_proxies)
            for match_result in executor.map(func, *parameters):
                if match_result[0] is not None:
                    all_match_results.append(match_result[0])
                    handled_match_ids.append(match_result[1])
                
        #如果一轮循环结束之后一场新比赛都没有下载到，则跳出(最开始可能大多数比赛都没有解析，所以放宽条件)
        if (len(handled_match_ids) == handled_match_count) and (len(handled_match_ids) / len(match_ids) >= 0.5):
            print('无法继续获取比赛，当前进度:{}/{}'.format(len(handled_match_ids), len(match_ids)))
            break
        elif len(handled_match_ids) / len(match_ids) >= complete_rate:
            break
        else:
            handled_match_count = len(handled_match_ids)
    return all_match_results