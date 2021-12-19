/*Joins practice*/
select users.id,count(*) from posts right join users on posts.user_id = users.id group by users.id;
select users.id,users.email,count(posts.id) as user_post_count from posts right join users on posts.user_id = users.id group by users.id;
select posts.id as post_id, votes.* from posts left join votes on posts.id = votes.post_id;
/* count the total number of votes for each post*/
select posts.id, count(votes.post_id) from posts left join votes on posts.id = votes.post_id group by posts.id;
/*order*/
select posts.id as post_id, count(votes.post_id) as vote_count from posts left join votes on posts.id = votes.post_id group by posts.id order by(vote_count) desc;
select posts.*, count(votes.post_id) as vote_count from posts left join votes on posts.id = votes.post_id group by posts.id order by(vote_count) desc;
/*get the vote count for a specific posts*/
select posts.id as post_id, count(votes.post_id) as vote_count from posts left join votes on posts.id = votes.post_id where posts.id =1 group by posts.id;
