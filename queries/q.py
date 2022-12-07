hero_with_hero = '''
SELECT
        heroes.localized_name ,player_matches.hero_id, player_matches2.hero_id hero_id2 ,
avg(1) "AVG Hero-Hero",
count(distinct matches.match_id) count,
sum(case when (player_matches.player_slot < 128) = radiant_win then 1 else 0 end)::float/count(1) winrate,
((sum(case when (player_matches.player_slot < 128) = radiant_win then 1 else 0 end)::float/count(1)) 
+ 1.96 * 1.96 / (2 * count(1)) 
- 1.96 * sqrt((((sum(case when (player_matches.player_slot < 128) = radiant_win then 1 else 0 end)::float/count(1)) * (1 - (sum(case when (player_matches.player_slot < 128) = radiant_win then 1 else 0 end)::float/count(1))) + 1.96 * 1.96 / (4 * count(1))) / count(1))))
/ (1 + 1.96 * 1.96 / count(1)) winrate_wilson,
sum(1) sum,
min(1) min,
max(1) max,
stddev(1::numeric) stddev
  
FROM matches
JOIN match_patch using(match_id)
JOIN leagues using(leagueid)
JOIN player_matches using(match_id)
JOIN heroes on heroes.id = player_matches.hero_id
LEFT JOIN notable_players ON notable_players.account_id = player_matches.account_id
LEFT JOIN teams using(team_id)
JOIN player_matches player_matches2
ON player_matches.match_id = player_matches2.match_id
AND player_matches.hero_id != player_matches2.hero_id 
AND abs(player_matches.player_slot - player_matches2.player_slot) < 10
AND player_matches.hero_id < player_matches2.hero_id
WHERE TRUE
AND 1 IS NOT NULL 
AND match_patch.patch >= '{patch}'
AND (player_matches.hero_id = {hero_id})
AND leagues.tier = '{tier_level}'
GROUP BY heroes.localized_name, player_matches.hero_id, player_matches2.hero_id
HAVING count(distinct matches.match_id) >= 1
ORDER BY "AVG Hero-Hero" DESC,count DESC NULLS LAST
LIMIT 200
'''

player = '''
SELECT
        heroes.localized_name ,player_matches.hero_id, player_matches.account_id ,
avg(1) "AVG Hero-Player",
count(distinct matches.match_id) count,
sum(case when (player_matches.player_slot < 128) = radiant_win then 1 else 0 end)::float/count(1) winrate,
((sum(case when (player_matches.player_slot < 128) = radiant_win then 1 else 0 end)::float/count(1)) 
+ 1.96 * 1.96 / (2 * count(1)) 
- 1.96 * sqrt((((sum(case when (player_matches.player_slot < 128) = radiant_win then 1 else 0 end)::float/count(1)) * (1 - (sum(case when (player_matches.player_slot < 128) = radiant_win then 1 else 0 end)::float/count(1))) + 1.96 * 1.96 / (4 * count(1))) / count(1))))
/ (1 + 1.96 * 1.96 / count(1)) winrate_wilson,
sum(1) sum,
min(1) min,
max(1) max,
stddev(1::numeric) stddev
  
FROM matches
JOIN match_patch using(match_id)
JOIN leagues using(leagueid)
JOIN player_matches using(match_id)
JOIN heroes on heroes.id = player_matches.hero_id
LEFT JOIN notable_players ON notable_players.account_id = player_matches.account_id
LEFT JOIN teams using(team_id)
WHERE TRUE
AND 1 IS NOT NULL 
AND match_patch.patch >= '{patch}'
AND (player_matches.account_id = {player_id})
GROUP BY heroes.localized_name, player_matches.hero_id, player_matches.account_id
HAVING count(distinct matches.match_id) >= 1
ORDER BY "AVG Hero-Player" DESC,count DESC NULLS LAST
LIMIT 200
'''

hero = '''
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
AND (player_matches.hero_id = {hero_id})
AND leagues.tier = '{tier_level}'
GROUP BY heroes.localized_name
HAVING count(distinct matches.match_id) >= 1
ORDER BY "AVG Kills" DESC,count DESC NULLS LAST
LIMIT 200
'''

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
AND leagues.tier = '{tier_level}'
GROUP BY heroes.localized_name
HAVING count(distinct matches.match_id) >= 1
ORDER BY "AVG Kills" DESC,count DESC NULLS LAST
LIMIT 200
'''