import aiohttp
import pandas as pd
import asyncio
import dataframe_image as dfi


heroes = '''
    SELECT
        heroes.localized_name ,
    avg(kills) "AVG Kills",
    count(distinct matches.match_id) count,
    sum(case when (player_matches.player_slot < 128) = radiant_win then 1 else 0 end)::float/count(1) winrate,
    ((sum(case when (player_matches.player_slot < 128) = radiant_win then 1 else 0 end)::float/count(1)) 
    + 1.96 * 1.96 / (2 * count(1)) 
    - 1.96 * sqrt((((sum(case when (player_matches.player_slot < 128) = radiant_win then 1 else 0 end)::float/count(1)) * (1 - (sum(case when (player_matches.player_slot < 128) = radiant_win then 1 else 0 end)::float/count(1))) + 1.96 * 1.96 / (4 * count(1))) / count(1))))
    / (1 + 1.96 * 1.96 / count(1)) winrate_wilson,
    sum(kills) sum,
    min(kills) min,
    max(kills) max,
    stddev(kills::numeric) stddev
    
    FROM matches
    JOIN match_patch using(match_id)
    JOIN leagues using(leagueid)
    JOIN player_matches using(match_id)
    JOIN heroes on heroes.id = player_matches.hero_id
    LEFT JOIN notable_players ON notable_players.account_id = player_matches.account_id
    LEFT JOIN teams using(team_id)
    WHERE TRUE
    AND kills IS NOT NULL 
    AND match_patch.patch >= '{patch}'
    AND leagues.tier = '{tier}'
    GROUP BY heroes.localized_name
    HAVING count(distinct matches.match_id) >= 1
    ORDER BY "AVG Kills" DESC,count DESC NULLS LAST
    LIMIT 200
    '''


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.opendota.com/api/explorer', params=dict(sql=heroes.format(patch=7.30, tier='premium'))) as resp:
            print(resp.status)
            if resp.status == 200:
                query = await resp.json()
                df = pd.DataFrame(query['rows']).head(10)
                df_styled = df.style.background_gradient()
                df.to_csv('df.csv', index=False)
                dfi.export(df_styled, 'mytable.png', table_conversion='matplotlib')
            else:
                print('Response error!')


asyncio.run(main())