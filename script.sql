/*Joins practice*/
select users.id,count(*) from posts right join users on posts.user_id = users.id group by users.id;
select users.id,users.email,count(posts.id) as user_post_count from posts right join users on posts.user_id = users.id group by users.id;
select posts.id as post_id, votes.* from posts left join votes on posts.id = votes.post_id
