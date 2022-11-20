# The Question
If my team is up by X points with Y minutes remaining, what is our chance of winning?

# The answer
todo

# The methodology
1. Obtain a large corpus of play-by-play statistics for any game with a clock
2. pre-process this data into a table of
   1. `id`, `cumulative home points`, `cumulative away points`, `time remaining`, `winner`
   2. This pre-processing should not assume the eventual bucket sizes
   3. id can just be sport + date + home team + away team
3. (for each sport) create a 2d grid of buckets at a reasonable intervals, say 5 per quarter
4. "scatter" data into buckets, creating a table
   1. `id`, `time bucket`, `winner signed score difference`
   2. rows are unique
5.  percent chance for bucket `t, d` = `count(*,t,d) / (count(*,t,d) + count(*,t,-d))`

# Progress
 - [x] get some data
 - [x] read data
 - [x] basic processing of data
 - [ ] plot data
 - [ ] get a lot more data
 - [ ] make some pretty plots
 - [ ] publish
