from enum import Enum, auto

class FileType(Enum):
    CSV = '.csv'
    XLSX = '.csv'

class DataType(Enum):
    AGGREGATE_SUM = 'Aggregate Sum'
    FREQUENCY = 'Frequency'
    GINI_COEFFICIENCT = 'Gini Coefficient'

comment_return_fields = [
                    'all_awardings',
                    'archived',
                    'author',
                    'author_flair_text',
                    'body',
                    'comment_type',
                    'controversiality',
                    'created_utc',
                    'datetime',
                    'gilded',
                    'link_id',
                    'locked',
                    'parent_id',
                    'permalink',
                    'retrieved_utc',
                    'score',
                    'score_hidden',
                    'send_replies',
                    'stickied',
                    'subreddit',
                    'subreddit_id',
                    'subreddit_name_prefixed',
                    'subreddit_type',
                    'total_awards_received',
                    'treatment_tags'
    ]

submission_return_fields = [
                    'all_awardings',
                    'allow_live_comments',
                    'author',
                    'author_flair_text',
                    'author_is_blocked',
                    'awarders',
                    'can_mod_post',
                    'contest_mode',
                    'created_utc',
                    'datetime',
                    'full_link',
                    'is_crosspostable',
                    'is_meta',
                    'is_original_content',
                    'is_reddit_media_domain',
                    'is_robot_indexable',
                    'is_self',
                    'is_video',
                    'link_flair_text',
                    'locked',
                    'media_only',
                    'num_comments',
                    'num_crossposts',
                    'over_18',
                    'permalink'
                    'pinned',
                    'retrieved_on',
                    'score',
                    'selftext',
                    'send_replies',
                    'spoiler',
                    'stickied',
                    'subreddit',
                    'subreddit_id',
                    'subreddit_subscribers',
                    'subreddit_type',
                    'title',
                    'total_awards_received',
                    'treatment_tags',
                    'upvote_ratio',
                    'url'
    ]