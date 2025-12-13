--Check wheather there are Dublicates
select [post_id],
count(*)
from [dbo].[Instagram_Analytics]
group by [post_id]
having count(*) > 1

--Time period
select
starting_date,
ending_date,
datediff(year,starting_date,ending_date) as Time_period_year,
datediff(MONTH,starting_date,ending_date) as Time_period_month
from(
select 
min([upload_date]) as starting_date,
max([upload_date]) as ending_date
from [dbo].[Instagram_Analytics]
)t

--Post Categaries
select distinct
[media_type]
from [dbo].[Instagram_Analytics]

--post categories by aggregating items
select 
[media_type],
avg([likes]) as avg_likes,
avg([comments]) as avg_comments,
avg([shares]) as avg_shares,
avg([shares]) as avg_shares,
avg([saves]) as avg_saves,
AVG(cast([reach] as bigint)) as avg_reach,
avg([caption_length]) as avg_caption_length,
avg([hashtags_count]) as avg_hastag_counts,
avg([followers_gained]) as avg_follower_gained,
concat(round(avg([engagement_rate]),2),'%') as avg_engagement_rate
from [dbo].[Instagram_Analytics]
group by [media_type]

--post content categories by aggregating items
select 
[content_category],
avg([likes]) as avg_likes,
avg([comments]) as avg_comments,
avg([shares]) as avg_shares,
avg([shares]) as avg_shares,
avg([saves]) as avg_saves,
AVG(cast([reach] as bigint)) as avg_reach,
avg([caption_length]) as avg_caption_length,
avg([hashtags_count]) as avg_hastag_counts,
avg([followers_gained]) as avg_follower_gained,
concat(round(avg([engagement_rate]),2),'%') as avg_engagement_rate
from [dbo].[Instagram_Analytics]
group by [content_category]

--Traffic source
select distinct
[traffic_source]
from [dbo].[Instagram_Analytics]

--
select distinct
[content_category]
from [dbo].[Instagram_Analytics]